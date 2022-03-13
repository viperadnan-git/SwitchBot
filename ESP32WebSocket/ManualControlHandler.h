#ifndef manual_control

void manual_control()
{
    for (int i = 0; i < 8; i++)
    {
        if (digitalRead(switchPins[i]) == LOW && switchState[i] == LOW)
        {
            digitalWrite(relayPins[i], LOW);
            if (webSocket.isConnected())
            {
                char s[16];
                sprintf(s, "{\"%d\":true}", i + 1);
                webSocket.sendTXT(s);
            }
            toggleState[i] = HIGH;
            switchState[i] = HIGH;
            Serial.printf("Switch-%d on\n", i + 1);
        }
        if (digitalRead(switchPins[i]) == HIGH && switchState[i] == HIGH)
        {
            digitalWrite(relayPins[i], HIGH);
            if (webSocket.isConnected())
            {
                char s[16];
                sprintf(s, "{\"%d\":false}", i + 1);
                webSocket.sendTXT(s);
            }
            toggleState[i] = LOW;
            switchState[i] = LOW;
            Serial.printf("Switch-%d off\n", i + 1);
        }
    }
}

#endif