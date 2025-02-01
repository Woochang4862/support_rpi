from serial import *
from serial.tools import list_ports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from datetime import datetime
from threading import Thread

last_value = 0

def find_arduino_port():
    arduino_ports = [
        p.device
        for p in list_ports.comports()
        if 'ttyACM' in p.description  # 아두이노 설명이 포함된 포트만 선택
    ]
    
    if not arduino_ports:
        raise Exception("아두이노를 찾을 수 없습니다.")
        
    return arduino_ports[0]

def get_data(ser):
    global last_value
    
    while True:
        try:
            if ser.inWaiting() > 0:
                last_value = float(ser.readline().decode().strip())
        except OSError as e:
            print(f'input/output error : {e}')
            return
        except Exception as e:
            print(f'error : {e}')            
    
    
            
if __name__ == '__main__':
    while True:
        try:
            if not firebase_admin._apps:
                # Firebase Admin SDK 초기화
                cred = credentials.Certificate('serviceAccountKey.json')
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://support-764f8-default-rtdb.firebaseio.com/'
                })    
        except Exception as e:
            print(f'firebase connection error : {e}')
            continue
    
    
        try:
            arduino_port = find_arduino_port()
            ser = Serial(arduino_port, 9600, timeout=1)
            thread1 = Thread(target = get_data, args=(ser,))
            thread1.start()        
        except Exception as e:
            print(f'arduino connection error : {e}')
            continue
        
        while thread1!=None and thread1.is_alive():
            try:
                """
                30 초 15 와트
                25 초 
                20 초 
                15 초 9 와트 ***
                """
                ref = db.reference('laundry')
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ref.set(last_value >= 8)
                print(f"저장됨: {current_time} - {last_value}")
                time.sleep(15)
                
            except Exception as e:
                print(f'error : {e}')
    
