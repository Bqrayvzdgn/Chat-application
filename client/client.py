import socket
from threading import Thread

HEADER = 64
IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT_SERVER_CODE"
USERNAME_MESSAGE = "EXAMPLE_APP_USERNAME_FIELD"
SEP = "///**//"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = str(len(message)).encode(FORMAT)
    header = msg_length + b' ' * (HEADER - len(msg_length))
    client.send(header)
    client.send(message)

def main(username, to_username):
    while True:
        message = input("")
        if message.lower() == "disconnect":
            send(f"{username}{SEP}{DISCONNECT_MESSAGE}")
            break
        send(f"{username}{SEP}{to_username}{SEP}{message}")

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
                        print(f"\n {messages[0]} -->  {messages[2]} \n")
                    else:
                        print("Security issue: Check server.py")
        except ConnectionResetError:
            print("Connection closed by server.")
            break

if __name__ == "__main__":
    username = input("Please write your user name: ")
    if username:
        send(f"{username}{SEP}{USERNAME_MESSAGE}")
        to_username = input("Who will you send messages to: ")
        print("You can write your message and press enter. Type 'disconnect' to exit.")
        main_thread = Thread(target=main, args=(username, to_username,))
        listen_thread = Thread(target=listen, args=(username,))
        main_thread.daemon = True
        main_thread.start()
        listen_thread.start()
        main_thread.join()