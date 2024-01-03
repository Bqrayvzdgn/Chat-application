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
            send_data(connection, msg)
            break

def delete_connection(username):
    for idx, user in enumerate(users):
        if user['username'] == username:
            del users[idx]
            break

def send_data(connection, data):
    msg = data.encode(FORMAT)
    msg_length = len(msg)
    header = str(msg_length).encode(FORMAT)
    header += b' ' * (HEADER - len(header))
    connection.send(header)
    connection.send(msg)

def handle_client(conn, addr):
    print(f"[New Connection] {addr} connected...")

    connected = True
    username = None

    while connected:
        try:
            max_length = conn.recv(HEADER).decode(FORMAT)
            if max_length:
                max_length = int(max_length)
                msg = conn.recv(max_length).decode(FORMAT)
                write_active_connections()
                messages = msg.split(SEP)

                if len(messages) > 1:
                    if USERNAME_MESSAGE in messages[0]:
                        username = messages[1]
                        users.append({"username": username, "connection": conn})
                        continue

                if DISCONNECT_MESSAGE in msg:
                    print(f"[Disconnect] {username} disconnecting from server")
                    delete_connection(username)
                    connected = False
                elif len(messages) > 2:
                    send_message(messages[1], f"{username} says: {messages[2]}")
                    print(f"\n[{addr}] {username} says: {messages[2]}\n")

        except ConnectionResetError:
            print(f"[Disconnect] Connection closed by {addr}")
            delete_connection(username)
            connected = False

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
        break

if __name__ == "__main__":
    print("[Starting] Socket Server is starting... Stand By")
    start()
