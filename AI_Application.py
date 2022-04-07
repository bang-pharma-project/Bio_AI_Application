from Backend import M1_saperation_main
from Backend import M2_purification_main
from threading import Thread
from settings import __APP_SETTINGS__

room_m1 = M1_saperation_main.Room_M1_Application()
room_m2 = M2_purification_main.Room_M2_Application()

room_m1_thread = Thread(target=room_m1.main_function)
room_m2_thread = Thread(target=room_m2.main_function)

if __APP_SETTINGS__.RUN_ROOM_M1:
    room_m1_thread.start()

if __APP_SETTINGS__.RUN_ROOM_M2:
    room_m2_thread.start()


if __APP_SETTINGS__.RUN_ROOM_M1:
    room_m1_thread.join()

if __APP_SETTINGS__.RUN_ROOM_M2:
    room_m2_thread.join()