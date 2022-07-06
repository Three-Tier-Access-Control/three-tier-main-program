from helpers.door import open_door
from helpers.facial import recognise_face
from helpers.fingerprint import get_fingerprint
from helpers.rfid import read_rfid_card


def main():
    # while True:
    id1 = get_fingerprint()
    # id1 = read_rfid_card()
    # id1 = recognise_face()

    if id1:
    # if id1 == id2 and id1 == id3:
        open_door(36, id1) 
    else:
        print("failed to authenticate user")

if __name__ == "__main__":
    main()
