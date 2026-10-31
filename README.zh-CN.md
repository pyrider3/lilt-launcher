# Lilt Launcher

面向 **niri / Wayland** 的独立应用启动器，注重连续过渡、稳定的搜索结果与简洁的初始界面。

**Based on iNiR by snowarch (https://github.com/snowarch/inir).**

这是修改后的非官方衍生项目，不是官方 iNiR 或 iRiS。原始界面、组件与动画系统归上游作者所有；本仓库提供独立运行适配。

## 功能

- 打开时只有搜索框，没有建议区。
- 背景与内容同步淡入、缩放和退出。
- 输入时不整组闪烁，清空搜索时输入框不跳动。
- 输入法正在组合拼音时隐藏占位提示。
- `>` 查看全部应用，限制面板高度并支持内部滚动。
- `> 名称` 筛选应用；`? 关键词` 用默认浏览器搜索网页。
- 优先加载实际图标文件，缺失时提供统一图标。
- 可与 Noctalia 共存，不更改顶栏、壁纸或 niri 窗口动画。

## 安装

初始验证环境：Arch Linux、niri 26.04、Quickshell 0.3.2、Qt 6.12 和 systemd 用户会话。其他发行版尚未验证。

```sh
sudo pacman -S --needed quickshell bubblewrap python go gtk3 kirigami syntax-highlighting \
  qt6-5compat qt6-multimedia qt6-svg qt6-wayland qt6-imageformats \
  ttf-material-symbols-variable breeze-icons

git clone https://github.com/pyrider3/lilt-launcher.git
cd lilt-launcher
python3 install.py
~/.local/bin/lilt-launcher check
~/.local/bin/lilt-launcher open
```

Go 1.26+ 用于首次编译上游配色求解器；没有 Go 时使用内置默认配色。仓库不附带预编译运行库、个人设置或缓存。

安装器不自动修改 niri，也不设置开机启动。在 niri 的 `binds` 中自行加入：

```kdl
Mod+Space repeat=false { spawn "lilt-launcher" "toggle"; }
```

请确保 niri 的 PATH 包含 `~/.local/bin`，否则填入命令的绝对路径。也可以改用 `Mod+D`，但需先移除相同按键的旧绑定。修改后执行 `niri validate`。

## 操作与设置

方向键或 Tab 选择，Enter 打开；Esc 清空搜索，再按一次收起。程序按需启动并保持后台运行，`lilt-launcher stop` 可退出。

运行数据位于 `${XDG_STATE_HOME:-~/.local/state}/lilt-launcher/`，配置是其中的 `config/illogical-impulse/config.json`。目录名沿用上游内部配置模型，不代表它会读取或修改整套 iNiR 桌面。日志在 `logs/session.log`。

网页搜索引擎由 `search.engineBaseUrl` 指定，默认 Google。应用与浏览器通过正常的 systemd 用户会话启动，不继承启动器的隔离配置。

卸载：

```sh
~/.local/bin/lilt-launcher stop
python3 install.py --uninstall
```

自行移除添加的 niri 快捷键。卸载保留用户状态，可按需另行删除。

## 范围与来源

只提供启动器，不提供上游的设置面板、Dock、控制中心和插件入口。为了 QML 导入兼容，仓库保留了部分共享模块，未全部实例化。跨发行版、全新系统依赖覆盖与不同显卡效果仍需进一步测试。

基于上游提交 `48cdcecb0f6089cfbb7019054602eab28e154b3b`。遵循 GPL-3.0 及 [NOTICE](NOTICE) 中适用的上游附加条款；字体许可证随文件保留。修改范围见 [UPSTREAM.md](UPSTREAM.md)。
