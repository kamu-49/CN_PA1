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
        print("---successfully received message from client---")
        status = buff[0]
        #print("\n. . .THREAD ATTEMPT. . .")
        print("\n. . .attempting registration (assuming not using multithread). . .")
        if(status == "REGISTRATION"):
            username = buff[1]
            ip = buff[2]
            cport = [3]
            server_reg(sock, caddr[0], username, ip, port, cport, server_list)
            print("registration attempt successfull")


        '''count = 0
        for i in buff:
            print("         >>", count, "'th item in buff: ", i)
            count += 1
        print("---test successfully received---")
        msg = "TEST_SUCCESS\nhi there"
        cport = buff[3]
        sock.sendto(msg.encode(), (str(caddr[0]), int(cport)))
        print("---test successfully sent---")'''

def client(username, serverip, serverport, clientport):
    local_list = {}
    print("\n. . .entering the client function. . .")
    sock = socket(AF_INET, SOCK_DGRAM)
    print("---socket sock has been created for client---")
    sock.bind(('',clientport))
    print("---client socket successfully bound---")

    print("\n. . .beginning test. . .")
    print("Welcome, %s. Your port number is %d and are attempting to connect to the port %d" % (username, clientport, serverport))
    test = "REGISTRATION\n{u}\n{i}\n{c}".format(u = str(username), i = str(serverip), c = int(clientport))
    sock.sendto(test.encode(), (serverip, serverport))
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

def server_respond(sock, caddr, cport):
    """
    attempt to use this function when attempting to speak with multiple clients

    ADDITIONAL NOTES:
    - possibly consider making one for client, since they must speak with multiple clients and a server as well
    """
    pass
def client_listen(sock, port):
    """
    attempt to use this function when listening to multiple clients and the server as well

    ADDITIONAL NOTES:   
    - consider making one for server since it has to listen to multiple clients as well
        possibly what it means to "respond". it means it's listening to multiple, then answering to the specific out of many
    """
    pass



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