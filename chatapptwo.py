from socket import *
import threading
import sys


"""
STATUS
- username
- serverip
- server port
- client port
"""

server_list = {}

def server(port):
    print("\n. . .creating socket server. . .")
    soct = socket(AF_INET, SOCK_DGRAM)
    bundle = ("localhost", port)
    host = gethostbyname(gethostname())
    print("server IP: ", host)
    """try:
        soct.bind(('',port))
    except soct.error as e:
        print(str(e)) """
    server_list = {}
    soct.connect((host, port))
    print("---Server successfully created---")
    print("\n. . .starting the wait to hear from client. . .")
    while True:
        buf, paddr = soct.recvfrom(4096)
        print("---received from client---")
        buf = buf.decode()
        lines = buf.splitlines()
        test_not = 0
        for i in lines:
            print("spot #", test_not, " for lines: ", i)
            test_not += 1
        stat = lines[0]
        if stat == "REGISTER":
            print("---received a REGISTER update---")
            u = str(lines[1])
            ip = str(lines[2])
            c = int(lines[3])
            print("\n. . .creating server registration thread. . .")
            serv_reg = threading.Thread(target=server_reg,args=(soct, paddr, u, ip, c, server_list))
            print("---thread created successfully. \nStarting the thread. . .")
            serv_reg.start()

def client(username, server_ip, server_port, client_port):
    local_list = {}
    print("\n. . .creating client socket. . .")
    soct = socket(AF_INET, SOCK_DGRAM)
    print("---got soct---\n")
    u = str(username)
    s = int(server_port)
    c = int(client_port)
    #p = str(server_ip)
    #bundle = (p,c)
    host = gethostbyname(gethostname())
    #print("server IP: ", host)
    soct.bind(('', c))
    soct.connect((host,s))
    print("--successfully bound the client---")
    
    """
    boolz = isDup_cli(soct)
    if boolz == True:
        print("invalid username. please try again")
        sys.exit(1)
    print("tested duplicates")
    """

    print("\n. . .beginning thread registration, duplicate test, and multithreading for listening thread. . .")
    cli_reg(soct, u, host, s, c)
    print("---registration return successful---")
    isDup = isDup_cli(soct)
    print("---duplicate return successful---")
    print("\n. . .CREATING MULTITHREAD FOR CLIENT LISTEN. . .")
    listen_thread = threading.Thread(target=clientlisten, args=(soct, local_list))
    print("---listening thread successfully created---")
    if isDup:
        print("sorry. Username already taken. Please choose one that is not taken")
        sys.exit(1)
    else:
        print("---no duplicates---")
        soct.connect((host,c))
        print("---successfully connected to server---")
    print("\n. . .STARTING THREAD LISTENING. . .")
    listen_thread.start()

def clientlisten(soct, locllst):
    print("---client listening---")
    while True:
        buf, saddr = soct.recvfrom(4096)
        print("---successfully received from server---")
        buf = buf.decode()
        lines = buf.splitlines()
        stat = lines[0]
        #extra stuff for the other lines idk
        print("\n. . .testing for status given by server. . .")
        if stat == "REGISTERED":
            print("---registration status successfully received---")
            usr = str(lines[1])
            ipaddr = str(lines[2])
            cport = int(lines[3])
            locllst[usr] = {}
            locllst[usr]["ip"] = ipaddr
            locllst[usr]["client port"] = cport
            locllst[usr]["status"] = "online"
            print("---Client table has been successfully updated---")

def server_reg(soct, paddr, username, ip, cport, server_list):
        print("\n. . .duplicate username test. . .")
        if username in server_list:
            isDup = True
            print("---duplicate found within clients---")
        else:
            isDup = False
        if isDup:
            dup = "ALREADY EXISTS\nUsername already exists"
            soct.sendto(dup.encode(), (paddr[0], cport))
        else:
            print("---no duplicate found. continuing. . .\n")
            server_list[username] = {}
            server_list[username]["ip"] = ip
            server_list[username]["client port"] = cport
            server_list[username]["status"] = "online"
            print("---server list dictionary successfully created---")
            print("\n. . .creating ACK. . .")
            ack = "REGISTERED\n{username}\n{ip}\n{cport}"
            soct.sendall(ack.encode())
            print("---acknowledgement successfully sent to all clients---")
        isDup = False

def cli_reg(soct, usrn, ip, sp, cp):
    if (sp >= 1024 and sp <= 65536) and (cp >= 1024 and cp <= 65535):
        print ("Welcome, %s! You are logging in from %s, and your personal port is %d. \n" % (usrn, ip, cp))

        print("\n. . .beginning registration. . .")

        bc_addr = (ip, cp)
        bs_addr = (ip, sp)
        reg = "REGISTER\n{u}\n{i}\n{c}".format(u = str(usrn), i = str(ip), c = int(cp))
        print("---registration successfully created---")

        """
        REGISTER
        tudbud
        127.0.0.1
        4000
        """
        print("\n. . .registration ack being sent. . .")
        soct.sendto(reg.encode(), bs_addr)
    else:
        print("error. incorrect size of port")
        sys.exit(1)


def serv_reg(port):
   pass

def isDup_cli(soct):
        print("\n. . .testing for duplicates. . .")
        buf, saddr = soct.recvfrom(4096)
        buf = buf.decode()
        lines = buf.splitlines()
        stat = lines[0]
        if stat == "ALREADY EXISTS":
            print("---dups found---")
            return True
        else:
            print("---no dups found---")
            return False
    
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