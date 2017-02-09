import socket
import argparse


def send_msg(ip, port, message):
    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(type(ip))
    print(type(port))
    s.connect((ip, port))

    # Send the data
    print("Sending: {}".format(message))
    len_sent = s.send(message.encode())

    # Receive a response
    response = s.recv(len_sent)
    dec_response = response.decode()
    print("Received: {}".format(dec_response))

    # Clean up
    s.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    parser.add_argument('port', type=int)
    parser.add_argument('msg')
    args = parser.parse_args()
    send_msg(args.ip, args.port, args.msg)
