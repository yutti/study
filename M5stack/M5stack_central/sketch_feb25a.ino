#include <M5Core2.h>
#include <WiFi.h>
#include <time.h>
#include <M5_ENV.h>
#include <stdio.h>
#include <stdlib.h>
#include <BLEDevice.h>
#include <string>

// 構造体の宣言
typedef struct {
	char *str;
} strct;

//Bluetooth
#define SERVER_NAME         "M5Atom-earth"
static BLEUUID  serviceUUID("8cf0a2f0-164d-4096-adef-9e89bc20044e");
static BLEUUID  charUUID("b5d67235-f2f0-4f81-9448-e029f3f4ea89");

static BLEAddress *pServerAddress;
static boolean doConnect = false;
static boolean connected = false;
static BLERemoteCharacteristic* pRemoteCharacteristic;
 
uint16_t earth_analog_val = 0;

// sprite 
TFT_eSprite sprite = TFT_eSprite(&M5.Lcd);

// csv file
//const char* fname = "/log.csv";
File file;

// set up sensor 
SHT3X sht30;
QMP6988 qmp6988;
long last_millis = 0;

// for WiFi
char ssid[] = "please input your SSID"; // your SSID
char pass[] = "please input your Pass word"; // your Pass word

float tmp      = 0.0;
float hum      = 0.0;
float pressure = 0.0;
int   earth_degtal = 0; 
int   earth_analog = 0; 
int   display_btm = 1; 
int   con_count = 0;
int   timer_reset = 0;
int   bule_address = 0;
bool  meas_csv = false;
bool  write_csv = false;
char info[40];

// for Time
const char* ntpServer = "ntp.jst.mfeed.ad.jp"; // NTP server
const long  gmtOffset_sec = 9 * 3600;          // Time offset 9hr
const int   daylightOffset_sec = 0;            // No summer time
RTC_DateTypeDef RTC_DateStruct; // Data
RTC_TimeTypeDef RTC_TimeStruct; // Time
struct tm timeinfo;
String dateStr;
String timeStr;

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice advertisedDevice) {
    Serial.print("BLE Advertised Device found: ");
    Serial.println(advertisedDevice.toString().c_str());//Address: 30:ae:a4:02:a3:fe, txPower: -21
    Serial.println(advertisedDevice.getName().c_str());//M5Atom-earth
    
    if(advertisedDevice.getName()==SERVER_NAME){
      Serial.println(advertisedDevice.getAddress().toString().c_str());
      advertisedDevice.getScan()->stop();
      pServerAddress = new BLEAddress(advertisedDevice.getAddress());
      doConnect = true;
    }
  }
};

void setup() {
  M5.begin();
  M5.Lcd.setBrightness(10);
  M5.Lcd.setRotation(1); 
  M5.Lcd.setTextSize(2);
  M5.Lcd.fillScreen(BLACK);

  Serial.println("Starting Arduino BLE Client application...");
  BLEDevice::init("");
  BLEScan* pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setInterval(1349);
  pBLEScan->setActiveScan(true);
  pBLEScan->start(5, false);

  // connect wifi  
  if (timer_reset == 1){
    WiFi.begin(ssid, pass);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      M5.Lcd.print(".");
      con_count++;
      if(con_count >= 20){
        break;
      }
    }
    if(con_count < 20){
      M5.Lcd.print("\nWiFi connected.");
      setNTP2RTC();
    }else{
      M5.Lcd.print("\nWiFi did not connect.");
    }
    M5.Lcd.print("\nIP=");
    M5.Lcd.print(WiFi.localIP());  
    delay(2 * 1000);
  }

  // Output on the display.
  M5.Lcd.fillScreen(BLACK);    
  M5.update();// update button state  
  delay(2 * 1000);

  Wire.begin();               //  // Wire init, adding the I2C bus.
  qmp6988.init();
  sprite.setColorDepth(8);
  sprite.setTextSize(2);
  sprite.fillScreen(BLACK);
  sprite.createSprite(M5.lcd.width(), M5.lcd.height());
  //make a directory
  if(!SD.exists("/sensor_data")){
    SD.mkdir("/sensor_data");
  }
}

void loop() {

  sprite.pushSprite( 0, 0);
  M5.update();// update button state

  //display select 
  if (M5.BtnA.wasPressed() == 1) display_btm = 1;
  if (M5.BtnB.wasPressed() == 1) display_btm = 2;
  if (M5.BtnC.wasPressed() == 1) display_btm = 3;

  if(display_btm == 1){
    // Get time 
    M5.Rtc.GetDate(&RTC_DateStruct);
    M5.Rtc.GetTime(&RTC_TimeStruct);

    pressure = qmp6988.calcPressure()* 0.01;
    if (sht30.get() == 0) {  // Obtain the data of shT30.  
      tmp = sht30.cTemp;     // Store the temperature obtained from shT30.
      hum = sht30.humidity;  // Store the humidity obtained from the SHT30.
    } else {
      tmp = 0, hum = 0;
    }

    // for Touch
    TouchPoint_t pos= M5.Touch.getPressPoint();
    if(pos.y > 240){
      if(pos.x < 109)
        sprite.setTextColor(RED,BLACK);
      else if(pos.x > 218)
        sprite.setTextColor(BLUE,BLACK);
      else if(pos.x >= 109 && pos.x <= 218)
        sprite.setTextColor(GREEN,BLACK);
    }

    sprite.fillScreen(BLACK);  

    sprite.setTextColor(WHITE);
    sprite.setCursor(0, 0, 1);
    sprite.printf("%04d.%02d.%02d ", RTC_DateStruct.Year, RTC_DateStruct.Month, RTC_DateStruct.Date);
    sprite.printf("%02d:%02d\n", RTC_TimeStruct.Hours, RTC_TimeStruct.Minutes);    
    sprite.printf("temperature: %4.1fdegC\n", tmp); 
    sprite.printf("humidity: %4.1f%%\n", hum); 
    sprite.printf("pressure: %4.1fhPa\n", pressure);    
    delay(1 * 1000);  
  }

  if(display_btm == 2){
    pressure = qmp6988.calcPressure()* 0.01;
    if (sht30.get() == 0) {  // Obtain the data of shT30.  
      tmp = sht30.cTemp;   // Store the temperature obtained from shT30.
      hum = sht30.humidity;  // Store the humidity obtained from the SHT30.
    } else {
      tmp = 0, hum = 0;
    }
    sprite.fillScreen(BLACK);     
    printData_btm2(sprite, 10,  10, 4, ORANGE, "temperature", tmp, "deg C");
    printData_btm2(sprite, 10,  80, 4, BLUE,      "humidity", hum, "%");
    printData_btm2(sprite, 10, 160, 4, TFT_MAROON,"pressure", pressure,"hPa");
    delay(0.5 * 1000);
  }

  if(display_btm == 3){

    if (doConnect == true) {
      delay(1 * 1000); 
      if (connectToServer(*pServerAddress)) {
        Serial.println("connected!");
        connected = true;
      } else {
      Serial.println("We have failed to connect to the server.");
      connected = false;
      }
      doConnect = false;
    }

    sprite.fillScreen(BLACK);
    // print for earth
    const char* bluetooth_status = connected ? "On" : "Off";
    printData_btm3(sprite, 10, 10, 4, ORANGE, "DEVICE NAM", "EARTH");
    printData_btm3(sprite, 10, 80, 4, BLUE, "Bluetooth connect", bluetooth_status);
    printData_btm3_int(sprite, 10, 160, 4, TFT_MAROON, "Analog value", earth_analog_val);    
    delay(1 * 1000); 
  }

  if (RTC_TimeStruct.Minutes % 5 == 4 ) meas_csv = true; 
  
  // get the csv per 5min
  if(RTC_TimeStruct.Minutes % 5 == 0){
     if (meas_csv == true){ 
      //write data per 5min.
      meas_csv = false;
      write_csv = true ;

      M5.Rtc.GetDate(&RTC_DateStruct);
      M5.Rtc.GetTime(&RTC_TimeStruct);

      pressure = qmp6988.calcPressure()* 0.01;
      if (sht30.get() == 0) {  // Obtain the data of shT30.  
        tmp = sht30.cTemp;     // Store the temperature obtained from shT30.
        hum = sht30.humidity;  // Store the humidity obtained from the SHT30.
      } else {
        tmp = 0, hum = 0;
      }

      // for Touch
      TouchPoint_t pos= M5.Touch.getPressPoint();
      if(pos.y > 240){
        if(pos.x < 109)
          sprite.setTextColor(RED,BLACK);
        else if(pos.x > 218)
          sprite.setTextColor(BLUE,BLACK);
        else if(pos.x >= 109 && pos.x <= 218)
          sprite.setTextColor(GREEN,BLACK);
      }   

      char fname[26];
      snprintf(fname, 26, "/sensor_data/%04d%02d%02d.csv", RTC_DateStruct.Year, RTC_DateStruct.Month, RTC_DateStruct.Date);

      // write data
      if(!SD.exists(fname)){
        file = SD.open(fname, FILE_APPEND);
        file.print("date,time,temperature,humidity,pressure\n");
        file.close();
        delay(0.1 * 1000); 
      }

      file = SD.open(fname, FILE_APPEND);
      file.print(RTC_DateStruct.Month);
      file.print("/");
      file.print(RTC_DateStruct.Date);
      file.print(",");      
      file.print(RTC_TimeStruct.Hours);
      file.print(":");
      if(RTC_TimeStruct.Minutes< 10) { 
        file.print("0");
      }
      file.print(RTC_TimeStruct.Minutes);
      file.print(",");

      file.print(tmp);
      file.print(",");    
      file.print(hum);
      file.print(",");
      file.print(pressure);
      file.print("\n");

      file.close();
    }
  }
}