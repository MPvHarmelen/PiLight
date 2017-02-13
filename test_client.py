import sys
import socket
import argparse


def send_msg(ip, port, msg):
    HOST, PORT = "localhost", 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    print("Step 1")
    s.send(msg.encode())
    print("Step 2")
    print(str(s.recv(1000)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    parser.add_argument('port', type=int)
    parser.add_argument('msg')
    args = parser.parse_args()
    send_msg(args.ip, args.port, args.msg)
