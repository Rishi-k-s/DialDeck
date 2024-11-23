from machine import Pin
import time

# Define row and column pins
row_pins = [Pin(12, Pin.OUT) for _ in range(5)]  # GPIO pins for rows (R0-R4)
col_pins = [Pin(33, Pin.IN, Pin.PULL_DOWN) for _ in range(5)]  # GPIO pins for columns (C0-C4)

# Define the keypad layout (adjust based on your circuit)
keys = [
    ['1', '2', '3', 'A', 'B'],
    ['4', '5', '6', 'C', 'D'],
    ['7', '8', '9', 'E', 'F'],
    ['*', '0', '#', 'G', 'H'],
    ['I', 'J', 'K', 'L', 'M']
]

def scan_keypad():
    """Scan the keypad and return the pressed key."""
    for row_idx, row_pin in enumerate(row_pins):
        # Set the current row HIGH
        row_pin.on()
        
        # Check each column for a HIGH signal
        for col_idx, col_pin in enumerate(col_pins):
            if col_pin.value() == 1:  # Key is pressed
                row_pin.off()  # Reset the row
                return keys[row_idx][col_idx]
        
        # Set the row back to LOW
        row_pin.off()
    return None

# Main loop
def main():
    print("Starting keypad scanning...")
    while True:
        key = scan_keypad()
        if key:  # If a key is pressed
            print(f"Key Pressed: {key}")
            time.sleep(0.2)  # Debounce delay

# Run the main loop
main()
