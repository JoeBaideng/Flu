import socket
import xml.etree.ElementTree as ET

class ValveDevice:
    def __init__(self, name, ip, port):
        """
        初始化Modbus ASCII设备对象

        Args:
            name (str): 设备名称
            ip (str): 设备IP地址
            port (int): 设备端口号
        """
        self.name = name
        self.ip = ip
        self.port = port
        self.socket_client = None
        self.commands = {}
        self.report_commands = {}
