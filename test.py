import serial

# Configure the serial connection
ser = serial.Serial(
    port='COM8',  # Replace with your port name (e.g., '/dev/ttyUSB0' for Linux)
    baudrate=115200,
    timeout=1  # Set a timeout in seconds
)

try:
    while True:
        if ser.in_waiting > 0:  # Check if there is incoming data
            data = ser.readline().decode('utf-8').strip()  # Read and decode the data
            print(f"Received: {data}")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()  # Close the serial port
