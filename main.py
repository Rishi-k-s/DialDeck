import sys
import serial
import serial.tools.list_ports
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QPushButton, QWidget, QComboBox, QLabel, QMessageBox, QTextEdit, 
    QDialog,QStackedWidget
)
from PyQt6.QtGui import QFont

class AlphabetMappingDialog(QDialog):
    def __init__(self, key, current_mapping, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Map Alphabets to Key {key}")
        self.key = key
        self.current_mapping = current_mapping
        self.is_single_key = True  # Default to single key mode

        layout = QVBoxLayout()

        # Button to toggle between single key and multi-key
        self.mode_toggle_btn = QPushButton("Switch to Multi-Key")
        self.mode_toggle_btn.clicked.connect(self.toggle_mode)
        layout.addWidget(self.mode_toggle_btn)

        # Single key selector
        self.single_key_selector = QComboBox()
        self.single_key_selector.addItem("")
        self.single_key_selector.addItems([chr(i) for i in range(65, 91)])
        self.single_key_layout = QVBoxLayout()
        self.single_key_layout.addWidget(QLabel("Select Single Alphabet:"))
        self.single_key_layout.addWidget(self.single_key_selector)

        # Multi-key selectors
        self.multi_key_layout = QVBoxLayout()
        self.modifier_selector = QComboBox()
        self.modifier_selector.addItems(["", "CTRL", "ALT", "SHIFT"])
        self.letter_selector = QComboBox()
        self.letter_selector.addItem("")
        self.letter_selector.addItems([chr(i) for i in range(65, 91)])
        self.multi_key_layout.addWidget(QLabel("Select Modifier:"))
        self.multi_key_layout.addWidget(self.modifier_selector)
        self.multi_key_layout.addWidget(QLabel("Select Letter:"))
        self.multi_key_layout.addWidget(self.letter_selector)
        self.multi_key_widget = QWidget()
        self.multi_key_widget.setLayout(self.multi_key_layout)

        # Stacked widget to switch between single and multi-key selectors
        self.selector_stack = QStackedWidget()
        self.selector_stack.addWidget(QWidget())
        self.selector_stack.addWidget(QWidget().setLayout(self.single_key_layout))
        self.selector_stack.addWidget(self.multi_key_widget)
        self.selector_stack.setCurrentIndex(1)
        layout.addWidget(self.selector_stack)

        # OK and Cancel buttons
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def toggle_mode(self):
        self.is_single_key = not self.is_single_key
        if self.is_single_key:
            self.mode_toggle_btn.setText("Switch to Multi-Key")
            self.selector_stack.setCurrentIndex(1)
        else:
            self.mode_toggle_btn.setText("Switch to Single Key")
            self.selector_stack.setCurrentIndex(2)

    def get_selection(self):
        if self.is_single_key:
            return self.single_key_selector.currentText()
        else:
            modifier = self.modifier_selector.currentText()
            letter = self.letter_selector.currentText()
            return f"{modifier}+{letter}" if modifier and letter else ""


class KeypadWidget(QWidget):
    def __init__(self, serial_connection=None):
        super().__init__()
        
        self.serial_connection = serial_connection
        
        # Telephone keypad layout with alphabet mapping
        self.keypad_layout = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['*', '0', '#']
        ]
        
        # Alphabet mapping for each key
        self.alphabet_mapping = {
            '1': [], '2': [], '3': [],
            '4': [], '5': [], '6': [],
            '7': [], '8': [], '9': []
        }
        
        self.init_ui()
    
    def update_alphabet_mapping(self, key, selection):
        if selection:
            # Handle single or multi-key mapping
            if '+' in selection:  # Multi-key
                display_text = selection.replace('+', ' + ')
            else:
                display_text = selection
            
            self.alphabet_mapping[key] = [selection]
            btn = getattr(self, f'btn_{key}')
            btn.setText(f"{key}\n({display_text})")
            btn.setStyleSheet("background-color: lightgreen; font-weight: bold;")
        else:
            # Clear mapping
            self.alphabet_mapping[key] = []
            btn = getattr(self, f'btn_{key}')
            btn.setText(key)
            btn.setStyleSheet("")

    
    def init_ui(self):
        layout = QVBoxLayout()
        keypad_grid = QVBoxLayout()
        
        for row in self.keypad_layout:
            row_widget = QHBoxLayout()
            for key in row:
                btn = QPushButton(key)
                btn.setFixedSize(80, 80)  # Larger button size
                btn.setFont(QFont('Arial', 16))  # Larger font
                
                # Only add mapping dialog for numeric keys
                if key in self.alphabet_mapping:
                    btn.clicked.connect(lambda checked, k=key: self.show_mapping_dialog(k))
                else:
                    btn.clicked.connect(lambda checked, k=key: self.on_key_press(k))
                
                # Store button as an attribute for color changing
                setattr(self, f'btn_{key}', btn)
                row_widget.addWidget(btn)
            
            keypad_grid.addLayout(row_widget)
        
        layout.addLayout(keypad_grid)
        self.setLayout(layout)
    
    def show_mapping_dialog(self, key):
        dialog = AlphabetMappingDialog(key, self.alphabet_mapping[key], self)
        if dialog.exec():
            alphabet = dialog.alphabet_dropdown.currentText()
            self.update_alphabet_mapping(key, alphabet)
    
    def update_alphabet_mapping(self, key, alphabet):
        # Update alphabet mapping for the specific key
        btn = getattr(self, f'btn_{key}')
        
        if alphabet:
            # Ensure no duplicate alphabets across keys
            for k, mapped_alphabets in self.alphabet_mapping.items():
                if alphabet in mapped_alphabets:
                    # Remove from previous key
                    mapped_alphabets.remove(alphabet)
            
            # Add to current key
            self.alphabet_mapping[key] = [alphabet]
            
            # Change button color to highlight mapping
            btn.setStyleSheet("""
                QPushButton {
                    background-color: lightgreen;
                    font-weight: bold;
                }
            """)
            btn.setText(f"{key}\n({alphabet})")
        else:
            # Clear mapping
            self.alphabet_mapping[key] = []
            
            # Reset button style
            btn.setStyleSheet("")
            btn.setText(key)
        
        print("Current Alphabet Mapping:", self.alphabet_mapping)
    
    def on_key_press(self, key):
        print(f"Pressed key: {key}")
        
        # If alphabet is mapped, send the alphabet
        if self.alphabet_mapping.get(key, []):
            send_text = self.alphabet_mapping[key][0]
        else:
            send_text = key
        
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(send_text.encode())
            except Exception as e:
                print(f"Error sending key over serial: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.serial_connection = None
        
        self.setWindowTitle("Dial ഡെക്ക്")
        self.setMinimumSize(QSize(600, 700))
        
        # Main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # COM Port selection section
        port_layout = QHBoxLayout()
        
        self.port_selector = QComboBox()
        self.refresh_ports()
        
        refresh_btn = QPushButton("Refresh Ports")
        refresh_btn.clicked.connect(self.refresh_ports)
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.toggle_connection)
        
        port_layout.addWidget(QLabel("COM Port:"))
        port_layout.addWidget(self.port_selector)
        port_layout.addWidget(refresh_btn)
        port_layout.addWidget(self.connect_btn)
        
        main_layout.addLayout(port_layout)
        
        # Terminal output
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        main_layout.addWidget(QLabel("Serial Data:"))
        main_layout.addWidget(self.terminal_output)
        
        # Create landline keypad
        self.keypad_widget = KeypadWidget()
        main_layout.addWidget(self.keypad_widget)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Setup timer for serial reading
        self.read_timer = QTimer(self)
        self.read_timer.timeout.connect(self.read_serial_data)
        self.read_timer.setInterval(50)  # Read every 50ms
    
    def refresh_ports(self):
        self.port_selector.clear()
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_selector.addItems(ports)
    
    def toggle_connection(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.disconnect_serial()
        else:
            self.connect_serial()
    
    def connect_serial(self):
        selected_port = self.port_selector.currentText()
        if not selected_port:
            QMessageBox.warning(self, "Connection Error", "No port selected!")
            return
        
        try:
            self.serial_connection = serial.Serial(
                port=selected_port, 
                baudrate=115200,
                timeout=0.1,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            
            # Update keypad's serial connection
            self.keypad_widget.serial_connection = self.serial_connection
            
            # Start reading timer
            self.read_timer.start()
            
            self.connect_btn.setText("Disconnect")
            self.terminal_output.append(f"Connected to {selected_port} at 115200 baud")
        
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))
    
    def read_serial_data(self):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                # Check if data is available
                if self.serial_connection.in_waiting > 0:
                    # Read available data
                    data = self.serial_connection.read(self.serial_connection.in_waiting)
                    
                    # Decode and display
                    decoded_data = data.decode('utf-8', errors='replace').strip()
                    if decoded_data:
                        self.terminal_output.append(decoded_data)
            except Exception as e:
                self.terminal_output.append(f"Error reading serial data: {e}")
    
    def disconnect_serial(self):
        if self.serial_connection:
            # Stop reading timer
            self.read_timer.stop()
            
            self.serial_connection.close()
            self.serial_connection = None
            self.keypad_widget.serial_connection = None
            self.connect_btn.setText("Connect")
            self.terminal_output.append("Serial port disconnected")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()