import socket
import xml.etree.ElementTree as ET
import time
class PeristalticPump:
    def __init__(self, name, ip, port):
        """
        初始化Modbus蠕动泵对象

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

    def load_commands_from_xml(self, file_path):
        """
        从XML文件中加载命令

        Args:
            file_path (str): XML文件路径
        """
        tree = ET.parse(file_path)
        root = tree.getroot()

        for cmd in root.findall('command'):
            name = cmd.find('name').text
            register_address = cmd.find('register_address').text
            function_code = cmd.find('function_code').text
            self.commands[name] = (register_address, function_code)

    def connect(self):
        """
        连接到Modbus设备
        """
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.connect((self.ip, self.port))
            print(f"Connected to {self.name} at {self.ip}:{self.port} using Modbus protocol")
        except Exception as e:
            print(f"Failed to connect to {self.name} at {self.ip}:{self.port} using Modbus protocol: {e}")

    def send_modbus_command(self, command):
        """
        发送Modbus命令并返回响应

        Args:
            command (str): Modbus命令字符串

        Returns:
            响应结果
        """
        try:
            spaced_command = ' '.join([command[i:i+2] for i in range(0, len(command), 2)])
            self.socket_client.sendall(bytes.fromhex(command))
            print(f"Modbus Command sent: {spaced_command}")
            response = self.socket_client.recv(1024)
            print(f"Raw response: {response}")
            response_hex = response.hex()
            print(f"Decoded response: {response_hex}")
            return response_hex
        except Exception as e:
            print(f"Modbus Error: {e}")
            return None

    def close(self):
        """
        关闭与Modbus设备的连接
        """
        if self.socket_client:
            self.socket_client.close()
        print(f"Connection to {self.name} closed")

    def generate_modbus_command(self, slave_address, function_code, register_address, data):
        """
        生成Modbus命令

        Args:
            slave_address (str): 从机地址
            function_code (str): 功能码
            register_address (str): 寄存器地址
            data (str): 数据

        Returns:
            str: 生成的Modbus命令
        """
        command = f"{slave_address}{function_code}{register_address}{data}"
        crc = self.calculate_crc(command)
        return f"{command}{crc}"

    def calculate_crc(self, command):
        """
        计算CRC校验码

        Args:
            command (str): Modbus命令

        Returns:
            str: 计算的CRC校验码
        """
        data = bytes.fromhex(command)
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for _ in range(8):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return f"{crc & 0xFF:02X}{(crc >> 8) & 0xFF:02X}"

    def execute(self, slave_address, command_name, param=None):
        """
        根据命令名称和参数生成并发送Modbus命令

        Args:
            slave_address (str): 从机地址
            command_name (str): 命令名称
            param (str): 命令参数

        Returns:
            响应结果
        """
        if command_name in self.commands:
            register_address, function_code = self.commands[command_name]
            data = f"{int(param):04X}" if param is not None else '0001'
            command = self.generate_modbus_command(slave_address, function_code, register_address, data)
            return self.send_modbus_command(command)
        else:
            print(f"Command '{command_name}' not found.")
            return None

# 示例使用
if __name__ == "__main__":
    pump = PeristalticPump("Peristaltic Pump", "192.168.0.80", 10123)
    pump.load_commands_from_xml("configs/modbus_pump_commands.xml")
    pump.connect()

    # 执行命令示例
    # eValve.execute('01', 'set_rotation', '01')
    pump.execute('08', 'set_run', '01')
    time.sleep(5)
    pump.execute('08', 'set_run', '00')
    # eValve.execute('01', 'set_run', '01')
    pump.execute('08', 'set_speed', '120')
    pump.execute('08', 'query_speed')
    pump.execute('08','set_stop')#停止命令
    pump.close()
