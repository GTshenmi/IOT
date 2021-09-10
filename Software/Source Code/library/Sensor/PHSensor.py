import serial
from time import sleep
import platform
import numpy as np
from Cloud.tcp_cloud_demo import *

def UpdatePH(is_upload):

    PH =0.0
    if platform.system() == 'Windows':
        PH=14.0 * np.random.rand()
        #port = "COM3"
        #sensor = PHQuerySerial(port)
        #PH = sensor.get_beam_data()
        # if sensor.is_open:
        #     PH = sensor.get_beam_data()
        # else:
        #     PH = 100*np.random.random()
        #sensor.close_serial()

    else:
        port = '/dev/ttyAMA1'
        sensor = PHQuerySerial(port)
        PH = sensor.get_sensor_data()
        #PH = 0
        sensor.close_serial()


    if is_upload:
        pass

    PH = float(str(PH)[0:6])

    return PH


class PHQuerySerial(object):

    def __init__(self, port):
        self.port = port

        #self.ser = serial.Serial(self.port, 4800, timeout=0.2,stopbits=1,parity=serial.PARITY_NONE,bytesize=serial.EiGHTBITS)
        self.ser = serial.Serial(self.port, 4800, timeout=0.2)
        self.is_busy = False

    # def get_sensor_data(self, command='01 03 00 00 00 01 84 0A'):
    #
    #     if not self.is_busy:
    #         self.is_busy = True
    #         try:
    #             cmd = bytes.fromhex(command)  # 查询地址转换成byte类型
    #             self.ser.write(cmd)  # 将查询命令写入串口
    #             data = self.ser.read(7)  # 读取串口的返回值
    #
    #
    #
    #             data = str(data.hex())
    #
    #             if data[0:2] == '01' and data[2:4]=='03':
    #                 ph = int('0x' + data[6:10], 16)
    #
    #                 ph = ph * 1.0 /10.0
    #
    #                 self.is_busy = False
    #
    #                 return ph
    #             else:
    #                 self.is_busy = False
    #                 return None
    #         except Exception as e:
    #             print('data error: ' + str(e))
    #             return None
    #     else:
    #         sleep(0.01)


    #def get_beam_data(self, command='01 03 00 00 00 01 84 0A'):#02 C4 0B
    def get_sensor_data(self, command='01 03 00 00 00 02 C4 0B'):

        if not self.is_busy:
            self.is_busy = True
            try:
                cmd = bytes.fromhex(command)  # 查询地址转换成byte类型
                self.ser.write(cmd)  # 将查询命令写入串口
                data = self.ser.read(9)  # 读取串口的返回值，具体的根据传感器的相关文档，填入数据长度

                data = str(data.hex())

                if data[0:2] == '01' and data[2:4]=='03':  # 判断0c开头的才是光照度的返回值
                    ph = int('0x' + data[6:10], 16)  # 截取返回值的数据位，将16进制转成10进制的数值

                    ph = ph * 1.0 /10.0

                    self.is_busy = False
                    ph = 7
                    return ph

                else:
                    self.is_busy = False
                    return 0.0
            except Exception as e:
                print('data error: ' + str(e))
                return 0.0
        else:
            sleep(0.01)


    def close_serial(self):
        self.ser.close()




