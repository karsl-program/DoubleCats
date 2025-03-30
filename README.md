# DoubleCats

A fast, clean, beautiful chat room.

## 简介
DoubleCats 是一个快速、简洁且美观的聊天室项目，包含客户端和服务器端。它允许用户在本地网络中进行实时聊天，并支持文件传输功能。

## 功能特性
- **实时聊天**：用户可以在聊天室中实时发送和接收消息。
- **文件传输**：支持在聊天室中发送和接收文件。
- **消息限制**：设置了消息冷却时间和最大消息长度，防止滥用。
- **用户昵称**：用户可以设置自己的昵称，方便识别。

## 安装与运行

### 前提条件
- Python 3.x
- PyQt5（仅客户端需要）

### 安装依赖
客户端需要安装 PyQt5，可以使用以下命令进行安装：
```bash
pip install PyQt5
```

### 配置
项目使用 JSON 文件进行配置：
- `client_config.json`：客户端配置文件，包含服务器的 IP 地址和端口号。
- `server_config.json`：服务器配置文件，包含服务器的 IP 地址、端口号、消息冷却时间和最大消息长度。

### 运行服务器
在项目根目录下运行以下命令启动服务器：
```bash
python server.py
```

### 运行客户端
在项目根目录下运行以下命令启动客户端：
```bash
python client.py
```

## 使用方法
1. 启动服务器后，客户端可以连接到服务器。
2. 客户端启动时，会提示输入昵称。输入昵称后，即可进入聊天室。
3. 在消息输入框中输入消息，按回车键或点击“发送消息”按钮发送消息。
4. 点击“发送文件”按钮，选择要发送的文件，即可将文件发送到聊天室。

## 贡献
如果你想为 DoubleCats 项目做出贡献，请遵循以下步骤：
1. Fork 本项目。
2. 创建一个新的分支：`git checkout -b feature/your-feature`。
3. 提交你的更改：`git commit -m 'Add some feature'`。
4. 推送至分支：`git push origin feature/your-feature`。
5. 提交 Pull Request。

## 许可证
本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 作者
karsl-program
