pragma Singleton
pragma ComponentBehavior: Bound
import QtQuick
import Quickshell
import qs.services
import qs.modules.common
import qs.modules.common.models

Singleton {
    id: root
    property string query: ""
    property string settledQuery: ""
    Timer { id: debounce; interval: 80; onTriggered: root.settledQuery = root.query }
    onQueryChanged: {
        if (query.length === 0) { debounce.stop(); settledQuery = "" }
        else debounce.restart()
    }
    property var results: {
        const raw = settledQuery.trim()
        if (raw.startsWith("?")) {
            const words = raw.slice(1).trim()
            const engine = Config.options?.search?.engineBaseUrl || "https://www.google.com/search?q="
            const url = engine + encodeURIComponent(words)
            return [{
                id: "web-search", name: words ? "搜索网页：" + words : "输入关键词搜索网页",
                comment: "使用默认浏览器打开", iconName: "travel_explore",
                iconType: LauncherSearchResult.IconType.Material,
                type: Translation.tr("Web"), verb: Translation.tr("Search"),
                keepOpen: !words,
                execute: () => {
                    if (!words) return
                    Quickshell.execDetached(["/usr/bin/systemd-run", "--user", "--quiet", "--collect",
                        "--property=ExitType=cgroup", "--", "/usr/bin/xdg-open", url])
                }
            }]
        }
        const all = raw.startsWith(">")
        const q = all ? raw.slice(1).trim() : raw
        if (!raw) return []
        const seen = new Set()
        return (all && !q ? AppSearch.list : AppSearch.fuzzyQuery(q)).filter(entry => {
            const key = String(entry?.name ?? "").trim().toLowerCase()
            if (!key || seen.has(key)) return false
            seen.add(key)
            return true
        }).map(entry => ({
            id: entry.id, name: entry.name, comment: entry.comment ?? "",
            iconName: entry.icon, iconType: LauncherSearchResult.IconType.System,
            type: Translation.tr("App"), verb: Translation.tr("Launch"),
            execute: () => AppSearch.launchEntry(entry)
        }))
    }
}
