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
        print("\n. . .receiving from client(s). . .")
        buff, caddr = sock.recvfrom(4096)
        buff = buff.decode()
        list = buff.splitlines()
        print("client address: ", caddr)
        print("---successfully received message from client---")
        status = buff[0]
        #print("\n. . .THREAD ATTEMPT. . .")
        print("\n. . .MULTITHREAD UTLIIZATION. . .")
        smt = threading.Thread(target=multiserver, args=(sock, caddr[0], cport, list, server_list))
        smt.start()
        print("---successfully started multithreading for server---")

def client(username, serverip, serverport, clientport):
    local_list = {}
    print("\n. . .entering the client function. . .")
    sock = socket(AF_INET, SOCK_DGRAM)
    print("---socket sock has been created for client---")
    sock.bind(('',clientport))
    print("---client socket successfully bound---")
    local_list = list_create(local_list, username, serverip, clientport)
    print("\n. . .beginning test. . .")
    print("Welcome, %s. Your port number is %d and are attempting to connect to the port %d" % (username, clientport, serverport))
    test = "REGISTRATION\n{u}\n{i}\n{c}".format(u = str(username), i = str(serverip), c = int(clientport))
    sock.sendto(test.encode(), (serverip, serverport))
    print("---message sent---")

    print("\n.. .MULTITHREAD UTILIZATION FOR CURRENT SERVER. . . ")
    cmt = threading.Thread(target=multiclient, args=(sock, cport, local_list))
    cmt.start()

def multiserver(sock, caddr, cport, recv_list, serv_list):
    list = recv_list
    status = list[0]


    if status == "REGISTRATION":
        print("\n. . .Beginning Registration process on server side. . .")
        username = list[1]
        ip = list[2]
        cliport = list[3]
        if username in serv_list:
            if (serv_list[username]["Client Port"] == cliport):
                print("===situation of a returning client===")
                upd = "RETURNER\n{u}\n{i}".format(u=username, i=ip)
                sock.sendall(upd.encode())
            else:
                print("===duplicate found===")
                dup = "DUPLICATE\nA duplicate was found. Need to get rid of client"
                sock.sendto(dup.encode(), (caddr, cliport))
        else:
            reg = "REGISTER\n{u}\n{i}\n{c}".format(u = username, i = ip, c = cliport)
            sock.sendall(reg.encode())
    else:
        print("unknown status. Currently working on it.")

def multiclient(sock, port, recv_list):
    while True:
        buff, addr = sock.recvfrom(4096)
        buff = buff.decode()
        lines = buff.splitlines()
        status = lines[0]

        if status == "RETURNER":
            username = lines[1]
            ip = lines[2]
            recv_list[username]["IP"] = ip
            recv_list[username]["Status"] = "Online"
        elif status == "DUPLICATE":
            print("hard exiting. need to restart because you have taken a name that already exists")
            sys.exit()
        elif status == "REGISTER":
            username = lines[1]
            ip = lines[2]
            cport = lines[3]
            list_create(recv_list, ip, cport)
        else:
            print("unkown status. Currently working on")

def server_reg(sock, caddr, name, ip, sport, cport, slist):
    print("\n. . .beginning client registration. . .")
    isDup = False
    if name in slist:
        print("===duplicate found within clients===")
        dup = "USER EXISTS\n Username already exists within another client"
        sock.sendto(dup.encode(), (caddr, cport))
    else:
        slist[name] = {}
        slist[name]["IP"] = ip
        slist[name]["Client Port"] = cport
        slist[name]["Status"] = "Online"
        print("---table successfully updated for server registration---")
        print("\n. . .creating ACK. . .")
        ack = "REGISTERED\n{n}\n{i}\n{c}".format(u = str(name), i = str(ip), c = int(cport))
        sock.sendall(ack.encode())

def list_create(list, name, ip, cport):
    list[name] = {}
    list[name]["IP"] = ip
    list[name]["Client Port"] = cport
    list[name]["Status"] = "Online"
    print("---table successfully updated---")
    return list

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