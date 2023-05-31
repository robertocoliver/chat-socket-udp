import socket
import sys

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def send_message(self, message):
        self.client_socket.sendto(message.encode(), (self.server_ip, self.server_port))
        
    def receive_message(self):
        data, server_address = self.client_socket.recvfrom(1024)
        return data.decode()

    def close(self):
        self.client_socket.close()


class Server:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        
    def wait_for_connections(self):
        print('Server listening on {}:{}'.format(self.server_ip, self.server_port))
        while True:
            data, client_address = self.server_socket.recvfrom(1024)
            print('Received message from {}: {}'.format(client_address, data.decode()))
            self.send_message(client_address, 'Message received')

    def send_message(self, client_address, message):
        self.server_socket.sendto(message.encode(), client_address)

    def close(self):
        self.server_socket.close()


def start_udp_client(server_ip, server_port):
    client = Client(server_ip, server_port)

    # Enviar mensagem do cliente para o servidor
    message = input('Digite a mensagem para enviar ao servidor: ')
    client.send_message(message)


    response = client.receive_message()
    print('Resposta do servidor:', response)

    client.close()


def start_udp_server(server_port):
    server = Server('', server_port)
    server.wait_for_connections()
    server.close()


if len(sys.argv) < 3:
    print("Usage: python <filename.py> <server_ip> <server_port> <client|server>")
    sys.exit(1)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
mode = sys.argv[3]

if mode == "client":
    start_udp_client(server_ip, server_port)
elif mode == "server":
    start_udp_server(server_port)
else:
    print("Usage: python <filename.py> <server_ip> <server_port> <client|server>.")
