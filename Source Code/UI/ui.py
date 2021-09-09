import __init__
from __init__ import  *
import os
import numpy as np
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5 import QtGui, QtCore
from UI.designer.mainwindow import Ui_MainWindow
from UI.designer.videowindow import Ui_VideoWindow
from UI.designer.photowindow import Ui_PhotoWindow
from app import ThreadCap,ThreadIde,ThreadUpdateTime,ThreadUpdateChart,ThreadUpdatPhoto,get_wheather,ThreadUpdateEnvironmentalParameters
import datetime
import platform
from UI.designer.chartwindow import *
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import *
from UI.designer.wheatherwindow import *
from multiprocessing import Process
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure


def setButtonStyle(object, path):

    pixmap = QPixmap(QImage(path))

    fixpixmap = pixmap.scaled(635, 360, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)

    icon = QIcon(fixpixmap)

    object.setIcon(icon)
    object.setIconSize(QSize(435, 360))

    object.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                            "QPushButton:hover{color:rgb(100,100,100,120);}")


def SetButtonIcon(object,path,width,hight):
        #拍照按钮
    pixmap = QPixmap(QImage(path))

    fixpixmap = pixmap.scaled(width, hight, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)

    icon = QIcon(fixpixmap)

    object.setIcon(icon)

    object.setIconSize(QSize(width, hight))

    object.setFlat(True)

    object.setStyleSheet("border:none")

class MainWindows(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super(MainWindows, self).__init__(None)

        self.humi = 0.0
        self.temp = 0.0
        self.time = ''


        # 设置UI
        self.setupUi(self)

        self.UpdateUi()

        # Button
        self.SetButtonConnected()

        self.SetLabelStyle()

        # 新的线程 更新时间
        self.InitThread()

        if SUPPORT_AIOT_BOARD:

            if usr_platform != 'Windows':
                try:
                    cmd_ip_eth0 = "ip addr show 'eth0'| grep 'inet '| awk '{print $2}'"
                    eth0_content = subprocess.getstatusoutput(cmd_ip_eth0)
                    if eth0_content[0] == 0:
                        if eth0_content[1] != '':
                            ip_content = eth0_content[1].split('/')
                            dev_ip = ip_content[0]
                            self.ShowIPLabel.setText(f'当前ip：\n{dev_ip}')
                        else:
                            self.ShowIPLabel.setText(f'当前ip：\n无')
                    else:
                        self.ShowIPLabel.setText(f'当前ip：\n无')
                except Exception as e:
                    if DEBUG == ON:
                        print(e)
                    self.ShowIPLabel.setText(f'当前ip：\n无')


    def InitThread(self):

        self.frameID = 0

        self.wthread3 = ThreadUpdateTime(self)
        self.wthread3.updatetime.connect(self.UpdateTime)
        self.wthread3.start()

        self.wthread = ThreadUpdateEnvironmentalParameters()
        self.wthread.start()

    def UpdateTime(self):

        self.time = str(datetime.datetime.now())
        self.dateLable.setText('\t' + self.time[0:19]+'\t\t\t\t')

    def SetLabelStyle(self):

        self.dateLable.setStyleSheet("QLabel{background:rgb(255,255,255,100)}")

        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        self.dateLable.setFont(font)

        self.School.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                          "QPushButton:hover{color:rgb(100,100,100,120);}")

    def SetButtonConnected(self):

        self.showchartbutton.pressed.connect(self.ShowChartButtonPressed)
        self.showlocationbutton.pressed.connect(self.ShowLocationButtonPressed)
        self.showvirusbutton.pressed.connect(self.ShowVirusButtonPressed)
        self.showperiodbutton.pressed.connect(self.ShowPeriodButtonPressed)
        self.showpestsbutton.pressed.connect(self.ShowPestsButtonPressed)
        self.exitbutton.pressed.connect(self.ExitButtonPressed)

    def UpdateUi(self):

        #设置背景图片
        self.setStyleSheet("#MainWindow{border-image:url(UI/images/backgroundpic.png);}")

        self.backgroundlable.setPixmap(QPixmap("UI/images/backgroundpic.png"))
        self.backgroundlable.setScaledContents(True)

        setButtonStyle(self.showchartbutton,"UI/images/icon/chart.png")

        self.SetWheatherIcon()

        setButtonStyle(self.showvirusbutton, "UI/images/icon/virus.png")
        setButtonStyle(self.showperiodbutton, "UI/images/icon/period.png")
        setButtonStyle(self.showpestsbutton, "UI/images/icon/pest.png")
        setButtonStyle(self.exitbutton, "UI/images/icon/exit.png")

        self.School.setPixmap(QPixmap('UI/images/yzu.png'))
        self.School.setStyleSheet("QPushButton{background:rgb(255,255,255,50);}"
                                           "QPushButton:hover{color:rgb(100,100,100,120);}")

        self.School.setScaledContents(True)
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)

        self.ShowIPLabel.setFont(font)

    def SetWheatherIcon(self):

        self.weather = get_wheather()

        if '晴' in self.weather[0]:
            setButtonStyle(self.showlocationbutton, "UI/images/icon/sun.png")
        elif '雨' in self.weather[0] :
            setButtonStyle(self.showlocationbutton, "UI/images/icon/rain.png")
        elif '多云' in self.weather[0]:
            setButtonStyle(self.showlocationbutton, "UI/images/icon/partlycloudy.png")
        else:
            setButtonStyle(self.showlocationbutton,"UI/images/icon/wheather.png")

    def ShowChartButtonPressed(self):

        self.showchartbutton.setEnabled(False)
        self.box = ChartBox()
        self.box.showFullScreen()

        self.showchartbutton.setEnabled(True)

        pass

    def ShowLocationButtonPressed(self):

        self.showlocationbutton.setEnabled(False)

        self.SetWheatherIcon()

        self.box = MapBox()
        self.box.showFullScreen()
        self.showlocationbutton.setEnabled(True)

        pass

    def ShowVirusButtonPressed(self):

        self.showvirusbutton.setEnabled(False)
        self.box = VideoBox(HIGHT, WIDTH, 1)  # 小麦病害情况
        self.StopThread()
        self.box.showFullScreen()
        self.showvirusbutton.setEnabled(True)


    def ShowPeriodButtonPressed(self):

        self.showperiodbutton.setEnabled(False)
        self.box = VideoBox(HIGHT, WIDTH,0)  # 小麦生长状况
        self.StopThread()
        self.box.showFullScreen()
        self.showperiodbutton.setEnabled(True)

    def ShowPestsButtonPressed(self):

        self.showpestsbutton.setEnabled(False)
        self.box = VideoBox(HIGHT, WIDTH, 2)  # 小麦虫害状况
        self.StopThread()
        self.box.showFullScreen()
        self.showpestsbutton.setEnabled(True)

        pass

    def ExitButtonPressed(self):

        self.exitbutton.setEnabled(False)
        self.exitbutton.setEnabled(True)

        if self.wthread3:
            self.wthread3.stop()
        if self.wthread:
            self.wthread.stop()

        self.StopThread()

        qApp = QApplication.instance()
        qApp.quit()  # 关闭窗口

    def StopThread(self):
        pass



class VideoBox(QMainWindow, Ui_VideoWindow):

    def __init__(self, capWidth, capHeight,workMode):

        super(VideoBox, self).__init__(None)
        # 工作模式选择
        global rootpath
        global usr_platform

        global WheatMaturityDetectionMode,WheatSickDetectionMode,WheatPestsDetectionMode
        global RiceMaturityDetectionMode,RiceSickDetectionMode,RicePestsDetectionMode

        self.workmode=workMode
        self.isRun=False
        self.fps = 0.0
        self.trantext=''
        self.temp = 0.0
        self.humi = 0.0
        self.ph = 0.0
        self.change = False
        self.diseasegrade = 0

        self.showtipsstate = False

        #设置界面
        self.setupUi(self)

        self.UpdateUi()

        self.AddFruitButton()

        self.SetButtonConnected()

        # 初始化摄像头

        self.url = cap_url

        if os.system(pingurl + cap_ip):
            self.url = 0
        else:
            pass

        self.showvideo = False

        self.cap = cv2.VideoCapture(self.url)

        self.StartShowVideo()

    def AddFruitButton(self):

        if self.workmode == WheatMaturityDetectionMode or self.workmode == RiceMaturityDetectionMode:

            self.wheatButton.setGeometry(QtCore.QRect(0, 253, 128, 80))
            self.riceButton.setGeometry(QtCore.QRect(0, 453, 128, 80))
            self.fruitButton = QtWidgets.QPushButton(self.centralwidget)
            self.fruitButton.setGeometry(QtCore.QRect(0, 653, 128, 80))
            self.fruitButton.setFocusPolicy(QtCore.Qt.NoFocus)
            self.fruitButton.setText("")
            self.fruitButton.setObjectName("fruitButton")
            SetButtonIcon(self.fruitButton, "UI/images/icon/fruit.svg", 64, 64)
            self.fruitButton.setFlat(False)
            self.fruitButton.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                                          "QPushButton:hover{color:rgb(100,100,100,120);}")

    def SetButtonConnected(self):

        self.shotButton.clicked.connect(self.shotButtonPressed)

        self.exitButton.clicked.connect(self.exitButtonPressed)

        self.riceButton.clicked.connect(self.riceButtonPressed)

        self.wheatButton.clicked.connect(self.wheatButtonPressed)

        self.showphotobutton.clicked.connect(self.ShowPhotoButtonPressed)

        self.reversebutton.clicked.connect(self.ReverseButtonPressed)

        self.ShowButton.clicked.connect(self.ShowButtonPressed)

        self.ShowTipsButton.clicked.connect(self.ShowTipsButtonPressed)

        if self.workmode == WheatMaturityDetectionMode or self.workmode == RiceMaturityDetectionMode:
            self.fruitButton.clicked.connect(self.FruitButtonPressed)


    def UpdateUi(self):

        #拍照按钮
        SetButtonIcon(self.shotButton,"UI/images/icon/photograph.png",96,96)

        #退出按钮
        SetButtonIcon(self.exitButton, "UI/images/btn_back_r_normal.png", 128, 64)

        #切换按钮

        SetButtonIcon(self.reversebutton, "UI/images/icon/reverse.svg", 96, 96)

        #显示图片按钮

        SetButtonIcon(self.showphotobutton, "UI/images/icon/pic.svg", 96, 96)

        SetButtonIcon(self.ShowTipsButton,"UI/images/icon/tipsoff.svg",48,48)
        self.ShowTipsButton.setFlat(True)
        self.ShowTipsButton.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                           "QPushButton:hover{color:rgb(100,100,100,120);}")
        self.ShowTipsButton.setEnabled(False)

        #切换水稻按钮

        SetButtonIcon(self.riceButton, "UI/images/icon/rice.png", 64, 64)

        self.riceButton.setFlat(False)

        self.riceButton.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                           "QPushButton:hover{color:rgb(100,100,100,120);}")



        #切换小麦按钮

        SetButtonIcon(self.wheatButton, "UI/images/icon/wheat.png", 64, 64)

        self.wheatButton.setFlat(False)

        self.wheatButton.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                           "QPushButton:hover{color:rgb(100,100,100,120);}")


        SetButtonIcon(self.ShowButton, "UI/images/icon/show.svg", 64, 64)

        self.ShowButton.setFlat(False)

        self.ShowButton.setStyleSheet("QPushButton{background:rgb(255,255,255,0);}"
                           "QPushButton:hover{color:rgb(100,100,100,120);}")

        #状态栏
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)

        self.head.setFont(font)

        self.head.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                "QLabel:hover{color:rgb(100,100,100,120);}")

        font = QFont()
        font.setBold(True)
        font.setPointSize(20)

        self.TipsLabel.setFont(font)

        self.TipsLabel.setStyleSheet("QTextBrowser{background:rgb(255,249,222,245);}"
                                "QTextBrowser:hover{color:rgb(100,100,100);}")

        self.TipsLabel.hide()

        self.setStyleSheet("#VideoWindow{border-image:url(UI/images/backgroundpic.png);}")


        #视频UI
        self.pictureLabel.setAutoFillBackground(True)  # 设置背景充满，为设置背景颜色的必要条件

        self.pictureLabel.setStyleSheet("QLabel{background:rgb(255,255,255,60);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")

        self.pictureLabelbackground.setAutoFillBackground(True)

        self.pictureLabelbackground.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")

        # 结果显示框
        self.resulttext.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                        "QLabel:hover{color:rgb(100,100,100,120);}")

        #设置文本框
        pixmap=QPixmap("UI/images/yzu.png")
        self.schoolbadge.setPixmap(pixmap)

        self.schoolbadge.setScaledContents(True)

        self.teammumber.setText("YZU-灵听者：\n包飞霞\r刘源\n牛恺锐\r薛鹏")

    def StartShowVideo(self):
        # 设置双线程
        self.frameID = 0
        self.isRun = True
        self.CapIsbasy = False
        self.AlgIsbasy = False

        # 设计视频采集参数
        self.showImage = None
        self.limg = None

        # 线程1相机采集

        self.wthread = None
        self.wthread = ThreadCap(self)
        self.wthread.updatedImage.connect(self.showframe)
        self.wthread.start()

        # 线程2算法处理
        self.wthread2 = None
        self.wthread2 = ThreadIde(self)
        self.wthread2.updatedresult.connect(self.showresult)
        self.wthread2.start()

    def ShowButtonPressed(self):
        try:
            if self.isRun:
                if self.wthread:
                    while self.CapIsbasy:
                        pass

                    self.wthread.stop()
                    self.wthread2.stop()

                    if self.cap.isOpened():
                        self.cap.release()
                        self.CapIsbasy = False

                    self.isRun = False
            if self.showvideo == True:
                self.showvideo = False

                self.ClearTips()

                backinfo = os.system(pingurl + cap_ip)  # 实现pingIP地址的功能，-n1指发送报文一次，-w1指等待1秒

                if backinfo:
                    self.url = 0
                else:
                    self.url = cap_url
            else:
                self.ClearTips()
                self.showvideo = True
                self.url = 'C:/01.mp4'

                if self.workmode == WheatMaturityDetectionMode:
                    self.url = f'{rootpath}video/WheatMaturity.mp4'
                elif self.workmode == WheatSickDetectionMode:
                    self.url = f'{rootpath}video/Maturity.mp4'
                elif self.workmode == WheatPestsDetectionMode:
                    self.url = f'{rootpath}video/Maturity.mp4'
                elif self.workmode == RiceMaturityDetectionMode:
                    self.url = f'{rootpath}video/Maturity.mp4'
                elif self.workmode == RiceSickDetectionMode:
                    self.url = f'{rootpath}video/Maturity.mp4'
                elif self.workmode == RicePestsDetectionMode:
                    self.url = f'{rootpath}video/Maturity.mp4'

            if os.path.exists(self.url):
                self.cap = cv2.VideoCapture(self.url)
            else:
                self.cap = cv2.VideoCapture(0)

            self.StartShowVideo()
        except Exception as e:
            if DEBUG == ON:
                print(e)
            pass

    def shotButtonPressed(self):

        ret,img = self.cap.read()

        if ret==True and self.text!='getting...' and self.trantext!='NULL':

            if self.workmode <= WheatPestsDetectionMode:
                self.type = 'Wheat'
            elif self.workmode >= RiceMaturityDetectionMode and self.workmode <= RicePestsDetectionMode:
                self.type = 'Rice'
            elif self.workmode == FruitSickDetectionMode:
                self.type = ''

            self.img = img
            self.img = cv2.resize(self.img,(640,540))

            if usr_platform == "Windows":
                self.imgname = f'{self.type}-{self.trantext}-{str(datetime.datetime.now()).replace(":","-")}.png'
            else:
                if self.workmode != FruitSickDetectionMode and self.workmode != FruitTypeDetectionMode:
                    self.imgname = f'{self.type}:{self.trantext}-{str(datetime.datetime.now())[0:19]}.png'
                else:
                    self.imgname = f'{self.trantext}-{str(datetime.datetime.now())[0:19]}.png'

            if(os.path.exists(rootpath+'camera/')):
                cv2.imwrite(rootpath+'camera/'+self.imgname,self.img)
            else:
                if DEBUG == ON:
                    print('error code -1:can not find dir')

    def ShowTips(self,text):

        if self.showtipsstate == False:
            self.TipsLabel.show()
            self.TipsLabel.setText(text)
            self.showtipsstate = True
        elif self.showtipsstate == True:
            self.TipsLabel.setText('')
            self.TipsLabel.hide()
            self.showtipsstate = False

    def ShowTipsButtonPressed(self):

        if self.text == '健康':
            self.ClearTips()
        else:
            if self.workmode <= WheatPestsDetectionMode:
                if self.text != 'getting...':
                    self.ShowTips(WheatTips[self.text])
            elif self.workmode <= RicePestsDetectionMode:
                if self.text != 'getting...':
                    self.ShowTips(RiceTips[self.text])

    def ChangeTipsIcon(self):

        if self.text != '健康':
            SetButtonIcon(self.ShowTipsButton,"UI/images/icon/tipson.svg",48,48)
            self.ShowTipsButton.setEnabled(True)
        else :
            SetButtonIcon(self.ShowTipsButton,"UI/images/icon/tipsoff.svg",48,48)
            if self.showtipsstate == False:
                self.ClearTips()
            else:
                self.ShowTipsButton.setEnabled(True)


    def showframe(self):

        if self.showImage != None:
            self.pictureLabel.setPixmap(self.showImage)
            self.pictureLabel.setScaledContents(True)

        self.currenttime = str(datetime.datetime.now())

        if self.temp != None and self.humi != None and self.ph != None:
            self.head.setText(f'    {self.currenttime[0:19]}    温度：  {str(self.temp)[0:5]}°C    湿度：  {str(self.humi)[0:7]}%    PH:  {str(self.ph)}')
        else:
            self.head.setText(f'    {self.currenttime[0:19]}    温度：Error    湿度：Error  PH:Error')

    def showresult(self):

        if self.text != 'getting...':
            self.time = f'{str(self.time)[0:8]} s'

        if self.fps != 'getting...':
            self.fps = str(self.fps)[0:8]

        self.tips = ''

        if(self.workmode == WheatMaturityDetectionMode):
            if self.text not in WheatMaturityIndex:

                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'

            if self.text == "生长期":

                if self.temp >= 13.0 and self.temp < 18.0:
                    self.tips = '温度适宜，小麦生长最快'
                elif self.temp >= 6.0 and self.temp < 13.0:
                    self.tips = '温度适宜,小麦生长较快'
                elif self.temp >= 3.0 and self.temp < 6.0:
                    self.tips = '温度偏低,小麦生长缓慢'
                elif self.temp >= 18.0:
                    self.tips = "温度偏高,小麦生长受到抑制"
                elif self.temp <= 0.0:
                    self.tips = "小麦停止生长,进入越冬期。"

            elif self.text == "灌浆期":

                if self.temp !=None:
                    if self.temp >= 20.0 and self.temp < 22.0:
                        self.tips = '温度适宜小麦生长'
                    elif self.temp >= 12.0 and self.temp < 20.0:
                        self.tips = '温度偏低,灌浆期可能延长,易获高产'
                    elif self.temp >= 22.0 and self.temp < 28.0:
                        self.tips = '温度偏高'
                    elif self.temp <= 12.0:
                        self.tips = "温度过低"
                    elif self.temp >= 28.0:
                        self.tips = "温度过高,植物失水加速,影响灌浆"
            else:
                self.tips = '注意及时收割。'

            self.resulttext.setText(f'小麦\n\n成熟度：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}\n\nTips:{self.tips}')

        if(self.workmode == WheatSickDetectionMode):

            if self.text not in WheatDiseaseIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
                self.diseasegrade = 'getting...'

            if self.text != 'getting...':
                self.ChangeTipsIcon()
            if self.text == '健康':
                self.resulttext.setText(f'小麦\n\n病害情况：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')
            else:
                self.resulttext.setText(f'小麦\n\n病害情况：{self.text}\n\n病害等级：{self.diseasegrade}\n\n计算用时：{self.time}\n\nfps：{self.fps}')

        if(self.workmode == WheatPestsDetectionMode):

            if self.text not in WheatPestsIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
            self.resulttext.setText(f'小麦\n\n虫害情况：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')

        if(self.workmode == RiceMaturityDetectionMode):

            if self.text not in RiceMaturityIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
            self.resulttext.setText(f'水稻\n\n成熟度：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')

        if(self.workmode == RiceSickDetectionMode):

            if self.text not in RiceDiseaseIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
                self.diseasegrade = 'getting...'

            if self.text != 'getting...':
                self.ChangeTipsIcon()

            if self.text == '健康':
                self.resulttext.setText(f'水稻\n\n病害情况：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')
            else:
                self.ChangeTipsIcon()
                self.resulttext.setText(f'水稻\n\n病害情况：{self.text}\n\n病害等级：{self.diseasegrade}\n\n计算用时：{self.time}\n\nfps：{self.fps}')


        if(self.workmode == RicePestsDetectionMode):

            if self.text not in RicePestsIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
            self.resulttext.setText(f'水稻\n\n虫害情况：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')

        if self.workmode == FruitSickDetectionMode:
            if self.text not in FruitStateIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
            self.resulttext.setText(f'{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')

        if self.workmode == FruitTypeDetectionMode:
            if self.text not in FruitTypesIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
            self.resulttext.setText(f'{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')


    def ShowPhotoButtonPressed(self):

        self.box = PhotoBox(self)
        self.box.showFullScreen()
        self.isRun = False
        pass

    def ClearTips(self):

        SetButtonIcon(self.ShowTipsButton,"UI/images/icon/tipsoff.svg",48,48)

        self.TipsLabel.hide()
        self.ShowTipsButton.setEnabled(False)
        self.TipsLabel.setText("")


    def FruitButtonPressed(self):

        lock = False

        self.ClearTips()

        self.text= 'getting...'
        self.time= 'getting...'
        self.fps = 'getting...'

        if self.workmode == FruitSickDetectionMode:

            self.workmode = FruitTypeDetectionMode
            lock = True

        if self.workmode == WheatMaturityDetectionMode or self.workmode == RiceMaturityDetectionMode:

            self.workmode = FruitSickDetectionMode
            lock = True

        if self.workmode == FruitTypeDetectionMode and not lock:

            self.workmode = FruitSickDetectionMode

            lock = True

    def ReverseButtonPressed(self):

        if self.isRun:
            if self.wthread:
                while self.CapIsbasy:
                    pass

                self.wthread.stop()
                self.wthread2.stop()

                if self.cap.isOpened():
                    self.cap.release()
                    self.CapIsbasy = False

                self.isRun = False

        if(self.url == 0):
            self.url = cap_url
            while self.CapIsbasy:
                pass

            if os.system(pingurl + cap_ip):
                self.url = 0

        else:
            self.url = 0

        self.cap = cv2.VideoCapture(self.url)

        self.StartShowVideo()

        pass



    def wheatButtonPressed(self):

        self.ClearTips()

        if self.workmode >= RiceMaturityDetectionMode:
            self.text= 'getting...'
            self.time= 'getting...'
            self.fps = 'getting...'

        if self.workmode == RiceMaturityDetectionMode or self.workmode == FruitSickDetectionMode or self.workmode == FruitTypeDetectionMode:

            self.workmode = WheatMaturityDetectionMode

        if self.workmode == RiceSickDetectionMode:
            self.workmode = WheatSickDetectionMode

        if self.workmode == RicePestsDetectionMode:
            self.workmode = WheatPestsDetectionMode

    def riceButtonPressed(self):

        self.ClearTips()

        if self.workmode <= WheatPestsDetectionMode:
            self.text= 'getting...'
            self.time= 'getting...'
            self.fps = 'getting...'

        if self.workmode == WheatMaturityDetectionMode  or self.workmode == FruitTypeDetectionMode or self.workmode == FruitSickDetectionMode:
            self.workmode = RiceMaturityDetectionMode

        if self.workmode == WheatSickDetectionMode:
            self.workmode = RiceSickDetectionMode

        if self.workmode == WheatPestsDetectionMode:
            self.workmode = RicePestsDetectionMode

    def exitButtonPressed(self):
        self.ClearTips()
        if self.isRun:
            if self.wthread:
                self.wthread.stop()
                self.wthread2.stop()


            self.isRun=False

        while self.CapIsbasy:
            pass

        self.cap.release()



        self.CapIsbasy=False
        self.close()





class MapBox(QMainWindow,Ui_WheatherWindow):

    def __init__(self):

        super(MapBox, self).__init__(None)

        self.wheather = get_wheather()
        self.setupUi(self)
        self.UpdateUi()
        self.exitButton.clicked.connect(self.ExitButtonPressed)
        self.wheatherbox.setText(self.wheather[0])

    def UpdateUi(self):

        #退出按钮
        SetButtonIcon(self.exitButton, "UI/images/btn_back_r_normal.png", 128, 64)

        #状态栏
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)

        self.head.setFont(font)

        self.head.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                "QLabel:hover{color:rgb(100,100,100,120);}")

        self.backgroundlabel.setPixmap(QPixmap("UI/images/backgroundpic.png"))
        self.backgroundlabel.setScaledContents(True)

        self.setStyleSheet("#MapWindow{border-image:url(UI/images/backgroundpic.png);}")


        #视频UI

        self.PictureLabel.setAutoFillBackground(True)  # 设置背景充满，为设置背景颜色的必要条件

        self.PictureLabel.setStyleSheet("QLabel{background:rgb(255,255,255,60);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")
        self.PictureLabel.setPixmap(QPixmap('UI/images/yzumap.png'))

        #self.Map.load(QUrl('https://zhaosiyi.github.io/demo/?tdsourcetag=s_pcqq_aiomsg'))

        self.pictureLabelbackground.setAutoFillBackground(True)

        self.pictureLabelbackground.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")

        # 结果显示框
        self.wheatherbox.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                        "QLabel:hover{color:rgb(100,100,100,120);}")


        self.wheatherbox.setText("YZU-灵听者：\n包飞霞\r刘源\n牛恺锐\r薛鹏")

    def ExitButtonPressed(self):
        self.close()


class PhotoBox(QMainWindow,Ui_PhotoWindow):

    def __init__(self,vw):
        super(PhotoBox, self).__init__(None)

        self.trantext = ''
        self.temp = 0.0
        self.humi = 0.0
        self.vw = vw

        # 设置界面
        self.setupUi(self)

        self.UpdateUi()

        self.SetButtonConnected()

        global rootpath

        self.capfilePath = rootpath+'camera/'

        self.piclist = os.listdir(self.capfilePath)
        self.piclistlen = len(self.piclist)

        if DEBUG == ON:
            print (self.piclist)
            print(self.piclistlen)

        self.picindex = 0

        if self.piclistlen!=0:
            self.pic = QtGui.QPixmap(self.capfilePath+self.piclist[0])
            self.resulttext.setText(self.readpicname(self.piclist[self.picindex]))
        else:
            self.pic = QtGui.QPixmap(rootpath+'UI/images/nopic.svg')
            self.resulttext.setText('No Picture.')

        self.pictureLabel.setPixmap(self.pic)

        self.pictureLabel.setScaledContents(True)

    def SetButtonConnected(self):

        self.exitButton.clicked.connect(self.exitButtonPressed)

        self.leftButton.clicked.connect(self.leftButtonPressed)

        self.rightButton.clicked.connect(self.rightButtonPressed)

        self.deleteButton.clicked.connect(self.DeleteButtonPressed)

    def UpdateUi(self):

        self.exitButton.setStyleSheet("border:none")

        # 退出按钮
        SetButtonIcon(self.exitButton,"UI/images/btn_back_r_normal.png",128,64)


        #左按钮
        SetButtonIcon(self.leftButton, "UI/images/icon/left.svg", 64, 64)

        #右按钮
        SetButtonIcon(self.rightButton, "UI/images/icon/right.svg", 64, 64)
        #删除
        SetButtonIcon(self.deleteButton, "UI/images/icon/delete.svg", 64, 64)

        self.deleteButton.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                                       "QPushButton:hover{color:rgb(100,100,100,120);}")
        # 状态栏
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)

        self.head.setFont(font)

        self.head.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                "QLabel:hover{color:rgb(100,100,100,120);}")

        self.backgroundlabel.setPixmap(QPixmap("UI/images/backgroundpic.png"))

        self.backgroundlabel.setScaledContents(True)

        self.setStyleSheet("#VideoWindow{border-image:url(UI/images/backgroundpic.png);}")

        # 视频UI
        self.pictureLabel.setAutoFillBackground(True)  # 设置背景充满，为设置背景颜色的必要条件

        self.pictureLabel.setStyleSheet("QLabel{background:rgb(255,255,255,60);}"
                                        "QLabel:hover{color:rgb(100,100,100,120);}")

        self.pictureLabelbackground.setAutoFillBackground(True)

        self.pictureLabelbackground.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                                  "QLabel:hover{color:rgb(100,100,100,120);}")

        # 结果显示框
        self.resulttext.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                      "QLabel:hover{color:rgb(100,100,100,120);}")

        # 设置文本框
        pixmap = QPixmap("UI/images/yzu.png")
        self.schoolbadge.setPixmap(pixmap)

        self.schoolbadge.setScaledContents(True)

        self.teammumber.setText("YZU-灵听者：\n包飞霞\r刘源\n牛凯瑞\r薛鹏")

        self.frameID = 0
        self.wthread5 = None
        self.wthread5 = ThreadUpdatPhoto(self)
        self.wthread5.updatephoto.connect(self.updateenv)
        self.wthread5.start()

    def updateenv(self):

        self.temp,self.humi,self.ph = Environment.Temperature,Environment.Humidity,Environment.PH

        self.currenttime = str(datetime.datetime.now())

        if self.temp != None and self.humi != None and self.ph != None:
            self.head.setText(f'    {self.currenttime[0:19]}    温度：  {str(self.temp)[0:5]}°C    湿度：  {str(self.humi)[0:7]}%    PH:  {str(self.ph)}')
        else:
            self.head.setText(f'    {self.currenttime[0:19]}    温度：Error    湿度：Error  PH:Error')

    def leftButtonPressed(self):

        if self.piclistlen!=0:

            if self.picindex==0:
                self.picindex = self.piclistlen-1
            else:
                self.picindex -= 1

            self.pic = QtGui.QPixmap(self.capfilePath + self.piclist[self.picindex])

            self.pictureLabel.setPixmap(self.pic)

            self.pictureLabel.setScaledContents(True)

            self.resulttext.setText(self.readpicname(self.piclist[self.picindex]))

        else:

            self.pictureLabel.setPixmap(QPixmap('UI/images/nopic.svg'))

    def rightButtonPressed(self):

        if self.piclistlen != 0:

            self.picindex += 1

            if self.picindex >self.piclistlen-1:
                self.picindex = 0

            self.pic = QtGui.QPixmap(self.capfilePath + self.piclist[self.picindex])

            self.pictureLabel.setPixmap(self.pic)

            self.pictureLabel.setScaledContents(True)

            self.resulttext.setText(self.readpicname(self.piclist[self.picindex]))

        else:

            self.pictureLabel.setPixmap(QPixmap('UI/images/nopic.svg'))

    def DeleteButtonPressed(self):

        if self.piclistlen!= 0:

            os.remove(os.path.join(self.capfilePath, self.piclist[self.picindex]))

            if DEBUG == ON:

                print("Delete File: " + os.path.join(self.capfilePath, self.piclist[self.picindex]))  # 控制台输出，查看删除了哪些图片

        else:

            self.pictureLabel.setPixmap(QPixmap('UI/images/nopic.svg'))

            if DEBUG == ON:

                print('Not Found Any Pic!')

            self.resulttext.setText('No Picture.')

        self.capfilePath = rootpath+'camera/'

        self.piclist = os.listdir(self.capfilePath)

        self.piclistlen = len(self.piclist)

        if self.piclistlen == 0:

            self.resulttext.setText('No Picture.')

        self.rightButtonPressed()

    def readpicname(self,picname):

        name = ''
        state = ''
        time = ''
        lockname = False
        lockstate = False
        locktime = False

        for s in picname:

            if s!= ':' and lockname != True:

                name = name+s

            else:

                lockname = True

                if s != '-' and lockstate != True:

                    if s!= ':':

                        state = state + s

                else:

                    lockstate = True

                    if s != '.':

                        if s == '-' and locktime !=True:

                            locktime = True
                            continue

                        else:

                            time = time +s

                    else:

                        break

        if name == 'Rice':

            name = '水稻'

            if state == 'Growing period':
                state = "成熟度：生长期"

            elif state == 'Leaf function or greening period':
                state = "成熟度：叶功能/返青期"

            elif state == 'Maturity':
                state = "成熟度：成熟期"

            elif state == 'Health':
                state = '病害情况：健康'
            elif state == 'Blight':
                state = "病害情况：枯纹病"
            elif state == 'Bugs':
                state = '虫害情况:有'

        elif name == 'Wheat' :

            name = '小麦'

            if state == 'Maturity':
                state = '成熟度：成熟期'

            elif state =='Grouting period':
                state = '成熟度：灌浆期'

            elif state =='Growing period':
                state ='成熟度：生长期'

            elif state == 'Health':
                state = '病害情况：健康'

            elif state == 'Rust':
                state = "病害情况：条锈病"

            elif state == 'powdery mildew':
                state = "病害情况：白粉病"

            elif state == 'Is_Buds':
                state = '虫害情况:有虫害'


        elif name == 'apples':
            name = '苹果'

        elif name == 'banana':
            name = '香蕉'

        elif name == 'orange':
            name = '橘子'

        else:
            name = 'Error'

        if state == 'fresh':
            state = '新鲜'

        elif state == 'rotten':
            state = '坏的'

        if name != 'Error' and state != 'Error':

            if state == '新鲜' or state == '坏的':
                str = f'{name}:{state}\n\n记录时间:{time}'
            else:
                str = f'{name}：\n\n{state}\n\n记录时间:{time}'

        else:
            str = 'Error'

        return str

    def exitButtonPressed(self):

        if self.wthread5:

            self.wthread5.stop()

        self.vw.isRun = True
        self.close()

class ChartBox(QMainWindow,Ui_ChartWindow):

    def __init__(self):

        global UpdateEveryOneSec,UpdateEveryOneMin,UpdateEveryOneHour

        super(ChartBox, self).__init__(None)

        self.temp = 0.0
        self.itemp = 0.0
        self.humi = 0.0
        self.ph = 0.0
        self.workmode = UpdateEveryOneMin


        self.maxtemp = 0.0
        self.mintemp = 0.0

        self.avetemp = 0.0

        self.maxhumi = 0.0
        self.minhumi = 0.0
        self.avehumi = 0.0

        self.setupUi(self)

        self.UpdataUI()

        self.leftButton.clicked.connect(self.LeftButtonPressed)
        self.rightButton.clicked.connect(self.RightButtonPressed)

        plt.rcParams['font.sans-serif'] = ['FangSong']
        plt.rcParams['axes.unicode_minus'] = False


        self.x = []  #建立空的x轴数组和y轴数组
        self.y = []
        self.z = []
        self.n = 0

        self.dynamic_showchart = self.dynamic_canvas.figure.subplots()

        self.workmode = UpdateEveryOneSec

        self.inittimer()
        self._timer.start()
        self.showchart()

        self.frameID = 0
        self.wthread4 = None
        self.wthread4 = ThreadUpdateChart(self)
        self.wthread4.updatechart.connect(self.UpdateEnv)
        self.wthread4.start()

        self.exitButton.clicked.connect(self.ExitButtonPressed)

    def inittimer(self):

        if self.workmode == UpdateEveryOneSec:
            self._timer = self.dynamic_canvas.new_timer(
                1000, [(self.showchart, (), {})])
        elif self.workmode == UpdateEveryOneMin:
            self._timer = self.dynamic_canvas.new_timer(
                60000, [(self.showchart, (), {})])
        elif self.workmode == UpdateEveryOneHour:
            self._timer = self.dynamic_canvas.new_timer(
                3600000, [(self.showchart, (), {})])

    def UpdateEnv(self):

        self.currenttime = str(datetime.datetime.now())

        self.temp,self.humi,self.ph = Environment.Temperature,Environment.Humidity,Environment.PH

        if self.temp != None and self.humi != None and self.ph != None:
            self.head.setText(f'    {self.currenttime[0:19]}    温度：  {str(self.temp)[0:5]}°C    湿度：  {str(self.humi)[0:7]}%    PH:  {str(self.ph)}')
        else:
            self.head.setText(f'    {self.currenttime[0:19]}    温度：Error    湿度：Error  PH:Error')



    def UpdataUI(self):

        self.dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))

        self.layout = QtWidgets.QVBoxLayout(self.showchartlabel)


        self.layout.addWidget(self.dynamic_canvas)

        self.head.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")

        self.backlabel.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")

        self.showchartlabel.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")

        #退出按钮
        SetButtonIcon(self.exitButton,"UI/images/btn_back_r_normal.png",128,64)

        #左按钮
        SetButtonIcon(self.leftButton, "UI/images/icon/left.svg", 64, 64)

        #右按钮
        SetButtonIcon(self.rightButton, "UI/images/icon/right.svg", 64, 64)

        #设置背景

        self.backgroundlabel.setPixmap(QPixmap("UI/images/backgroundpic.png"))

        self.backgroundlabel.showFullScreen()

        self.setStyleSheet("#ChartWindow{border-image:url(UI/images/backgroundpic.png);}")

        font = QFont()

        font.setBold(True)
        font.setPointSize(20)

        self.head.setFont(font)

        font.setPointSize(15)

        self.TempLabel.setFont(font)

        self.HumiLabel.setFont(font)

    def showchart(self):
        self.n += 1

        if self.workmode == UpdateEveryOneHour:
            if self.n == 24:
                self.n = 0
                self.x = []
                self.y = []
                self.z = []
        else:
            if self.n == 60:
                self.n = 0
                self.x = []
                self.y = []
                self.z = []


        self.dynamic_showchart.clear()

        if self.workmode == UpdateEveryOneSec:
            sec = str(datetime.datetime.now())[17:19]
            sec = int(sec)
            self.timebase = sec

            if usr_platform == 'Windows':
                self.dynamic_showchart.set_ylabel('温度(°C)/湿度(%)')
                self.dynamic_showchart.set_xlabel('时间(秒)')
            else:
                self.dynamic_showchart.set_ylabel('Temp(°C)/Humi(%)')
                self.dynamic_showchart.set_xlabel('Time(sec)')


        elif self.workmode == UpdateEveryOneMin:
            min = str(datetime.datetime.now())[14:16]
            min = int(min)
            self.timebase = min
            if usr_platform == 'Windows':
                self.dynamic_showchart.set_ylabel('温度(°C)/湿度(%)')
                self.dynamic_showchart.set_xlabel('时间(分钟)')
            else:
                self.dynamic_showchart.set_ylabel('Temp(°C)/Humi(%)')
                self.dynamic_showchart.set_xlabel('Time(min)')
        elif self.workmode == UpdateEveryOneHour:
            hour = str(datetime.datetime.now())[11:13]
            hour = int(hour)
            self.timebase = hour
            if usr_platform == 'Windows':
                self.dynamic_showchart.set_ylabel('温度(°C)/湿度(%)')
                self.dynamic_showchart.set_xlabel('时间(小时)')
            else:
                self.dynamic_showchart.set_ylabel('Temp(°C)/Humi(%)')
                self.dynamic_showchart.set_xlabel('Time(hour)')


        self.x.append(self.timebase)

        self.y.append(self.temp)

        self.z.append(self.humi)

        self.maxtemp = float(str(np.max(self.y))[0:5])

        self.mintemp = float(str(np.min(self.y))[0:5])

        self.avetemp = float(str(np.average(self.y))[0:5])

        self.maxhumi = float(str(np.max(self.z))[0:5])

        self.minhumi = float(str(np.min(self.z))[0:5])

        self.avehumi = float(str(np.average(self.z))[0:5])

        humistate = 'None'

        if float(self.avehumi) > 75.0:
            humistate = "湿润"
        elif float(self.avehumi) >= 50.0:
            humistate = "半湿润"
        elif float(self.avehumi) >= 25.0:
            humistate = "半干旱"
        else:
            humistate = "干旱"

        tempstate = 'None'


        if float(self.avetemp) > 40.0:
            tempstate = "超高温"
        elif float(self.avetemp) >= 28.0:
            tempstate = "高温"
        elif float(self.avetemp) >= 14.0:
            tempstate = "温和"
        elif float(self.avetemp) >= 10.0:
            tempstate = "温凉"
        elif float(self.avetemp) >= -10.0:
            tempstate = "低温"
        else:
            tempstate = "超低温"


        humitips = ''
        temptips = ''

        if self.avehumi >= 85:
            humitips = '湿度偏高,易滋生病虫害,影响光合作用。'
        elif self.avehumi <= 20:
            humitips = "湿度较低,易引发干旱,注意及时灌溉。"
        else:
            humitips = "湿度适宜作物生长。"

        hour = int(str(datetime.datetime.now())[11:13])

        if hour >= 0 and hour <= 14:

            if self.avetemp > 23.0 and self.avetemp <= 30:
                temptips = '温度适宜作物生长'
            elif self.avetemp <23.0:
                temptips = '温度偏低'
            elif self.avetemp >30:
                temptips = '温度偏高'

        elif hour > 18:

            if self.avetemp > 23.0 and self.avetemp <= 26:
                temptips = '温度适宜作物生长'
            elif self.avetemp <23.0:
                temptips = '温度偏低'
            elif self.avetemp >26:
                temptips = '温度偏高'

        else:

            if self.avetemp > 18.0 and self.avetemp <= 20:
                temptips = '温度适宜作物生长'
            elif self.avetemp <18.0:
                temptips = '温度偏低'
            elif self.avetemp >20:
                temptips = '温度偏高'


        self.itemp = ((self.maxtemp + self.mintemp)/2.0 -10)

        self.TempLabel.setText(f'当日最高温度：{str(self.maxtemp)[0:5]}°C\n当日最低温度：{str(self.mintemp)[0:5]}°C\n当日有效积温：{str(self.itemp)[0:5]}°C\n温度状况:{tempstate}\nTips：{temptips}')

        self.HumiLabel.setText(f'当日最高湿度：{str(self.maxhumi)[0:5]}%\n当日最低湿度：{str(self.minhumi)[0:5]}%\n当日平均湿度：{str(self.avehumi)[0:5]}%\n湿度状况:{humistate}\nTips：{humitips}')


        yy = np.array(self.y)

        zz = np.array(self.z)

        self.dynamic_showchart.plot(yy,color='blue',label = 'Tempture')
        self.dynamic_showchart.plot(zz, color='red', label='Humidity')

        self.dynamic_showchart.set_xlim(0,60)
        self.dynamic_showchart.set_ylim(-20, 100)

        self.dynamic_showchart.figure.legend()

        self.dynamic_showchart.figure.canvas.draw()

    def LeftButtonPressed(self):

        self.itemp = 0.0
        self._timer.stop()

        self.workmode -= 1

        if self.workmode < UpdateEveryOneSec:
            self.workmode = UpdateEveryOneHour

        self.dynamic_showchart.clear()

        self.n = 0
        self.x = []
        self.y = []
        self.z = []

        self.inittimer()
        self._timer.start()

        self.showchart()


    def RightButtonPressed(self):

        self.itemp = 0.0
        self._timer.stop()
        self.dynamic_showchart.clear()

        self.workmode += 1

        if self.workmode > UpdateEveryOneHour:
            self.workmode = UpdateEveryOneSec


        self.n = 0
        self.x = []
        self.y = []
        self.z = []

        self.inittimer()
        self._timer.start()
        self.showchart()


    def ExitButtonPressed(self):
        if DEBUG == ON:
            print('exit')
        self._timer.stop()
        if self.wthread4:
            self.wthread4.stop()
        self.close()



