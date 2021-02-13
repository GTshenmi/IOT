import serial
from time import sleep
import platform
import numpy as np
from Cloud.tcp_cloud_demo import *

def UpdateLight(is_upload):

    if platform.system() == 'Windows':
        humi = 100.0 * np.random.rand()
        temp = 100.0 * np.random.rand()
    else:
        port = '/dev/ttyAMA1'
        sensor = QuerySerial(port)
        temp, humi = sensor.get_beam_data()
        sensor.close_serial()
    if is_upload:
        UploadTempHumi(temp,humi)



    return temp,humi

    pass

class QuerySerial(object):
    """
    获取温湿传感器的值
    """
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(self.port, 9600, timeout=0.2)
        self.is_busy = False

    def get_beam_data(self, command='01 03 00 07 00 02 75 CA'):
        """

        查询温湿度
        """
        if not self.is_busy:
            self.is_busy = True
            try:
                cmd = bytes.fromhex(command)  # 查询地址转换成byte类型
                self.ser.write(cmd)  # 将查询命令写入串口
                data = self.ser.read(9)  # 读取串口的返回值，具体的根据传感器的相关文档，填入数据长度

                data = str(data.hex())
                if data[0:2] == '01' and data[2:4]=='03':  # 判断0c开头的才是光照度的返回值
                    light = int('0x' + data[6:14], 16)  # 截取返回值的数据位，将16进制转成10进制的数值
                    self.is_busy = False
                    return light
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




