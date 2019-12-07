import sys
import logging
import random
import requests


def main():
    tested_amplifier = random.randint(111111, 999999)
    print('Pair new amplifier')
    pair_new_amplifier = requests.post('http://localhost:8080/pair/new/amplifier', {"email": "tester@email.xx", "amplifier": tested_amplifier})
    print(pair_new_amplifier)
    if pair_new_amplifier.status_code != 200:
        print('Status code not 200 in pairing new amplifier')

    paired_amplifier = requests.get('http://localhost:8080/get/paired/amplifier/tester@email.xx').json()
    if paired_amplifier['amplifier'] != str(tested_amplifier):
        print('Paired amplifier is not one we paired in previous step')


    print('Test succesfull')
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Exited with error: ', e)
        sys.exit(1)