#模拟TCP接收设备
import socket
import threading
import logging

class TCPSimulatorDevice:
    def __init__(self, name, ip, port):
        """
        初始化TCP模拟设备对象

        Args:
            name (str): 设备名称
            ip (str): 设备IP地址
            port (int): 设备端口号
        """
        self.name = name
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.is_running = False

    def start(self):
        """
        启动TCP模拟设备，并开始监听连接
        """
        self.socket.listen(1)
        self.is_running = True
        logging.info(f"{self.name} started and listening on {self.ip}:{self.port}")

        while self.is_running:
            client_socket, client_address = self.socket.accept()
            logging.info(f"Connection established from {client_address}")
            thread = threading.Thread(target=self.handle_connection, args=(client_socket,))
            thread.start()

    def handle_connection(self, client_socket):
        """
        处理客户端连接

        Args:
            client_socket (socket.socket): 客户端套接字对象
        """
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            request = self.parse_request(data)
            logging.info(f"Received request: {request}")

            response = self.process_request(request)
            logging.info(f"Sending response: {response}")

            client_socket.sendall(response.encode())

        client_socket.close()
        logging.info("Connection closed")

    def parse_request(self, data):
        """
        解析请求数据

        Args:
            data (bytes): 请求数据

        Returns:
            解析后的请求对象
        """
        # 根据实际情况解析请求数据
        request = data.decode()
        return request

    def process_request(self, request):
        """
        处理请求并生成响应数据

        Args:
            request: 请求对象

        Returns:
            响应数据
        """
        # 根据实际情况处理请求，并生成响应数据
        response = f"Response to {request}"
        return response

    def stop(self):
        """
        停止TCP模拟设备
        """
        self.is_running = False
        self.socket.close()
        logging.info(f"{self.name} stopped")

# 设置日志输出级别和格式
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 创建TCPSimulatorDevice对象
device = TCPSimulatorDevice("Device1", "127.0.0.1", 502)

# 启动设备
device.start()
