import threading
import sys
import os
import socket
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from collections import defaultdict


with open("client_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

HOST = config["ip"]
PORT = config["port"]

class ChatClient(QWidget):

    file_conflict_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.nickname, ok = QInputDialog.getText(self, "设置昵称", "请输入您的昵称:")
        if not ok or not self.nickname.strip():
            sys.exit()

        self.received_files = defaultdict(dict)
        self.init_ui()
        self.connect_to_server()

        self.file_conflict_signal.connect(self.handle_file_conflict)

    def init_ui(self):
        self.setWindowTitle(f"DoubleCats Client by karsl-program - {self.nickname}")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("输入消息...")
        self.message_input.returnPressed.connect(self.send_message)
        layout.addWidget(self.message_input)

        self.send_button = QPushButton("发送消息")
        self.send_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 16px; padding: 10px; border-radius: 5px;"
        )
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        self.file_button = QPushButton("发送文件")
        self.file_button.setStyleSheet(
            "background-color: #2196F3; color: white; font-size: 16px; padding: 10px; border-radius: 5px;"
        )
        self.file_button.clicked.connect(self.send_file)
        layout.addWidget(self.file_button)

        self.setLayout(layout)

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

        self.client_socket.sendall(self.nickname.encode("utf-8"))
        threading.Thread(target=self.receive_messages).start()

    def send_message(self):
        message = self.message_input.text().strip()
        if not message:
            return
        full_message = f"{self.nickname}: {message}"
        self.client_socket.sendall(full_message.encode("utf-8"))

        self.chat_display.append(f"<b>{full_message}</b>")
        self.message_input.clear()

    def send_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if file_path:
            with open(file_path, "rb") as f:
                file_data = f.read()
            filename = os.path.basename(file_path)
            filesize = len(file_data)

            header = f"HEADER:{self.nickname}:{filename}:{filesize}".encode("utf-8")
            self.client_socket.sendall(header)
            self.client_socket.sendall(file_data)
            self.chat_display.append(f"已发送文件 '{filename}'")

    def handle_file_conflict(self, original_filename, sender):
        new_filename, ok = QInputDialog.getText(self, "文件名冲突", f"文件 '{original_filename}' 已存在，请输入新文件名:")
        if ok and new_filename.strip():
            self.save_file_with_new_name(sender, original_filename, new_filename)

            if sender in self.received_files and original_filename in self.received_files[sender]:
                del self.received_files[sender][original_filename]
        elif not ok:
            self.chat_display.append(f"文件 '{original_filename}' 未保存")

    def save_file_with_new_name(self, sender, original_filename, new_filename):
        self.chat_display.append(f"文件 '{original_filename}' 将保存为 '{new_filename}'")
        with open(new_filename, "wb") as f:
            f.write(self.received_files[sender][original_filename])

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    if data.startswith(b"HEADER:"):
                        header = data.decode("utf-8").split(":")
                        sender, filename, filesize = header[1], header[2], int(header[3])
                        file_data = b""
                        remaining_size = filesize
                        while remaining_size > 0:
                            chunk = self.client_socket.recv(min(1024, remaining_size))
                            file_data += chunk
                            remaining_size -= len(chunk)


                        if os.path.exists(filename):
                            self.received_files[sender][filename] = file_data
                            self.file_conflict_signal.emit(filename, sender)
                        else:
                            with open(filename, "wb") as f:
                                f.write(file_data)
                            self.chat_display.append(f"已接收文件并保存为 '{filename}'")
                    else:
                        message = data.decode("utf-8")
                        if not message.startswith(f"{self.nickname}:"):
                            self.chat_display.append(message)
            except:
                self.chat_display.append("与服务器断开连接")
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec_())