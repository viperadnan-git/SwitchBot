#ifndef webSocketEvent

#ifndef hexdump

void hexdump(const void *mem, uint32_t len, uint8_t cols = 16)
{
    const uint8_t *src = (const uint8_t *)mem;
    DEBUG_SERIAL.printf("\n[HEXDUMP] Address: 0x%08X len: 0x%X (%d)", (ptrdiff_t)src, len, len);
    for (uint32_t i = 0; i < len; i++)
    {
        if (i % cols == 0)
        {
            DEBUG_SERIAL.printf("\n[0x%08X] 0x%08X: ", (ptrdiff_t)src, i);
        }
        DEBUG_SERIAL.printf("%02X ", *src);
        src++;
    }
    DEBUG_SERIAL.printf("\n");
}

#endif

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length)
{

    switch (type)
    {
    case WStype_DISCONNECTED:
    {
        DEBUG_SERIAL.printf("[WSc] Disconnected!\n");
        connected = false;
        digitalWrite(BOARD_LED_PIN, LOW);
    }
    break;
    case WStype_CONNECTED:
    {
        DEBUG_SERIAL.printf("[WSc] Connected to url: %s\n", payload);
        connected = true;
        if (firstStart)
        {
            webSocket.sendTXT("update");
            firstStart = false;
        }
        else
        {
            for (int i = 0; i < 8; i++)
            {
                if (switchState[i] == HIGH)
                {
                    char s[16];
                    sprintf(s, "{\"%d\":true}", i + 1);
                    webSocket.sendTXT(s);
                }
                if (switchState[i] == LOW)
                {
                    char s[16];
                    sprintf(s, "{\"%d\":false}", i + 1);
                    webSocket.sendTXT(s);
                }
            }
        }
        digitalWrite(LED_BUILTIN, HIGH);
    }
    break;
    case WStype_TEXT:
    {
        DEBUG_SERIAL.printf("[WSc] Received: %s\n", payload);
        DeserializationError error = deserializeJson(doc, payload);
        if (!error)
        {
            JsonObject pinStates = doc.as<JsonObject>();
            for (JsonPair kv : pinStates)
            {
                int key = atoi(kv.key().c_str());
                if (kv.value().as<bool>())
                {
                    DEBUG_SERIAL.printf("Relay on - %d\n", key);
                    digitalWrite(relayPins[key - 1], LOW);
                    toggleState[key - 1] = LOW;
                }
                else
                {
                    DEBUG_SERIAL.printf("Relay off - %d\n", key);
                    digitalWrite(relayPins[key - 1], HIGH);
                    toggleState[key - 1] = HIGH;
                }
            }
        }
    }
    break;
    case WStype_BIN:
        DEBUG_SERIAL.printf("[WSc] get binary length: %u\n", length);
        hexdump(payload, length);
        break;
    case WStype_PING:
        DEBUG_SERIAL.printf("[WSc] get ping\n");
        break;
    case WStype_PONG:
        break;

    case WStype_ERROR:
    case WStype_FRAGMENT_TEXT_START:
    case WStype_FRAGMENT_BIN_START:
    case WStype_FRAGMENT:
    case WStype_FRAGMENT_FIN:
        break;
    }
}

#endif