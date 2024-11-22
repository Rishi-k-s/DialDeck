#include <Arduino.h>

// Define row and column pins
const int rowPins[5] = {12, 14, 27, 26, 25}; // GPIO pins for rows (R0-R4)
const int colPins[5] = {33, 32, 35, 34, 39}; // GPIO pins for columns (C0-C4)

// Define the keypad layout (adjust based on your circuit)
char keys[5][5] = {
  {'1', '2', '3', 'A', 'B'},
  {'4', '5', '6', 'C', 'D'},
  {'7', '8', '9', 'E', 'F'},
  {'*', '0', '#', 'G', 'H'},
  {'I', 'J', 'K', 'L', 'M'}
};

void setup() {
  Serial.begin(115200);
  
  // Initialize row pins as OUTPUT
  for (int i = 0; i < 5; i++) {
    pinMode(rowPins[i], OUTPUT);
    digitalWrite(rowPins[i], LOW);
  }

  // Initialize column pins as INPUT with pull-down
  for (int i = 0; i < 5; i++) {
    pinMode(colPins[i], INPUT_PULLDOWN);
  }
}

void loop() {
  // Scan rows to detect keypresses
  for (int row = 0; row < 5; row++) {
    // Set the current row HIGH
    digitalWrite(rowPins[row], HIGH);

    // Check each column for a HIGH signal
    for (int col = 0; col < 5; col++) {
      if (digitalRead(colPins[col]) == HIGH) {
        Serial.print("Key Pressed: ");
        Serial.println(keys[row][col]);
        delay(200); // Debounce delay
      }
    }

    // Set the row back to LOW
    digitalWrite(rowPins[row], LOW);
  }
}
