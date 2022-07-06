import os
import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError, Timeout

load_dotenv()


BASE_URL_HARDWARE = os.getenv('BASE_URL_HARDWARE')
BASE_URL_MAIN = os.getenv('BASE_URL_MAIN')

# read rfid card
def read_rfid_card():
    try:
        rfid_response = requests.get(
            f'{BASE_URL_HARDWARE}/read-rfid-card')
        json_rfid_response = rfid_response.json()
        # check to see who's rfid card it is
        uid = json_rfid_response['data']['uid']
        employee_id = json_rfid_response['data']['employee_id']

        employee_response = requests.get(
            f'{BASE_URL_MAIN}/rfid/?employee__id={employee_id}')

        results = employee_response.json()
        if results:
            current_employee = results[0]["employee"]
            first_name = current_employee["first_name"]
            last_name = current_employee["last_name"]
            print(
                f"successfully authenticated user: {first_name} {last_name}")
            return employee_id
        else:
            print(
                f"No employee found with the given id: {employee_id}")
            return None
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Timeout:
        print('The request timed out')
    except Exception as err:
        print(f'Other error occurred: {err}')

