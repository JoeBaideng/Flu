
from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian

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
        self.client.connect()

    #request=[1,25,2]
    def send_request(self, request):
        """
        发送单个Modbus请求并返回响应

        Args:
            request: Modbus请求对象，格式为 [address, value, unit]

        Returns:
            响应结果
        """
        address, value, unit = request
        write_response = self.client.write_register(address=address, value=value, unit=unit)
        return write_response

    #requests = [1, [25,12,30,48], 2]
    def send_requests(self, requests):
        """
        发送单个Modbus请求并返回响应

        Args:
            request: Modbus请求对象，格式为 [address, value, unit]

        Returns:
            响应结果
        """
        address, values, unit = requests
        write_response = self.client.write_registers(address=address, values=values, unit=unit)
        return write_response




    def close(self):
        """
        关闭与Modbus设备的连接
        """
        self.client.close()
