import pandas as pd
import matplotlib.pyplot as plt

def read_csv_file(file_path):
    try:
        # CSV 파일 읽기
        df = pd.read_csv(file_path, encoding='euc-kr')
        
        # 데이터 기본 정보 출력
        print("데이터 크기:", df.shape)
        print("\n처음 5행:")
        print(df.head())
        
        # 각 열의 최소값 출력
        print("\n각 열의 최소값:")
        print(df.min())
        
        return df
    
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return None

def plot_watt_averages(df):
    try:
        plt.figure(figsize=(12, 6))
        
        # 현재 와트 플롯
        plt.plot(df.index, df['현재 와트'], label='현재 와트', alpha=0.3, color='gray')
        
        # 10초 와트평균 (CSV에서 직접 사용)
        plt.plot(df.index, df['10초 와트평균'], label='10초 평균', linewidth=2)
        
        # 30초 이동평균
        plt.plot(df.index, df['30초와트평균'], label='30초 평균', linewidth=2)
        
        plt.axhline(y=25, color='r', linestyle='--', label='100W')
        
        plt.title('와트 측정값 및 이동평균')
        plt.xlabel('시간')
        plt.ylabel('와트')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    except Exception as e:
        print(f"그래프 생성 중 오류 발생: {str(e)}")

# 사용 예시
if __name__ == "__main__":
    file_path = "data.csv"  # CSV 파일 경로를 지정하세요
    data = read_csv_file(file_path)
    plot_watt_averages(data)