#define US_KEYBOARD 1

#include <Arduino.h>
#include "BLEDevice.h"
#include "BLEHIDDevice.h"
#include "HIDTypes.h"
#include "HIDKeyboardTypes.h"

#define MODIFIER_CTRL_LEFT  0x01
#define MODIFIER_SHIFT_LEFT 0x02
#define MODIFIER_ALT_LEFT   0x04

// Change the below values if desired
#define BUTTON_PIN 33
#define MESSAGE "Rishi krishnaS\n"
#define DEVICE_NAME "ESP32 Keyboard"

// Define GPIO pins for rows (outputs) and columns (inputs)
int R0 = 12;  // Row 0
int R1 = 14;  // Row 1
int R2 = 27;  // Row 2
int R3 = 26;  // Row 3
int R4 = 25;  // Row 4

int C0 = 33;  // Column 0
int C1 = 32;  // Column 1
int C2 = 35;  // Column 2
int C3 = 34;  // Column 3
int C4 = 39;  // Column 4

// Variables to store column states
int col0, col1, col2, col3, col4;

// Forward declarations
void bluetoothTask(void*);
void typeText(const char* text);

bool isBleConnected = false;


void setup() {
  // Configure row pins as outputs
  pinMode(R0, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);
  pinMode(R3, OUTPUT);
  pinMode(R4, OUTPUT);

  // Configure column pins as inputs with pull-up resistors
  pinMode(C0, INPUT_PULLUP);
  pinMode(C1, INPUT_PULLUP);
  pinMode(C2, INPUT_PULLUP);
  pinMode(C3, INPUT_PULLUP);
  pinMode(C4, INPUT_PULLUP);

  // Initialize serial communication
  Serial.begin(115200);

  // start Bluetooth task
    xTaskCreate(bluetoothTask, "bluetooth", 20000, NULL, 5, NULL);
}

void loop() {
  if (isBleConnected) {
    // Scan Row 0
    digitalWrite(R0, LOW);
    digitalWrite(R1, HIGH);
    digitalWrite(R2, HIGH);
    digitalWrite(R3, HIGH);
    digitalWrite(R4, HIGH);

    col0 = digitalRead(C0);
    col1 = digitalRead(C1);
    col2 = digitalRead(C2);
    col3 = digitalRead(C3);
    col4 = digitalRead(C4);

    if (col0 == LOW) {
      Serial.println("1");
      sendKeyCombination(MODIFIER_CTRL_LEFT, 'a');
      delay(200);
    } else if (col1 == LOW) {
      Serial.println("2");
      sendKeyCombination(MODIFIER_CTRL_LEFT, 'c');
      delay(200);
    } else if (col2 == LOW) {
      Serial.println("3");
      sendKeyCombination(MODIFIER_CTRL_LEFT, 'v');
      delay(200);
    }

    // Scan Row 1
    digitalWrite(R0, HIGH);
    digitalWrite(R1, LOW);
    digitalWrite(R2, HIGH);
    digitalWrite(R3, HIGH);
    digitalWrite(R4, HIGH);

    col0 = digitalRead(C0);
    col1 = digitalRead(C1);
    col2 = digitalRead(C2);
    col3 = digitalRead(C3);
    col4 = digitalRead(C4);

    if (col0 == LOW) {
      Serial.println("4");
      sendKeyCombination(MODIFIER_CTRL_LEFT, 'z');
      delay(200);
    } else if (col1 == LOW) {
      Serial.println("5");
      sendKeyCombination(MODIFIER_CTRL_LEFT, 'y');
      delay(200);
    } else if (col2 == LOW) {
      Serial.println("6");
      sendKeyCombination(MODIFIER_CTRL_LEFT, 's');
      delay(200);
    }

    // Scan Row 2
    digitalWrite(R0, HIGH);
    digitalWrite(R1, HIGH);
    digitalWrite(R2, LOW);
    digitalWrite(R3, HIGH);
    digitalWrite(R4, HIGH);

    col0 = digitalRead(C0);
    col1 = digitalRead(C1);
    col2 = digitalRead(C2);
    col3 = digitalRead(C3);
    col4 = digitalRead(C4);

    if (col0 == LOW) {
      Serial.println("7");
      sendAltTab();
      delay(200);
    } else if (col1 == LOW) {
      Serial.println("8");
      sendKeyCombination(MODIFIER_CTRL_LEFT, 'a');
      delay(200);
    } else if (col2 == LOW) {
      Serial.println("9");
      sendKeyCombination(MODIFIER_CTRL_LEFT, 'a');
      delay(200);
    }

    // Scan Row 3
    digitalWrite(R0, HIGH);
    digitalWrite(R1, HIGH);
    digitalWrite(R2, HIGH);
    digitalWrite(R3, LOW);
    digitalWrite(R4, HIGH);

    col0 = digitalRead(C0);
    col1 = digitalRead(C1);
    col2 = digitalRead(C2);
    col3 = digitalRead(C3);
    col4 = digitalRead(C4);

    if (col0 == LOW) {
      Serial.println("*");
      sendKeyCombination(MODIFIER_CTRL_LEFT, 'a');
      delay(200);
    } else if (col1 == LOW) {
      Serial.println("0");
      sendKeyCombination(MODIFIER_CTRL_LEFT, 'a');
      delay(200);
    } else if (col2 == LOW) {
      Serial.println("#");
      sendKeyCombination(MODIFIER_CTRL_LEFT, 'a');
      delay(200);
    }

    // Scan Row 4
    digitalWrite(R0, HIGH);
    digitalWrite(R1, HIGH);
    digitalWrite(R2, HIGH);
    digitalWrite(R3, HIGH);
    digitalWrite(R4, LOW);

    col0 = digitalRead(C0);
    col1 = digitalRead(C1);
    col2 = digitalRead(C2);
    col3 = digitalRead(C3);
    col4 = digitalRead(C4);

    if (col0 == LOW) {
      Serial.println("I");
      delay(200);
    } else if (col1 == LOW) {
      Serial.println("J");
      delay(200);
    } else if (col2 == LOW) {
      Serial.println("K");
      delay(200);
    }
  }
}

// Message (report) sent when a key is pressed or released
struct InputReport {
    uint8_t modifiers;	     // bitmask: CTRL = 1, SHIFT = 2, ALT = 4
    uint8_t reserved;        // must be 0
    uint8_t pressedKeys[6];  // up to six concurrenlty pressed keys
};

// Message (report) received when an LED's state changed
struct OutputReport {
    uint8_t leds;            // bitmask: num lock = 1, caps lock = 2, scroll lock = 4, compose = 8, kana = 16
};


// The report map describes the HID device (a keyboard in this case) and
// the messages (reports in HID terms) sent and received.
static const uint8_t REPORT_MAP[] = {
    USAGE_PAGE(1),      0x01,       // Generic Desktop Controls
    USAGE(1),           0x06,       // Keyboard
    COLLECTION(1),      0x01,       // Application
    REPORT_ID(1),       0x01,       //   Report ID (1)
    USAGE_PAGE(1),      0x07,       //   Keyboard/Keypad
    USAGE_MINIMUM(1),   0xE0,       //   Keyboard Left Control
    USAGE_MAXIMUM(1),   0xE7,       //   Keyboard Right Control
    LOGICAL_MINIMUM(1), 0x00,       //   Each bit is either 0 or 1
    LOGICAL_MAXIMUM(1), 0x01,
    REPORT_COUNT(1),    0x08,       //   8 bits for the modifier keys
    REPORT_SIZE(1),     0x01,       
    HIDINPUT(1),        0x02,       //   Data, Var, Abs
    REPORT_COUNT(1),    0x01,       //   1 byte (unused)
    REPORT_SIZE(1),     0x08,
    HIDINPUT(1),        0x01,       //   Const, Array, Abs
    REPORT_COUNT(1),    0x06,       //   6 bytes (for up to 6 concurrently pressed keys)
    REPORT_SIZE(1),     0x08,
    LOGICAL_MINIMUM(1), 0x00,
    LOGICAL_MAXIMUM(1), 0x65,       //   101 keys
    USAGE_MINIMUM(1),   0x00,
    USAGE_MAXIMUM(1),   0x65,
    HIDINPUT(1),        0x00,       //   Data, Array, Abs
    REPORT_COUNT(1),    0x05,       //   5 bits (Num lock, Caps lock, Scroll lock, Compose, Kana)
    REPORT_SIZE(1),     0x01,
    USAGE_PAGE(1),      0x08,       //   LEDs
    USAGE_MINIMUM(1),   0x01,       //   Num Lock
    USAGE_MAXIMUM(1),   0x05,       //   Kana
    LOGICAL_MINIMUM(1), 0x00,
    LOGICAL_MAXIMUM(1), 0x01,
    HIDOUTPUT(1),       0x02,       //   Data, Var, Abs
    REPORT_COUNT(1),    0x01,       //   3 bits (Padding)
    REPORT_SIZE(1),     0x03,
    HIDOUTPUT(1),       0x01,       //   Const, Array, Abs
    END_COLLECTION(0)               // End application collection
};


BLEHIDDevice* hid;
BLECharacteristic* input;
BLECharacteristic* output;

const InputReport NO_KEY_PRESSED = { };


/*
 * Callbacks related to BLE connection
 */
class BleKeyboardCallbacks : public BLEServerCallbacks {

    void onConnect(BLEServer* server) {
        isBleConnected = true;

        // Allow notifications for characteristics
        BLE2902* cccDesc = (BLE2902*)input->getDescriptorByUUID(BLEUUID((uint16_t)0x2902));
        cccDesc->setNotifications(true);

        Serial.println("Client has connected");
    }

    void onDisconnect(BLEServer* server) {
        isBleConnected = false;

        // Disallow notifications for characteristics
        BLE2902* cccDesc = (BLE2902*)input->getDescriptorByUUID(BLEUUID((uint16_t)0x2902));
        cccDesc->setNotifications(false);

        Serial.println("Client has disconnected");
    }
};


/*
 * Called when the client (computer, smart phone) wants to turn on or off
 * the LEDs in the keyboard.
 * 
 * bit 0 - NUM LOCK
 * bit 1 - CAPS LOCK
 * bit 2 - SCROLL LOCK
 */
 class OutputCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic* characteristic) {
        OutputReport* report = (OutputReport*) characteristic->getData();
        //Serial.print("LED state: ");
        Serial.print((int) report->leds);
        Serial.println();
    }
};


void bluetoothTask(void*) {

    // initialize the device
    BLEDevice::init(DEVICE_NAME);
    BLEServer* server = BLEDevice::createServer();
    server->setCallbacks(new BleKeyboardCallbacks());

    // create an HID device
    hid = new BLEHIDDevice(server);
    input = hid->inputReport(1); // report ID
    output = hid->outputReport(1); // report ID
    output->setCallbacks(new OutputCallbacks());

    // set manufacturer name
    hid->manufacturer()->setValue("Maker Community");
    // set USB vendor and product ID
    hid->pnp(0x02, 0xe502, 0xa111, 0x0210);
    // information about HID device: device is not localized, device can be connected
    hid->hidInfo(0x00, 0x02);

    // Security: device requires bonding
    BLESecurity* security = new BLESecurity();
    security->setAuthenticationMode(ESP_LE_AUTH_BOND);

    // set report map
    hid->reportMap((uint8_t*)REPORT_MAP, sizeof(REPORT_MAP));
    hid->startServices();

    // set battery level to 100%
    hid->setBatteryLevel(100);

    // advertise the services
    BLEAdvertising* advertising = server->getAdvertising();
    advertising->setAppearance(HID_KEYBOARD);
    advertising->addServiceUUID(hid->hidService()->getUUID());
    advertising->addServiceUUID(hid->deviceInfo()->getUUID());
    advertising->addServiceUUID(hid->batteryService()->getUUID());
    advertising->start();

    Serial.println("BLE ready");
    delay(portMAX_DELAY);
};


void typeText(const char* text) {
    int len = strlen(text);
    for (int i = 0; i < len; i++) {
        // translate character to key combination
        uint8_t val = (uint8_t)text[i];
        if (val > KEYMAP_SIZE)
            continue; // character not available on keyboard - skip
        
        KEYMAP map = keymap[val];

        // create input report with modifiers
        InputReport report = {
            .modifiers = map.modifier,  // Add modifier keys if needed
            .reserved = 0,
            .pressedKeys = {
                map.usage,
                0, 0, 0, 0, 0
            }
        };

        // send the input report
        input->setValue((uint8_t*)&report, sizeof(report));
        input->notify();

        delay(5);

        // release all keys
        input->setValue((uint8_t*)&NO_KEY_PRESSED, sizeof(NO_KEY_PRESSED));
        input->notify();

        delay(5);
    }
}

//helper
void sendKeyCombination(uint8_t modifier, char key) {
    if (isBleConnected) {
        // Find the keymap entry for the character
        uint8_t val = (uint8_t)key;
        if (val > KEYMAP_SIZE) return; // character not available
        
        KEYMAP map = keymap[val];

        InputReport report = {
            .modifiers = modifier,  // Add provided modifier
            .reserved = 0,
            .pressedKeys = {
                map.usage,
                0, 0, 0, 0, 0
            }
        };

        // Send key press
        input->setValue((uint8_t*)&report, sizeof(report));
        input->notify();

        delay(5);

        // Release keys
        input->setValue((uint8_t*)&NO_KEY_PRESSED, sizeof(NO_KEY_PRESSED));
        input->notify();

        delay(5);
    }
}

void sendAltTab() {
    if (isBleConnected) {
        // Alt key press
        InputReport altPress = {
            .modifiers = MODIFIER_ALT_LEFT,
            .reserved = 0,
            .pressedKeys = {
                0x2B,  // Tab key usage
                0, 0, 0, 0, 0
            }
        };

        // Send Alt+Tab
        input->setValue((uint8_t*)&altPress, sizeof(altPress));
        input->notify();

        delay(50);

        // Release keys
        input->setValue((uint8_t*)&NO_KEY_PRESSED, sizeof(NO_KEY_PRESSED));
        input->notify();
    }
}