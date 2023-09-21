/**
 * Project:     BasicOTA for VSCode-PlatformIO
 * Doc:         https://github.com/JakubAndrysek/BasicOTA-ESP32-library/blob/master/README.md
 * Proj URL:    https://github.com/JakubAndrysek/BasicOTA-ESP32-library  
 * Author:      Kuba Andrýsek
 * Created:     2020-5-5
 * Website:     https://kubaandrysek.cz
 * Inspiration: https://lastminuteengineers.com/esp32-ota-updates-arduino-ide/
*/

#include <Arduino.h>
#include <WiFi.h>
#include "BasicOTA.hpp"

#define SSID      "Robotat"
#define PASSWORD  "iemtbmcit116"

BasicOTA OTA;
//variables for blinking an LED with Millis
const int led = 33; // ESP32 Pin to which onboard LED is connected
unsigned long previousMillis = 0;  // will store last time LED was updated
const long interval = 1000;  // interval at which to blink (milliseconds)
int ledState = LOW;  // ledState used to set the LED

void setup() {
  pinMode(led, OUTPUT); 

  Serial.begin(115200);
  Serial.println("Startup");
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }

  OTA.begin(); // Setup settings

  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  OTA.handle();  
  
  //     //loop to blink without delay
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
  // save the last time you blinked the LED
  previousMillis = currentMillis;
  // if the LED is off turn it on and vice-versa:
  ledState = not(ledState);
  // set the LED with the ledState of the variable:
  digitalWrite(led,  ledState);
  }
}