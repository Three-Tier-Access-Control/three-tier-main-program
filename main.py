from helpers.authenticate_face_id import authenticate_face_id
from helpers.authenticate_fingerprint import authenticate_fingerprint
from helpers.authenticate_rfid import authenticate_rfid
from helpers.door import open_door


def main():
    # while True:
    id1 = authenticate_fingerprint()
    id2 = authenticate_rfid()
    id3 = authenticate_face_id()

    if id1:
        open_door(36, id1) 
    elif id2:
        open_door(36, id2) 
    elif id3:
        open_door(36, id3) 
    else:
        print("failed to authenticate user")

if __name__ == "__main__":
    main()
