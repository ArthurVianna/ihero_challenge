import socketio
import pprint
import json

from app.core.settings import get_settings
from app.db.session import get_db
from app.crud.occurrence import create_occurrence
from app.db.session import SessionLocal



def start_socket():
    sio = socketio.Client()
    settings = get_settings()
    sio.connect(settings.SOCKET_SERVER_ADDRESS)
    # print('my sid is', sio.sid)
    db = get_db()

    @sio.on(settings.SOCKET_EVENT_NAME)
    def occurence(data):
        # print('I received a occurrence!')
        occ = create_occurrence(data, db)
        # print("Occurrence created with id : " + str(occ.id))