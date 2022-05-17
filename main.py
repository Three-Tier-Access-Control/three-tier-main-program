import requests


current_employee = {}

# read fingerprint


def get_fingerprint():
    finger_print_response = requests.get('/read-fingerprint')

    if finger_print_response.status == 200:
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
    rfid_response = requests.get('/read-rfid-card')
    if rfid_response.status == 200:
        # check to see who's rfid card it is

        employee_response = requests.get('/badges/find/{id}')
        current_employee = employee_response.data.employee

        # if error:
        # return False
        #
    else:
        # not found or error
        # retry 
        pass


def main():
    while True:
        get_fingerprint()

        read_rfid_card()

        # detect and capture face