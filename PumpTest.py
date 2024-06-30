import serial
from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer


class ModbusDevice:
    def __init__(self, name, ip=None, port=None, protocol='rtu', serial_port=None, baudrate=9600):
        """
        初始化Modbus设备对象

        Args:
            name (str): 设备名称
            ip (str): 设备IP地址 (用于RTU/TCP协议)
            port (int): 设备端口号 (用于RTU/TCP协议)
            protocol (str): 协议类型，可以是 'rtu' 或 'ascii'
            serial_port (str): 串口号 (用于ASCII协议)
            baudrate (int): 串口波特率 (用于ASCII协议)
        """
        self.name = name
        self.ip = ip
        self.port = port
        self.protocol = protocol.lower()
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.client = None
        self.serial_client = None

        if self.protocol == 'ascii':
            if serial_port is None:
                raise ValueError("serial_port must be specified for ASCII protocol")
        else:
            if ip is None or port is None:
                raise ValueError("ip and port must be specified for RTU protocol")
            self.client = ModbusTcpClient(ip, port, framer=ModbusRtuFramer)

    def connect(self):
        """
        连接到Modbus设备
        """
        if self.protocol == 'ascii':
            try:
                self.serial_client = serial.Serial(self.serial_port, self.baudrate, timeout=1)
                print(f"Connected to {self.name} on serial port {self.serial_port} using ASCII protocol")
            except Exception as e:
                print(f"Failed to connect to {self.name} on serial port {self.serial_port} using ASCII protocol: {e}")
        else:
            connected = self.client.connect()
            if connected:
                print(f"Connected to {self.name} at {self.ip}:{self.port} using RTU protocol")
            else:
                print(f"Failed to connect to {self.name} at {self.ip}:{self.port}")

    def send_ascii_command(self, command):
        """
        发送ASCII类型的Modbus命令并返回响应

        Args:
            command (str): ASCII命令字符串

        Returns:
            响应结果
        """
        if self.protocol != 'ascii':
            print("Current protocol is not ASCII. Cannot send ASCII command.")
            return None

        try:
            self.serial_client.write((command + '\r\n').encode('ascii'))
            print(f"ASCII Command sent: {command}")
            response = self.serial_client.readline().decode('ascii').strip()
            print(f"Response: {response}")
            return response
        except Exception as e:
            print(f"Modbus ASCII Error: {e}")
            return None

    def send_request(self, request):
        """
        发送单个Modbus请求并返回响应

        Args:
            request: Modbus请求对象，格式为 [address, value, unit]

        Returns:
            响应结果
        """
        if self.protocol == 'ascii':
            print("ASCII protocol does not use send_request method.")
            return None

        address, value, unit = request
        try:
            write_response = self.client.write_register(address=address, value=value, unit=unit)
            print(f"Request sent: address={address}, value={value}, unit={unit}")
            print(f"Response: {write_response}")
            return write_response
        except Exception as e:
            print(f"Modbus RTU Error: {e}")
            return None

    def send_requests(self, requests):
        """
        发送多个Modbus请求并返回响应

        Args:
            request: Modbus请求对象，格式为 [address, values, unit]

        Returns:
            响应结果
        """
        if self.protocol == 'ascii':
            print("ASCII protocol does not use send_requests method.")
            return None

        address, values, unit = requests
        try:
            write_response = self.client.write_registers(address=address, values=values, unit=unit)
            print(f"Requests sent: address={address}, values={values}, unit={unit}")
            print(f"Response: {write_response}")
            return write_response
        except Exception as e:
            print(f"Modbus RTU Error: {e}")
            return None

    def close(self):
        """
        关闭与Modbus设备的连接
        """
        if self.protocol == 'ascii':
            if self.serial_client:
                self.serial_client.close()
        else:
            self.client.close()
        print(f"Connection to {self.name} closed")


# 示例代码
device = ModbusDevice("MyDevice", serial_port='COM1', baudrate=9600, protocol='ascii')
device.connect()

command = '/1A0R'
result = device.send_ascii_command(command)
print(result)

if result:
    print("Command sent successfully")
else:
    print("Failed to send command")

device.close()
