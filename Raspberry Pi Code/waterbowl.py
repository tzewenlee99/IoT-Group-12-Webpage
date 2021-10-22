#!/usr/bin/python
import picamera
import time
import json
from datetime import datetime
from gpiozero import MotionSensor
from gpiozero import LED
import pyrebase
import RPi.GPIO as GPIO
import firebase
import uuid


# Firebase Credentials
config = {
    "apiKey": "AIzaSyACREYUwibmDnsGBuogmRF7yIuhVzD6fXQ",
    "authDomain": "iot5506.firebaseapp.com",
    "databaseURL": "https://iot5506-default-rtdb.firebaseio.com",
    "storageBucket": "iot5506.appspot.com",
    "serviceAccount": "/home/pi/Downloads/iot5506-firebase-adminsdk-82jka-a39cbdeed6.json"
    }

#Initialising Firebase connection and Signing in
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('testuser@test.com', 'testing')
db = firebase.database()

#storage = firebase.storage()

#Initialising Camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)

#Initialising PIR
pir = MotionSensor(12)
counter = 0

#Initialsing Ultrasonic Water Bowl
GPIO.setmode(GPIO.BCM)
PIN_TRIGGER_1 = 3
PIN_ECHO_1 = 14
GPIO.setup(PIN_TRIGGER_1, GPIO.OUT)
GPIO.setup(PIN_ECHO_1, GPIO.IN)

#Initialising Ultrasonic Water Tank
PIN_TRIGGER_2 = 18
PIN_ECHO_2 = 24
GPIO.setup(PIN_TRIGGER_2, GPIO.OUT)
GPIO.setup(PIN_ECHO_2, GPIO.IN)

#Initialising relay
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)


#Initialise other variables (time = time from last water level reading)
timer = 0;
lastTime = time.time()
currentTime = time.time()

while True:
    timer = timer + currentTime - lastTime
    lastTime = currentTime
    print(timer)
    if(timer > 3):
        #First ultrasonic Calculation
        GPIO.output(PIN_TRIGGER_1, GPIO.LOW)
        print("Waiting for sensor to settle")
        time.sleep(1)
        print("Calculating distance")
        GPIO.output(PIN_TRIGGER_1, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER_1, GPIO.LOW)
 
        while GPIO.input(PIN_ECHO_1)==0:
            pulse_start_time_1=time.time()
        while GPIO.input(PIN_ECHO_1)==1:
            pulse_end_time_1=time.time()
    
        pulse_duration_1 = pulse_end_time_1-pulse_start_time_1
        distance_1 = round(pulse_duration_1 * 17150, 2)
        print("Distance_1: {} cm".format(distance_1))
        time.sleep(1)
        #When water level is below..., turb on the water pump:
        if(distance_1>7.0):
            GPIO.output(21, GPIO.HIGH)
            time.sleep(10)
            GPIO.output(21, GPIO.LOW)
            
            
        #Second Ultrasonic Calculation
        GPIO.output(PIN_TRIGGER_2, GPIO.LOW)
        print("Waiting for sensor to settle")
        time.sleep(1)
        print("Calculating distance")
        GPIO.output(PIN_TRIGGER_2, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER_2, GPIO.LOW)
 
        while GPIO.input(PIN_ECHO_2)==0:
            pulse_start_time_2=time.time()
        while GPIO.input(PIN_ECHO_2)==1:
            pulse_end_time_2=time.time()
    
        pulse_duration_2 = pulse_end_time_2-pulse_start_time_2
        distance_2 = round(pulse_duration_2 * 17150, 2)
        print("Distance_2: {} cm".format(distance_2))
        time.sleep(1)
        
        #Push to Database
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        bowl_percentage = int(((12.5 - distance_1 )/12.5) * 100)
        tank_percentage = int(((12 - distance_2)/12) * 100)
        data = {
            "DateTime": dt_string,
            "bowlPercentage": bowl_percentage,
            "tankPercentage": tank_percentage
        }
        user = auth.refresh(user['refreshToken'])
        
        results = db.child("test").push(data, user['idToken'])
#       storage.child("images").put("image0.jpg" , user['idToken'])
        print("Has been pushed to database")
        
        #If water level is below ..% trigger pump code(with relay)
        
        
        #Reset Timer
        timer = 0
        print(timer)
        
    #If PIR triggers
        #PIR Code + Take picture
        #Push picture to DB

    currentTime = time.time()
    
    if(pir.wait_for_motion()):
        print("Motion Detected")        
        pir.wait_for_no_motion()
        print("Motion stopped")
        #pir.wait
        print("taking picture")
        img_name = f'{str(uuid.uuid4())}.jpeg'
        camera.capture(img_name)
        
        time.sleep(3)
        
        user = auth.refresh(user['refreshToken'])
        storage.child(img_name).put(img_name , user['idToken'])
        counter += 1
        results = db.child("images").push(f"https://firebasestorage.googleapis.com/v0/b/iot5506.appspot.com/o/{img_name}?alt=media", user['idToken'])
        print("Has been pushed to database")
        

