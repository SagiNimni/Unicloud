import threading
import socket
import json

IP = socket.gethostbyname(socket.gethostname())
PORT = 20
BUFFER = 1024

DATA = {}
MESSAGE = None
NUM_OF_THREADS = 0


def get_message(client_socket):
    message = client_socket.recv(BUFFER)
    return message.decode()


def ack(client_socket):
    try:
       client_socket.send("ack".encode())
    except ConnectionResetError:
        pass
    except OSError:
        pass


def end(client_socket):
    try:
       client_socket.send("end".encode())
    except ConnectionResetError:
        pass
    except OSError:
        pass


def sign_up(client_socket):
    global DATA
    while True:
        registration_info = get_message(client_socket)
        if registration_info == 'end':
            break
        if registration_info is not None:
            username, password = registration_info.split(',')
            DATA[username] = {}
            DATA[username].update({
              'password': password
            })
            with open('data.json', 'w') as outfile:
                json.dump(DATA, outfile)
            ack(client_socket)
            print("success")
            break


def login(client_socket):
    global DATA
    while True:
        login_info = get_message(client_socket)
        if login_info == 'end':
            break
        if login_info is not None:
            username, password = login_info.split(',')
            if username in DATA:
                if DATA[username]['password'] == password:
                    print("logged in")
                    break
                else:
                    client_socket.send('wrong'.encode())
            else:
                client_socket.send('wrong'.encode())


def communicate(client_socket, client_address):
    global DATA, BUFFER
    ip, port = client_address
    print("Client connected, ip: ", ip, " port: ", port)
    print("Number of connected clients: " + str(threading.active_count() - 1))
    try:
        while True:
            message = get_message(client_socket)
            if message == 'disconnect':
                end(client_socket)
                client_socket.close()
                print("Client disconnected, ip: ", ip, " port: ", port)
                break
            if message == 'create':
                ack(client_socket)
                sign_up(client_socket)
            elif message == 'login':
                ack(client_socket)
                login(client_socket)
    except Exception as e:
        client_socket.close()
        print("Client crashed, ip: ", ip, " port: ", port, ", Error:")
        print(e)


def main():
    global DATA
    with open("data.json") as data_json:
        DATA = json.load(data_json)

    global NUM_OF_THREADS
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    print("Server Online")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread_for_clients = threading.Thread(target=communicate, args=(client_socket, client_address))
            thread_for_clients.start()
            NUM_OF_THREADS += 1
    finally:
        server_socket.close()
        print("Server Crashed")


if __name__ == '__main__':
    main()
