// ----------------------------------------------------------------------------
// --- RTC set up                                                          ----
// ----------------------------------------------------------------------------

void setNTP2RTC(){
    // timeSet
    getTimeFromNTP();
    getLocalTime(&timeinfo);
    // read RTC
    M5.Rtc.GetTime(&RTC_TimeStruct);
    M5.Rtc.GetDate(&RTC_DateStruct);
    // --- to over write date&time
    RTC_DateStruct.Year = timeinfo.tm_year + 1900;
    RTC_DateStruct.Month = timeinfo.tm_mon + 1;
    RTC_DateStruct.Date = timeinfo.tm_mday;
    RTC_DateStruct.WeekDay = timeinfo.tm_wday;
    M5.Rtc.SetDate(&RTC_DateStruct);
    RTC_TimeStruct.Hours = timeinfo.tm_hour;
    RTC_TimeStruct.Minutes = timeinfo.tm_min;
    RTC_TimeStruct.Seconds = timeinfo.tm_sec;
    M5.Rtc.SetTime(&RTC_TimeStruct);
}

void getTimeFromNTP(){
  // To get Time from NTP server
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  while (!getLocalTime(&timeinfo)) {
    delay(1000);
  }
}

// ----------------------------------------------------------------------------
// --- BLE set up                                                          ----
// ----------------------------------------------------------------------------

static void notifyCallback(
  BLERemoteCharacteristic* pBLERemoteCharacteristic,  uint8_t* pData,  size_t length,  bool isNotify) {
    earth_analog_val=0;
    earth_analog_val=(uint16_t)(pData[1]<<8 | pData[0]);
    Serial.println(earth_analog_val);
}

bool connectToServer(BLEAddress pAddress) {
    Serial.print("Forming a connection to ");
    Serial.println(pAddress.toString().c_str());

    BLEClient*  pClient  = BLEDevice::createClient();
    pClient->connect(pAddress);

    BLERemoteService* pRemoteService = pClient->getService(serviceUUID); 
    //notify してクライアントの電源が切れると、サーバー側も電源を落とす。サービスが読み込めなくなるため。
    Serial.println(pRemoteService->toString().c_str());
    if (pRemoteService == nullptr) {
      return false;
    }
    pRemoteCharacteristic = pRemoteService->getCharacteristic(charUUID);
    if (pRemoteCharacteristic == nullptr) {
      return false;
    }
    pRemoteCharacteristic->registerForNotify(notifyCallback);
    return true;
}

// ----------------------------------------------------------------------------
// --- Botton operation                                                    ----
// ----------------------------------------------------------------------------

void printData_btm2(TFT_eSprite& sprite, int x, int y, int textSize, uint16_t color, const char* label, float value, const char* unit) {
  sprite.setTextColor(WHITE);
  sprite.setCursor(x, y, 1); 
  sprite.printf(label);
  
  sprite.setTextColor(color);
  sprite.setCursor(x + 70, y + 20, textSize);
  sprite.printf("%4.1f", value);
  
  sprite.setTextColor(color);
  sprite.setCursor(x + 230, y + 30, textSize-1);
  sprite.printf(unit);
}

void printData_btm3(TFT_eSprite& sprite, int x, int y, int textSize, uint16_t color, const char* label, const char* unit) {
  sprite.setTextColor(WHITE);
  sprite.setCursor(x, y, 1); 
  sprite.printf(label);
  
  sprite.setTextColor(color);
  sprite.setCursor(x + 50, y + 30, textSize);
  sprite.printf(unit);
}

void printData_btm3_int(TFT_eSprite& sprite, int x, int y, int textSize, uint16_t color, const char* label,uint16_t value) {
  sprite.setTextColor(WHITE);
  sprite.setCursor(x, y, 1); 
  sprite.printf(label);
  
  sprite.setTextColor(color);
  sprite.setCursor(x + 50, y + 30, textSize);
  sprite.printf("%d",value);
}

