# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chartwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChartWindow(object):
    def setupUi(self, ChartWindow):
        ChartWindow.setObjectName("ChartWindow")
        ChartWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(ChartWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(360, 160, 1200, 800))
        self.groupBox.setObjectName("groupBox")
        self.backlabel = QtWidgets.QLabel(self.groupBox)
        self.backlabel.setGeometry(QtCore.QRect(100, 100, 1000, 600))
        self.backlabel.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.backlabel.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.backlabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.backlabel.setText("")
        self.backlabel.setObjectName("backlabel")
        self.showchartlabel = QtWidgets.QLabel(self.groupBox)
        self.showchartlabel.setGeometry(QtCore.QRect(200, 120, 800, 400))
        self.showchartlabel.setFrameShape(QtWidgets.QFrame.Box)
        self.showchartlabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.showchartlabel.setText("")
        self.showchartlabel.setObjectName("showchartlabel")
        self.leftButton = QtWidgets.QPushButton(self.groupBox)
        self.leftButton.setGeometry(QtCore.QRect(18, 336, 64, 64))
        self.leftButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.leftButton.setText("")
        self.leftButton.setObjectName("leftButton")
        self.rightButton = QtWidgets.QPushButton(self.groupBox)
        self.rightButton.setGeometry(QtCore.QRect(1118, 336, 64, 64))
        self.rightButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rightButton.setText("")
        self.rightButton.setObjectName("rightButton")
        self.TempLabel = QtWidgets.QLabel(self.groupBox)
        self.TempLabel.setGeometry(QtCore.QRect(200, 520, 400, 160))
        self.TempLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.TempLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.TempLabel.setText("")
        self.TempLabel.setObjectName("TempLabel")
        self.HumiLabel = QtWidgets.QLabel(self.groupBox)
        self.HumiLabel.setGeometry(QtCore.QRect(600, 520, 400, 160))
        self.HumiLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.HumiLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.HumiLabel.setText("")
        self.HumiLabel.setObjectName("HumiLabel")
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(1792, 8, 128, 64))
        self.exitButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.exitButton.setText("")
        self.exitButton.setObjectName("exitButton")
        self.head = QtWidgets.QLabel(self.centralwidget)
        self.head.setGeometry(QtCore.QRect(0, 0, 1920, 80))
        self.head.setText("")
        self.head.setObjectName("head")
        self.backgroundlabel = QtWidgets.QLabel(self.centralwidget)
        self.backgroundlabel.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.backgroundlabel.setText("")
        self.backgroundlabel.setObjectName("backgroundlabel")
        self.backgroundlabel.raise_()
        self.groupBox.raise_()
        self.head.raise_()
        self.exitButton.raise_()
        ChartWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ChartWindow)
        QtCore.QMetaObject.connectSlotsByName(ChartWindow)

    def retranslateUi(self, ChartWindow):
        _translate = QtCore.QCoreApplication.translate
        ChartWindow.setWindowTitle(_translate("ChartWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("ChartWindow", "温湿度变化曲线"))
