// Define pins for rows (outputs) and columns (inputs)
int R0 = 3;  // Row 0 connected to D3
int R1 = 4;  // Row 1 connected to D4
int R2 = 5;  // Row 2 connected to D5
int R3 = 6;  // Row 3 connected to D6
int R4 = 7;  // Row 4 connected to D7

int C0 = 8;  // Column 0 connected to D8
int C1 = 9;  // Column 1 connected to D9
int C2 = 10; // Column 2 connected to D10
int C3 = 11; // Column 3 connected to D11
int C4 = 12; // Column 4 connected to D12

// Variables to store column states
int col0, col1, col2, col3, col4;

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
  Serial.begin(9600);
}

void loop() {
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
    delay(200);
  } else if (col1 == LOW) {
    Serial.println("2");
    delay(200);
  } else if (col2 == LOW) {
    Serial.println("3");
    delay(200);
  } 
  // else if (col3 == LOW) {
  //   Serial.println("4");
  //   delay(200);
  // } else if (col4 == LOW) {
  //   Serial.println("5");
  //   delay(200);
  // }

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
    delay(200);
  } else if (col1 == LOW) {
    Serial.println("5");
    delay(200);
  } else if (col2 == LOW) {
    Serial.println("6");
    delay(200);
  }
  //  else if (col3 == LOW) {
  //   Serial.println("9");
  //   delay(200);
  // } else if (col4 == LOW) {
  //   Serial.println("0");
  //   delay(200);
  // }

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
    delay(200);
  } else if (col1 == LOW) {
    Serial.println("8");
    delay(200);
  } else if (col2 == LOW) {
    Serial.println("9");
    delay(200);
  }
  //  else if (col3 == LOW) {
  //   Serial.println("D");
  //   delay(200);
  // } else if (col4 == LOW) {
  //   Serial.println("*");
  //   delay(200);
  // }

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
    delay(200);
  } else if (col1 == LOW) {
    Serial.println("0");
    delay(200);
  } else if (col2 == LOW) {
    Serial.println("#");
    delay(200);
  } 
  // else if (col3 == LOW) {
  //   Serial.println("G");
  //   delay(200);
  // } else if (col4 == LOW) {
  //   Serial.println("H");
  //   delay(200);
  // }

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
  // else if (col3 == LOW) {
  //   Serial.println("L");
  //   delay(200);
  // } else if (col4 == LOW) {
  //   Serial.println("M");
  //   delay(200);
  // }
}
