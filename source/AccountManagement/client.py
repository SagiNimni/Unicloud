import socket
import threading

HOST_IP = "10.100.102.16"
HOST_PORT = 20
BUFFER = 1024


class ConnectAndLoginThread(threading.Thread):
    def run(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_IP, HOST_PORT))

        print("asd")


def main():
    ConnectAndLoginThread().start()


if __name__ == '__main__':
    main()
