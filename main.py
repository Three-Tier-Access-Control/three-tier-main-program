import os
from urllib import response
import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError


load_dotenv()


BASE_URL_HARDWARE = os.getenv('BASE_URL_HARDWARE')
BASE_URL_MAIN = os.getenv('BASE_URL_MAIN')

current_employee = {}

# read fingerprint


def get_fingerprint():
    fingerprint_response = requests.get('/read-fingerprint')

    if fingerprint_response.status_code == 200:
        # match found
        # check to see who's finger it is

        employee_response = requests.get('/fingerprints/find/{id}')
        current_employee = employee_response.data.employee

        # if error:
        # return False
        #
    else:
        # not found or error
        # retry
        pass


def read_rfid_card():
    try:
        rfid_response = requests.get(f'{BASE_URL_HARDWARE}/read-rfid-card')
        json_rfid_response = rfid_response.json()
        # check to see who's rfid card it is
        uid = json_rfid_response['uid']
        text = json_rfid_response['text']

        print(f"Got {text} from card with id {uid}")

        # employee_response = requests.get(
        #     f'{BASE_URL_MAIN}/badges/find/{id}')

        # json_employee_response = employee_response.json()
        # current_employee = json_employee_response['data']['employee']

        # print(current_employee)


        # if authenticated:
        print("successfully authenticated user")

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def main():
    while True:
        read_rfid_card()

        # get_fingerprint()

        # detect and capture face


if __name__ == "__main__":
    main()
