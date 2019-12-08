#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import random
import subprocess
import time
import requests


def main():
    # Set up logging
    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.root.setLevel(logging.NOTSET)

    # Run backend
    logging.info('Starting backend')
    subprocess.Popen(['python3', 'backend.py', '-h',
                      'localhost', '-p', '8080'])
    time.sleep(2)

    # Generate random TESTER-<INT> amplifier
    tested_amplifier = 'TESTER-' + str(random.randint(111111, 999999))

    # Try to pair generated amplifier before it is registred
    logging.info(
        'Try to pair virtual amplifier to account tester@email.xx')
    pair_new_amplifier = requests.post('http://localhost:8080/pair/new/amplifier',
                                       {"email": "tester@email.xx", "amplifier":
                                        tested_amplifier})
    if pair_new_amplifier.status_code != 200:
        logging.info('Status code not 200 in pairing new amplifier. Code: {}'.format(
            pair_new_amplifier.status_code))

    else:
        logging.critical('Virtual amplifier paired before it is created')
        sys.exit(1)

    # Register generated amplifier
    logging.info('Register virtual amplifier')
    register_new_amplifier = requests.post('http://localhost:8080/register/new/amplifier',
                                           {"amplifier": tested_amplifier})
    logging.info('Virtual amplifier successfully created')
    if register_new_amplifier.status_code != 200:
        logging.critical('Register failed')
        sys.exit(1)

    # Try to pair register generated virtual amplifier
    logging.info(
        'Try to pair virtual amplifier again after it is registered to account tester@email.xx')
    pair_new_amplifier = requests.post('http://localhost:8080/pair/new/amplifier',
                                       {"email": "tester@email.xx", "amplifier":
                                        tested_amplifier})
    if pair_new_amplifier.status_code != 200:
        logging.info('Status code not 200. Code: {}'.format(
            pair_new_amplifier.status_code))
        sys.exit(1)

    else:
        logging.info('Virtual amplifier paired')

    # Check if pair was successfull
    logging.info('Check if virtual amplifier paired with account')
    paired_amplifier = requests.get(
        'http://localhost:8080/get/paired/amplifier/tester@email.xx').json()
    if paired_amplifier['amplifier'] != str(tested_amplifier):
        logging.critical(
            'Paired amplifier is not one we paired in previous step')
        sys.exit(1)

    # Change volume to 40 by amplifier id
    logging.info('Change volume to 40 by amplifier id')
    change_volume = requests.post(
        'http://localhost:8080/change/volume/by/id', {"amplifier": tested_amplifier, "volume": 40})
    if change_volume.status_code != 200:
        logging.critical('Error while changing volume')
        sys.exit(1)

    volume = requests.get(
        'http://localhost:8080/get/volume/by/id/{}'.format(tested_amplifier)).json()['volume']

    if volume == str(40):
        logging.info('Change succesfull successfull')

    else:
        logging.critical('Volume not 40 after change')
        sys.exit(1)

    # Change volume to 80 by email
    logging.info('Change volume to 40 by email')
    change_volume = requests.post(
        'http://localhost:8080/change/volume/by/email', {"email": "tester@email.xx", "volume": 80})
    if change_volume.status_code != 200:
        logging.critical('Error while changing volume')
        sys.exit(1)

    volume = requests.get(
        'http://localhost:8080/get/volume/by/email/tester@email.xx').json()['volume']

    if volume == str(80):
        logging.info('Change succesfull successfull')

    else:
        logging.critical('Volume not 40 after change')
        sys.exit(1)

    # Now we are done, test successfull
    logging.info('Test successfull')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Exited with error: ', e)
        sys.exit(1)
