import socket
import xml.etree.ElementTree as ET

class ValveDevice:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.socket_client = None
        self.commands = {}
        self.report_commands = {}

    def load_commands_from_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for cmd in root.findall('command'):
            name = cmd.find('name').text
            function_code = cmd.find('function_code').text
            if cmd.find('type').text == 'report':
                self.report_commands[name] = function_code
            else:
                self.commands[name] = function_code

    def connect(self):
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.connect((self.ip, self.port))
            print(f"Connected to {self.name} at {self.ip}:{self.port} using HEX protocol")
        except Exception as e:
            print(f"Failed to connect to {self.name} at {self.ip}:{self.port} using HEX protocol: {e}")

    def send_hex_command(self, command):
        try:
            self.socket_client.sendall(bytes.fromhex(command))
            print(f"HEX Command sent: {command}")
            response = self.socket_client.recv(1024)
            print(f"Raw response: {response}")
            response = response.hex().upper()
            print(f"Hex response: {response}")
            return response
        except Exception as e:
            print(f"Modbus HEX Error: {e}")
            return None

    def close(self):
        if self.socket_client:
            self.socket_client.close()
        print(f"Connection to {self.name} closed")

    def generate_command(self, command_name, param=None):
        if command_name in self.commands:
            function_code = self.commands[command_name]
        elif command_name in self.report_commands:
            function_code = self.report_commands[command_name]
        else:
            print(f"Command '{command_name}' not found.")
            return None

        address = '00'
        fixed_part = 'DD'
        if param is None:
            command = f"CC {address} {function_code} 00 00 {fixed_part}"
        else:
            command = f"CC {address} {function_code} {param:02X} 00 {fixed_part}"

        checksum = self.calculate_checksum(command)
        command = f"{command} {checksum} 01"
        return command

    def calculate_checksum(self, command):
        # 将命令字符串按空格拆分成字节列表
        bytes_list = [int(byte, 16) for byte in command.split()]
        # 计算字节列表的和
        checksum = sum(bytes_list) & 0xFF
        return f"{checksum:02X}"

    def execute(self, command_name, param=None):
        command = self.generate_command(command_name, param)
        if command:
            return self.send_hex_command(command)

    def parse_response(self, response, command_name):
        # 将无空格的响应值转换为带空格的形式
        response_with_spaces = ' '.join(response[i:i + 2] for i in range(0, len(response), 2))

        if response_with_spaces.startswith('CC'):
            parts = response_with_spaces.split()
            if command_name == 'query_position':
                data_value = parts[2]
                return {"position": int(data_value, 16)}
            elif command_name == 'query_current_pass':
                data_value = parts[3]
                return {"current_pass": int(data_value, 16)}
        print(f"Unknown response format: {response_with_spaces}")
        return None

    def handle_report_command(self, command_name):
        response = self.execute(command_name)
        if response:
            parsed_data = self.parse_response(response, command_name)
            if parsed_data:
                if command_name == 'query_position':
                    print(f"Position Report: {parsed_data['position']}")
                elif command_name == 'query_current_pass':
                    print(f"Current Pass Report: {parsed_data['current_pass']}")
                return parsed_data
            else:
                print(f"Failed to parse response for {command_name}")
        else:
            print(f"No response for {command_name}")
        return None

def main():
    device = ValveDevice("MyDevice", ip='192.168.0.80', port=10123)
    device.connect()
    device.load_commands_from_xml('configs/valve_commands.xml')

    # 示例: 切换阀门到2号口
    response = device.execute("valve_switch", param=5)
    print(f"Response: {response}")

    # 示例: 查询地址
    position = device.handle_report_command("query_position")
    print(f"Current Position: {position}")

    # 示例: 查询当前通道
    current_pass = device.handle_report_command("query_current_pass")
    print(f"Current Pass: {current_pass}")

    device.close()

if __name__ == "__main__":
    main()
