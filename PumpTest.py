import socket
import xml.etree.ElementTree as ET


class ModbusASCIIDevice:
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
            ascii_code = cmd.find('ascii').text
            if cmd.find('type').text == 'report':
                self.report_commands[name] = ascii_code
            else:
                self.commands[name] = ascii_code

    def connect(self):
        """
        连接到Modbus ASCII设备
        """
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.connect((self.ip, self.port))
            print(f"Connected to {self.name} at {self.ip}:{self.port} using ASCII protocol")
        except Exception as e:
            print(f"Failed to connect to {self.name} at {self.ip}:{self.port} using ASCII protocol: {e}")

    def send_ascii_command(self, command):
        """
        发送ASCII类型的Modbus命令并返回响应

        Args:
            command (str): ASCII命令字符串

        Returns:
            响应结果
        """
        try:
            self.socket_client.sendall((command + '\r\n').encode('ascii'))
            print(f"ASCII Command sent: {command}")
            response = self.socket_client.recv(1024)
            print(f"Raw response: {response}")
            response = response.decode('ascii', errors='ignore').strip()
            print(f"Decoded response: {response}")
            return response
        except Exception as e:
            print(f"Modbus ASCII Error: {e}")
            return None

    def close(self):
        """
        关闭与Modbus ASCII设备的连接
        """
        if self.socket_client:
            self.socket_client.close()
        print(f"Connection to {self.name} closed")

    def generate_command(self, command_name, param=None):
        """
        根据命令名称和参数生成ASCII命令

        Args:
            command_name (str): 命令名称
            param (str): 命令参数

        Returns:
            str: 生成的ASCII命令
        """
        if command_name in self.commands:
            ascii_code = self.commands[command_name]
        elif command_name in self.report_commands:
            ascii_code = self.report_commands[command_name]
        else:
            print(f"Command '{command_name}' not found.")
            return None

        if param is None:
            return f"/1{ascii_code}R"
        else:
            return f"/1{ascii_code}{param}R"

    def execute(self, command_name, param=None):
        """
        根据命令名称和参数生成并发送ASCII命令

        Args:
            command_name (str): 命令名称
            param (str): 命令参数

        Returns:
            响应结果
        """
        command = self.generate_command(command_name, param)
        if command:
            return self.send_ascii_command(command)

    def parse_response(self, response):
        """
        解析返回的ASCII响应数据

        Args:
            response (str): ASCII响应数据

        Returns:
            dict: 解析后的数据字典
        """
        if response.startswith('/0`'):
            data_value = response[3:-1]
            return {"value": int(data_value)}

        print(f"Unknown response format: {response}")
        return None

    def handle_report_command(self, command_name):
        """
        处理报告命令，解析返回的数据并输出报告内容

        Args:
            command_name (str): 命令名称

        Returns:
            int or None: 解析后的数值，如果解析失败返回 None
        """
        response = self.execute(command_name)
        if response:
            parsed_data = self.parse_response(response)
            if parsed_data and 'value' in parsed_data:
                if command_name == 'query_position_command':
                    print(f"Position Report: {parsed_data['value']}")
                elif command_name == 'query_speed_command':
                    print(f"Speed Report: {parsed_data['value']}")
                else:
                    print(f"Unknown report command: {command_name}")
                return parsed_data['value']
            else:
                print(f"Failed to parse response for {command_name}")
        else:
            print(f"No response for {command_name}")

        return None


def main():
    # 初始化设备
    device = ModbusASCIIDevice("MyDevice", ip='192.168.0.80', port=10123)
    device.connect()

    # 加载命令
    device.load_commands_from_xml('configs/ascii_commands.xml')

    # 执行命令并获取响应
    response = device.execute("suck_command", param=3000)
    print(f"Response: {response}")

    # device.handle_report_command("query_position_command")
    # device.handle_report_command("query_speed_command")

    device.close()


if __name__ == "__main__":
    main()
