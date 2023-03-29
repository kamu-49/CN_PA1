from socket import *
import threading
import sys

def server(port):

    print("\n. . .entering the server function. . .")
    server_list = {}
    sock = socket(AF_INET, SOCK_DGRAM)
    print("---socket sock has been been created for server---")
    sock.bind(('',port))
    print("---server socket successfully bound---")

    while True:
        print("\n. . .receiving from client. . .")
        buff, caddr = sock.recvfrom(4096)
        buff = buff.decode()
        buff = buff.splitlines()
        print("client address: ", caddr)
        count = 0
        for i in buff:
            print("         >>", count, "'th item in buff: ", i)
            count += 1
        print("---test successfully received---")
        msg = "TEST_SUCCESS\nhi there"
        cport = buff[3]
        sock.sendto(msg.encode(), (str(caddr[0]), int(cport)))
        print("---test successfully sent---")

def client(username, serverip, serverport, clientport):
    local_list = {}
    print("\n. . .entering the client function. . .")
    sock = socket(AF_INET, SOCK_DGRAM)
    print("---socket sock has been created for client---")
    sock.bind(('',clientport))
    print("---client socket successfully bound---")

    print("\n. . .beginning test. . .")
    user = username
    house = serverip
    servport = serverport
    cliport = clientport
    print("Welcome, %s. Your port number is %d and are attempting to connect to the port %d" % (user, cliport, servport))
    test = "TEST_SUCCESS\n{u}\n{i}\n{c}".format(u = str(user), i = str(house), c = int(cliport))
    sock.sendto(test.encode(), (serverip, servport))
    print("---message sent---")
    while True:
        buff, saddr = sock.recvfrom(4096)
        print("server address: ", saddr)
        buff = buff.decode()
        buff = buff.splitlines()
        count = 0
        for i in buff:
            print("         >>", count, "'th item in buff: ", i)
            count += 1
        print("---test successfully received---")



if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == '-s':
        sport = int(sys.argv[2])
        server(sport)
    elif mode == '-c':
        name = str(sys.argv[2])
        ip = str(sys.argv[3])
        sport = int(sys.argv[4])
        cport = int(sys.argv[5])
        print("starting cli")
        client(name, ip, sport, cport)
    else:
        print("invalid")