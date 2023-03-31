from socket import *
import threading
import sys
import signal

"""
test = "{s}\n{u}\n{i}\n{c}".format(s = "REGISTRATION", u = str(un), i = str(ip), c = int(cport))
sock.sendto(test.encode(), (ip, sport))
"""

qq = False
BUF = 4096
ai = AF_INET
sd = SOCK_DGRAM

def lister(list, name, ip, port): #client port
    print("LISTER TST: ", list, name, ip, port)
    list[name] = {}
    list[name]["IP"] = str(ip)
    list[name]["Port"] = int(port)
    list[name]["Status"] = "Online"

def server(sport): #server port
    list = {}
    sock = socket(ai, sd)
    sock.bind(('',sport))

    while True:
        reg, addr = sock.recvfrom(BUF)
        buff = reg.decode()
        lines = buff.splitlines()
        reg = threading.Thread(target=server_reg, args=(sock, sport, lines, list))
        reg.start()
        reg.join()

def client_reg(sock, list, un, ip, sp, cp):
    """
    sending...

    FRESH_REG
    tudbud
    IP
    CPORT
    """

    test = "{s}\n{u}\n{i}\n{c}".format(s = "REGISTRATION", u = str(un), i = str(ip), c = int(cport))
    sock.sendto(test.encode(), (ip, sp))

    reg, addr = sock.recvfrom(BUF)
    buff = reg.decode()
    lines = buff.splitlines()
    status = lines[0]
    un1 = lines[1]
    print(un1, "gu ogg")
    ip1 = lines[2]
    cport1 = lines[3]
    if cport1 == cport: #means that they don't have to re-update
        if status == "RET":
            list[un]["IP"] = ip1
            print(">>> [Welcome. You are registered]")
        elif status == "DUP":
            print("hard exiting. need to restart because you have taken a name that already exists")
            sys.exit()
        elif status == "REG":
            list = lister(list, un1, ip1, cport1)
            print(">>> [Welcome. You are registered]")
    else:
        if status == "RET":
            list = lister(list, un1, ip1, cport1)
        elif status == "DUP":
            pass
        elif status == "REG":
            list = lister(list, un1, ip1, cport1)

        print(">>> [Welcome. You are registered]")

def server_reg(sock, sport, lines, list):
    status = lines[0]
    un = lines[1]
    ip = lines[2]
    cport = lines[3]
    if status == "REGISTRATION":
            if un in list:
                if(list[un]["Port"] == cport):
                    list[un]["IP"] = ip
                    upd =  "{s}\n{u}\n{i}\n{c}".format(s = "RET", u = str(un), i = str(ip), c = int(cport))
                    for un in list:
                        combo = (un["IP"], un["Port"])
                        sock.sendto(upd.decode(), combo)
                    print(">>> [Welcome. You are registered]")
                else:
                    dup = "{s}\n{u}\n{i}\n{c}".format(s = "DUP", u = str(un), i = str(ip), c = int(cport))
                    print(">>> [Welcome. Username already taken. Please try again]")
                    sock.sendto(dup.decode(), (ip, cport))
            else:
                list = lister(list, un, ip, cport)
                reg = "{s}\n{u}\n{i}\n{c}".format(s = "REG", u = str(un), i = str(ip), c = int(cport))
                send_all_func(sock, reg, list, ip, cport, sport, True, un)
                print(">>> [Welcome. You are registered]")

def client(un, ip, sport, cport):
    quitter = False
    list = {}
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('',cport))
    local_list = lister(list, un, ip, cport)
    print("LOCAL LIST TEST; ", un, ip, cport)
    cmt = threading.Thread(target=client_reg, args=(sock, local_list, un, ip, sport, cport))
    cmt.start()
    cmt.join()

    while True:
        temp = input(">>>:: ")
        print(temp)

def send_all_func(sock, encoded, list, clip, cport, sport, isServ, username):
    if isServ:
        if list:
            if len(list) > 1:
                for un in list:
                    if list[un] != username:
                        sock.sendto(encoded.encode(), combo)
        else:
                combo = (str(clip), int(cport))
                sock.sendto(encoded.encode(), combo)
    else:
        sock.sendto(encoded.encode(), (str(clip), int(sport)))

if __name__ == "__main__":
    #signal.signal(signal.SIGINT, silent_leave)
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