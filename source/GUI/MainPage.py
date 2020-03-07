# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\nimni\PycharmProjects\Unicloud-VC\source\GUI\ui scripts\mainPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, QObject, QMutexLocker, QMutex
from GUI.BuildPage import Ui_Form as bp
from GUI.EditPage import Ui_Form as ep
from GUI.BuildPage import get_message, set_message
import configparser as cp
import socket

HOST_IP = "10.100.102.16"
HOST_PORT = 20
BUFFER = 1024
MESSAGE = None

BUILD_PAGE_ON = False
LOCK = QMutex()
LOCK.lock()
LOCK2 = QMutex()
LOCK2.lock()


class ConnectAndLoginThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global HOST_PORT, HOST_IP, BUFFER, MESSAGE, LOCK
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST_IP, HOST_PORT))
        print("Connected to server")

        should_lock = False
        while True:
            if should_lock:
                LOCK.lock()
                should_lock = False
            print("test")
            with QMutexLocker(LOCK):
                should_lock = True
                if MESSAGE is not None:
                    print("sent " + MESSAGE)
                    self.client.send(MESSAGE.encode())
                    MESSAGE = None
                    while True:
                        response = self.client.recv(BUFFER).decode()
                        if response == 'ack':
                            print('sign up')
                            self.sign_up()
                            break

    def sign_up(self):
        global MESSAGE, LOCK2, BUILD_PAGE_ON
        while True:
            with QMutexLocker(LOCK2):
                print("sign up lock release")
                if not BUILD_PAGE_ON:
                    print("force exist")
                    break
                MESSAGE = get_message()
                if MESSAGE is not None:
                    print("sent " + MESSAGE)
                    self.client.send(MESSAGE.encode())
                    MESSAGE = None
                    set_message(None)
                    while True:
                        if self.client.recv(BUFFER).decode() == 'ack':
                            break
                    print("exit create loop")
                    break
        self.client.send('end'.encode())
        LOCK2.lock()


class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(788, 533)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-image: url(:/newPrefix/background.jpg);")
        self.centralwidget.setObjectName("centralwidget")
        self.drivesList = QtWidgets.QListWidget(self.centralwidget)
        self.drivesList.setGeometry(QtCore.QRect(90, 80, 621, 192))
        self.drivesList.setObjectName("drivesList")
        self.removeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.removeBtn.setGeometry(QtCore.QRect(580, 390, 141, 101))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.removeBtn.setFont(font)
        self.removeBtn.setIconSize(QtCore.QSize(16, 16))
        self.removeBtn.setObjectName("removeBtn")
        self.buildBtn = QtWidgets.QPushButton(self.centralwidget)
        self.buildBtn.setGeometry(QtCore.QRect(320, 390, 141, 101))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.buildBtn.setFont(font)
        self.buildBtn.setIconSize(QtCore.QSize(16, 16))
        self.buildBtn.setObjectName("buildBtn")
        self.editBtn = QtWidgets.QPushButton(self.centralwidget)
        self.editBtn.setGeometry(QtCore.QRect(80, 390, 141, 101))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.editBtn.setFont(font)
        self.editBtn.setIconSize(QtCore.QSize(16, 16))
        self.editBtn.setObjectName("editBtn")
        self.editBtn.setEnabled(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.refreshList()
        self.client = ConnectAndLoginThread()
        self.client.start()

        self.buildBtn.clicked.connect(self.openBuildWindow)
        self.editBtn.clicked.connect(self.openEditWindow)
        self.drivesList.itemActivated.connect(self.enableEditBtn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.removeBtn.setText(_translate("MainWindow", "Login"))
        self.buildBtn.setText(_translate("MainWindow", "Sign Up"))
        self.editBtn.setText(_translate("MainWindow", "Edit Account"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))

    def openBuildWindow(self):
        global MESSAGE, BUILD_PAGE_ON, LOCK
        MESSAGE = 'create'
        BUILD_PAGE_ON = True
        self.buildWindow = QtWidgets.QWidget()
        self.ui = bp()
        self.ui.setupUi(self.buildWindow)
        self.ui.done.connect(LOCK2.unlock)
        self.ui.closed.connect(self.disableBuildPage)
        self.buildWindow.show()
        self.refreshList()
        LOCK.unlock()

    def openEditWindow(self):
        self.editWIndow = QtWidgets.QWidget()
        self.ui = ep()
        diskDrive = self.drivesList.currentItem().text().split(' ')
        self.ui.setupUi(self.editWindow, diskDrive)
        self.editWindow.show()

    def refreshList(self):
        config = cp.ConfigParser()
        config.read("mappedDrives.ini")
        sections = config.sections()
        for s in sections:
            item = self.drivesList.findItems(s, Qt.Qt.MatchFlag.MatchRecursive)
            if not item:
                item = QtWidgets.QListWidgetItem(s)
                item.setFont(QFont("Segoe UI", 12, QFont.StyleItalic))
                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.drivesList.addItem(item)

    def enableEditBtn(self):
        self.editBtn.setEnabled(True)

    @staticmethod
    def disableBuildPage():
        global BUILD_PAGE_ON, LOCK2
        LOCK2.unlock()
        BUILD_PAGE_ON = False


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
