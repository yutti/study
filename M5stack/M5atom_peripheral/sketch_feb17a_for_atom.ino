#include "M5Atom.h"
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>
 
#define SERVICE_UUID        "8cf0a2f0-164d-4096-adef-9e89bc20044e"
#define CHARACTERISTIC_UUID "b5d67235-f2f0-4f81-9448-e029f3f4ea89"
#define SERVER_NAME         "M5Atom-earth"
 
BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;

uint16_t analogRead_value = 0;
uint16_t digitalRead_value = 0;
uint16_t device_id = 0x0101;        // your any sensor device id
 
void readEarthSensor() {
  analogRead_value = analogRead(32);
  digitalRead_value = digitalRead(26);
  Serial.printf("0x%04x, %d, %d\n", device_id, digitalRead_value, analogRead_value);
}

void print_readEarthSensor() {
  analogRead_value = analogRead(32);
  digitalRead_value = digitalRead(26);
  pCharacteristic->setValue(analogRead_value);
  pCharacteristic->notify(); 
}

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      Serial.println("connect");
      deviceConnected = true;
    };
    void onDisconnect(BLEServer* pServer) {
      Serial.println("disconnect");
      deviceConnected = false;
    }
};
 
class MyCallbacks: public BLECharacteristicCallbacks {
  void onRead(BLECharacteristic *pCharacteristic) {
    Serial.println("read");
//    std::string value = pCharacteristic->getValue();
//    Serial.println(value.c_str());
  }
  void onWrite(BLECharacteristic *pCharacteristic) {
    Serial.println("write");
  }
};
 
void setup() {
  M5.begin(true, false, true);
  delay(10);
  Serial.begin(115200);
  M5.dis.clear();
  pinMode(26, INPUT);
  Serial.println("\nM5Atom Earth Test");
  // Read earth sensor value
  readEarthSensor();
  
  BLEDevice::init(SERVER_NAME);
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE |
                                         BLECharacteristic::PROPERTY_NOTIFY
                                       );
  pCharacteristic->setCallbacks(new MyCallbacks());
  pCharacteristic->addDescriptor(new BLE2902());
 
  pService->start();
  BLEAdvertising *pAdvertising = pServer->getAdvertising();
  pAdvertising->start();
}
void loop() {

//  if (deviceConnected) {
    if (M5.Btn.wasPressed()) {
      // Read earth sensor value
      readEarthSensor();
      print_readEarthSensor();
    }
//  }
  M5.update();
  delay(1*1000);
}