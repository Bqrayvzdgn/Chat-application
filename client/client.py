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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_username(username):
    send(f"{USERNAME_MESSAGE}{SEP}{username}")

def send(msg):
    send_data(client, msg)

def send_data(connection, data):
    msg = data.encode(FORMAT)
    msg_length = len(msg)
    header = str(msg_length).encode(FORMAT)
    header += b' ' * (HEADER - len(header))
    connection.send(header)
    connection.send(msg)

def main(username, to_username):
    try:
        while True:
            message = input("Your message: ")
            if message.lower() == "disconnect":
                print("You disconnected.")
                break
            send(f"{username}{SEP}{to_username}{SEP}{message}")
    except KeyboardInterrupt:
        print("You disconnected.")
        send(f"{username}{SEP}{DISCONNECT_MESSAGE}")


def listen(username):
    connected = True
    while connected:
        try:
            max_length = client.recv(HEADER).decode(FORMAT)
            if max_length:
                max_length = int(max_length)
                msg = client.recv(max_length).decode(FORMAT)
                messages = msg.split(SEP)
                if len(messages) > 2:
                    if messages[1] == username:
                        print(f"\n You -->  {messages[2]}\n")
                    else:
                        print(f"\n{messages[0]} --> {messages[2]}\n")

        except ConnectionResetError:
            print("Connection closed by server.")
            connected = False
            break

if __name__ == "__main__":
    username = input("Please write your user name: ")
    if username:
        send_username(username)
        to_username = input("Who will you send messages to: ")
        print("You can write your message and press enter. Type 'disconnect' to exit.")
        main_thread = threading.Thread(target=main, args=(username, to_username,))
        listen_thread = threading.Thread(target=listen, args=(username,))
        main_thread.daemon = True
        main_thread.start()
        listen_thread.start()
        main_thread.join()
