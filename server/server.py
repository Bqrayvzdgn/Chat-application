import socket
import threading

HEADER = 64
IP = socket.gethostbyname(socket.gethostname())
PORT = 50001
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT_SERVER_CODE"
USERNAME_MESSAGE = "EXAMPLE_APP_USERNAME_FIELD"
SEP = "///**//"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

users = []

def send_message(to_username, msg):
    for user in users:
        if user['username'] == to_username:
            connection = user["connection"]
            msg = msg.encode(FORMAT)
            msg_length = str(len(msg)).encode(FORMAT)
            header = msg_length + b' ' * (HEADER - len(msg_length))
            connection.send(header)
            connection.send(msg)
            break

def delete_connection(username):
    for idx, user in enumerate(users):
        if user['username'] == username:
            del users[idx]
            break

def handle_client(conn, addr):
    print(f"[New Connection] {addr} connected...")

    connected = True
    while connected:
        max_length = conn.recv(HEADER).decode(FORMAT)
        if max_length:
            max_length = int(max_length)
            msg = conn.recv(max_length).decode(FORMAT)
            write_active_connections()
            messages = msg.split(SEP)
            username = messages[0]
            print(f"{users}")
            if USERNAME_MESSAGE in msg:
                data = {
                    "username": username,
                    "connection": conn
                }
                users.append(data)
                continue

            if DISCONNECT_MESSAGE in msg:
                print("[Disconnect] Disconnecting from server")
                delete_connection(username)
                connected = False
            elif len(messages) > 2:
                print(f"[{addr}] message will send -> {msg}")
                to_username = messages[1]
                send_message(to_username, msg)

    conn.close()
    write_active_connections()

def write_active_connections():
    print(f"Active Connection Count is {len(users)}")

def start():
    server.listen()
    print(f"[Listening] Server is Listening now on {IP}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        write_active_connections()


if __name__ == "__main__":
    print("[Starting] Socket Server is starting... Stand By")
    start()
