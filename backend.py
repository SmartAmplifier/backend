import sys
from firebase import Firebase
from flask import Flask
from flask import request
from flask_api import status
import requests

def main():
    config = {
        "apiKey": "AIzaSyD9kyPxezXpH7mhRwWULwhrehEI-LaZjzY",
        "databaseURL": "https://smart-amplifier-gsyadn.firebaseio.com/",
        "authDomain": "smart-amplifier-gsyadn.firebaseapp.com",
        "storageBucket": "smart-amplifier-gsyadn.appspot.com"
    }

    firebase_db = Firebase(config).database()

    app = Flask(__name__)

    @app.route("/get/paired/amplifier/<email>", methods=['GET'])
    def paired_amplifier(email):
        value = firebase_db.child('users').child(str(email).split(
                '@')[0]).child('paired').child('amplifier').get()
        return value.val()

    @app.route("/pair/new/amplifier", methods=['POST'])
    def paired_new_amplifier():
        try:
            firebase_db.child('users').child(str(request.form['email']).split('@')[0]).child(
            'paired').child('amplifier').set({'amplifier': request.form['amplifier']})

            return '200'

        except requests.exceptions.HTTPError:
            return '400'

    
    
    app.run('0.0.0.0', 8080)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Exited with error: ', e)
        sys.exit(1)