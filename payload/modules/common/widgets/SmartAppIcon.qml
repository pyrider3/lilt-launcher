import QtQuick
import qs.services
Item {
    id: root
    property string icon: ""
    property string fallback: "application-x-executable"
    property bool filled: false
    property int iconSize: 24
    property alias implicitSize: root.iconSize
    property bool monochrome: false
    property color color: "white"
    property bool useFluent: false
    implicitWidth: iconSize
    implicitHeight: iconSize
    property bool failed: false
    onIconChanged: failed = false
    Image {
        anchors.fill: parent
        source: AppSearch.resolveIcon(root.failed ? root.fallback : root.icon, root.fallback)
        sourceSize.width: root.iconSize * 2
        sourceSize.height: root.iconSize * 2
        fillMode: Image.PreserveAspectFit
        smooth: true
        onStatusChanged: if (status === Image.Error && !root.failed) root.failed = true
    }
}
