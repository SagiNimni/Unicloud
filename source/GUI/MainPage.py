# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\nimni\PycharmProjects\Unicloud-VC\source\GUI\ui scripts\mainPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QFont
from GUI.BuildPage import Ui_Form as bp
from GUI.EditPage import Ui_Form as ep
import configparser as cp


class Ui_MainWindow(object):
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

        self.buildBtn.clicked.connect(self.openBuildWindow)
        self.editBtn.clicked.connect(self.openEditWindow)
        self.drivesList.itemActivated.connect(self.enableEditBtn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.removeBtn.setText(_translate("MainWindow", "Remove Drive"))
        self.buildBtn.setText(_translate("MainWindow", "Build New Drive"))
        self.editBtn.setText(_translate("MainWindow", "Edit Drive"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))

    def openBuildWindow(self):
        self.buildWindow = QtWidgets.QWidget()
        self.ui = bp()
        self.ui.setupUi(self.buildWindow)
        self.buildWindow.show()
        self.refreshList()

    def openEditWindow(self):
        self.editWindow = QtWidgets.QWidget()
        self.ui = ep()
        diskDrive = self.drivesList.currentItem().text().split(' ')
        self.ui.setupUi(self.editWindow, diskDrive)
        self.editWindow.show()

    def refreshList(self):
        config = cp.ConfigParser()
        config.read("mappedDrives.ini")
        sections = config.sections()
        for s in sections:
            s = s.replace(':', ': ')
            item = self.drivesList.findItems(s, Qt.Qt.MatchFlag.MatchRecursive)
            if not item:
                item = QtWidgets.QListWidgetItem(s)
                item.setFont(QFont("Segoe UI", 12, QFont.StyleItalic))
                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.drivesList.addItem(item)

    def enableEditBtn(self):
        self.editBtn.setEnabled(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
