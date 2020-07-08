import sys
import os
conf_path = os.getcwd()
sys.path.append(conf_path)
sys.path.append(conf_path + r'\scripts\Setup')

from Crypto.Cipher import AES
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, QObject, QMutexLocker, QMutex
from PyQt5.QtWidgets import QMessageBox
from GUI.BuildPage import Ui_Form as bp
from GUI.EditPage import Ui_Form as ep
from GUI.LoginPage import Ui_Form as lp
from GUI.BuildPage import get_message, set_message
from GUI.LoginPage import get_message as b_get_message, set_message as b_set_message
from BuildDiskDrive import buildSkeleton
import configparser as cp
import socket
import definitions

HOST_IP = "10.100.102.10"
HOST_PORT = 20
BUFFER = 1024
MESSAGE = None

PAGE_ON = False
LOCK = QMutex()
LOCK.lock()
LOCK2 = QMutex()
LOCK2.lock()


class ConnectAndLoginThread(QThread):
    def __init__(self, ui):
        QThread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ui = ui

    def run(self):
        """
        start the thread of the client and waits for the users requests
        """
        global HOST_PORT, HOST_IP, BUFFER, MESSAGE, LOCK
        self.client.connect((HOST_IP, HOST_PORT))
        print("Connected to server")

        should_lock = False
        while True:
            try:
                if should_lock:
                    LOCK.lock()
                    should_lock = False
                print("test")
                with QMutexLocker(LOCK):
                    should_lock = True
                    if MESSAGE is not None:
                        print("sent " + MESSAGE)
                        self.client.send(MESSAGE.encode())
                        while True:
                            response = self.client.recv(BUFFER).decode()
                            if response == 'ack':
                                if MESSAGE == 'create':
                                    MESSAGE = None
                                    print('sign up')
                                    self.sign_up()
                                    break
                                elif MESSAGE == 'login':
                                    MESSAGE = None
                                    print('login')
                                    self.login()
                                    break
                                elif MESSAGE == 'edit':
                                    MESSAGE = None
                                    print('edit')
                                    self.edit()
                                    break

            except Exception as e:
                print(e)
                self.close()

    def sign_up(self):
        """
        starts the sign up function loop until a success
        or abort
        """
        global MESSAGE, LOCK2, PAGE_ON, BUFFER
        while True:
            with QMutexLocker(LOCK2):
                print("sign up lock release")
                if not PAGE_ON:
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
        self.ui.refreshList()
        LOCK2.lock()

    def login(self):
        """
        starts the login function loop until a success
        or abort
        """
        global MESSAGE, LOCK2, BUFFER, PAGE_ON
        while True:
            with QMutexLocker(LOCK2):
                print("login lock release")
                if not PAGE_ON:
                    print("force exist")
                    break
                MESSAGE = b_get_message()
                if MESSAGE is not None:
                    print("sent " + MESSAGE)
                    self.client.send(MESSAGE.encode())
                    unicloud_username = MESSAGE.split(',')[0]
                    item = self.ui.drivesList.findItems(unicloud_username, Qt.Qt.MatchFlag.MatchRecursive)
                    MESSAGE = None
                    b_set_message(None)
                    if not item:
                        while True:
                            response = self.client.recv(BUFFER).decode()
                            if response == 'wrong':
                                config = cp.ConfigParser()
                                config.read(definitions.DRIVES_LIST_DIR)
                                config.remove_section(unicloud_username)
                                with open(definitions.DRIVES_LIST_DIR, 'w+') as f:
                                    config.write(f)
                                print('wrong')
                                break
                            else:
                                print(response)
                                config = cp.ConfigParser()
                                config.read(definitions.DRIVES_LIST_DIR)
                                for account in eval(response):
                                    username, password, drive_type, folder_name = account
                                    account_dir = config.get(unicloud_username, 'disk').split(':')[0] + ':/' + folder_name
                                    buildSkeleton.establishUnicloudConnectionToFolder(account_dir, username, password, drive_type)
                                print("success")
                                break
                        print("exit login loop")
                        break
                    else:
                        print('already exists')
                        break
        self.client.send('end'.encode())
        self.ui.refreshList()
        LOCK2.lock()

    def edit(self):
        """
          starts the edit function loop until a success
          or abort
          """
        global BUFFER, MESSAGE, LOCK2, BUFFER, PAGE_ON
        while True:
            with QMutexLocker(LOCK2):
                print("add lock realese")
                if not PAGE_ON:
                    self.client.send('end'.encode())
                    print("force exist")
                    break
                if self.ui.ui.MESSAGE2:
                    for i in range(len(self.ui.ui.MESSAGE2)):
                        MESSAGE = self.ui.ui.MESSAGE2[i] + ',' + definitions.MAC_ADDRESS
                        print('sent ' + MESSAGE)
                        self.client.send(MESSAGE.encode())
                        MESSAGE = None
                        while True:
                            response = self.client.recv(BUFFER).decode()
                            if response == 'success':
                                if i < len(self.ui.ui.MESSAGE2) - 1:
                                    self.client.send('again'.encode())
                                else:
                                    self.client.send('end'.encode())
                                break
                    print('exit edit loop')
                    break
        LOCK2.lock()

    def close(self):
        global BUFFER
        self.client.send('disconnect'.encode())
        while True:
            if self.client.recv(BUFFER).decode() == 'end':
                self.client.close()
                print('disconnected')
                break


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
        self.loginBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loginBtn.setGeometry(QtCore.QRect(580, 390, 141, 101))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.loginBtn.setFont(font)
        self.loginBtn.setIconSize(QtCore.QSize(16, 16))
        self.loginBtn.setObjectName("removeBtn")
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
        self.client = ConnectAndLoginThread(self)
        self.client.start()

        self.loginBtn.clicked.connect(self.openLoginWindow)
        self.buildBtn.clicked.connect(self.openBuildWindow)
        self.editBtn.clicked.connect(self.openEditWindow)
        self.drivesList.itemActivated.connect(self.enableEditBtn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loginBtn.setText(_translate("MainWindow", "Login"))
        self.buildBtn.setText(_translate("MainWindow", "Sign Up"))
        self.editBtn.setText(_translate("MainWindow", "Edit Account"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))

    def openBuildWindow(self):
        global MESSAGE, PAGE_ON, LOCK, LOCK2
        MESSAGE = 'create'
        PAGE_ON = True
        self.buildWindow = QtWidgets.QWidget()
        self.ui = bp()
        self.ui.setupUi(self.buildWindow)
        self.ui.done.connect(LOCK2.unlock)
        self.ui.closed.connect(self.disableAdditionalPage)
        self.buildWindow.show()
        LOCK.unlock()

    def openEditWindow(self):
        global MESSAGE, PAGE_ON, LOCK, LOCK2
        MESSAGE = 'edit'
        PAGE_ON = True
        self.editWindow = QtWidgets.QWidget()
        self.ui = ep()
        self.ui.setupUi(self.editWindow, self.drivesList.currentItem().text())
        self.ui.add.connect(LOCK2.unlock)
        self.ui.closed.connect(self.disableAdditionalPage)
        self.editWindow.show()
        LOCK.unlock()

    def openLoginWindow(self):
        global MESSAGE, LOCK2, LOCK, PAGE_ON
        MESSAGE = 'login'
        PAGE_ON = True
        self.loginWindow = QtWidgets.QWidget()
        self.ui = lp()
        self.ui.setupUi(self.loginWindow)
        self.ui.done.connect(LOCK2.unlock)
        self.ui.close.connect(self.disableAdditionalPage)
        self.loginWindow.show()
        LOCK.unlock()

    def refreshList(self):
        config = cp.ConfigParser()
        config.read(definitions.DRIVES_LIST_DIR)
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

    def disableAdditionalPage(self):
        global PAGE_ON, LOCK2
        self.refreshList()
        LOCK2.unlock()
        PAGE_ON = False


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    app.aboutToQuit.connect(ui.client.close)
    MainWindow.show()
    sys.exit(app.exec_())
