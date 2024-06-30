from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer

class ModbusDevice:
    def __init__(self, name, ip, port):
        """
        初始化Modbus设备对象

        Args:
            name (str): 设备名称
            ip (str): 设备IP地址
            port (int): 设备端口号
        """
        self.name = name
        self.ip = ip
        self.port = port
        self.client = ModbusTcpClient(ip, port, framer=ModbusRtuFramer)

    def connect(self):
        """
        连接到Modbus设备
        """
        connected = self.client.connect()
        if connected:
            print(f"Connected to {self.name} at {self.ip}:{self.port}")
        else:
            print(f"Failed to connect to {self.name} at {self.ip}:{self.port}")

    def send_request(self, request):
        """
        发送单个Modbus请求并返回响应

        Args:
            request: Modbus请求对象，格式为 [address, value, unit]

        Returns:
            响应结果
        """
        address, value, unit = request
        try:
            write_response = self.client.write_register(address=address, value=value, unit=unit)
            print(f"Request sent: address={address}, value={value}, unit={unit}")
            print(f"Response: {write_response}")
            return write_response
        except Exception as e:
            print(f"Modbus Error: {e}")
            return None

    def send_requests(self, requests):
        """
        发送单个Modbus请求并返回响应

        Args:
            request: Modbus请求对象，格式为 [address, values, unit]

        Returns:
            响应结果
        """
        address, values, unit = requests
        try:
            write_response = self.client.write_registers(address=address, values=values, unit=unit)
            print(f"Request sent: address={address}, values={values}, unit={unit}")
            print(f"Response: {write_response}")
            return write_response
        except Exception as e:
            print(f"Modbus Error: {e}")
            return None

    def close(self):
        """
        关闭与Modbus设备的连接
        """
        self.client.close()
        print(f"Connection to {self.name} closed")