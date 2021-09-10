from gpio4 import SysfsGPIO
from time import sleep
DHT11PIN = 43

class DHT11Driver():
    def __init__(self):
        self.DHT11_Init()

    def DHT11_Init(self):
        self.DHT11_GPIOInit()
        self.DHT11_Reset()

    def DHT11_GPIOInit(self):
        self.pin = SysfsGPIO(DHT11PIN)
        self.pin.export = True
        self.pin.direction = 'out'

    def DHT11_Reset(self):
        self.pin.direction='out'
        self.pin.value=0
        sleep(0.02)
        self.pin.value=1
        sleep(0.00003)

    def DHT11_GetAck(self):
        retry = 0
        self.pin.direction='in'
        while self.pin.value and retry<100:
            retry+=1
            sleep(0.000001)
        if retry>100:
            return 'can not get dht11 ack'
        retry=0
        while not self.pin.value and retry < 100:
            retry+=1
            sleep(0.000001)
        if retry>100:
            return 'can not get dht11 ack'
        else:
            return 'get dht11 ack success'


    def DHT11_GetTemp(self):
        ret,temp,humi = self.DHT11_ReadData()
        if ret != 'fail':
            return temp
        else:
            return 'null'

    def DHT11_GetHumi(self):
        ret,temp,humi = self.DHT11_ReadData()
        if ret != 'fail':
            return humi
        else:
            return 'null'

    def DHT11_ReadBit(self):
        retry = 0
        while (self.pin.value and (retry < 100)):
            retry+=1
            sleep(0.000001)
            retry = 0

        while (not self.pin.value and (retry < 100)):
            retry+=1
            sleep(0.000001)

        sleep(0.00004)

        if self.pin.value:
            return 1
        else:
            return 0

    def DHT11_ReadByte(self):
        self.data=0
        for i in range(8):
            self.data <<= 1
            self.data |= self.DHT11_ReadBit()
        return self.data

    def DHT11_ReadData(self):
        self.state = ''
        self.DHT11_Init()
        self.buff= []
        for retry in range(5):
            if self.DHT11_GetAck() == 'get dht11 ack success':
                for i in range(5):
                    self.buff.append(self.DHT11_ReadByte())
                break
            else:
                if retry>=5:
                    self.state = 'fail'
                retry+=1
        if self.buff[0]+self.buff[1]+self.buff[5]+self.buff[3] == self.buff[4]:
            decimal=(self.buff[1]&0x0f)
            decimal *= 0.00390625
            self.buff[1] >>= 4
            decimal += (self.buff[1] & 0x0f) * 0.0625
            self.humi = self.buff[0] + decimal
            decimal = (self.buff[3] & 0x0f)
            decimal *= 0.00390625
            self.buff[3] >>= 4
            decimal += (self.buff[3] & 0x0f) * 0.0625
            self.temp = self.buff[2] + decimal
            self.state = 'success'

        return self.state,self.temp,self.humi




