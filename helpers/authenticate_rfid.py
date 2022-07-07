#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
import requests
from mfrc522 import SimpleMFRC522

BASE_URL_HARDWARE = "http://threetiersystem.local:5000/api/v1"
BASE_URL_MAIN = "http://threetiersystem.local:8000/api"

reader = SimpleMFRC522()


def authenticate_rfid():
    try:
        print("----------------")
        print("Authenticating card...")
        print("----------------")
        requests.post(
            f'{BASE_URL_HARDWARE}/write-to-lcd', json={'text': "Place card..."})
        id, text = reader.read()
        employee_id = text.strip()
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
    except Exception as err:
        print(f'Other error occurred: {err}')
    finally:
        GPIO.cleanup()

