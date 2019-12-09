import sys
import click
from flask import Flask
from flask import request
from flask import make_response
import requests
import firebase

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

    firebase_db = firebase.Firebase(config)

    app = Flask(__name__)

    @app.route('/get/paired/amplifier/<email>', methods=['GET'])
    def paired_amplifier(email):
        return firebase_db.get_paired_amplifier(email)

    @app.route('/pair/new/amplifier', methods=['POST'])
    def paired_new_amplifier():
        return firebase_db.pair_new_amplifier(request.form['amplifier'], request.form['email'])

    @app.route('/register/new/amplifier', methods=['POST'])
    def register_new_amplifier():
        return firebase_db.register_new_amplifier(request.form['amplifier'])

    @app.route('/change/volume/by/id', methods=['POST'])
    def change_volume_by_id():
        return firebase_db.change_volume_by_id(request.form['amplifier'], request.form['volume'])

    @app.route('/change/volume/by/email', methods=['POST'])
    def change_volume_by_email():
        return firebase_db.change_volume_email(request.form['email'], request.form['volume'])

    @app.route('/get/volume/by/id/<id>', methods=['GET'])
    def get_volume_by_id(id):
        return firebase_db.get_volume_by_id(id)

    @app.route('/get/volume/by/email/<email>', methods=['GET'])
    def get_volume_by_email(email):
        return firebase_db.get_volume_by_email(email)

    @app.route('/is/registred/<id>', methods=['GET'])
    def is_registred(id):
        return firebase_db.is_registred_amplifier(id)

    app.run(hostname, port)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Exited with error: ', e)
        sys.exit(1)
