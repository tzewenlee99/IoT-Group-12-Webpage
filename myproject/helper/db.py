import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('data/iot5506-firebase-adminsdk-82jka-4dd6217eae.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot5506-default-rtdb.firebaseio.com/',
    'storageBucket': 'gs://iot5506.appspot.com'
})


def db_init():
    ref = db.reference('')
    return ref.get()
