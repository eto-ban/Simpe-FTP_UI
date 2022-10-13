import socket
import os


def list_cmd(c):
    directory = os.listdir('./home/')
    msg = ""
    for i in directory:
        msg = msg + " " + i
    c.send(msg.encode(FORMAT))


def retr_cmd(c, filename):
    file = open('./home/' + filename, 'r')
    data = file.read()
    c.send(data.encode(FORMAT))


def stor_cmd(c, filename):
    file = open('./home/{}'.format(filename), 'w')
    data = c.recv(SIZE).decode(FORMAT)
    file.write(data)
    file.close()


s = socket.socket()
print("[CREATED] Сокет успешно создан")

PORT = 12345
NUM_CLINETS = 5
FORMAT = 'utf-8'
SIZE = 1024

s.bind(('', PORT))
print("[BINDED] Сокет подключен к %s" % (PORT))

s.listen(NUM_CLINETS)
print("[LISTENING] Обновление . . .")


while True:

    c, addr = s.accept()
    print("")
    print('[NEW CONNECTION] Новый пользаватель', addr)
    command = c.recv(SIZE).decode(FORMAT).split()

    if command[0] == 'list':
        print("[LIST] Клиент запросил список файлов из {} .".format(addr))
        list_cmd(c)

    elif command[0] == 'RETR':
        print("[RETR {}] Клиент скачал файл {}".format(command[1], addr))
        retr_cmd(c, command[1])

    elif command[0] == 'STOR':
        print("[STOR {}] Клиент загрузил файл {} .".format(command[1], addr))
        stor_cmd(c, command[1])

    c.close()
    print("[CONNECTION CLOSED] Соедининие закрыто")
    print("")
