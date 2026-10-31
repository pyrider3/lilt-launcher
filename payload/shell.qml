//@ pragma UseQApplication
//@ pragma ShellId lilt-launcher
//@ pragma Env QT_QUICK_CONTROLS_STYLE=Basic
//@ pragma Env QSG_RENDER_LOOP=threaded
import QtQuick
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import qs
import qs.modules.common
import qs.services
import qs.services.deferred
import qs.modules.iris.palette

ShellRoot {
    id: app
    Component.onCompleted: {
        Quickshell.watchFiles = false
        CompositorService.setSortingConsumer("irisLauncher", true)
        GlobalStates.shellEntryReady = true
        GlobalStates.deferredPanelsReady = true
    }
    Component.onDestruction: CompositorService.setSortingConsumer("irisLauncher", false)
    IpcHandler {
        target: "launcher"
        function toggle(): void { GlobalStates.searchOpen = !GlobalStates.searchOpen }
        function open(): void { GlobalStates.searchOpen = true }
        function close(): void { GlobalStates.searchOpen = false }
        function activate(): void {
            const entry = LauncherSearch.results[0]
            if (entry && typeof entry.execute === "function") {
                entry.execute()
                GlobalStates.searchOpen = false
            }
        }
        function search(query: string): void {
            LauncherSearch.query = query
            GlobalStates.searchOpen = true
        }
        function status(): string { return JSON.stringify({ open: GlobalStates.searchOpen, query: LauncherSearch.query, results: LauncherSearch.results.length, settled: LauncherSearch.settledQuery, apps: AppSearch.list.length, surfaces: windows.instances.map(w => ({progress: w.progress, displayed: w.displayed, fade: w.fade, geometry: w.geometry})) }) }
        function quit(): void { Qt.quit() }
    }
    Variants {
        id: windows
        model: Quickshell.screens
        PanelWindow {
            id: host
            readonly property var geometry: palette.geometryState
            readonly property var fade: palette.fadeState
            readonly property real progress: palette.transitionProgress
            readonly property string displayed: palette.displayedQuery
            required property var modelData
            screen: modelData
            color: "transparent"
            visible: palette.present
            exclusionMode: ExclusionMode.Ignore
            anchors { top: true; bottom: true; left: true; right: true }
            WlrLayershell.namespace: "lilt-launcher"
            WlrLayershell.layer: WlrLayer.Overlay
            WlrLayershell.keyboardFocus: palette.here && GlobalStates.searchOpen ? WlrKeyboardFocus.Exclusive : WlrKeyboardFocus.None
            IrisPalette {
                id: palette
                anchors.fill: parent
                screen: host.screen
            }
        }
    }
}
