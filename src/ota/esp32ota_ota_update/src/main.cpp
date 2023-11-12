/**
 * Project:     Control for the Pololu 3Pi+ template with OTA
 * Doc:
 * Proj URL:
 * Author:      Jonathan Pu
 * Created:     october 2023
 */

// ================================================================================
// Libraries
// ================================================================================
#include <Arduino.h>
#include <WiFi.h>
#include "BasicOTA.hpp"
#include <tinycbor.h>
#include "codegen.h"
#include <ArduinoJson.h>
// https://github.com/bblanchon/ArduinoJson/issues/731
// ================================================================================
// Variable definitions
// ================================================================================
#define SSID "Robotat"
#define PASSWORD "iemtbmcit116"
// #define SSID "HUAWEI Y8s"
// #define PASSWORD "003831e381aa"

BasicOTA OTA;
// variables for blinking an LED with Millis
const int led = 33;               // ESP32 Pin to which onboard LED is connected
unsigned long previousMillis = 0; // will store last time LED was updated
const long interval = 1000;       // interval at which to blink (milliseconds)
int ledState = LOW;               // ledState used to set the LED

// ================================================================================
// Funcionamiento básico del robot, ***NO MODIFICAR***
// ================================================================================
uint8_t uart_send_buffer[32] = {0};              // buffer CBOR
static const unsigned int control_time_ms = 100; // período de muestreo del control
volatile float phi_ell = 0;                      // en rpm
volatile float phi_r = 0;                        // en rpm
// WiFi+Robotat
const unsigned robot_id = 7; // PONER EL NÚMERO DE MARKER AQUÍ
const char *ssid = "Robotat";
const char *password = "iemtbmcit116";
const char *host = "192.168.50.200";
const int port = 1883;
char msg2robotat[] = "{\"dst\":1,\"cmd\":1,\"pld\":100}";
WiFiClient client;
StaticJsonDocument<512> doc;
String msg = "";
char c;
int t1 = 0;
int ti = 60;
int t2 = 180;

volatile double x, y, z, n, ex, ey, ez, roll, pitch, yaw;
void encode_send_wheel_speeds_task(void *p_params)
{
  TickType_t last_control_time;
  const TickType_t control_freq_ticks = pdMS_TO_TICKS(control_time_ms);

  // Tiempo actual
  last_control_time = xTaskGetTickCount();

  while (1)
  {
    // Se espera a que se cumpla el período de muestreo
    vTaskDelayUntil(&last_control_time, control_freq_ticks);

    TinyCBOR.Encoder.init(uart_send_buffer, sizeof(uart_send_buffer));
    TinyCBOR.Encoder.create_array(2);
    TinyCBOR.Encoder.encode_float(phi_ell);
    TinyCBOR.Encoder.encode_float(phi_r);
    TinyCBOR.Encoder.close_container();
    Serial2.write(TinyCBOR.Encoder.get_buffer(), TinyCBOR.Encoder.get_buffer_size());
  }
}
// ================================================================================
void connect2robotat_task(void *p_params)
{

  while (1) // loop()
  {
    if (client.available())
    {
      client.write(msg2robotat);
      while (t1 < t2)
      {
        c = client.read();
        msg = msg + c;
        t1 = t1 + 1;
        if (c == '}')
          t1 = t2;
      }
      // Serial.println(msg);

      DeserializationError err = deserializeJson(doc, msg);
      if (err == DeserializationError::Ok)
      {
        x = doc["data"][0].as<double>();
        y = doc["data"][1].as<double>();
        z = doc["data"][2].as<double>();
        n = doc["data"][3].as<double>();
        ex = doc["data"][4].as<double>();
        ey = doc["data"][5].as<double>();
        ez = doc["data"][6].as<double>();

        // Serial.print("x = ");
        // Serial.print(x);
        // Serial.print(", y = ");
        // Serial.print(y);
        // Serial.print(", z = ");
        // Serial.print(z);
        // Serial.print(", n = ");
        // Serial.print(n);
        // Serial.print(", ex = ");
        // Serial.print(ex);
        // Serial.print(", ey = ");
        // Serial.print(ey);
        // Serial.print(", ez = ");
        // Serial.println(ez);
      }
      else
      {
        Serial.print("deserializeJson() returned ");
        Serial.println(err.c_str());
      }

      msg = "";
      t1 = 0;
    }
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}
// ================================================================================
// Control
// ================================================================================

void control_algorithm_task(void *p_params)
{
  while (1) // loop()
  {
    double temp[2];
    double q[4] = {n, ex, ey, ez};
    roll = atan2((q[0] * q[1] + q[2] * q[3]), 0.5 - (q[1] * q[1] + q[2] * q[2]));
    pitch = asin(2.0 * (q[0] * q[2] - q[1] * q[3]));
    yaw = atan2(2*(q[1] * q[2] + q[0] * q[3]), 1 - 2*(q[2] * q[2] + q[3] * q[3]));
    
    // to degrees
    yaw *= 180.0 / PI;
    pitch *= 180.0 / PI;
    roll *= 180.0 / PI;
    double theta = yaw;
    Serial.print("theta");
    Serial.println(theta);
    control(0.0, 0.0, x, y, theta, temp);
    // phi_ell = temp[0];
    // phi_r = temp[1];


    // phi_ell = temp[0];
    // phi_r = temp[1];
    Serial.print("phi_ell");
    Serial.println(phi_ell);
    Serial.print("phi_r");
    Serial.println(phi_r);
    phi_ell = 10;
    phi_r = 10;
    if (phi_ell > 100.0)
    {
      phi_ell = 0;
    }
    else if(phi_ell < -100){
      phi_ell = 0;
    }
    if (phi_r > 100.0)
    {
      phi_r = 0;
    }
    else if(phi_r < -100){
      phi_r = 0;
    }


    vTaskDelay(10 / portTICK_PERIOD_MS); // delay de 1 segundo (thread safe)
  }
}

void setup()
{
  // Serial.begin(115200);
 

  Serial.begin(115200);  // ***NO MODIFICAR***
  Serial2.begin(115200); // ***NO MODIFICAR***
  TinyCBOR.init();       // ***NO MODIFICAR***
  Serial.println("Startup");
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.waitForConnectResult() != WL_CONNECTED)
  {
    Serial.println("Connection Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }

  OTA.begin(); // Setup settings

  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  // Si alguna de sus librerías requiere setup, colocarlo aquí
  // WiFi+Robotat
  if (robot_id < 10)
  {
    msg2robotat[25] = 48 + robot_id;
  }

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  Serial.println("Connected to the WiFi network");
  Serial.println(WiFi.localIP());

  Serial.println("Connecting to Robotat");
  if (client.connect(host, port))
  {
    Serial.println("Connected");
    while (client.available())
    {
      client.read();
    }
    client.write(msg2robotat);
  }
  else
    Serial.println("Connection failed");
  // Creación de tasks ***NO MODIFICAR***
  xTaskCreate(encode_send_wheel_speeds_task, "encode_send_wheel_speeds_task", 1024 * 2, NULL, configMAX_PRIORITIES, NULL);
  xTaskCreate(connect2robotat_task, "connect2robotat_task", 1024 * 2, NULL, configMAX_PRIORITIES - 1, NULL);
  xTaskCreate(control_algorithm_task, "control_algorithm_task", 1024 * 2, NULL, configMAX_PRIORITIES - 1, NULL);
}

void loop()
{
  OTA.handle();
}
