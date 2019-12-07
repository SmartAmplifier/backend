import sys
import click
from firebase import Firebase
from flask import Flask
from flask import request
from flask import make_response
import requests


@click.command()
@click.option('--hostname', '-h', required=True)
@click.option('--port', '-p', required=True)
def main(hostname=None, port=None):
    config = {
        "apiKey": "AIzaSyD9kyPxezXpH7mhRwWULwhrehEI-LaZjzY",
        "databaseURL": "https://smart-amplifier-gsyadn.firebaseio.com/",
        "authDomain": "smart-amplifier-gsyadn.firebaseapp.com",
        "storageBucket": "smart-amplifier-gsyadn.appspot.com"
    }

    firebase_db = Firebase(config).database()

    app = Flask(__name__)

    @app.route('/get/paired/amplifier/<email>', methods=['GET'])
    def paired_amplifier(email):
        value = firebase_db.child('users').child(str(email).split(
            '@')[0]).child('paired').get()
        return value.val()

    @app.route('/pair/new/amplifier', methods=['POST'])
    def paired_new_amplifier():
        try:
            registred_amplifiers = firebase_db.child("amplifiers").child(
                request.form['amplifier']).get().val()

            if registred_amplifiers == None:
                return make_response({"Error": "Amplifier not registered"}, 400)

            firebase_db.child('users').child(str(request.form['email']).split('@')[0]).child(
                'paired').set({'amplifier': request.form['amplifier']})

            return 'Sucesfully created', 200

        except requests.exceptions.HTTPError:
            return 'Error', 400

    @app.route('/register/new/amplifier', methods=['POST'])
    def register_new_amplifier():
        if firebase_db.child('amplifiers').child(request.form['amplifier']).set({"volume": 0}):
            return 'Successfully registered', 200

        return 'Successfully registered', 400

    @app.route('/change/volume/by/id', methods=['POST'])
    def change_volume_by_id():
        amplifier = request.form['amplifier']
        volume = request.form['volume']

        if firebase_db.child('amplifiers').child(amplifier).child('volume').set(volume):
            return 'Volume successfully changed', 200

        return 'Error', 400

    @app.route('/change/volume/by/email', methods=['POST'])
    def change_volume_by_email():
        try:
            amplifier = firebase_db.child('users').child(
                str(request.form['email']).split('@')[0]).child(
                    'paired').child('amplifier').get().val()
        except Exception:
            return 'Account have no amplifiers paired', 400
        volume = request.form['volume']

        if firebase_db.child('amplifiers').child(amplifier).child('volume').set(volume):
            return 'Volume successfully changed', 200

        return 'Error', 400

    @app.route('/get/volume/by/id/<id>', methods=['GET'])
    def get_volume_by_id(id):
        print(id)
        volume = firebase_db.child('amplifiers').child(
            id).child('volume').get().val()

        if volume:
            return {"volume": volume}, 200

        return 'Error', 400

    @app.route('/get/volume/by/email/<email>', methods=['GET'])
    def get_volume_by_email(email):
        try:
            amplifier = firebase_db.child('users').child(
                email.split('@')[0]).child(
                    'paired').child('amplifier').get().val()
        except Exception:
            return 'Account have no amplifiers paired', 400

        volume = firebase_db.child('amplifiers').child(
            amplifier).child('volume').get().val()

        if volume:
            return {"volume": volume}, 200

    app.run(hostname, port)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Exited with error: ', e)
        sys.exit(1)
