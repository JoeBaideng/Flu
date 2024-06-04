from flask import Flask, request
from pymodbus.constants import Endian
from Device import ModbusDevice
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
app = Flask(__name__)

# 创建Modbus设备对象
device = ModbusDevice("Device1", "127.0.0.1", 502)

@app.route('/connect', methods=['POST'])
def connect_device():
    """
    连接到Modbus设备
    """
    device.connect()
    return 'Device connected'

@app.route('/send_request', methods=['POST'])
def send_modbus_request():
    """
    发送单个Modbus请求并返回响应
    """
    request_data = request.get_json()
    address = request_data.get("address")
    value = request_data.get("value")
    unit = request_data.get("unit")
    response = device.send_request([address, value, unit])
    return str(response)
@app.route('/send_requests', methods=['POST'])
def send_modbus_requests():
    """
    发送多个Modbus请求并返回响应
    """
    request_data = request.get_json()
    address = request_data.get("address")
    values = request_data.get("values")
    unit = request_data.get("unit")
    response = device.send_requests([address, values, unit])
    return str(response)


@app.route('/close', methods=['POST'])
def close_connection():
    """
    关闭与Modbus设备的连接
    """
    device.close()
    return 'Connection closed'



if __name__ == '__main__':
    app.run(debug=True)
