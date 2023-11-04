import pyrebase
import os, cv2
import urllib
import numpy as np

def upload_image_to_firebase(image_path):
    config = {
        'apiKey': "AIzaSyCpLoNzYhVbo_caUDp13zO92ycpP9EDjUY",
        'authDomain': "datn-4adc6.firebaseapp.com",
        'projectId': "datn-4adc6",
        'storageBucket': "datn-4adc6.appspot.com",
        'databaseURL': "datn-4adc6-default-rtdb.firebaseio.com",
        'messagingSenderId': "550503333699",
        'appId': "1:550503333699:web:d1e0baa6c2d5eafa7cb9f6",
        'measurementId': "G-RXXZQFCP67",
        "serviceAccount": "./key.json"
    }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    storage.child('images/result.jpg').put(image_path)
    return storage.child('images/result.jpg').get_url(None)

def download_image(image):
    config = {
        'apiKey': "AIzaSyCpLoNzYhVbo_caUDp13zO92ycpP9EDjUY",
        'authDomain': "datn-4adc6.firebaseapp.com",
        'projectId': "datn-4adc6",
        'storageBucket': "datn-4adc6.appspot.com",
        'databaseURL': "datn-4adc6-default-rtdb.firebaseio.com",
        'messagingSenderId': "550503333699",
        'appId': "1:550503333699:web:d1e0baa6c2d5eafa7cb9f6",
        'measurementId': "G-RXXZQFCP67",
        "serviceAccount": "./key.json"
    }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    url_image = storage.child("images/" + image).get_url(None)
    req = urllib.request.urlopen(url_image)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    cv2.imwrite('images/image_remote.jpg', img)
download_image('WIN_20221105_22_00_23_Pro.jpg')