import sys
import socket
import ctypes
import argparse
from coder import encode, decode


def send_msg(ip, port, cmd):
    print(cmd)
    msg = encode(*cmd)
    print("Encoded {}; Sending..".format(msg))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to {}:{}".format(ip, port))
    s.connect((ip, port))
    print(msg.to_bytes(4, byteorder='big'))
    print(msg.to_bytes(4, byteorder='little'))
    s.send(msg.to_bytes(4, byteorder='little'))
    print("Sent {}; Waiting for answer..".format(msg))
    print(str(s.recv(1000)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    parser.add_argument('port', type=int)
    parser.add_argument('cmd', type=int, nargs=7)
    args = parser.parse_args()
    send_msg(args.ip, args.port, args.cmd)
