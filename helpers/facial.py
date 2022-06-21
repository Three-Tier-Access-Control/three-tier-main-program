import os
import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError, Timeout


load_dotenv()


BASE_URL_HARDWARE = os.getenv('BASE_URL_HARDWARE')
BASE_URL_MAIN = os.getenv('BASE_URL_MAIN')


def recognise_face():
    try:
        facial_response = requests.get(
            f'{BASE_URL_HARDWARE}/recognize-face', timeout=30)
        json_facial_response = facial_response.json()
        employee_id = json_facial_response['id']
        print(
            f"successfully authenticated user with id: {employee_id}")
        return employee_id
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Timeout:
        print(
            f"The request timed out. No employee found: {employee_id}")
    except Exception as err:
        print(f'Other error occurred: {err}')
