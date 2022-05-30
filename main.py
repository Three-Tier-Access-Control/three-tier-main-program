import os
import time
from urllib import response
import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError, Timeout


load_dotenv()


BASE_URL_HARDWARE = os.getenv('BASE_URL_HARDWARE')
BASE_URL_MAIN = os.getenv('BASE_URL_MAIN')

current_employee = {}


# open door for 5 seconds
def open_door(number: int):
    try:
        door_on = requests.post(
            f'{BASE_URL_HARDWARE}/turn-on', json={'number': number})
        print("Door open!!!")
        time.sleep(5)
        door_off = requests.post(
            f'{BASE_URL_HARDWARE}/turn-off', json={'number': number})
        print("Door closed.")
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Timeout:
        print('The request timed out')
    except Exception as err:
        print(f'Other error occurred: {err}')


# read fingerprint


def get_fingerprint():
    try:

        fingerprint_response = requests.get(f'{BASE_URL_HARDWARE}/read-fingerprint')

        if fingerprint_response.status_code == 200:
            json_fingerprint_response = fingerprint_response.json()
            finger = json_fingerprint_response['data']['finger']
            confidence = json_fingerprint_response['data']['confidence']
            msg = json_fingerprint_response['data']['msg']


            # match found
            # check to see who's finger it is

            # employee_response = requests.get(f'{BASE_URL_MAIN}/fingerprints/find/{finger}')
            # json_employee_response = employee_response.json()

            # current_employee = json_employee_response['data']['employee']

            # print(current_employee)

            print("successfully authenticated user")
            open_door(16)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Timeout:
        print('The request timed out')
    except Exception as err:
        print(f'Other error occurred: {err}')

# read rfid card


def read_rfid_card():
    try:
        rfid_response = requests.get(
            f'{BASE_URL_HARDWARE}/read-rfid-card')
        json_rfid_response = rfid_response.json()
        # check to see who's rfid card it is
        uid = json_rfid_response['data']['uid']
        text = json_rfid_response['data']['text']

        print(f"Got {text} from card with id {uid}")

        # employee_response = requests.get(
        #     f'{BASE_URL_MAIN}/badges/find/{id}')

        # json_employee_response = employee_response.json()
        # current_employee = json_employee_response['data']['employee']

        # print(current_employee)

        # if authenticated:
        print("successfully authenticated user")
        open_door(16)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Timeout:
        print('The request timed out')
    except Exception as err:
        print(f'Other error occurred: {err}')


def main():
    # while True:
    # read_rfid_card()

    get_fingerprint()

    # detect and capture face


if __name__ == "__main__":
    main()
