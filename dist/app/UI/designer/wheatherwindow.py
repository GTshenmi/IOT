# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wheatherwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WheatherWindow(object):
    def setupUi(self, WheatherWindow):
        WheatherWindow.setObjectName("WheatherWindow")
        WheatherWindow.resize(1920, 1080)
        WheatherWindow.setMinimumSize(QtCore.QSize(60, 60))
        WheatherWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        WheatherWindow.setAutoFillBackground(False)
        WheatherWindow.setStyleSheet("")
        WheatherWindow.setIconSize(QtCore.QSize(60, 60))
        self.centralwidget = QtWidgets.QWidget(WheatherWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pictureLabelbackground = QtWidgets.QLabel(self.centralwidget)
        self.pictureLabelbackground.setGeometry(QtCore.QRect(220, 150, 960, 720))
        self.pictureLabelbackground.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pictureLabelbackground.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.pictureLabelbackground.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pictureLabelbackground.setText("")
        self.pictureLabelbackground.setObjectName("pictureLabelbackground")
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(1792, 8, 128, 64))
        self.exitButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.exitButton.setText("")
        self.exitButton.setObjectName("exitButton")
        self.wheatherbox = QtWidgets.QLabel(self.centralwidget)
        self.wheatherbox.setGeometry(QtCore.QRect(1330, 150, 451, 720))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        font.setUnderline(False)
        self.wheatherbox.setFont(font)
        self.wheatherbox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.wheatherbox.setText("")
        self.wheatherbox.setTextFormat(QtCore.Qt.AutoText)
        self.wheatherbox.setObjectName("wheatherbox")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(1255, 107, 3, 1080))
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
        self.PictureLabel = QtWidgets.QLabel(self.centralwidget)
        self.PictureLabel.setGeometry(QtCore.QRect(250, 180, 900, 660))
        self.PictureLabel.setText("")
        self.PictureLabel.setObjectName("PictureLabel")
        self.backgroundlabel.raise_()
        self.pictureLabelbackground.raise_()
        self.wheatherbox.raise_()
        self.line.raise_()
        self.teammumber.raise_()
        self.head.raise_()
        self.exitButton.raise_()
        self.PictureLabel.raise_()
        WheatherWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(WheatherWindow)
        QtCore.QMetaObject.connectSlotsByName(WheatherWindow)

    def retranslateUi(self, WheatherWindow):
        _translate = QtCore.QCoreApplication.translate
        WheatherWindow.setWindowTitle(_translate("WheatherWindow", "MainWindow"))
