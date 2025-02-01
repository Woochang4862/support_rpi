#include <Arduino.h>
#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <Simpletimer.h>
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

// WiFi 자격증명
#define WIFI_SSID "당신의_WiFi_SSID"
#define WIFI_PASSWORD "당신의_WiFi_비밀번호"

// Firebase 프로젝트 설정
#define API_KEY "당신의_FIREBASE_API_KEY"
#define DATABASE_URL "당신의_FIREBASE_DATABASE_URL"

// Firebase 객체 선언
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

Simpletimer timer{};

// sen0211 센서 설정
const int sensorPin = A0;  
float currentValue = 0;
float powerValue = 0;

void sendToFirebase() {
  if (Firebase.ready()) {
    // 현재 타임스탬프 생성
    String timestamp = String(millis());
    
    // 데이터 저장 경로 설정
    String path = "/sensor_data/" + timestamp;
    
    // Firebase에 데이터 저장
    Firebase.RTDB.setFloat(&fbdo, path + "/current", currentValue);
    Firebase.RTDB.setFloat(&fbdo, path + "/power", powerValue);
  }
}

Simpletimer::callback callbacks[] = {sendToFirebase};
unsigned long intervals[] = {10000}; // 10초

void setup() {
  Serial.begin(115200);
  
  // WiFi 연결
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("WiFi 연결 중...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("연결됨, IP 주소: ");
  Serial.println(WiFi.localIP());

  // Firebase 설정
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  // 타이머 설정
  timer.register_multiple_callbacks(callbacks, intervals, 1);
}

void loop() {
  // sen0211 센서 읽기
  int sensorValue = analogRead(sensorPin);
  
  // 전류값 계산 (센서 사양에 맞게 조정 필요)
  currentValue = (sensorValue - 2048) * 0.0488; // mA
  
  // 전력 계산 (220V 가정)
  powerValue = 220 * currentValue; // mW
  
  // 타이머 실행
  timer.run();
  
  // 시리얼 모니터에 출력
  Serial.print("전류(mA): ");
  Serial.print(currentValue);
  Serial.print("\t전력(mW): ");
  Serial.println(powerValue);
  
  delay(100);
}
