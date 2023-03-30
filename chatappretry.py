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
        cport = caddr[1]
        caddr = caddr[0]
        print("client address: ", caddr)
        print("---successfully received registration from client---")
        status = buff[0]
        #print("\n. . .THREAD ATTEMPT. . .")
        print("\n. . .MULTITHREAD UTILIZATION. . .")
        smt = threading.Thread(target=multiserver, args=(sock, caddr, cport, sport, list, server_list))
        smt.start()
        smt.join()
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
    print("---registration message sent---")

    print("\n.. .MULTITHREAD UTILIZATION FOR CURRENT SERVER. . . ")
    cmt = threading.Thread(target=multiclient, args=(sock, int(cport), local_list))
    cmt.start()

def multiserver(sock, caddr, cport, sport, recv_list, serv_list):
    print("---successfully entered into the multithread server function----")
    line = recv_list
    list = serv_list
    status = line[0]
    print("HOW IS THIS WRONG**************************************: ", status)

    print("\n. . .Testing Status in multithread function. . .")
    if status == "REGISTRATION":
        print("\n. . .Beginning Registration process on server side. . .")
        username = line[1]
        ip = line[2]
        cliport = line[3]
        if username in list:
            if (list[username]["Client Port"] == cliport):
                #assumming the server list is not empty
                print("===situation of a returning client===")
                upd = "RETURNER\n{u}\n{i}".format(u=username, i=ip)
                for un in list:
                    combo = (un["IP"], un["Client Port"])
                    print("*********sending registeration to ", combo)
                    sock.sendto(upd.decode(), combo)
            else:
                #assuming the server list is not empty
                print("===duplicate found===")
                dup = "DUPLICATE\nA duplicate was found. Need to get rid of client"
                sock.sendto(dup.encode(), (caddr, cliport))
        else:
            print("---not found in list, so need to do new registration---")
            reg = "REGISTER\n{u}\n{i}\n{c}".format(u = username, i = ip, c = cliport)
            send_all_func(sock, reg, list, ip, cliport, sport, True)
            print("---presumably successfully sent to all clients.---")
            list = list_create(list, username, ip, cliport)
    elif status == "REGISTRATION_UPDATED":
        print("\n. . .updating registration. . .")
        pp = line[1]
        printer = line[2]
        print(printer)
        ready = "ACK\nsend when you're ready"
        send_all_func(sock, ready, list, pp, cliport, sport, True)
    elif status == "REGISTRATION_FINISHED":
        print("\n. . .finishing up registration. . .")
        pp = line[1]
        cp = line[2]
        printer = line[3]
        print(printer)
        ready = "ACK\nsend when you're ready"
        send_all_func(sock, ready, list, pp, cp, sport, True)
    else:
        print("unknown status. Currently working on it.")

def multiclient(sock, port, recv_list):
    while True:
        buff, addr = sock.recvfrom(4096)
        print("server addres: ", addr)
        buff = buff.decode()
        lines = buff.splitlines()
        status = lines[0]

        if status == "RETURNER":
            username = lines[1]
            ip = lines[2]
            recv_list[username]["IP"] = ip
            recv_list[username]["Status"] = "Online"
            ack = "REGISTRATION_UPDATED\nClient updated registration and is ready"
            sock.sendto(ack.encode(), addr)
        elif status == "DUPLICATE":
            print("hard exiting. need to restart because you have taken a name that already exists")
            sys.exit()
        elif status == "REGISTER":
            username = lines[1]
            ip = lines[2]
            cport = lines[3]
            recv_list = list_create(recv_list, username, ip, cport)
            ack = "REGISTRATION_FINISHED\n{i}\n{c}\nClient finished registration and is ready".format(i = ip, c = cport)
            sock.sendto(ack.encode(), addr)
        elif status == "ACK":
            print("this is where I will start texting.")
        else:
            print("unkown status. Currently working on")

def list_create(list, name, ip, cport):
    list[name] = {}
    list[name]["IP"] = str(ip)
    list[name]["Client Port"] = int(cport)
    list[name]["Status"] = "Online"
    print("---table successfully updated---")
    return list

def send_all_func(sock, encoded, list, clip, cport, sport, isServ):
    print("i still hate this test: ", list)
    if len(list) > 1:
        for un in list:
            print("i hate this test: ", un)
            combo = (un["IP"], un["Client Port"])
            print("*********sending registeration to ", combo)
            sock.sendto(encoded.encode(), combo)
    else:
            print("************************* too tired: ", clip, cport)
            combo = (str(clip), int(cport))
            print("******sending registration to ", combo)
            sock.sendto(encoded.encode(), combo)
            print("---new list---\n     ", list)

    if not isServ:
        sock.sendto(encoded.encode(), (str(clip), int(sport)))

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