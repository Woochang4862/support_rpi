import Adafruit_DHT
import time

# DHT11 센서 설정
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO 4번 핀 사용

def read_sensor():
    try:
        # 센서에서 온습도 데이터 읽기
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        
        if humidity is not None and temperature is not None:
            print(f'온도: {temperature:.1f}°C')
            print(f'습도: {humidity:.1f}%')
        else:
            print('센서 읽기 실패. 다시 시도해주세요.')
            
    except Exception as e:
        print(f'에러 발생: {e}')

def main():
    while True:
        read_sensor()
        # 2초 간격으로 센서 값 읽기
        time.sleep(2)

if __name__ == "__main__":
    main()
