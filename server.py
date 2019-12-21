import time
import socket
import random
import threading

EXIT_CODE = 'exit'


class Server(object):

    def __init__(self):
        self.lock = threading.Lock()
        self.port = 11000
        self.address = 'localhost'
        self.flights = self.fetch_flights()
        self.max_read_time = 2
        self.max_write_time = 6


    def listen(self):
        '''
        Arxikopioish ypodoxhs kai leitourgia afths.
        Gia kathe nea sindesh ksekinaei thread gia na eksipiretei ton pelath se diaforetiki porta
               
        '''
        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection_socket.bind((self.address, self.port))
        connection_socket.listen(1)
        print('Server listening on port {}'.format(self.port))

        while True:
            connection, address = connection_socket.accept()
            print(f'Connection Opened for {address}')
            threading.Thread(target = self.handle_client, 
                             args = (connection, )).start()

        connection_socket.close()


    def handle_client(self, connection):
        '''
        Methodos gia tin eksipirethsh tou pelath analoga me to minima pou dexete
        
        parametroi: connection (TCP syndesh sthn periptwsh afti)
        
        '''
        while True:
            client_mes = connection.recv(1024).decode('utf-8')

            if client_mes == EXIT_CODE:
                connection.close()
                break
            elif 'read' in client_mes:
                _, flight_code = client_mes.split()
                flight = self.get_flight(int(flight_code))
                if flight is not None:
                    connection.sendall('ROK {}'.format(flight).encode('utf-8'))
                else:
                    connection.sendall('RERR'.encode('utf-8'))
            elif 'write' in client_mes:
                _, code, status, flight_time = client_mes.split()
                self.add_flight(code, status, flight_time)
                connection.sendall('WOK'.encode('utf-8'))
            elif 'modify' in client_mes:
                _, code, status, time = client_mes.split()
                flight = self.modify_flight(code, status, time)
                if flight is not None:
                    connection.sendall('MOK'.encode('utf-8'))
                else:
                    connection.sendall('MERR'.encode('utf-8'))
            elif 'delete' in client_mes:
                _, code = client_mes.split()
                self.delete_flight(code)
                connection.sendall('DOK'.encode('utf-8'))
            else:
                connection.sendall('ERROR'.encode('utf-8'))


    def get_flight(self, code: int):
        '''
        Psaxnei sthn "vash" gia tin ptish pou zititai analoga me ton kwdiko pou dothike
        An den vrethei epistrefei None
        
        parametroi: code:int (O kwdikos tis pthshs)
        
        '''
        found_flight = None

        with self.lock:

            time.sleep(random.randrange(0, self.max_read_time))

            for flight in self.flights:
                if int(code) == flight['code']:
                    found_flight = flight
                    break

        return found_flight


    def add_flight(self, code, status, flight_time):
        '''
        Dexete ta dedomena mias neas pthshs kai prosthetei ena neo leksiko sthn lista
        
        parametroi: code:int 
                    status
                    flight_time
                    
        '''
        new_flight = {
            'code': int(code),
            'status': status,
            'time': flight_time
            }

        self.lock.acquire()

        time.sleep(random.randrange(0, self.max_write_time))
        self.flights.append(new_flight)

        self.lock.release()
        
    
    def modify_flight(self, code, new_status, new_time):
        '''
        
        Tropopioish mias pthshs pou hdh iparxei.
        Ean den vrethei h pthshl, epistrefei None
        
        parametroi: code:int
                    new_status
                    new_time
        
        '''
                
        with self.lock:    
            time.sleep(random.randrange(0, self.max_write_time))
            
            for flight in self.flights:
                if flight['code'] == int(code):
                    print('mpike')
                    flight['status'] = new_status
                    flight['time'] = new_time
                    return flight
                
        return None
    
    def delete_flight(self, code):
        '''
        Diagrafh mia pthshs apo thn 'vash'
        
        parametroi: code:int
        
        '''
        
        with self.lock:

            time.sleep(random.randrange(0, self.max_write_time))
            
            temp_list = [i for i in self.flights if not (i['code'] == int(code))]
            self.flights = temp_list

    def fetch_flights(self):
        return [
           {'code': 1, 'status': 'Departing', 'time': '12:35'},
           {'code': 2, 'status': 'Arriving', 'time': '11:55'},
           {'code': 3, 'status': 'Departing', 'time': '13:05'},
           {'code': 4, 'status': 'Arriving', 'time': '14:25'}
           ]


if __name__ == "__main__":
    SERVER = Server()
    SERVER.listen()
