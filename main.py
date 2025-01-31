import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from datetime import datetime

# Firebase Admin SDK 초기화
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://support-764f8-default-rtdb.firebaseio.com/'
})

def update_boolean_value():
    try:
        while True:
            # boolean 값 토글
            ref = db.reference('laundry')
            value = not ref.get()
            
            # Firebase에 데이터 저장
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ref.set(value)
            print(f"저장됨: {current_time} - {value}")
            
            # 10초 대기
            time.sleep(1)
            
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    print("Firebase에 boolean 값 저장 시작...")
    update_boolean_value()
