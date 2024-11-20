import sys
import os
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow

def windowInit():
    QQuickWindow.setSceneGraphBackend('software')
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.load('./UI/main.qml')

    sys.exit(app.exec())

if __name__ == "__main__":
    windowInit()