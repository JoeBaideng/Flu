from Device import RTUDevice
from Device import ASCIIDevice
import DeviceInfoParser as info_parser

# # 创建 TCP ASCII 设备实例
# ascii_device = ASCIIDevice("TCP_ASCII_Device", "192.168.0.80", 10123)
# ascii_device.connect()
# ascii_command = "/1ZR"  # 示例 ASCII 命令
# ascii_device.send_command(ascii_command)
# ascii_device.close()

# 创建 RTU 设备实例
rtu_device = RTUDevice("RTU_Device", "192.168.0.80", 10123)
rtu_device.connect()
rtu_command = [0, 40001, 1]  # 示例 RTU 命令
rtu_device.send_command(rtu_command)
rtu_device.close()
# modes=info_parser.parse_xml('configs/devices_programs.xml') #工作模式以及对应的设备参数
# print(modes[1].id)

# # 创建 ModbusDevice 实例
# device = RTUDevice("MyDevice", "192.168.0.80", 10123)
#
# # 连接到设备
# device.connect()
#
#
#
# request=[1,1,0]
# result = device.send_command(request)
# request=[1,25,2]
# result2 = device.send_command("01", "40001", "01")
# 检查结果
# if result:
#     print("Command sent successfully")
# else:
#     print("Failed to send command")

# 关闭连接





