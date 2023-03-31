from socket import *
import threading
import sys

def serverrespond(sock, taddr, tport):
    ack = "ack\n Message:\n This is an ack"
    sock.sendto(ack.encode(), (taddr, tport))
    print("ack sent")

def servermode(port):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('',port))
    print(">>Server is online")

    while True:
        buffer, addr = sock.recvfrom(4096)
        buffer = buffer.decode()
        lines = buffer.splitlines()

        header = lines[0]
        cport = lines[2]
        msg = lines[3]

        print("header: ", header)
        print(">>> ", msg)
        print("wtf is addr", addr)
        print("cport type: ", cport)
        #serverrespond(sock, addr[0], cport)
        send = threading.Thread(target=serverrespond, args=(sock, str(addr[0]), int(cport)))
        send.start()

        #multithreading
        
def clientlisten(port):
    print("client listening")
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('',port))

    while True:
        buf, saddr = sock.recvfrom(4096)
        buf = buf.decode()
        lines = buf.splitlines()
        header = lines[0]
        msg = lines[2]
        print("header: ", header)
        print(">>>", msg)

def clientmode(un, ip, sport, cport):
    sock = socket(AF_INET, SOCK_DGRAM)
    msg = "header\n" + "port:\n" + str(cport) + "\nmessage:\n Hello there"
    sock.sendto(msg.encode(), (ip, sport))
    print("first msg sent")

    #multithreading
    listen = threading.Thread(target=clientlisten, args = (cport,))
    listen.start()

    while True:
        print(">>> ", end="")
        temp = input()
        inputlist = temp.split()
        try:
            header = inputlist[0]
        except:
            print("\n invalid, try again")
            continue
        if header == "send":
            message = ""
            for i in range(1, len(inputlist)):
                message = message + inputlist[i]
                send = "header" + header + "\n port:\n" + str(cport) + "\nmessage:\n Hello there"
                print(">>>message sent")

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == '-s':
        sport = int(sys.argv[2])
        servermode(sport)
    elif mode == '-c':
        uname = str(sys.argv[2])
        ip = str(sys.argv[3])
        sport = int(sys.argv[4])
        cport = int(sys.argv[5])
        clientmode(uname, ip, sport, cport)
    else:
        print("invalid")