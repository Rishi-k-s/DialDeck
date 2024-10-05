import QtQuick
import QtQuick.Controls.Basic

ApplicationWindow {
    visible: true
    width: 600
    height: 500
    title: "HelloApp"
    
    Text {
    anchors.centerIn: parent
    text: "Hello World"
    font.pixelSize: 24
    }
}