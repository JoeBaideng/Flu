import socket
import serial
import threading

# 使得能够通过串口向网口发送信息
class SerialServer:
    def __init__(self, host, port, serial_port, baudrate):
        self.host = host
        self.port = port
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.server = None
        self.serial_conn = None

    def handle_client(self, client_socket):
        """
        处理来自网络客户端的连接，将数据转发到串口并将串口的响应发送回客户端
        """
        try:
            while True:
                # 从网络读取数据
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received from network: {data}")

                # 发送数据到串口
                self.serial_conn.write(data)

                # 从串口读取响应
                response = self.serial_conn.readline()
                print(f"Received from serial: {response}")

                # 发送响应到网络客户端
                client_socket.sendall(response)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    def start(self):
        # 初始化串口
        self.serial_conn = serial.Serial(self.serial_port, self.baudrate, timeout=1)

        # 创建网络监听套接字
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Listening on {self.host}:{self.port}")

        try:
            while True:
                # 接受来自客户端的连接
                client_socket, addr = self.server.accept()
                print(f"Accepted connection from {addr}")

                # 启动新线程处理客户端连接
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
        except KeyboardInterrupt:
            print("Shutting down server.")
        finally:
            self.server.close()
            self.serial_conn.close()


def start_serial_server(host, port, serial_port, baudrate):
    server = SerialServer(host, port, serial_port, baudrate)
    server.start()
