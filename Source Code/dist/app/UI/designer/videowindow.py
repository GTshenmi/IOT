# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'videowindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import platform

class Ui_VideoWindow(object):
    def setupUi(self, VideoWindow):
        VideoWindow.setObjectName("VideoWindow")
        VideoWindow.resize(1920, 1080)
        VideoWindow.setMinimumSize(QtCore.QSize(60, 60))
        VideoWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        VideoWindow.setAutoFillBackground(False)
        VideoWindow.setStyleSheet("")
        VideoWindow.setIconSize(QtCore.QSize(60, 60))
        self.centralwidget = QtWidgets.QWidget(VideoWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pictureLabelbackground = QtWidgets.QLabel(self.centralwidget)
        self.pictureLabelbackground.setGeometry(QtCore.QRect(220, 123, 960, 720))
        self.pictureLabelbackground.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pictureLabelbackground.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.pictureLabelbackground.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pictureLabelbackground.setText("")
        self.pictureLabelbackground.setObjectName("pictureLabelbackground")
        self.shotButton = QtWidgets.QPushButton(self.centralwidget)
        self.shotButton.setGeometry(QtCore.QRect(652, 900, 96, 96))
        self.shotButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.shotButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.shotButton.setText("")
        self.shotButton.setAutoDefault(False)
        self.shotButton.setObjectName("shotButton")
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(1792, 8, 128, 64))
        self.exitButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.exitButton.setText("")
        self.exitButton.setObjectName("exitButton")
        self.resulttext = QtWidgets.QLabel(self.centralwidget)

        self.resulttext.setGeometry(QtCore.QRect(1330, 483, 451, 360))

        #self.resulttext.setGeometry(QtCore.QRect(1330,483,451,400))
        font = QtGui.QFont()
        font.setFamily("Rage Italic")
        font.setPointSize(20)

        if platform.system() == 'Windows':
           font.setPointSize(15)

        font.setUnderline(True)
        self.resulttext.setFont(font)
        self.resulttext.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.resulttext.setText("")
        self.resulttext.setTextFormat(QtCore.Qt.AutoText)
        self.resulttext.setObjectName("resulttext")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(1255, 80, 3, 1080))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.backgroundlabel = QtWidgets.QLabel(self.centralwidget)
        self.backgroundlabel.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        font = QtGui.QFont()
        font.setFamily("华文行楷")
        font.setPointSize(24)
        self.backgroundlabel.setFont(font)
        self.backgroundlabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.backgroundlabel.setText("")
        self.backgroundlabel.setObjectName("backgroundlabel")
        self.pictureLabel = QtWidgets.QLabel(self.centralwidget)
        self.pictureLabel.setGeometry(QtCore.QRect(250, 153, 900, 660))
        self.pictureLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pictureLabel.setText("")
        self.pictureLabel.setObjectName("pictureLabel")
        self.schoolbadge = QtWidgets.QLabel(self.centralwidget)
        self.schoolbadge.setGeometry(QtCore.QRect(1330, 123, 451, 200))
        font = QtGui.QFont()
        font.setFamily("Rage Italic")
        font.setPointSize(20)
        font.setUnderline(True)
        self.schoolbadge.setFont(font)
        self.schoolbadge.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.schoolbadge.setText("")
        self.schoolbadge.setTextFormat(QtCore.Qt.AutoText)
        self.schoolbadge.setObjectName("schoolbadge")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(1255, 430, 1200, 3))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.teammumber = QtWidgets.QLabel(self.centralwidget)
        self.teammumber.setGeometry(QtCore.QRect(1680, 920, 200, 120))
        font = QtGui.QFont()
        font.setFamily("Rage Italic")
        font.setPointSize(20)
        font.setUnderline(False)
        self.teammumber.setFont(font)
        self.teammumber.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.teammumber.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.teammumber.setText("")
        self.teammumber.setTextFormat(QtCore.Qt.AutoText)
        self.teammumber.setObjectName("teammumber")
        self.head = QtWidgets.QLabel(self.centralwidget)
        self.head.setGeometry(QtCore.QRect(0, 0, 1920, 80))
        self.head.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.head.setText("")
        self.head.setObjectName("head")
        self.wheatButton = QtWidgets.QPushButton(self.centralwidget)
        self.wheatButton.setGeometry(QtCore.QRect(0, 309, 128, 80))
        self.wheatButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.wheatButton.setText("")
        self.wheatButton.setObjectName("wheatButton")
        self.riceButton = QtWidgets.QPushButton(self.centralwidget)
        self.riceButton.setGeometry(QtCore.QRect(0, 575, 128, 80))
        self.riceButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.riceButton.setText("")
        self.riceButton.setObjectName("riceButton")
        self.showphotobutton = QtWidgets.QPushButton(self.centralwidget)
        self.showphotobutton.setGeometry(QtCore.QRect(420, 900, 96, 96))
        self.showphotobutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.showphotobutton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.showphotobutton.setText("")
        self.showphotobutton.setAutoDefault(False)
        self.showphotobutton.setObjectName("showphotobutton")
        self.reversebutton = QtWidgets.QPushButton(self.centralwidget)
        self.reversebutton.setGeometry(QtCore.QRect(884, 900, 96, 96))
        self.reversebutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.reversebutton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.reversebutton.setText("")
        self.reversebutton.setAutoDefault(False)
        self.reversebutton.setObjectName("reversebutton")
        self.ShowButton = QtWidgets.QPushButton(self.centralwidget)
        self.ShowButton.setGeometry(QtCore.QRect(1560, 900, 96, 96))
        self.ShowButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ShowButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.ShowButton.setText("")
        self.ShowButton.setAutoDefault(False)
        self.ShowButton.setObjectName("ShowButton")
        self.ShowTipsButton = QtWidgets.QPushButton(self.centralwidget)
        self.ShowTipsButton.setGeometry(QtCore.QRect(1186, 91, 64, 64))
        self.ShowTipsButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ShowTipsButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.ShowTipsButton.setText("")
        self.ShowTipsButton.setAutoDefault(False)
        self.ShowTipsButton.setObjectName("ShowTipsButton")
        self.TipsLabel = QtWidgets.QTextBrowser(self.centralwidget)
        self.TipsLabel.setGeometry(QtCore.QRect(1234, 123, 640, 720))
        self.TipsLabel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.TipsLabel.setObjectName("TipsLabel")

        self.backgroundlabel.raise_()
        self.pictureLabelbackground.raise_()
        self.shotButton.raise_()
        self.resulttext.raise_()
        self.pictureLabel.raise_()
        self.line.raise_()
        self.schoolbadge.raise_()
        self.line_2.raise_()
        self.teammumber.raise_()
        self.head.raise_()
        self.exitButton.raise_()
        self.wheatButton.raise_()
        self.riceButton.raise_()
        self.showphotobutton.raise_()
        self.reversebutton.raise_()
        self.ShowButton.raise_()
        self.ShowTipsButton.raise_()
        self.TipsLabel.raise_()
        VideoWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(VideoWindow)
        QtCore.QMetaObject.connectSlotsByName(VideoWindow)

    def retranslateUi(self, VideoWindow):
        _translate = QtCore.QCoreApplication.translate
        VideoWindow.setWindowTitle(_translate("VideoWindow", "MainWindow"))