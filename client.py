import sys
import socket


EXIT_CODE = 'exit'

class Client(object):
    def __init__(self):
        self.server_adress = 'localhost'
        self.server_port = 11000


    def options(self):
        '''
        Oi epiloges tou xrhsth
        '''
        print('1: read, 2: write, 3: modify, 4: delete, 5: exit')


    def connect(self):
        
        '''
        Ylopioish kai prospathia syndeshs me ton server
        
        '''
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.options()
            connection_info = (self.server_adress, self.server_port)

            sock.connect_ex(connection_info)

            while True:
                message = input('Enter your message: ')
                if message == 'exit':
                    print('Exiting')
                    break

                sock.sendall(message.encode('utf-8'))
                data = sock.recv(1024).decode('utf-8')
                print(data)

            sock.sendall('{}'.format(message).encode('utf-8'))
            sock.close()
            sys.exit()


if __name__ == "__main__":
    client = Client()
    client.connect()
