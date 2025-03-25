# Stream Recorder

一个功能强大的流媒体录制和格式转换工具，支持 Windows 和 Ubuntu 平台。

## 功能特点

- 录制流媒体内容（支持 TS 和 MP4 格式）
- 历史记录管理和快速访问
- 格式转换（支持批量转换）
- 自定义 FFmpeg 配置
- 跨平台支持 (Windows & Ubuntu)
- 简洁的用户界面

## 系统要求

### Windows
- Windows 10/11
- FFmpeg（需要单独下载安装）

### Ubuntu
- Ubuntu 20.04 或更高版本
- Python 3.6+
- FFmpeg (`sudo apt install ffmpeg`)
- Python 依赖: Tkinter, Pillow (`sudo apt install python3-tk && pip3 install pillow`)

## 安装说明

### Windows

1. 下载最新版本的 StreamRecorder：
   - 访问 [Releases](https://github.com/lanlicyuen/Live_Tools/releases) 页面
   - 下载最新版本的 `StreamRecorder.exe`

2. 安装 FFmpeg：
   - 访问 [FFmpeg 官网](https://ffmpeg.org/download.html#build-windows)
   - 下载并解压 FFmpeg
   - 记住 FFmpeg 的安装路径

3. 首次运行配置：
   - 运行 StreamRecorder.exe
   - 点击"关于我" -> "设置"
   - 配置 FFmpeg 路径

### Ubuntu

1. 安装必要依赖：
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk ffmpeg git
pip3 install pillow
```

2. 克隆仓库：
```bash
git clone https://github.com/lanlicyuen/Live_Tools.git
cd Live_Tools
```

3. 将 icon.ico 转换为 icon.png：
```bash
python3 -c "from PIL import Image; Image.open('icon.ico').save('icon.png')"
```

4. 运行程序：
```bash
python3 app.py
```

5. 可选：创建可执行文件：
```bash
pip3 install pyinstaller
pyinstaller --onefile --noconsole --icon=icon.png --name=StreamRecorder app.py
```

6. 可选：创建桌面快捷方式：
```bash
cat > ~/Desktop/StreamRecorder.desktop << 'EOF'
[Desktop Entry]
Name=Stream Recorder
Comment=Stream recording tool
Exec=/完整路径/StreamRecorder
Icon=/完整路径/icon.png
Terminal=false
Type=Application
Categories=AudioVideo;Video;
EOF

chmod +x ~/Desktop/StreamRecorder.desktop
```

## 使用说明

### 录制流媒体
1. 在主界面输入流媒体 URL
2. 选择保存格式（TS 或 MP4）
3. 选择保存文件夹
4. 点击"开始录制"

### 格式转换
1. 点击菜单"格式转换" -> "打开转换窗口"
2. 选择一个或多个输入文件（支持 TS、FLV 格式）
3. 选择输出目录
4. 点击"开始转换"

### 历史记录
- 点击菜单"记录" -> "查看历史记录"
- 右键点击记录可以打开所在文件夹

## 平台特定注意事项

### Windows
- 所有功能都有图形界面操作
- 支持文件浏览和选择
- 录制过程会打开命令行窗口显示进度

### Ubuntu
- 功能与 Windows 版本相同
- 录制过程在后台进行，不会显示命令行窗口
- 确保 FFmpeg 路径正确设置（通常为 `/usr/bin/ffmpeg`）

## 注意事项

- 首次使用必须配置 FFmpeg 路径
- 确保有足够的磁盘空间
- 建议使用稳定的网络连接
- 某些杀毒软件可能会误报，这是由于打包技术导致，程序本身是安全的

## 版本历史

### v1.4.1
- 添加 Ubuntu 支持
- 优化跨平台兼容性
- 改进文件路径处理
- 更新使用说明文档

### v1.4
- 新增格式转换功能
- 支持批量文件处理
- 优化用户界面
- 改进文件路径处理
- 更新程序图标

## 常见问题

### 杀毒软件报警
如果杀毒软件将程序标记为可疑文件，您可以：
1. 将程序添加到杀毒软件的白名单中
2. 程序已经过作者测试，请放心使用

### FFmpeg 配置
如果遇到 FFmpeg 相关问题：
1. 确保已正确安装 FFmpeg
2. 检查 FFmpeg 路径配置
3. 确保 FFmpeg 可以正常运行

## 联系方式

作者：Lanlic Yuen  
邮箱：lanlic@hotmail.com

## 许可证

本软件仅供个人研究和学习使用。
