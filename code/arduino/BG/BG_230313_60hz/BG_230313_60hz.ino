#include "SparkFun_AS7265X.h"
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define DATA_POINTS 1680

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
 
AS7265X sensor;

const int LED_940 = 7;
const int LED_860 = 6;
const int LED_810 = 5;

static const unsigned char epd_bitmap_rim [] PROGMEM = {
	0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff
};

static unsigned char bitmap[320];

uint16_t previousData[64] = {0};
uint16_t minValue = 65535;
uint16_t maxValue = 0;

long start_t;
long last_t;
long current_t;
long count=1;

float avg_hz = 0.0f;

void recordLED(int data_points, int type);
void record3cycles();

void setup()
{
  Wire.begin();
  Serial.begin(115200);

  pinMode(LED_810, OUTPUT);
  pinMode(LED_860, OUTPUT);
  pinMode(LED_940, OUTPUT);
  
  digitalWrite(LED_810, HIGH);
  digitalWrite(LED_860, HIGH);
  digitalWrite(LED_940, HIGH);  

  Serial.println("starting");
  
  if(sensor.begin() == false){
    Serial.println("Sensor does not appear to be connected. Please check wiring. Freezing...");
    while(1);
  }

  sensor.disableIndicator();

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("SSD1306 allocation failed"));
    while(1);
  }

  display.display();

  delay(2000); // Pause for 2 seconds

  display.clearDisplay();

  Serial.println("started");
    
  Wire.setClock(400000);    
    
  sensor.setMeasurementMode(AS7265X_MEASUREMENT_MODE_4CHAN);    //用continuous是一直收資料的模式

  sensor.setIntegrationCycles(1);

  start_t = millis();
  last_t = start_t;  
}

void loop()
{ 
  // if(Serial.available() && Serial.read()) record3cycles();
  // if(Serial.available() && Serial.read()) recordNoneStop();
  recordNoneStop();
}

void recordNoneStop(){
  digitalWrite(LED_810, HIGH);
  digitalWrite(LED_860, HIGH);
  digitalWrite(LED_940, HIGH);  
  // 指定要亮的LED
  // digitalWrite(LED_810, HIGH);

  uint16_t w = 0;
  uint16_t v = 0;
  uint16_t l = 0;

  while(1){
    count++;
    if(count%100 == 0){
      current_t = millis();
      avg_hz =  ((float)count - 1.0f) * 1000.0f / (current_t - last_t);
      last_t = current_t;
      count = 1;
    }
    // w = sensor.getW();
    v = sensor.getV();
    // l = sensor.getL();
    // Serial.print(w); //810nm
    // Serial.print(",");
    // Serial.print(v); //810nm
    // Serial.print(",");
    // Serial.print(l); //810nm
    // Serial.print(",");
    // Serial.print(avg_hz);
    // Serial.println();
    drawData(w, v, l, avg_hz, LED_860);
  }
}

void record3cycles(){
  int data_points = DATA_POINTS;
  recordLED(data_points, LED_810);
  // recordLED(data_points, LED_860);
  // recordLED(data_points, LED_940);
  
  // csv end identifier
  Serial.print(99); //810nm
  Serial.print(",");
  Serial.print(99); //860nm
  Serial.print(",");
  Serial.print(99); //940nm
  Serial.println();
}

void recordLED(int data_points, int type){
  int count = 0;

  // csv start identifier
  Serial.print(data_points); 
  Serial.print(",");
  Serial.print(type); 
  Serial.print(",");
  Serial.print(0); 
  Serial.println();

  // reset LED state
  // 將每一盞LED預設為low  
  digitalWrite(LED_810, LOW);
  digitalWrite(LED_860, LOW);
  digitalWrite(LED_940, LOW);  
  // 指定要亮的LED
  digitalWrite(type, HIGH);

  //原本還沒亮就會開始收資料，所以加delay
  delay(100);


  // record section
  while(count++ < data_points){

    current_t = millis();

    //只顯示現在亮燈波長的數值
    switch(type) {
      case LED_810:  
        Serial.print(sensor.getCalibratedV());
        Serial.println(); //810nm
        break;
      
      case LED_860:
        Serial.print(sensor.getCalibratedW()); //860nm
        Serial.println();
        break;

      case LED_940: 
        Serial.print(sensor.getCalibratedL()); //940nm
        Serial.println();      
        break;
    }

    // Serial.print(sensor.getCalibratedV()); //810nm
    // Serial.print(",");
    // Serial.print(sensor.getCalibratedW()); //860nm
    // Serial.print(",");
    // Serial.print(sensor.getCalibratedL()); //940nm
    // Serial.println();

    last_t = current_t;
  }

}

void drawData(uint16_t Data_810, uint16_t Data_860, uint16_t Data_940, float Hertz, int type) {
  Data_810 = min(999, Data_810);
  Data_860 = min(999, Data_860);
  Data_940 = min(999, Data_940);

  display.clearDisplay();

  display.setTextSize(1);             // Normal 1:1 pixel scale
  display.setTextColor(WHITE);        // Draw white text
  display.setCursor(0,0);             // Start at top-left corner
  display.print("810nm: ");
  display.println(Data_810);
  display.println();

  display.setTextColor(WHITE); 
  display.print("860nm: ");
  display.println(Data_860);
  display.println();

  display.setTextColor(WHITE); 
  display.print("940nm: ");
  display.println(Data_940);
  display.println();

  display.setTextColor(BLACK, WHITE);
  display.print(" Current Hertz: ");
  display.println(Hertz);
  display.println();

  for (int i = 1; i < 64; i++) {
    previousData[i - 1] = previousData[i];
  }

  switch(type) {
      case LED_810:  
        previousData[63] = Data_810;
        break;
      
      case LED_860:
        previousData[63] = Data_860;
        break;

      case LED_940: 
        previousData[63] = Data_940;
        break;
  }

  for (int i = 0; i < 64; i++) {
    minValue = 65535;
    maxValue = 0;
    minValue = min(minValue, previousData[i]);
    maxValue = max(maxValue, previousData[i]);
  }

  drawNewDataPoint(previousData, minValue, maxValue);

  display.drawBitmap(64, 0, bitmap, 64, 40, SSD1306_WHITE);

  display.display();
}

void drawNewDataPoint(uint16_t newData[], uint16_t minValue, uint16_t maxValue) {
  uint16_t padding = (maxValue - minValue) * 0.1;
  minValue = minValue > padding ? minValue - padding : 0;
  maxValue += padding;

  for (int i=0; i<320; i++){
    bitmap[i] = 0;
  }

  for (int i = 0; i < 64; i++) {
    uint16_t value = newData[i];

    uint16_t pixelHeight = v_map(value, minValue, maxValue, 0, 39);

    Serial.println(pixelHeight);

    for (int j = 39; j >= 0; j--) {
      int byteIndex = (j * 8) + (i / 8);
      int bitIndex = i % 8;
      if(pixelHeight == j);
        bitmap[byteIndex] |= (1 << bitIndex);
    }
  }

  for (int i=0; i<320; i++){
    bitmap[i] |= epd_bitmap_rim[i];
  }
}

uint16_t v_map(uint16_t value, uint16_t inMin, uint16_t inMax, uint16_t outMin, uint16_t outMax) {
  return (uint16_t)((uint32_t)(value - inMin) * (uint32_t)(outMax - outMin) / (uint32_t)(inMax - inMin + 1) + outMin);
}