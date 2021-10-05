import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('myproject/data/water-level-db7ff-firebase-adminsdk-7etxl-30fbcd22ee.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://water-level-db7ff-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'gs://water-level-db7ff.appspot.com'
})


def db_init():
    ref = db.reference('')
    return ref.get()
