import __init__
from __init__ import *
import serial
from time import sleep
import platform
import numpy as np
from Cloud.tcp_cloud_demo import *

def UpdateTempHumi(is_upload):

    if usr_platform == 'Windows':
        humi = 100.0 * np.random.rand()
        temp = 100.0 * np.random.rand()
    else:
        port = '/dev/ttyAMA1'
        sensor = TempHumiQuerySerial(port)
        temp, humi = sensor.get_beam_data()
        sensor.close_serial()
    if is_upload:
        pass

    temp = float(str(temp)[0:7])
    humi = float(str(humi)[0:7])

    return temp,humi

    pass

class TempHumiQuerySerial(object):
    """
    获取温湿传感器的值
    """
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(self.port, 4800, timeout=0.2)
        self.is_busy = False


    def get_beam_data(self, command='01 03 00 00 00 02 C4 0B'):
        """
        查询温湿度
        """

        if not self.is_busy:
            self.is_busy = True
            try:
                cmd = bytes.fromhex(command)  # 查询地址转换成byte类型
                self.ser.write(cmd)  # 将查询命令写入串口
                data = self.ser.read(9)  # 读取串口的返回值，具体的根据传感器的相关文档，填入数据长度
                #print(data)


                data = str(data.hex())
                if data[0:2] == '01' and data[2:4]=='03':  # 判断0c开头的才是光照度的返回值
                    humi = int('0x' + data[6:10], 16)  # 截取返回值的数据位，将16进制转成10进制的数值
                    temp = int('0x' + data[10:14], 16)
                    humi = humi * 1.0 /10
                    temp = temp * 1.0 /10
                    self.is_busy = False
                    return temp,humi
                else:
                    self.is_busy = False
                    return 0.0,0.0
            except Exception as e:
                print('data error: ' + str(e))
                return 0.0,0.0
        else:
            sleep(0.01)

    def close_serial(self):
        self.ser.close()




