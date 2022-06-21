import os
import time
from urllib import response
import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError, Timeout

from helpers.door import open_door
from helpers.facial import recognise_face
from helpers.fingerprint import get_fingerprint
from helpers.rfid import read_rfid_card


load_dotenv()


BASE_URL_HARDWARE = os.getenv('BASE_URL_HARDWARE')
BASE_URL_MAIN = os.getenv('BASE_URL_MAIN')


def main():
    # while True:
    id1 = read_rfid_card()
    id2 = get_fingerprint()
    id3 = recognise_face()

    if id1 == id2 and id1 == id3:
        open_door(16, id1) 
    else:
        print("failed to authenticate user")

if __name__ == "__main__":
    main()
