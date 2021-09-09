import __init__
from __init__ import  *
from UI.ui import *
from UI.designer.chartwindow import Ui_ChartWindow
import datetime
import urllib.request
import gzip
from PyQt5.QtCore import *
from library.Sensor.TempHumiSensor import *
from library.Sensor.PHSensor import *
import platform
from Cloud.tcp_cloud_demo import *
from time import *

def MainApplication():

    SystemInit()

    app = QApplication(sys.argv)

    window = MainWindows()

    window.showFullScreen()

    sys.exit(app.exec_())

def RunAIModel(modelpath,mode):

    cvNet = cv2.dnn.readNetFromTensorflow(modelpath)
    cvNet.setInput(cv2.dnn.blobFromImage(limg, 1. / 255, size=(224, 224)))

    cvOut = cvNet.forward()
    point = np.argmax(cvOut)

    return point

# 算法线程
class ThreadIde(QThread):

    updatedresult = QtCore.pyqtSignal(int)

    def __init__(self, mw):

        global WheatMaturityDetectionMode,WheatSickDetectionMode,WheatPestsDetectionMode
        global RiceMaturityDetectionMode,RiceSickDetectionMode,RicePestsDetectionMode

        self.mw = mw
        self.working = True

        self.diseasegrade = 0

        self.workmode=self.mw.workmode

        super(ThreadIde, self).__init__(None)

        global rootpath

    def __del__(self):

        if usr_platform == "Windows":
            pass
        else:
            self.wait()

    def run(self):

        QApplication.processEvents()

        while self.working:

            if  self.mw.AlgIsbasy == False and not (self.mw.limg is None) and self.mw.isRun:

                self.workmode = self.mw.workmode

                self.mw.AlgIsbasy = True

                limg = self.mw.limg

                t1 = cv2.getTickCount()

                if self.workmode == WheatMaturityDetectionMode:

                    if(os.path.exists(rootpath+'model/Wheat/period/model_1.15.pb')):

                        point = RunAIModel(rootpath+'model/Wheat/period/model_1.15.pb',self.workmode)

                        self.text = WheatMaturityIndexCh[int(point)]
                        self.trantext = WheatMaturityIndexEn[int(point)]

                    else:

                        self.text = 'NULL'
                        self.trantext='NULL'

                elif self.workmode == WheatSickDetectionMode:

                    if(os.path.exists(rootpath+'model/Wheat/virus/mode_porday_rust1.1_cnn1.15.pb')):

                        point = RunAIModel(rootpath + 'model/Wheat/virus/mode_porday_rust1.1_cnn1.15.pb', self.workmode)

                        if point == 0:
                            pass
                        elif point == 1:
                            limg2 = cv2.resize(limg, (224, 224))
                            R = np.mean(limg2[:, :, 0])
                            G = np.mean(limg2[:, :, 1])
                            B = np.mean(limg2[:, :, 2])

                            result = 0.38 * R + 0.35 * (255 - G) + 0.27 * B

                            if result < 79.56:
                                self.diseasegrade = 1
                            elif result < 100.06:
                                self.diseasegrade = 2
                            elif result < 111.58:
                                self.diseasegrade = 3
                            elif result < 122.61:
                                self.diseasegrade = 4
                            else:
                                self.diseasegrade = 5

                        elif point == 2:

                            limg2 = limg
                            limg2 = cv2.resize(limg2, (224, 224))

                            R = np.mean(limg2[:, :, 0])
                            G = np.mean(limg2[:, :, 1])
                            B = np.mean(limg2[:, :, 2])

                            result = 0.472 * (R) + 0.318 * (255 - G) + 0.210 * B
                            #
                            if result < 80.78:
                                self.diseasegrade = 1
                            elif result < 99.07:
                                self.diseasegrade = 2
                            elif result < 109.63:
                                self.diseasegrade = 3
                            elif result < 121.41:
                                self.diseasegrade = 4
                            else:
                                self.diseasegrade = 5

                        self.text = WheatDiseaseIndexCh[int(point)]
                        self.trantext = WheatDiseaseIndexEn[int(point)]

                    else:

                        self.text = 'NULL'
                        self.trantext='NULL'

                elif self.workmode == WheatPestsDetectionMode:

                    if(os.path.exists(rootpath+'model/mode1.1_bugs1.15.pb')):

                        point = RunAIModel(rootpath + 'model/Wheat/virus/mode_porday_rust1.1_cnn1.15.pb',self.workmode)
                        self.text = WheatPestsIndexCh[int(point)]
                        self.trantext = WheatPestsIndexEn[int(point)]

                    else:

                        self.text = 'NULL'
                        self.trantext='NULL'

                # 水稻成熟度检测
                elif self.workmode == RiceMaturityDetectionMode:

                    if(os.path.exists(rootpath+'model/Rice/period/mode_paddy_rice_cnn1.15.pb')):

                        point = RunAIModel(rootpath + 'model/Wheat/virus/mode_porday_rust1.1_cnn1.15.pb',self.workmode)

                        self.text = RiceMaturityIndexCh[int(point)]
                        self.trantext = RiceMaturityIndexEn[int(point)]

                    else:

                        self.text = 'NULL'
                        self.trantext='NULL'

                elif self.workmode == RiceSickDetectionMode:

                    if(os.path.exists(rootpath+'model/Rice/virus/mode_sick_rice_cnn1.15.pb')):

                        point = RunAIModel(rootpath + 'model/Wheat/virus/mode_porday_rust1.1_cnn1.15.pb',self.workmode)

                        self.text = RiceDiseaseIndexCh[int(point)]
                        self.trantext = RiceDiseaseIndexEn[int(point)]

                        limg2 = limg
                        limg2 = cv2.resize(limg2, (224, 224))
                        R = np.mean(limg2[:, :, 0])
                        G = np.mean(limg2[:, :, 1])
                        B = np.mean(limg2[:, :, 2])

                        result = 0.318 * (255 - R) + 0.388 * (255 - G) + 0.294 * B

                        if result < 117.16:
                            self.diseasegrade = 1
                        elif result < 135.09:
                            self.diseasegrade = 2
                        elif result < 146.90:
                            self.diseasegrade = 3
                        elif result < 157.99:
                            self.diseasegrade = 4
                        else:
                            self.diseasegrade = 5

                    else:

                        self.text = 'NULL'
                        self.trantext='NULL'

                elif self.workmode == RicePestsDetectionMode:

                    if(os.path.exists(rootpath+'model/mode1.1_bugs1.15.pb')):

                        cvNet = cv2.dnn.readNetFromTensorflow(rootpath+'model/mode1.1_bugs1.15.pb')
                        cvNet.setInput(cv2.dnn.blobFromImage(limg, 1. / 255, size=(224, 224)))

                        cvOut = cvNet.forward()
                        point = np.argmax(cvOut)

                        self.text = WheatPestsIndexCh[int(point)]
                        self.trantext = WheatPestsIndexEn[int(point)]

                    else:

                        self.text = 'NULL'
                        self.trantext='NULL'

                elif self.workmode == FruitSickDetectionMode:

                    if(os.path.exists(rootpath+'model/Fruit/model_freshfruits1.15GPU.pb')):

                        cvNet = cv2.dnn.readNetFromTensorflow(rootpath+'model/Fruit/model_freshfruits1.15GPU.pb')

                        cvNet.setInput(cv2.dnn.blobFromImage(limg, 1. / 255, size=(224, 224)))
                        cvOut = cvNet.forward()
                        point = np.argmax(cvOut)

                        self.text=FruitStateIndexCh[int(point)]
                        self.trantext=FruitStateIndexEn[int(point)]

                    else:

                        self.text = 'NULL'
                        self.trantext='NULL'

                elif self.workmode == FruitTypeDetectionMode:

                    if(os.path.exists(rootpath+'model/Fruit/model_fruits1.15GPU.pb')):

                        cvNet = cv2.dnn.readNetFromTensorflow(rootpath+'model/Fruit/model_fruits1.15GPU.pb')
                        cvNet.setInput(cv2.dnn.blobFromImage(limg, 1. / 255, size=(224, 224)))

                        cvOut = cvNet.forward()
                        point = np.argmax(cvOut)

                        self.text = FruitTypesIndexCh[int(point)]
                        self.trantext = FruitTypesIndexEn[int(point)]

                    else:

                        self.text = 'NULL'
                        self.trantext='NULL'

                t2 = cv2.getTickCount()

                self.mw.time = (t2 - t1) / cv2.getTickFrequency()
                self.mw.fps = 1.0/self.mw.time
                self.mw.text=self.text
                self.mw.trantext=self.trantext
                self.mw.temp, self.mw.humi = Environment.Temperature,Environment.Humidity
                self.mw.ph = Environment.PH
                self.mw.diseasegrade=self.diseasegrade
                self.mw.AlgIsbasy = False

                self.updatedresult.emit(self.mw.frameID)

            else:

                sleep(0.001)

    def stop(self):  # 重写stop方法

        if self.working:
            self.working = False
            if DEBUG == ON:
                print('Thread Exit.')

# 线程读取摄像机
class ThreadCap(QThread):

    updatedImage = QtCore.pyqtSignal(int)

    def __init__(self, mw):

        self.mw = mw
        self.working = True
        self.retrytimes = 0
        QThread.__init__(self)
        global rootpath

    def __del__(self):

        if usr_platform == "Windows":
            pass
        else:
            self.wait()

    def run(self):

        QApplication.processEvents()

        while self.working:

            if not self.mw.CapIsbasy and self.mw.cap.isOpened() and self.mw.isRun:
                # 采集图像的过程中
                self.mw.CapIsbasy = True
                ret,image = self.mw.cap.read()  # 获取新的一帧图片

                if ret == False:
                    if DEBUG == ON:
                        print("Capture Image Failed")

                    self.mw.isthreadActiv = False
                    self.mw.CapIsbasy = False

                try:

                    img_len = len(image.shape)
                    if img_len == 3:
                        self.mw.limg = image
                    else:
                        self.mw.limg = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

                    height, width, bytesPerComponent = self.mw.limg.shape
                    bytesPerLine = bytesPerComponent * width
                    rgb = cv2.cvtColor(self.mw.limg, cv2.COLOR_BGR2RGB)

                    showImage = QImage(rgb.data, width, height, bytesPerLine, QImage.Format_RGB888) #对获取到的图片进行转换

                    self.mw.showImage = QPixmap.fromImage(showImage)    #传递到前端界面以及算法线程

                    self.mw.CapIsbasy = False

                    self.updatedImage.emit(self.mw.frameID)

                except Exception as e:      #对摄像头掉线进行处理

                    if not self.mw.showvideo:
                        self.mw.showImage = QPixmap(QImage("UI/images/icon/nocamera.svg"))
                        self.mw.pictureLabel.setPixmap(self.mw.showImage)

                    while self.mw.CapIsbasy:
                        pass

                    self.mw.cap.release()                  #尝试重新连接

                    if os.system(pingurl + cap_ip):
                        self.mw.url = 0                                 #连接失败切换到本地USB摄像头

                    if self.mw.showvideo:

                        self.mw.url = 'C:/01.mp4'
                        if self.mw.workmode == WheatMaturityDetectionMode:
                            self.mw.url = f'{rootpath}video/WheatMaturity.mp4'
                        elif self.mw.workmode == WheatSickDetectionMode:
                            self.mw.url = f'{rootpath}video/Maturity.mp4'
                        elif self.mw.workmode == WheatPestsDetectionMode:
                            self.mw.url = f'{rootpath}video/Maturity.mp4'
                        elif self.mw.workmode == RiceMaturityDetectionMode:
                            self.mw.url = f'{rootpath}video/Maturity.mp4'
                        elif self.mw.workmode == RiceSickDetectionMode:
                            self.mw.url = f'{rootpath}video/Maturity.mp4'
                        elif self.mw.workmode == RicePestsDetectionMode:
                            self.mw.url = f'{rootpath}video/Maturity.mp4'

                    self.mw.cap = cv2.VideoCapture(self.mw.url)

                    self.mw.CapIsbasy = False

                    self.updatedImage.emit(self.mw.frameID)

            else:

                sleep(1.0 / 30)

    def stop(self):  # 重写stop方法

        if self.working:
            self.working = False
            if DEBUG == ON:
                print('Thread Exit.')

class ThreadUpdateTime(QThread,QMainWindow,Ui_MainWindow):

    updatetime = QtCore.pyqtSignal(int)

    def __init__(self,mw):

        super(ThreadUpdateTime, self).__init__()
        self.mw = mw
        self.working = True

    def __del__(self):

        if usr_platform == "Windows":
            pass
        else:
            self.wait()

    def run(self):

        QApplication.processEvents()

        while self.working:

            if (self.working):

                self.mw.time = str(datetime.datetime.now())

                self.updatetime.emit(self.mw.frameID)

                sleep(1.0)

    def stop(self):

        if self.working:
            self.working = False
            if DEBUG == ON:
                print('Thread Exit.')

class ThreadUpdatPhoto(QThread,QMainWindow,Ui_PhotoWindow):

    updatephoto = QtCore.pyqtSignal(int)

    def __init__(self,mw):

        super(ThreadUpdatPhoto, self).__init__()

        self.mw = mw

        self.working = True


    def __del__(self):

        if usr_platform == "Windows":
            pass
        else:
            self.wait()

    def run(self):

        QApplication.processEvents()

        while self.working:

            if (self.working):

                self.updatephoto.emit(self.mw.frameID)
                sleep(1.0)

    def stop(self):

        if self.working:
            self.working = False
            if DEBUG == ON:
                print('Thread Exit.')

class ThreadUpdateEnvironmentalParameters(QThread):

    UpdateEnvironmentalParameters = QtCore.pyqtSignal(int)

    def __init__(self):

        super(ThreadUpdateEnvironmentalParameters, self).__init__()

        self.working = True

    def __del__(self):

        if usr_platform == "Windows":
            pass
        else:
            self.wait()

    def run(self):

        QApplication.processEvents()

        while self.working:

            self.UpdateParameters()
            sleep(UPDATE_INTERVAL)

    def UpdateParameters(self):

        Environment.PH = UpdatePH(IS_UPDATED)
        Environment.Humidity,Environment.Temperature = UpdateTempHumi(IS_UPDATED)

    def stop(self):

        if self.working:
            self.working = False
            if DEBUG == ON:
                print('Thread Exit.')


class ThreadUpdateChart(QThread,QMainWindow,Ui_ChartWindow):

    updatechart = QtCore.pyqtSignal(int)

    def __init__(self,mw):

        super(ThreadUpdateChart, self).__init__()

        self.mw = mw

        self.working = True

    def __del__(self):
        if usr_platform == "Windows":
            pass
        else:
            self.wait()

    def run(self):

        QApplication.processEvents()
        while self.working:

            self.updatechart.emit(self.mw.frameID)
            sleep(1.0)

    def stop(self):
        if self.working:
            self.working = False
            if DEBUG == ON:
                print('Thread Exit.')

def get_wheather():

    url = 'www.baidu.com'

    errortimes = 0

    try:
        if not os.system(pingurl + url):

            weather = []

            cityname = '扬州'

            url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + urllib.parse.quote(cityname)
            # 发出请求并读取到weather_data
            weather_data = urllib.request.urlopen(url).read()
            # 以utf-8的编码方式解压数据
            weather_data = gzip.decompress(weather_data).decode('utf-8')
            # 将json数据转化为dict数据
            weather_dict = json.loads(weather_data)

            if weather_dict.get('desc') == 'invilad-citykey':
                weather_info = '输入的城市名有误'
                return [weather_info, weather_info, weather_info, weather_info, weather_info]
            elif weather_dict.get('desc') == 'OK':
                forecasts = weather_dict.get('data').get('forecast')

                for forecast in forecasts:
                    weather_info = '城市：' + weather_dict.get('data').get('city') + '\n' \
                            + '日期：' + forecast.get('date') + '\n' \
                            + '温度：' + weather_dict.get('data').get('wendu') + '℃\n' \
                            + '高温：' + forecast.get('high') + '\n' \
                            + '低温: ' + forecast.get('low') + '\n' \
                            + '风向：' + forecast.get('fengxiang') + '\n' \
                            + '风力：' + forecast.get('fengli').replace('[CDATA', '[').replace('!', '') + '\n' \
                            + '天气：' + forecast.get('type') + '\n'

                    weather.append(weather_info)

                return weather

        else:
            weather_info = 'Failed to get weather\nPlease check the network'
            return [weather_info,weather_info,weather_info,weather_info,weather_info]

    except Exception as e:
        if DEBUG == ON:
            print(e)
        errortimes += 1
        if errortimes >= 2:
            weather_info = '城市：' + '无' + '\n' \
                        + '日期：' + '无' + '\n' \
                        + '温度：' + '无' + '℃\n' \
                        + '高温：' + "无" + '\n' \
                        + '低温: ' + '无' + '\n' \
                        + '风向：' + '无' + '\n' \
                        + '风力：' + '[无]' + '\n' \
                        + '天气：' + '无' + '\n'
            return [weather_info, weather_info, weather_info, weather_info, weather_info]

def SystemInit():

    if os.system(pingurl+'www.baidu.com'):
        if DEBUG == ON:
            print('fail')
        pass
    else:
        if DEBUG == ON:
            print('success')
        pass


if __name__ == "__main__":

    try:
        MainApplication()
    except Exception as e:
        if DEBUG == ON:
            print(e)





