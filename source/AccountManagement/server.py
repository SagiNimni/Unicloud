import threading
import socket
import json

import sys
import ntpath

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
            username, password, device_mac = registration_info.split(',')
            DATA[username] = {}
            DATA[username].update({
              'password': password,
              'devices': "('{0}',)".format(device_mac),
              'methods': "{}",
              'accounts': "[]"
            })
            with open('data.json', 'w') as f:
                json.dump(DATA, f)
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
            username, password, device_mac = login_info.split(',')
            if username in DATA:
                if DATA[username]['password'] == password:
                    devices = eval("{0} + ('{1}',)".format(DATA[username]['devices'], device_mac))
                    DATA[username]['devices'] = str(devices)
                    with open("data.json", 'w+') as f:
                        json.dump(DATA, f)
                    client_socket.send(DATA[username]['accounts'].encode())
                    print("logged in")
                    break
                else:
                    client_socket.send('wrong'.encode())
            else:
                client_socket.send('wrong'.encode())


def edit(client_socket):
    global DATA
    while True:
        edit_info = get_message(client_socket)
        if edit_info == 'end':
            break
        if edit_info is not None:
            method, cloud_username, credentials, drive_type, folder_name, account_username, password, user_id = edit_info.split(',')
            if account_username in DATA:
                if DATA[account_username]['password'] == password:
                    instruction = "{'" + method + "':('{0}', '{1}', '{2}', '{3}', ['{4}'])"\
                        .format(cloud_username, credentials, drive_type, folder_name, user_id) + '}'
                    DATA[account_username]['methods'] = str({**eval(DATA[account_username]['methods']), **eval(instruction)})
                    account = "('{0}', '{1}', '{2}', '{3}')".format(cloud_username, credentials, drive_type, folder_name)
                    list = eval(DATA[account_username]['accounts'])
                    list.append(eval(account))
                    DATA[account_username]['accounts'] = str(list)
                    with open('data.json', 'w+') as f:
                        json.dump(DATA, f)
                client_socket.send('success'.encode())
                print('success')
                break


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
            elif message == 'edit':
                ack(client_socket)
                edit(client_socket)
    except Exception as e:
        client_socket.close()
        tb = sys.exc_info()[2]
        f = tb.tb_frame
        line = tb.tb_lineno
        filename = ntpath.split(f.f_code.co_filename)[1]
        print("Client crashed, ip: ", ip, " port: ", port, ", Exception in {0} line {1}:".format(filename, line))
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
