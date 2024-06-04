#针对非标准设备的解决办法
def send_custom_requests(requests):
    """
    向非标准Modbus设备发送自定义请求，并返回解码后的响应

    Args:
        requests (list): 包含多个请求的列表，每个请求包含从机ID、功能码和参数的元组

    Returns:
        解码后的响应结果列表
    """
    modbus_requests = []
    for command in requests:
        slave_id, func_code, parameters = command
        frame = build_custom_frame(slave_id, func_code, parameters)
        modbus_requests.append(frame)

    encoded_requests = [frame.encode() for frame in modbus_requests]
    encoded_responses = self.client.socket.send(encoded_requests)
    decoded_responses = [decode_custom_response(response) for response in encoded_responses]
    return decoded_responses

def build_custom_frame(slave_id, func_code, parameters):
    """
    构建非标准Modbus请求帧

    Args:
        slave_id (int): 从机ID
        func_code (int): 功能码
        parameters (bytes): 参数字节序列

    Returns:
        构建的请求帧
    """
    frame_header = bytes([0xCC])  # 帧头
    address = bytes([slave_id])  # 从机地址
    func = bytes([func_code])  # 功能码
    frame_tail = bytes([0xDD])  # 帧尾
    checksum = calculate_checksum(frame_header + address + func + parameters + frame_tail)  # 校验和

    frame = frame_header + address + func + parameters + frame_tail + checksum
    return frame

def calculate_checksum(data):
    """
    计算校验和

    Args:
        data (bytes): 数据字节序列

    Returns:
        校验和结果（2字节，低字节在前，高字节在后）
    """
    checksum = sum(data)  # 累加和校验
    low_byte = checksum & 0xFF
    high_byte = (checksum >> 8) & 0xFF
    return bytes([low_byte, high_byte])

def decode_custom_response(response):
    """
    解码非标准Modbus响应

    Args:
        response (bytes): 响应字节序列

    Returns:
        解码后的响应结果
    """
    # 解析响应逻辑
    return decoded_response
