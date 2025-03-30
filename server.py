import socket
import threading
import json
import time


with open("server_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

HOST = config["ip"]
PORT = config["port"]
COOLDOWN_TIME = config["cooldown_time"]
MAX_MESSAGE_LENGTH = config["max_message_length"]

clients = []
lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[+] {addr} 已连接")
    last_message_time = 0

    nickname = conn.recv(1024).decode("utf-8")
    print(f"[+] {nickname} ({addr}) 已连接")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break


            if data.startswith(b"HEADER:"):
                header = data.decode("utf-8").split(":")
                sender, filename, filesize = header[1], header[2], int(header[3])
                print(f"[+] 收到文件 '{filename}'，正在广播...")
                broadcast(data, conn)
                remaining_size = filesize
                while remaining_size > 0:
                    chunk = conn.recv(min(1024, remaining_size))
                    broadcast(chunk, conn)
                    remaining_size -= len(chunk)
            else:
                current_time = time.time()
                with lock:
                    if current_time - last_message_time < COOLDOWN_TIME:
                        conn.sendall("Error: 冷却时间未到，请稍后再试！".encode("utf-8"))
                        continue
                    last_message_time = current_time

                message = data.decode("utf-8")
                if len(message) > MAX_MESSAGE_LENGTH:
                    conn.sendall("Error: 消息长度超出限制！".encode("utf-8"))
                    continue
                if not message.strip():
                    conn.sendall("Error: 不允许发送空白消息！".encode("utf-8"))
                    continue

                print(f"[{nickname}] {message}")
                broadcast(message.encode("utf-8"), conn)

        except Exception as e:
            print(f"[-] {nickname} ({addr}) 断开连接: {e}")
            break

    with lock:
        clients.remove(conn)
    conn.close()

def broadcast(message, sender_conn):
    with lock:
        for client in clients:
            if client != sender_conn:
                try:
                    client.sendall(message)
                except:
                    client.close()
                    clients.remove(client)

def start_server():
    print("--- DoubleCats Server v1.0 by karsl-program ---")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] 服务器启动，监听 {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        with lock:
            clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()