import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QPushButton, QWidget
)
from PyQt6.QtGui import QFont

class LandlineKeypad(QWidget):
    def __init__(self):
        super().__init__()
        
        # Telephone keypad layout
        self.keypad_layout = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['*', '0', '#']
        ]
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Keypad grid
        keypad_grid = QVBoxLayout()
        
        for row in self.keypad_layout:
            row_layout = QHBoxLayout()
            for key in row:
                btn = QPushButton(key)
                btn.setFixedSize(80, 80)  # Larger button size
                btn.setFont(QFont('Arial', 16))  # Larger font
                
                btn.clicked.connect(lambda checked, k=key: self.on_key_press(k))
                row_layout.addWidget(btn)
            
            keypad_grid.addLayout(row_layout)
        
        layout.addLayout(keypad_grid)
        self.setLayout(layout)
    
    def on_key_press(self, key):
        print(f"Pressed key: {key}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Dial ഡെക്ക്")
        self.setMinimumSize(QSize(300, 500))
        
        # Main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Create landline keypad
        landline_keypad = LandlineKeypad()
        main_layout.addWidget(landline_keypad)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()