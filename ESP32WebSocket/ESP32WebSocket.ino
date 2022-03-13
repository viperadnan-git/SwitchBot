/*
    TODO
*/

#include <Arduino.h>
#include <WiFiManager.h>
#include <Preferences.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>

WebSocketsClient webSocket;
WiFiManager wifiManager;
Preferences preferences;

String SwitchBotServer = "switchbot-v.herokuapp.com";
int SwitchBotPort = 443;
String SwitchBotPath = "/ws/";

String SwitchBotUsername;
String SwitchBotPassword;

unsigned long messageInterval = 5000;
bool connected = false;

#define DEBUG_SERIAL Serial

DynamicJsonDocument doc(1024);

short int BOARD_LED_PIN = 2;
short int RESET_PIN = 17;
int relayPins[8] = {23, 22, 21, 19, 18, 5, 25, 26};
int switchPins[8] = {13, 12, 14, 27, 33, 32, 15, 4};

bool switchState[8] = {LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW};
bool toggleState[8] = {LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW};

bool firstStart = true;

#include "ManualControlHandler.h"
#include "WebSocketEventHandler.h"

bool shouldSaveConfig = false;

void saveConfigCallback()
{
    shouldSaveConfig = true;
}

void setup()
{
    DEBUG_SERIAL.begin(115200);
    //  DEBUG_SERIAL.setDebugOutput(true);
    DEBUG_SERIAL.println();
    DEBUG_SERIAL.println();
    DEBUG_SERIAL.println();

    for (uint8_t t = 3; t > 0; t--)
    {
        DEBUG_SERIAL.printf("[SETUP] BOOT WAIT %d...\n", t);
        DEBUG_SERIAL.flush();
        delay(1000);
    }

    for (int i = 0; i < 8; i++)
    {
        pinMode(relayPins[i], OUTPUT);
    }

    for (int i = 0; i < 8; i++)
    {
        pinMode(switchPins[i], INPUT_PULLUP);
    }

    for (int i = 0; i < 8; i++)
    {
        digitalWrite(relayPins[i], HIGH);
    }

    pinMode(RESET_PIN, INPUT_PULLUP);
    pinMode(BOARD_LED_PIN, OUTPUT);
    digitalWrite(BOARD_LED_PIN, LOW);


    preferences.begin("SwitchBot", false);
    SwitchBotUsername = preferences.getString("SBUsername", "");
    SwitchBotPassword = preferences.getString("SBPassword", "");

    if (SwitchBotUsername == "" || SwitchBotPassword == "")
    {
        WiFiManagerParameter custom_username("SBUsername", "SwitchBot Username", SwitchBotUsername.c_str(), 12, " required");
        WiFiManagerParameter custom_password("SBPassword", "SwitchBot Password", SwitchBotPassword.c_str(), 12, " required");

        wifiManager.setSaveConfigCallback(saveConfigCallback);

        wifiManager.addParameter(&custom_username);
        wifiManager.addParameter(&custom_password);

        wifiManager.startConfigPortal("SwitchBot");
        if (shouldSaveConfig)
        {
            SwitchBotUsername = custom_username.getValue();
            SwitchBotPassword = custom_password.getValue();
            preferences.putString("SBUsername", SwitchBotUsername);
            preferences.putString("SBPassword", SwitchBotPassword);
        }
        preferences.end();
    }

    wifiManager.autoConnect("SwitchBot");

    webSocket.beginSSL(SwitchBotServer, SwitchBotPort, SwitchBotPath + SwitchBotUsername);
    webSocket.setAuthorization(SwitchBotUsername.c_str(), SwitchBotPassword.c_str());

    webSocket.onEvent(webSocketEvent);
}

unsigned long lastUpdate = millis();

void loop()
{
    manual_control();
    webSocket.loop();
    if (connected && lastUpdate + messageInterval < millis())
    {
        webSocket.sendPing();
        lastUpdate = millis();
    }

    if (digitalRead(RESET_PIN) == LOW)
    {
        wifiManager.resetSettings();
        preferences.begin("SwitchBot", false);
        preferences.clear();
        preferences.end();
        ESP.restart();
    }
}
