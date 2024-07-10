import socket
import time
class ElectricValve:
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

    def close(self):
        """
        关闭与Modbus设备的连接
        """
        if self.socket_client:
            self.socket_client.close()
        print(f"Connection to {self.name} closed")

    def send_modbus_command(self, command):
        """
        发送Modbus命令并返回响应

        Args:
            command (str): Modbus命令字符串

        Returns:
            响应结果
        """
        try:
            spaced_command = ' '.join([command[i:i + 2] for i in range(0, len(command), 2)])
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

    def execute(self, valve_indices, param):
        """
        根据命令名称和参数生成并发送Modbus命令

        Args:
            valve_indices (list): 电磁阀序号列表
            param (str): 命令参数 ('1' 或 '0')

        Returns:
            响应结果列表
        """
        slave_address = "01"
        function_code = "05"
        param_value = 'FF00' if param == '1' else '0000'
        register_address_base = "0000"
        results = []

        for valve_index in valve_indices:
            address_hex = f"{int(register_address_base, 16) + valve_index:04X}"
            command = self.generate_modbus_command(slave_address, function_code, address_hex, param_value)
            result = self.send_modbus_command(command)
            results.append(result)
            time.sleep(0.05)

        return results

    def get_valve_status(self):
        """
        获取所有阀门的开关状态

        Returns:
            str: 阀门状态的二进制字符串
        """
        command = "010100000020"
        command = self.generate_modbus_command(command[:2], command[2:4], command[4:8], command[8:])
        response = self.send_modbus_command(command)

        if response:
            # Remove the first 6 characters (address, function code, and byte count) and last 4 characters (CRC)
            data = response[6:-4]
            binary_status = ''.join(
                [bin(int(byte, 16))[2:].zfill(8) for byte in [data[i:i + 2] for i in range(0, len(data), 2)]])
            return binary_status
        else:
            return None

# 注意，这章代码由于数据内容少，没有使用xml储存数据
if __name__ == "__main__":
    eValve = ElectricValve("ElectricValve", "192.168.0.80", 10123)
    eValve.connect()

    # 执行命令示例
    eValve.execute(list(range(32)), '0')  # 打开电磁阀0-13
    valve_status = eValve.get_valve_status()  # 获取所有阀门的开关状态,是一串二进制数，比如11111111001111110000000000000000
    print(f"Valve Status: {valve_status}")  # 打印阀门状态
    eValve.close()
