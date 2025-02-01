from serial import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from datetime import datetime
from threading import Thread
import os

# Firebase Admin SDK 초기화
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://support-764f8-default-rtdb.firebaseio.com/'
})

last_value = 0

def get_data(ser):
    global last_value
    
    while True:
        try:
            if ser.inWaiting() > 0:
                last_value = float(ser.readline().decode().strip())
            
        except Exception as e:
            print(f'error : {e}')
    
    
            
if __name__ == '__main__':
    ser = Serial('/dev/ttyACM0', 9600, timeout=1)
    ref = db.reference('laundry')
    
    thread1 = Thread(target = get_data, args=(ser,))
    thread1.start()
    while True:
        try:
            """
            30 초 15 와트
            25 초 
            20 초 
            15 초 9 와트 ***
            """
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ref.set(last_value >= 8)
            print(f"저장됨: {current_time} - {last_value}")
            time.sleep(15)
            
        except Exception as e:
            print(f'firebase error : {e}')
    
    ser.close()
    
