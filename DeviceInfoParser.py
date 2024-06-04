# 用于读取xml文件，解析xml文件中的数据，返回一个Mode列表
import xml.etree.ElementTree as ET

# 用于储存从xml中读取的设备和程序信息
class Mode:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.DeviceGroups = []
        self.Programs = []

class Device:
    def __init__(self, id, name, slave_id, address=None):
        self.id = id
        self.name = name
        self.slave_id = slave_id
        self.address = address

class DeviceGroup:
    def __init__(self, id):
        self.id = id
        self.devices = []

class Program:
    def __init__(self, id, name=None):
        self.id = id
        self.name = name
        self.actions = []
class Action:
    def __init__(self, name, device_id, value=None, address=None):
        self.name = name
        self.device_id = device_id
        self.value = value
        self.address = address



def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    modes = []

    for mode_elem in root.findall('mode'):
        mode_id = mode_elem.get('id')
        mode_name = mode_elem.get('name')

        mode = Mode(mode_id, mode_name)

        for group_elem in mode_elem.findall('device_groups/group'):
            group_id = group_elem.get('id')
            device_group = DeviceGroup(group_id)

            for device_elem in group_elem.findall('device'):
                device_id = device_elem.get('id')
                device_name = device_elem.get('name')
                slave_id = device_elem.get('slave_id')
                address = device_elem.get('address')

                device = Device(device_id, device_name, slave_id, address)
                device_group.devices.append(device)

            mode.DeviceGroups.append(device_group)

        for program_elem in mode_elem.findall('programs/program'):
            program_id = program_elem.get('id')
            program_name = program_elem.get('name')
            program = Program(program_id, program_name)

            for action_elem in program_elem.findall('action'):
                action_name = action_elem.get('name')
                device_id = action_elem.get('device_id')
                value = action_elem.get('value')
                address = action_elem.get('address')

                action = Action(action_name, device_id, value, address)
                program.actions.append(action)

            mode.Programs.append(program)

        modes.append(mode)

    return modes

# modes = parse_xml('MYGUI/programs.xml')
# print(modes[0].id)
# print(modes[0].name)
# print(modes[0].DeviceGroups[0].id)