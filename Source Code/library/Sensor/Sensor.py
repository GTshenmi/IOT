import serial
from serial import *
from time import sleep
import platform
import numpy as np
from Cloud.tcp_cloud_demo import *


class QuerySerial(object):

    def __init__(self,port,baud):
        self.port = port

        self.ser = serial.Serial(self.port, baud, timeout=0.2)

        self.is_busy = False

    def get_beam_data(self, command,datalen):

        if not self.is_busy:
            self.is_busy = True
            try:
                cmd = bytes.fromhex(command)  # 查询地址转换成byte类型
                self.ser.write(cmd)  # 将查询命令写入串口
                data = self.ser.read(7)  # 读取串口的返回值，具体的根据传感器的相关文档，填入数据长度

                data = str(data.hex())
                if data[0:2] == '02' and data[2:4] == '03':
                    PH = int('0x' + data[6:10], 16)  # 截取返回值的数据位，将16进制转成10进制的数值
                    self.is_busy = False
                    return PH / 10.0
                else:
                    self.is_busy = False
                    return None
            except Exception as e:
                print('data error: ' + str(e))
                return None
        else:
            sleep(0.01)

    def close_serial(self):
        self.ser.close()




