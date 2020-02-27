import threading
import socket

IP = "10.100.102.16"
PORT = 20
BUFFER = 1024

MESSAGE = None
NUM_OF_THREADS = 0
COUNTED_THREADS = 0


def main():
    global NUM_OF_THREADS
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)