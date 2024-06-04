from Device import ModbusDevice
import DeviceInfoParser as info_parser



# modes=info_parser.parse_xml('configs/devices_programs.xml') #工作模式以及对应的设备参数
# print(modes[1].id)

# 创建 ModbusDevice 实例
device = ModbusDevice("MyDevice", "192.168.1.100", 502)

# 连接到设备
device.connect()



request=[1,40001,1]
result = device.send_request(request)
# request=[1,25,2]
# result2 = device.send_command("01", "40001", "01")

# 检查结果
if result:
    print("Command sent successfully")
else:
    print("Failed to send command")

# 关闭连接
device.close()




