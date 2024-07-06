from abc import ABC, abstractmethod
from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer
import socket

class SocketDevice():
    def __init__(self, name, ip, port, protocol='ASCII'):
        self.name = name
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.socket_client = None

    def connect(self):
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.connect((self.ip, self.port))
            print(f"Connected to {self.name} at {self.ip}:{self.port} using {self.protocol} protocol")
        except Exception as e:
            print(f"Failed to connect to {self.name} at {self.ip}:{self.port} using {self.protocol} protocol: {e}")

    def send_command(self, command):
        try:
            if self.protocol == 'ASCII':
                self.socket_client.sendall((command + '\r\n').encode('ascii'))
                print(f"ASCII Command sent: {command}")
            elif self.protocol == 'RTU':
                # Example: Modbus RTU command handling
                pass
            else:
                print(f"Unsupported protocol: {self.protocol}")
                return None

            response = self.socket_client.recv(1024).decode('ascii').strip()
            print(f"Response: {response}")
            return response
        except Exception as e:
            print(f"Error: {e}")
            return None

    def close(self):
        if self.socket_client:
            self.socket_client.close()
        print(f"Connection to {self.name} closed")
