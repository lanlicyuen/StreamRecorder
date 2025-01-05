# Live Record

Live Record 是一个用于检测直播状态的应用程序。它可以检测多个平台的直播状态，并通过 API 提供给 Android 应用使用。

## 项目简介

该项目最初是一个基于 Tkinter 的桌面应用程序，现在已转换为 Flask Web 应用程序。它可以检测直播状态，并通过 API 提供给其他应用程序使用。

## 安装步骤

1. 克隆仓库到本地：
    ```sh
    git clone https://github.com/lanlicyuen/live_record.git
    cd live_record
    ```

2. 创建并激活虚拟环境：
    ```sh
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    source .venv/bin/activate  # macOS/Linux
    ```

3. 安装依赖：
    ```sh
    pip install -r requirements.txt
    ```

4. 运行 Flask 应用：
    ```sh
    python app.py
    ```

## 使用说明
API 说明
GET /streamers
获取所有主播信息。

POST /streamers
添加新的主播。

请求体示例：

### 添加主播

通过 POST 请求添加新的主播：
```sh
curl -X POST http://localhost:5000/streamers -H "Content-Type: application/json" -d '{
    "name": "主播名称",
    "platform": "SOOP",
    "link": "https://play.sooplive.co.kr/主播ID",
    "avatar": "头像路径",
    "check_interval": 5
}'
```
