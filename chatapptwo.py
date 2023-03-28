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
    soct = socket(AF_INET, SOCK_DGRAM)
    bundle = ("localhost", port)
    soct.bind(("localhost",port))
    server_list = {}
    print("Server successfully created...\n")

    while True:
        buf, paddr = soct.recvfrom(4096)
        buf = buf.decode()
        lines = buf.splitlines()
        stat = lines[0]
        if stat == "REGISTER":
            u = str(lines[1])
            ip = str(lines[2])
            c = int(lines[3])
            serv_reg = threading.Thread(target=server_reg,args=(soct, paddr, u, ip, c, server_list))
            serv_reg.start()

def client(username, server_ip, server_port, client_port):
    local_list = {}
    soct = socket(AF_INET, SOCK_DGRAM)
    print("got soct")
    u = str(username)
    s = int(server_port)
    c = int(client_port)
    p = str(server_ip)
    bundle = (p,c)
    soct.bind((p, c))
    print("finished bind")
    
    """
    boolz = isDup_cli(soct)
    if boolz == True:
        print("invalid username. please try again")
        sys.exit(1)
    print("tested duplicates")
    """

    reg_thread = threading.Thread(target=cli_reg, args=(soct, u, p, s, c))
    tester = threading.Thread(target=isDup_cli, args=(soct,))
    listen_thread = threading.Thread(target=clientlisten, args=(soct, local_list))
    print("STARTING THREAD REGISTRATION")
    reg_thread.start()

    tester.start()
    isDup = tester.join()
    if isDup:
        print("sorry. Username already taken. Please choose one that is not taken")
        sys.exit(1)
    else:
        print("all looks good")
    print("STARTING THREAD LISTENING")
    listen_thread.start()

def clientlisten(bundle, locllst):
    print("client listening")
    soct = socket(AF_INET, SOCK_DGRAM)
    while True:
        buf, saddr = soct.recvfrom(4096)
        buf = buf.decode()
        lines = buf.splitlines()
        stat = lines[0]
        #extra stuff for the other lines idk
        if stat == "REGISTERED":
            usr = str(lines[1])
            ipaddr = str(lines[2])
            cport = int(lines[3])
            locllst[usr] = {}
            locllst[usr]["ip"] = ipaddr
            locllst[usr]["client port"] = cport
            locllst[usr]["status"] = "online"
            print(">>> Client table has been successfully updated. \n")

def server_reg(soct, paddr, username, ip, cport, server_list):
        if username in server_list:
            isDup = True
        if isDup:
            dup = "ALREADY EXISTS\nUsername already exists"
            soct.sendto(dup.encode(), (paddr[0], cport))
        else:
            server_list[username] = {}
            server_list[username]["ip"] = ip
            server_list[username]["client port"] = cport
            server_list[username]["status"] = "online"
            ack = "REGISTERED\n{username}\n{ip}\n{cport}"
            soct.sendall(ack.encode())
        isDup = False

def cli_reg(soct, usrn, ip, sp, cp):
    if (sp >= 1024 and sp <= 65536) and (cp >= 1024 and cp <= 65535):
        print ("Welcome, %s! You are logging in from %s, and your personal port is %d. \n" % (usrn, ip, cp))

        print("beginning registration... \n")

        bc_addr = (ip, cp)
        bs_addr = (ip, sp)
        print("i think the coputer doesn't like this part")
        #reg = "%s \n %s \n %d \n %d", str(usrn), str(ip), int(sp), int(cp)
        reg = "REGISTER\n{str(usrn)}\n{str(ip)}\n\n{int(cp)}"

        """
        REGISTER
        tudbud
        127.0.0.1
        4000
        """
        
        soct.sendto(reg.encode(), bs_addr)
        print("client registration being sent to server")
    else:
        print("error. incorrect size of port")
        sys.exit(1)


def serv_reg(port):
   pass

def isDup_cli(soct):
        buf, saddr = soct.recvfrom(4096)
        buf = buf.decode()
        lines = buf.splitlines()
        stat = lines[0]
        if stat == "ALREADY EXISTS":
            return True
    
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