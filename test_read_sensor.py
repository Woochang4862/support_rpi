import time
import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

# SPI 통신 설정
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)  # CE0 핀
mcp = MCP3008(spi, cs)

# TDS 센서 연결된 채널 (MCP3008의 채널 0 사용)
tds_channel = AnalogIn(mcp, MCP3008.P0)

# 보정 값 (필요에 따라 조정)
VREF = 5.0  # 참조 전압
TEMPERATURE = 25.0  # 물 온도

def read_tds():
    try:
        # 아날로그 값 읽기
        rawValue = tds_channel.value
        voltage = (rawValue * VREF) / 65536.0
        
        # 온도 보정
        compensation_coefficient = 1.0 + 0.02 * (TEMPERATURE - 25.0)
        
        # 보정된 전압
        compensation_voltage = voltage / compensation_coefficient
        
        # TDS 값 계산 (ppm)
        tds = (133.42 * compensation_voltage * compensation_voltage * compensation_voltage 
               - 255.86 * compensation_voltage * compensation_voltage 
               + 857.39 * compensation_voltage) * 0.5
        
        return tds
    except Exception as e:
        print(f'에러 발생: {e}')
        return None

def main():
    try:
        while True:
            tds_value = read_tds()
            if tds_value is not None:
                print(f'TDS 값: {tds_value:.2f} ppm')
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")

if __name__ == "__main__":
    main()
