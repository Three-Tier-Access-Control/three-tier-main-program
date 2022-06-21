import os
import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError, Timeout


load_dotenv()


BASE_URL_HARDWARE = os.getenv('BASE_URL_HARDWARE')
BASE_URL_MAIN = os.getenv('BASE_URL_MAIN')

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
            employee_id = current_employee["id"]
            print(
                f"successfully authenticated user: {first_name} {last_name}")
            return employee_id
        else:
            print(
                f"No employee found with the given fingerprint id: {finger}")
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Timeout:
        print('The request timed out')
    except Exception as err:
        print(f'Other error occurred: {err}')


