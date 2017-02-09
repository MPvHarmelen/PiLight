import socketserver
import netifaces as ni


class EchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        print(data)
        self.request.send(data)
        return


if __name__ == '__main__':
    import socket
    import threading
    try:
        hostip = ni.ifaddresses('wlan0')[2][0]['addr']
        address = (hostip, 0)  # let the kernel give us a port
        server = socketserver.TCPServer(address, EchoRequestHandler)
        ip, port = server.server_address  # find out what port we were given
        print("Address: {}:{}".format(ip, port))
        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True)  # don't hang on exit
        t.start()
        while True:
            pass
    except KeyboardInterrupt:
        print("\nclosing server")
        server.socket.close()
