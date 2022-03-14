import os

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

BUTTON_STATE = {}
WEBSOCKETS = {}

ALL_SWITCH_OFF = {
    "1":False,
    "2":False,
    "3":False,
    "4":False,
    "5":False,
    "6":False,
    "7":False,
    "8":False
}