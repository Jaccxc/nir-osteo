#include "SparkFun_AS7265X.h" 
AS7265X sensor;

const int LED_940 = 5;
long start_t;
long last_t;
long current_t;
long count = 0 ;

void setup()
{
  Wire.begin();    //Arduino與sensor用i2c連線
  Serial.begin(115200);
  pinMode(LED_940, OUTPUT);
  digitalWrite(LED_940, HIGH);
  if(sensor.begin() == false){
    Serial.println("Sensor does not appear to be connected. Please check wiring. Freezing...");
    while(1);
  }
  
  Wire.setClock(400000);    
    
  sensor.setMeasurementMode(AS7265X_MEASUREMENT_MODE_6CHAN_CONTINUOUS);    //用continuous是一直收資料的模式
  
  sensor.setIntegrationCycles(1);  

  start_t = millis();
  last_t = start_t;
}

void loop()
{
  // sensor.takeMeasurements(); //This is a hard wait while all 18 channels are measured

  current_t = millis();
  count++;

  Serial.print(sensor.getCalibratedV()); //810nm
  // Serial.print(",");
  // Serial.print(sensor.getCalibratedW()); //860nm
  // Serial.print(",");
  // Serial.print(sensor.getCalibratedL()); //940nm
  Serial.print(", count: ");  
  // Serial.print(1000.0f/(current_t-last_t));
  Serial.print(count);
  Serial.println();

  last_t = current_t;
}