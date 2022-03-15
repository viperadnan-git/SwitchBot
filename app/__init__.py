import os

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

ACTIVE_DEVICES = {}
TEMP_CON_DB = {}