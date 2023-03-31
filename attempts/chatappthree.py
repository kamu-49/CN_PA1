from socket import *
import threading
import sys
import signal

qq = False

def server(port):
    print("@@@Location: server(port)")
    server_list = {}
    sock = socket(AF_INET, SOCK_DGRAM)
    print("- - - - - -server socket created")
    sock.bind(('',port))
    print("- - - - - -server socket bound")

    while True:
        print("- - - - - -listening")
        buff, caddr = sock.recvfrom(4096)
        print("- - - - - -received signal")
        buff = buff.decode()
        list = buff.splitlines()
        cport = caddr[1]
        caddr = caddr[0]
        print("- - - - - -successfully received signal")
        status = buff[0]
        print("\n. . . . .SERVER MULTITHREAD UTILIZATION. . . . .")
        smt = threading.Thread(target=multiserver, args=(sock, caddr, cport, sport, list, server_list))
        smt.start()
        smt.join()
        print("- - - - - -successfully started and joined multiserver thread")

def client(username, serverip, serverport, clientport):
    print("@@@Location: client(username, serverip, serverport, clientport)")
    quitter = False
    local_list = {}
    sock = socket(AF_INET, SOCK_DGRAM)
    print("- - - - - -client socket created")
    sock.bind(('',clientport))
    print("- - - - - -client socket bound")
    local_list = list_create(local_list, username, serverip, clientport)
    print("- - - - - -local list created. current look:\n   ", local_list, "\n")
    print("Welcome, %s. Your port number is %d and are attempting to connect to the port %d\n" % (username, clientport, serverport))
    test = "REGISTRATION\n{u}\n{i}\n{c}".format(u = str(username), i = str(serverip), c = int(clientport))
    sock.sendto(test.encode(), (serverip, serverport))
    print("- - - - - -REGISTRATION message sent to server")

    print("\n. . . . .CLIENT MULTITHREAD UTLIIZATION. . . . . ")
    cmt = threading.Thread(target=multiclient, args=(sock, int(cport), local_list))
    talkative = threading.Thread(target=client_sendmsg,args=(sock, local_list, cport))
    cmt.start()
    cmt.join()
    """
    if q is True:
        sq = "SILENT_QUIT\n{u}\n{i}\n{p}\n silent quit commence".format(u = str(username), i = str(serverip), p=int(clientport))
        sock.sendto(sq.encode(), (serverip, serverport))
        print("- - - - - -successfull silent quit test")"""
    print("- - - - - -successfully started multiserver thread")
    talkative.start()
    ##talkative.join()
def multiserver(sock, caddr, cport, sport, recv_list, serv_list):
    print("@@@Location: multiserver(sock, clientaddr, clientport, serverport, line, list)")
    line = recv_list
    list = serv_list
    status = line[0]
    print("- - - - - -line properly extracted")

    print("- - - - - -testing status...")
    if status == "REGISTRATION":
        print("! ! ! Status: REGISTRATION")
        username = line[1]
        ip = line[2]
        cliport = line[3]
        print("- - - - - -line extracted again")
        if username in list:
            print("! ! ! Status: username in list")
            if (list[username]["Client Port"] == cliport):
                print("! ! ! Status: username and cport identical. A returning user")
                upd = "RETURNER\n{u}\n{i}".format(u=username, i=ip)
                for un in list:
                    combo = (un["IP"], un["Client Port"])
                    sock.sendto(upd.decode(), combo)
                print("- - - - - -REGISTRATION sent to users")
            else:
                print("! ! ! Status: duplicate username without similar client port")
                dup = "DUPLICATE\nA duplicate was found. Need to get rid of client"
                print("TEST TEST*******************\n", str(caddr), str(cliport))
                sock.sendto(dup.encode(), (str(caddr), int(cliport)))
                print("- - - - - -dup status sent to the proper client")
        else:
            print("! ! ! Status: original user")
            reg = "REGISTER\n{u}\n{i}\n{c}".format(u = username, i = ip, c = cliport)
            send_all_func(sock, reg, list, ip, cliport, sport, True, username)
            print("- - - - - -send_all_func called. sent REGISTER signal to all clients(if any others)")
            list = list_create(list, username, ip, cliport)
            print("- - - - - -server list updated:  ", list, "\n")
    elif status == "REGISTRATION_UPDATED" or status == "REGISTRATION_FINISHED":
        print("! ! ! Status: registration update received")
        pp = line[1]
        user = line[2]
        cliport = line[3]
        ready = "ACK\nsend when you're ready"
        send_all_func(sock, ready, list, pp, cliport, sport, True, user)
        print("- - - - - -send all func called to send an ACK to all clients")
    elif status == "SILENT_QUIT":
        print("! ! !client has quit! ! !")
        user = line[1]
        ip = line[2]
        port = line[3]
        list[user]["Status"] = "Offline"
        for u in list:
            if list[u]["Status"] == "Online":
                userr = u
                ipp = list[u]["IP"]
                portt = list[u]["Client Port"]
                squit = "SILENT_QUIT_LIST_UPDATE\n{uz}\n{i}\n{p}\nA user has quit".format(uz=userr, i=ipp, p=portt)
                sock.sendto(squit.encode(), (ipp, portt))
    elif  status == "QUIT_ACK":
        ready = "ACK\nsend when you're ready"
        un = line[1]
        ii = line[2]
        ppp = line[3]
        sock.sendto(ready.encode(), (ii, ppp))
    else:
        print("unknown status. Currently working on it.")

def multiclient(sock, port, recv_list):
    print("@@@Loctaion: multiclient(sock, port, line)")
    while True:
        if qq is True:
            return True

        buff, addr = sock.recvfrom(4096)
        print("- - - - - -signal received on client side")
        buff = buff.decode()
        lines = buff.splitlines()
        status = lines[0]
        print("- - - - - -line split and checking status")

        if status == "RETURNER":
            print("! ! ! Status: returning user")
            username = lines[1]
            ip = lines[2]
            recv_list[username]["IP"] = ip
            recv_list[username]["Status"] = "Online"
            print("- - - - - -local list updated:   ", recv_list, "\n")
            ack = "REGISTRATION_UPDATED\n{i}\n{u}\n{c}Client updated registration and is ready".format(i=ip, u = username, c = port)
            sock.sendto(ack.encode(), addr)
            print("- - - - - -REGISTRATION UPATED sent to server")
        elif status == "DUPLICATE":
            print("hard exiting. need to restart because you have taken a name that already exists")
            sys.exit()
        elif status == "REGISTER":
            print("! ! !Status: registering process")
            username = lines[1]
            ip = lines[2]
            cport = lines[3]
            recv_list = list_create(recv_list, username, ip, cport)
            print("- - - - - -local list created and updated:   ", recv_list, "\n")
            ack = "REGISTRATION_FINISHED\n{i}\n{u}\n{c}\nClient finished registration and is ready".format(i = ip, u=username, c = cport)
            sock.sendto(ack.encode(), addr)
            print("- - - - - -REGISTRATION FINISHED sent to server")
        elif status == "ACK":
            print("this is where I will start texting.")
            return "finished"
        elif status == "SILENT_QUIT_LIST_UPDATE":
            username = lines[1]
            recv_list[username]["Status"] = "Offline"
            del_ack = "QUIT_ACK\n{u}\n{i}\n{c}".format(u=username, i=ip, c=cport)
            sock.sendto(del_ack.encode(), addr)
            #threading.Thread.exit()
        elif status == "TEXT":
            username = lines[1]
            message = lines[2]
            print(">>> %s: %s" % (username, message))
            ack = "TEXT_ACK\n{u}\n{i}\n{c}".format(u=username, i=addr[0], c=addr[1])
            sock.sendto(ack.encode(), addr)
        else:
            print("unkown status. Currently working on")

def client_sendmsg(sock,list, cport):
    print("****************************PLEASE IM REALLY TRYING")
    #while True:
    message = input(">>> ")
    """
    USER INPUT NOT WORKING FOR SOME REASON. CANNOT FIGURE OUT WHY
    """
    print("trying to configure message...")
    for u in list:
        if list[u]["Client Port"] == cport:
            tester_user = u
    message="send {u} hello this is the test message".format(u = tester_user)
    ot = message.split() #send, tudbud, test, message
    """if len(ot) <= 2:
        message = input("Incorrect length of words. Retry...\n>>>")"""
    user = ot[1]
    string = ' '.join(ot[x] for x in range(2, len(ot)))
    chattee_ip = list[user]["IP"]
    chattee_port = list[user]["Client Port"]
    chattee = (chattee_ip, chattee_port)
    msg = "TEXT\n{u}\n{m}".format(u=str(user), m=str(string))
    sock.sendto(msg.encode(), chattee)

    try:
        ack, addr = sock.recvfrom(4096)
        buff = ack.decode()
        lines = buff.splitlines()
        status = lines[0]
        if status == "TEXT_ACK":
            print(">>> [Messge received by %s]" % user)

    except socket.Timeouterror:
        print(">>> [No ACK from %s,message not delivered]." % user)

"""def client_groupchat(sock, list, port):
    #USER INPUT NTO WORKING. CONFIGURING TEST INSTANCES...
    test_group = "the fantastics"
    for u in list:
        if list[u]["Client Port"] == cport:
            tester_user = u
    message = ">>> create_group {d}".format(d = test_group)
    gc = message.split()
    if len(gc) < 2:
        message"""

def silent_leave(recv, frame):
    global qq
    print("! ! !CTRL C pressed! ! !")
    qq = True

def list_create(list, name, ip, cport):
    print("@@@Location: list create")
    list[name] = {}
    list[name]["IP"] = str(ip)
    list[name]["Client Port"] = int(cport)
    list[name]["Status"] = "Online"
    print("---table successfully updated---")
    return list

def send_all_func(sock, encoded, list, clip, cport, sport, isServ, username):
    print("@@@ Location: send all func")
    if isServ:
        if len(list) > 1:
            print("- - - - - -server contains more than yourself")
            for un in list:
                if list[un] != username:
                    combo = (list[un]["IP"], list[un]["Client Port"])
                    sock.sendto(encoded.encode(), combo)
        else:
                print("- - - - - -multiple people in server")
                combo = (str(clip), int(cport))
                sock.sendto(encoded.encode(), combo)
                print("- - - - - -new list after sending to proper clients:     ", list, "\n")
    else:
        print("- - - - - -sending fromclient. Need to send to server too")
        sock.sendto(encoded.encode(), (str(clip), int(sport)))

if __name__ == "__main__":
    signal.signal(signal.SIGINT, silent_leave)
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