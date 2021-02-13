import socket
import json
import time
import random
from threading import Thread



host = "117.78.1.201" #AIOT云平台tcp连接host地址
port = 8700           #AIOT云平台tcp连接port


def UploadTempHumi(temp,humi):

    AIOT = AIOT_Send_Data(host,port)



    AIOT.Send_Data('temphuimtest','c6512811db194d6b98a9a0c7fd965745',"Temp",float(temp))

    AIOT.Send_Data('temphuimtest', 'c6512811db194d6b98a9a0c7fd965745',"huim",float(humi))

    print ('done!')
    #AIOT.tcp_client.close()



    pass

class AIOT_Send_Data():
    def __init__(self,host,port):

        self.host = host
        self.port = port
        self.busy = False

    def Send_Data(self,device,key,datatype,data):

        if not self.busy:
            self.busy = True

            self.tcp_client = self.socket_client(self.host, self.port,device,key)  # 创建tcp　sockt 对象
            self.t1 = Thread(target=self.listen_server, args=(self.tcp_client,))  # 监听服务端发送数据
            self.t1.start()
            self.t2 = Thread(target=self.tcp_ping, args=(self.tcp_client,))  # 创建与云平台保持心跳的线程
            self.t2.start()


            data_to_send = {
                    "t": 3,                                      #固定数字,代表数据上报
                    "datatype": 1,                               #数据上报格式类型
                    "datas": {
                        datatype: data,
                    },
                    "msgid": str(random.randint(100,100000))     #消息编号
                    }
            try:
                self.tcp_client.send(json.dumps(data_to_send).encode())       #发送数据
            except Exception as e:
                print(e)

            #self.tcp_client.close()
            self.busy = False

        else:
            time.sleep(0.1)


    def socket_client(self,host,port,device,key):
        ''''
        创建TCP连接
        '''
        handshare_data = {
                "t": 1,                                    #固定数据代表连接请求
                "device": device,                          #设备标识
                "key": key, #传输密钥
                "ver": "v1.0"}                             #客户端代码版本号,可以是自己拟定的一组客户端代码版本号值
        try:
            tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建socket
            tcp_client.connect((host,port))                                #建立tcp连接
            tcp_client.send(json.dumps(handshare_data).encode())           #发送云平台连接请求
            res_msg = tcp_client.recv(1024).decode()                       #接收云平台响应
        except Exception as e:
            print(e)
            return False
        return tcp_client                                                  #返回socket对象


    def listen_server(self,socket_obj):
        '''
        监听TCP连接服务端消息
        :param socket_obj:
        :return:
        '''
        while True:
            try:
                res = socket_obj.recv(1024).decode() #接收服务端数据
                if not res:
                    exit()
            except Exception as e:
                print(e)
                exit()


    def tcp_ping(self,socket_obj):
        '''
        TCP连接心跳包
        :param socket_obj:
        :param obj:
        :return:
        '''
        while True:
            try:
                socket_obj.send("$#AT#".encode())   #发送心跳包数据
                time.sleep(30)
            except Exception as e:
                print(e)
                exit()




