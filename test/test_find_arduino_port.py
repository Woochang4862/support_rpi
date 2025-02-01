from serial import *
from serial.tools import list_ports

def find_arduino_port():
    """아두이노 포트를 자동으로 찾는 함수 (고급 버전)"""
    arduino_ports = [
        p.device
        for p in list_ports.comports()
        if 'Arduino' in p.description  # 아두이노 설명이 포함된 포트만 선택
    ]
    
    if not arduino_ports:
        raise Exception("아두이노를 찾을 수 없습니다.")
        
    return arduino_ports[0]

if __name__ == '__main__':
    arduino_port = find_arduino_port()
    ser = Serial(arduino_port, 9600, timeout=1)
    
    print(arduino_port)