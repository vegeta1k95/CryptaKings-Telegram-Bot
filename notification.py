from threading import Thread
from time import sleep
import socket
import pickle
import struct

class SocketError(Exception):
    pass

class CustomClientSocket:
    SERVER_IP = socket.gethostname()
    SERVER_PORT = 994
    def __init__(self, func, **kwargs):
        self._read_thread = Thread(target=self._reader, args=(func,), kwargs=kwargs)
        self._connected = False

    def _receive_message(self):
        encoded_length = self._sock.recv(4)
        if len(encoded_length) == 0:
            raise SocketError
        length = struct.unpack('>I', encoded_length)[0]
        pickled_obj = self._sock.recv(length)
        return pickle.loads(pickled_obj)
        
    def _reader(self, func, **kwargs):
        print('Socket reading started...')
        if not self._connected:
            self._connect()
        while True:
            try:
                data = self._receive_message()
            except ConnectionResetError:
                print('Server has dropped connection!')
                self._connected = False
                self._connect()
            except ConnectionAbortedError:
                print('Server has aborted connection!')
                self._connected = False
                self._connect()
            except SocketError:
                print('SocketError')
                self._reconnect()
            else:
                if data:
                    func(data, *kwargs)

    def _disconnect(self):
        if self._connected:
            self._sock.close()
            self._connected = False

    def _reconnect(self):
        self._disconnect()
        self._connect()
    
    def _connect(self):
        while True:
            try:
                self._sock = socket.socket()
                self._sock.connect((self.SERVER_IP, self.SERVER_PORT))
            except ConnectionRefusedError:
                print('Connection to server cannot be established. Retry in 30 seconds.')
                sleep(30)
            else:
                self._connected = True
                break
        
    def start(self):
        self._read_thread.start()
        
    def set_server(self, ip, port):
        self.SERVER_IP = ip
        self.SERVER_PORT = port

class CustomServerSocket:
    SERVER_IP = socket.gethostname()
    SERVER_PORT = 994
    def __init__(self):
        self._sock = socket.socket()
        self._sock.bind((self.SERVER_IP, self.SERVER_PORT))
        self._sock.listen(5)

        self._connections = []
        Thread(target=self._write).start()

    @staticmethod
    def _create_message(obj):
        pickled_obj = pickle.dumps(obj)
        data_length = len(pickled_obj)
        encoded_length = struct.pack('>I', data_length)

        return encoded_length + pickled_obj
        
    def _write(self):
        conn, addr = self._sock.accept()

        msg = self._create_message({'suka':'pidor'})
        
        for _ in range(100):
            conn.sendall(msg)

        #conn.shutdown(socket.SHUT_RDWR)
        conn.close()
