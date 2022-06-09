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
def open_door(pin_number: int, employee_id: str):
    try:
        door_access_log = requests.post(
            f'{BASE_URL_MAIN}/access/', json={'employee': employee_id, "direction": "in", "status": True})
        door_on = requests.post(
            f'{BASE_URL_HARDWARE}/turn-on', json={'number': pin_number})
        print("Door open!!!")
        time.sleep(5)
        door_off = requests.post(
            f'{BASE_URL_HARDWARE}/turn-off', json={'number': pin_number})
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
        fingerprint_response = requests.get(
            f'{BASE_URL_HARDWARE}/read-fingerprint')

        json_fingerprint_response = fingerprint_response.json()
        finger = json_fingerprint_response['data']['finger']
        confidence = json_fingerprint_response['data']['confidence']
        msg = json_fingerprint_response['data']['msg']

        print(finger, confidence, msg)

        # match found
        # check to see who's finger it is
        employee_response = requests.get(
            f'{BASE_URL_MAIN}/fingerprint/?fingerprint_id={finger}')
        json_employee_response = employee_response.json()
        results = json_employee_response['results']
        if results:
            current_employee = results[0]["employee"]
            first_name = current_employee["first_name"]
            last_name = current_employee["last_name"]
            print(
                f"successfully authenticated user: {first_name} {last_name}")
            open_door(pin_number=16, employee_id=current_employee["id"])
        else:
            print(
                f"No employee found with the given fingerprint id: {finger}")
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
        employee_id = json_rfid_response['data']['employee_id']

        print(f"Got {employee_id} from card with id {uid}")

        employee_response = requests.get(
            f'{BASE_URL_MAIN}/rfid/?employee__id={employee_id}')

        json_employee_response = employee_response.json()
        results = json_employee_response['results']
        if results:
            current_employee = results[0]["employee"]
            first_name = current_employee["first_name"]
            last_name = current_employee["last_name"]
            print(
                f"successfully authenticated user: {first_name} {last_name}")
            open_door(pin_number=16, employee_id=current_employee["id"])
        else:
            print(
                f"No employee found with the given id: {employee_id}")
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Timeout:
        print('The request timed out')
    except Exception as err:
        print(f'Other error occurred: {err}')


def main():
    # while True:
    read_rfid_card()
        # get_fingerprint()

    # detect and capture face


if __name__ == "__main__":
    main()
