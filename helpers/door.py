import os
import time
import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError, Timeout


load_dotenv()


BASE_URL_HARDWARE = os.getenv('BASE_URL_HARDWARE')
BASE_URL_MAIN = os.getenv('BASE_URL_MAIN')

# open door for 5 seconds


def open_door(pin_number: int, employee_id: str):
    try:
        requests.post(
            f'{BASE_URL_HARDWARE}/turn-on', json={'number': pin_number})
        print("Door open!!!")
        requests.post(
            f'{BASE_URL_HARDWARE}/write-to-lcd', json={'text': "Door open..."})
        time.sleep(5)
        requests.post(
            f'{BASE_URL_HARDWARE}/turn-off', json={'number': pin_number})
        print("Door closed.")
        requests.post(
            f'{BASE_URL_HARDWARE}/write-to-lcd', json={'text': "Door closed..."})
        requests.post(
            f'{BASE_URL_MAIN}/access/', json={'employee': employee_id, "direction": "in", "status": True})
        requests.post(
            f'{BASE_URL_HARDWARE}/write-to-lcd', json={'text': ""})
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Timeout:
        print('The request timed out')
    except Exception as err:
        print(f'Other error occurred: {err}')

