import socket


def connect_to_device(ip, port):
    """
    连接到设备

    Args:
        ip (str): 设备IP地址
        port (int): 设备端口号

    Returns:
        socket: 连接后的socket对象
    """
    try:
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_client.connect((ip, port))
        print(f"Connected to device at {ip}:{port}")
        return socket_client
    except Exception as e:
        print(f"Failed to connect to device at {ip}:{port}: {e}")
        return None


def send_modbus_command(socket_client, command):
    """
    发送Modbus命令并返回响应

    Args:
        socket_client (socket): 连接的socket对象
        command (str): Modbus命令字符串（16进制）

    Returns:
        响应结果
    """
    try:
        spaced_command = ' '.join([command[i:i + 2] for i in range(0, len(command), 2)])
        socket_client.sendall(bytes.fromhex(command))
        print(f"Modbus Command sent: {spaced_command}")
        response = socket_client.recv(1024)
        print(f"Raw response: {response}")
        response_hex = response.hex()
        print(f"Decoded response: {response_hex}")
        return response_hex
    except Exception as e:
        print(f"Modbus Error: {e}")
        return None


def main():
    ip = "192.168.0.80"  # 修改为你的设备IP地址
    port = 10123  # 修改为你的设备端口号

    # 16进制命令
    command = "01 05 00 00 00 00 CD CA"

    # 连接到设备
    socket_client = connect_to_device(ip, port)
    if socket_client:
        # 发送命令并获取响应
        response = send_modbus_command(socket_client, command)

        # 关闭连接
        socket_client.close()
        print("Connection closed")


if __name__ == "__main__":
    main()
