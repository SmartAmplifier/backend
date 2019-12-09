import pyrebase

class Firebase:
    def __init__(self, config):
        self._db = pyrebase.pyrebase.Firebase(config).database()

    def get_paired_amplifier(self, email):
        try:
            return dict(self._db.child('users').child(str(email).split(
                '@')[0]).child('paired').get().val()), 200
        
        except Exception:
            return {'paired': None}, 200

    def pair_new_amplifier(self, id, email):
        try:
            registred = self._db.child("amplifiers").child(id).get().val()

            if not registred:
                return {'Error': 'Not register'}, 400

            self._db.child('users').child(str(email).split('@')[0]).child(
                'paired').set({'amplifier': id})

            return {'Message': 'Successfully paired'}, 200
        
        except Exception:
            return {'Error': 'Cannot pair new amplifier'}, 400

    def register_new_amplifier(self, id):
        try:
            self._db.child('amplifiers').child(id).set({"volume": 0})

            return {'Message': 'Successfully registred'}, 200
        
        except Exception:
            return {'Error': 'Error while registring new amplifier'}, 400

    def change_volume_by_id(self, id, volume):
        try:
            try:
                volume = int(volume)
            except ValueError:
                return {'Error': 'Volume not intiger'}, 400

            if volume > 100:
                return {'Error': 'Maximal volume is 100 (%)'}, 400

            self._db.child('amplifiers').child(id).child('volume').set(volume)

            return {'Message': 'Volume changed'}, 200
        
        except Exception:
            return {'Error': 'Error while changing volume'}, 400

    def change_volume_email(self, email, volume):
        try:
            amplifier = self._db.child('users').child(
                str(email).split('@')[0]).child(
                'paired').child('amplifier').get().val()
            
            if not amplifier:
                return {'Error': 'No amplifier paired to account'}, 400

            try:
                volume = int(volume)
            except ValueError:
                return {'Error': 'Volume not intiger'}, 400

            if volume > 100:
                return {'Error': 'Maximal volume is 100 (%)'}, 400

            if self._db.child('amplifiers').child(amplifier).child('volume').set(volume):
                return 'Volume successfully changed', 200
        
        except Exception:
            return {'Error': 'Error while changing volume'}, 400

# TODO: Add if device is registred
    def get_volume_by_id(self, id):
        try:
            volume = self._db.child('amplifiers').child(id).child('volume').get().val()

            if volume:
                return {'volume': volume}

            elif self.is_registred_amplifier(id)[1] == 400:
                return {'Error': 'Amplifier not registred'}

            return {'Error': 'Cannot get volume'}, 400
        
        except Exception:
            return {'Error': 'Error while getting volume'}, 400

    def get_volume_by_email(self, email):
        try:
            amplifier = self._db.child('users').child(
                email.split('@')[0]).child(
                    'paired').child('amplifier').get().val()

            if not amplifier:
                return {'Error': 'No amplifier paired'}, 400

            volume = self._db.child('amplifiers').child(
                amplifier).child('volume').get().val()

            if volume:
                return {'volume': volume}, 200

            elif self.is_registred_amplifier(id)[1] == 400:
                return {'Error': 'Amplifier not registred'}

            return {'Error': 'Cannot get volume'}, 400
        
        except Exception:
            return {'Error': 'Account have no amplifiers paired'}, 400

    def is_registred_amplifier(self, id):
        try:
            if self._db.child('amplifiers').child(id).get().val():
                return {"registred": True}, 200

            return {"registred": False}, 400
        except Exception:
            return {'Error': 'Error while checking if registred'}, 400