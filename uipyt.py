import sys
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QComboBox, QPushButton,
                           QMessageBox, QPlainTextEdit, QGridLayout, QCheckBox,
                           QGroupBox, QFrame)
from PyQt6.QtCore import Qt, QTimer
from string import ascii_uppercase

class LetterNumberUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Number-Letter Selection with Serial Terminal")
        self.setGeometry(100, 100, 1200, 900)
        
        # Serial port connection
        self.serial_connection = None
        self.BAUD_RATE = 115200
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Create serial connection section
        serial_layout = self.create_serial_section()
        main_layout.addLayout(serial_layout)
        
        # Create horizontal layout for keypad and modifier sections
        content_layout = QHBoxLayout()
        
        # Create left side with keypad
        keypad_container = self.create_keypad_section()
        content_layout.addWidget(keypad_container)
        
        # Create right side with modifiers and preview
        right_side = QVBoxLayout()
        
        # Add modifier section
        modifier_group = self.create_modifier_section()
        right_side.addWidget(modifier_group)
        
        # Add preview section
        preview_group = self.create_preview_section()
        right_side.addWidget(preview_group)
        
        # Add right side to content layout
        right_widget = QWidget()
        right_widget.setLayout(right_side)
        content_layout.addWidget(right_widget)
        
        # Add content layout to main layout
        main_layout.addLayout(content_layout)
        
        # Create terminal section
        terminal_section = self.create_terminal_section()
        main_layout.addWidget(terminal_section)
        
        # Set terminal to take remaining space
        main_layout.setStretch(main_layout.count()-1, 1)
        
        # Setup timer for reading serial data
        self.serial_timer = QTimer()
        self.serial_timer.timeout.connect(self.read_serial)
        self.serial_timer.setInterval(10)  # Check every 10ms
        
        # Initial port refresh
        self.refresh_ports()
        
        # Store current number and letter
        self.current_number = None
        self.current_letter = None
    def create_serial_section(self):
        """Create the serial connection section of the UI"""
        serial_layout = QHBoxLayout()
        
        self.port_label = QLabel("Serial Port:")
        self.port_combo = QComboBox()
        self.refresh_button = QPushButton("Refresh Ports")
        self.connect_button = QPushButton("Connect")
        self.connect_button.setCheckable(True)
        self.clear_button = QPushButton("Clear Terminal")
        
        serial_layout.addWidget(self.port_label)
        serial_layout.addWidget(self.port_combo)
        serial_layout.addWidget(self.refresh_button)
        serial_layout.addWidget(self.connect_button)
        serial_layout.addWidget(self.clear_button)
        serial_layout.addStretch()
        
        # Connect button signals
        self.refresh_button.clicked.connect(self.refresh_ports)
        self.connect_button.clicked.connect(self.toggle_connection)
        self.clear_button.clicked.connect(self.clear_terminal)
        
        return serial_layout

    def create_terminal_section(self):
        """Create the terminal section of the UI"""
        terminal_container = QGroupBox("Serial Terminal")
        terminal_layout = QVBoxLayout()
        
        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setMaximumBlockCount(1000)  # Limit the number of lines for performance
        self.terminal.setStyleSheet("""
            QPlainTextEdit {
                background-color: black;
                color: #00FF00;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }
        """)
        
        terminal_layout.addWidget(self.terminal)
        terminal_container.setLayout(terminal_layout)
        
        return terminal_container

    def clear_terminal(self):
        """Clear the terminal contents"""
        self.terminal.clear()

    def refresh_ports(self):
        """Refresh the list of available serial ports"""
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)

    def toggle_connection(self):
        """Toggle serial connection state"""
        if self.connect_button.isChecked():
            try:
                port = self.port_combo.currentText()
                if not port:
                    raise ValueError("No port selected")
                
                self.serial_connection = serial.Serial(port, self.BAUD_RATE, timeout=0)
                self.connect_button.setText("Disconnect")
                self.port_combo.setEnabled(False)
                self.refresh_button.setEnabled(False)
                
                self.serial_timer.start()
                self.terminal.appendPlainText(f"Connected to {port} at {self.BAUD_RATE} baud\n")
                
            except Exception as e:
                self.connect_button.setChecked(False)
                QMessageBox.critical(self, "Error", f"Failed to connect: {str(e)}")
                self.serial_connection = None
        else:
            if self.serial_connection:
                self.serial_timer.stop()
                self.serial_connection.close()
                self.serial_connection = None
            
            self.connect_button.setText("Connect")
            self.port_combo.setEnabled(True)
            self.refresh_button.setEnabled(True)
            self.terminal.appendPlainText("Disconnected\n")

    def read_serial(self):
        """Read data from serial port and display in terminal"""
        if self.serial_connection and self.serial_connection.is_open:
            try:
                if self.serial_connection.in_waiting:
                    data = self.serial_connection.read(self.serial_connection.in_waiting)
                    text = data.decode('utf-8', errors='replace')
                    self.terminal.insertPlainText(text)
                    self.terminal.ensureCursorVisible()
            except Exception as e:
                self.terminal.appendPlainText(f"Error reading serial: {str(e)}\n")

    def get_modifier_string(self):
        """Get the current modifier combination"""
        modifiers = []
        if self.ctrl_check.isChecked():
            modifiers.append("CTRL")
        if self.alt_check.isChecked():
            modifiers.append("ALT")
        if self.shift_check.isChecked():
            modifiers.append("SHIFT")
        
        special_key = self.special_combo.currentText()
        if special_key != "None":
            modifiers.append(special_key)
            
        return "+".join(modifiers) if modifiers else ""

    def create_preview_section(self):
        preview_group = QGroupBox("Command Preview")
        preview_layout = QVBoxLayout()
        
        self.preview_label = QLabel("No selection")
        self.preview_label.setStyleSheet("""
            QLabel {
                font-family: Consolas, Monaco, monospace;
                font-size: 14px;
                padding: 10px;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        preview_layout.addWidget(self.preview_label)
        preview_group.setLayout(preview_layout)
        return preview_group

    def create_modifier_section(self):
        modifier_group = QGroupBox("Key Modifiers")
        modifier_layout = QVBoxLayout()
        
        # Modifier checkboxes with custom styling
        checkbox_style = """
            QCheckBox {
                font-size: 12px;
                padding: 5px;
            }
            QCheckBox:hover {
                background-color: #f0f0f0;
            }
        """
        
        # Modifier checkboxes
        modifier_row = QHBoxLayout()
        self.ctrl_check = QCheckBox("CTRL")
        self.alt_check = QCheckBox("ALT")
        self.shift_check = QCheckBox("SHIFT")
        
        for checkbox in [self.ctrl_check, self.alt_check, self.shift_check]:
            checkbox.setStyleSheet(checkbox_style)
            checkbox.toggled.connect(self.update_preview)
            
        modifier_row.addWidget(self.ctrl_check)
        modifier_row.addWidget(self.alt_check)
        modifier_row.addWidget(self.shift_check)
        modifier_row.addStretch()
        
        # Special keys dropdown
        special_row = QHBoxLayout()
        special_row.addWidget(QLabel("Special Key:"))
        self.special_combo = QComboBox()
        special_keys = ["None", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                       "Enter", "Escape", "Backspace", "Delete", "Tab", "Space",
                       "Up", "Down", "Left", "Right", "Home", "End", "PgUp", "PgDown"]
        self.special_combo.addItems(special_keys)
        self.special_combo.currentTextChanged.connect(self.update_preview)
        special_row.addWidget(self.special_combo)
        special_row.addStretch()
        
        # Quick Combination Buttons
        quick_combo_group = QGroupBox("Quick Combinations")
        quick_combo_layout = QGridLayout()
        
        quick_combos = [
            ("Ctrl+Alt", lambda: self.set_quick_combo(ctrl=True, alt=True)),
            ("Ctrl+Shift", lambda: self.set_quick_combo(ctrl=True, shift=True)),
            ("Alt+Shift", lambda: self.set_quick_combo(alt=True, shift=True)),
            ("Ctrl+Alt+Shift", lambda: self.set_quick_combo(ctrl=True, alt=True, shift=True)),
            ("Clear All", lambda: self.set_quick_combo())
        ]
        
        for i, (text, func) in enumerate(quick_combos):
            btn = QPushButton(text)
            btn.clicked.connect(func)
            quick_combo_layout.addWidget(btn, i // 2, i % 2)
            
        quick_combo_group.setLayout(quick_combo_layout)
        
        # Add all sections to modifier layout
        modifier_layout.addLayout(modifier_row)
        modifier_layout.addLayout(special_row)
        modifier_layout.addWidget(quick_combo_group)
        
        modifier_group.setLayout(modifier_layout)
        return modifier_group

    def set_quick_combo(self, ctrl=False, alt=False, shift=False):
        """Set quick combination of modifier keys"""
        self.ctrl_check.setChecked(ctrl)
        self.alt_check.setChecked(alt)
        self.shift_check.setChecked(shift)
        self.special_combo.setCurrentText("None")
        self.update_preview()

    def create_keypad_section(self):
        keypad_container = QGroupBox("Number Keypad")
        keypad_layout = QGridLayout()
        keypad_layout.setSpacing(10)

        # Define keypad layout (9-0 and *#)
        keypad_numbers = [
            ['9', '8', '7'],
            ['6', '5', '4'],
            ['3', '2', '1'],
            ['*', '0', '#']
        ]

        button_style = """
            QLabel {
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QComboBox {
                min-width: 80px;
                padding: 5px;
            }
        """

        self.dropdowns = {}
        for row, numbers in enumerate(keypad_numbers):
            for col, number in enumerate(numbers):
                container = QWidget()
                layout = QVBoxLayout(container)
                layout.setSpacing(5)

                # Label for the number
                label = QLabel(number)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet(button_style)

                # Dropdown with A-Z and None
                combo = QComboBox()
                if number in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    combo.addItem('-Select-')
                    combo.addItems(list(ascii_uppercase))
                    self.dropdowns[int(number)] = combo
                    combo.currentTextChanged.connect(
                        lambda text, num=number: self.on_selection_changed(int(num), text)
                    )
                else:
                    combo.addItem('-')
                    combo.setEnabled(False)

                layout.addWidget(label)
                layout.addWidget(combo)
                keypad_layout.addWidget(container, row, col)

        keypad_container.setLayout(keypad_layout)
        return keypad_container

    def update_preview(self):
        """Update the preview label with current selection"""
        if self.current_number is not None and self.current_letter is not None:
            modifiers = self.get_modifier_string()
            if modifiers:
                preview = f"{self.current_number}:{self.current_letter}:{modifiers}"
            else:
                preview = f"{self.current_number}:{self.current_letter}"
            self.preview_label.setText(preview)
            self.preview_label.setStyleSheet("""
                QLabel {
                    font-family: Consolas, Monaco, monospace;
                    font-size: 14px;
                    padding: 10px;
                    background-color: #e8f5e9;
                    border: 1px solid #81c784;
                    border-radius: 4px;
                }
            """)

    def on_selection_changed(self, number, letter):
        """Handle dropdown selection changes"""
        if letter == '-Select-':
            return
            
        self.current_number = number
        self.current_lette r = letter
        self.update_preview()

        if self.serial_connection and self.serial_connection.is_open:
            try:
                # Get modifiers
                modifiers = self.get_modifier_string()
                
                # Create message with modifiers if any
                if modifiers:
                    message = f"{number}:{letter}:{modifiers}\n"
                else:
                    message = f"{number}:{letter}\n"
                
                self.serial_connection.write(message.encode())
                self.terminal.appendPlainText(f"Sent: {message}")
            except Exception as e:
                self.terminal.appendPlainText(f"Error sending data: {str(e)}\n")


    def closeEvent(self, event):
        """Clean up serial connection when closing"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_timer.stop()
            self.serial_connection.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = LetterNumberUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()