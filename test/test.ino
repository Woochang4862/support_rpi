#include<Simpletimer.h>

Simpletimer timer{};

int sensorPin = A2;    
int sensorValue = 0;
static const int number_of_time = 2;
double accW[number_of_time] {0,0};
double accA[number_of_time] {0,0};
double mW[number_of_time]  {0,0};
double mA[number_of_time] {0,0};
int count[number_of_time] {0,0};

void calculateByTenSeconds(){
   mW[0] = accW[0] / count[0];
   mA[0] = accA[0] / count[0];
   accW[0] = 0;
   accA[0] = 0;
   count[0] = 0;
}

void calculateByThirtySeconds(){
   mW[1] = accW[1] / count[1];
   mA[1] = accA[1] / count[1];
   accW[1] = 0;
   accA[1] = 0;
   count[1] = 0;
}

void calculateByOneMinute(){
   mW[2] = accW[2] / count[2];
   mA[2] = accA[2] / count[2];
   accW[2] = 0;
   accA[2] = 0;
   count[2] = 0;
}

Simpletimer::callback callbacks[number_of_time]
{
  calculateByTenSeconds,
  calculateByThirtySeconds
  // calculateByOneMinute
};
#define ONE_SECOND 1000
unsigned long intervals[number_of_time]
{
  10*ONE_SECOND,
  30*ONE_SECOND
  // 34*ONE_SECOND
};

void setup() {
  // declare the ledPin as an OUTPUT:
  int ledPin = 12;
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  timer.register_multiple_callbacks(callbacks, intervals, number_of_time);
  // Serial.print("와트, ");
  // Serial.print("암페어, ");
  // Serial.print("평균와트(10초), ");
  // Serial.print("평균와트(30초), ");
  // Serial.print("평균와트(60초), ");
  // Serial.print("평균암페어(10초), ");
  // Serial.print("평균암페어(30초), ");
  // Serial.print("평균암페어(60초), ");
  // Serial.print("데이터 수(10초)");
  // Serial.print("데이터 수(30초)");
  // Serial.println("데이터 수(60초)");
}

// bool Simpletimer::timer(unsigned long waitTime) {
//   Serial.println(_run_count);
//   return true;
// }

void loop() {
  // read the value from the sensor:
  sensorValue = analogRead(sensorPin);
  //Serial.print(" D : ");
  //Serial.println(sensorValue);
  timer.run();
  float A = map(sensorValue,0,573,0,20000) * 0.001;
  //Serial.print(" A : ");
  accA[0] += A;
  accA[1] += A;
  // accA[2] += A;
  //Serial.print(A*0.001);
  float W = 220 * A;
  accW[0] += W;
  accW[1] += W;
  // accW[2] += W;
  count[0]++;
  count[1]++;
  // count[2]++;
  //Serial.print(" W : ");
  Serial.println(W);
  /*Serial.print(",\t");
  Serial.print(A);
  Serial.print(",\t");
  Serial.print(mW[0]);
  Serial.print(",\t");
  Serial.print(mW[1]);
  Serial.print(",\t");
  // Serial.print(mW[2]);
  // Serial.print(",\t");
  Serial.print(mA[0]);
  Serial.print(",\t");
  Serial.print(mA[1]);
  Serial.print(",\t");
  // Serial.print(mA[2]);
  // Serial.print(",\t");
  Serial.print(count[0]);
  Serial.print(",\t");
  Serial.println(count[1]);
  // Serial.print(",\t");
  // Serial.println(count[2]);*/
  
}