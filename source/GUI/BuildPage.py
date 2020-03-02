# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\nimni\PycharmProjects\Unicloud-VC\source\GUI\ui scripts\BuildPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


import configparser as cp
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject
from WindowsManagement.VirtualDisk import MappedDrive

MESSAGE = None


class Ui_Form(QObject):
    done = pyqtSignal()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(559, 446)
        self.letterLbl = QtWidgets.QLabel(Form)
        self.letterLbl.setGeometry(QtCore.QRect(30, 190, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.letterLbl.setFont(font)
        self.letterLbl.setObjectName("letterLbl")
        self.letterBox = QtWidgets.QComboBox(Form)
        self.letterBox.setGeometry(QtCore.QRect(180, 190, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        font.setPointSize(11)
        self.letterBox.setFont(font)
        self.letterBox.setObjectName("letterBox")
        self.letterBox.addItem("")
        self.letterBox.addItem("")
        self.letterBox.addItem("")
        self.letterBox.addItem("")
        self.letterBox.addItem("")
        self.nameLbl = QtWidgets.QLabel(Form)
        self.nameLbl.setGeometry(QtCore.QRect(30, 240, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameLbl.setFont(font)
        self.nameLbl.setObjectName("nameLbl")
        self.nameEdit = QtWidgets.QTextEdit(Form)
        self.nameEdit.setGeometry(QtCore.QRect(180, 240, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameEdit.setFont(font)
        self.nameEdit.setObjectName("nameEdit")
        self.directortyLbl = QtWidgets.QLabel(Form)
        self.directortyLbl.setGeometry(QtCore.QRect(30, 290, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.directortyLbl.setFont(font)
        self.directortyLbl.setObjectName("directortyLbl")
        self.directoryEdit = QtWidgets.QTextEdit(Form)
        self.directoryEdit.setGeometry(QtCore.QRect(180, 290, 331, 31))
        self.directoryEdit.setObjectName("directoryEdit")
        self.browseBtn = QtWidgets.QToolButton(Form)
        self.browseBtn.setGeometry(QtCore.QRect(510, 300, 25, 21))
        self.browseBtn.setObjectName("browseBtn")
        self.CreateBtn = QtWidgets.QPushButton(Form)
        self.CreateBtn.setGeometry(QtCore.QRect(410, 390, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CreateBtn.setFont(font)
        self.CreateBtn.setObjectName("CreateBtn")
        self.cancelBtn = QtWidgets.QPushButton(Form)
        self.cancelBtn.setGeometry(QtCore.QRect(300, 390, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cancelBtn.setFont(font)
        self.cancelBtn.setObjectName("cancelBtn")
        self.usernameLbl = QtWidgets.QLabel(Form)
        self.usernameLbl.setEnabled(True)
        self.usernameLbl.setGeometry(QtCore.QRect(30, 70, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.usernameLbl.setFont(font)
        self.usernameLbl.setObjectName("usernameLbl")
        self.passwordLbl = QtWidgets.QLabel(Form)
        self.passwordLbl.setGeometry(QtCore.QRect(30, 110, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.passwordLbl.setFont(font)
        self.passwordLbl.setObjectName("passwordLbl")
        self.usernameEdit = QtWidgets.QTextEdit(Form)
        self.usernameEdit.setEnabled(True)
        self.usernameEdit.setGeometry(QtCore.QRect(120, 70, 201, 31))
        self.usernameEdit.setObjectName("usernameEdit")
        self.passwordEdit = QtWidgets.QLineEdit(Form)
        self.passwordEdit.setEnabled(True)
        self.passwordEdit.setGeometry(QtCore.QRect(120, 110, 201, 31))
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.browseBtn.clicked.connect(self.browseForPath)
        self.CreateBtn.clicked.connect(self.buildDrive)
        self.cancelBtn.clicked.connect(Form.close)
        self.done.connect(Form.close)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.letterLbl.setText(_translate("Form", "Enter Drive Letter:"))
        self.letterBox.setItemText(0, _translate("Form", "U:"))
        self.letterBox.setItemText(1, _translate("Form", "Q:"))
        self.letterBox.setItemText(2, _translate("Form", "T:"))
        self.letterBox.setItemText(3, _translate("Form", "E:"))
        self.letterBox.setItemText(4, _translate("Form", "P:"))
        self.nameLbl.setText(_translate("Form", "Enter Drive Name:"))
        self.directortyLbl.setText(_translate("Form", "Enter directory:"))
        self.browseBtn.setText(_translate("Form", "..."))
        self.CreateBtn.setText(_translate("Form", "Create Account"))
        self.cancelBtn.setText(_translate("Form", "Cancel"))
        self.usernameLbl.setText(_translate("Form", "Username:"))
        self.passwordLbl.setText(_translate("Form", "Password:"))

    def browseForPath(self):
        folder_dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select folder', '',
                                                                QtWidgets.QFileDialog.ShowDirsOnly)
        self.directoryEdit.setPlainText(folder_dir)

    def buildDrive(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Create Drive')
        box.setText('Are you sure you want to create this drive?')
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setDefaultButton(QMessageBox.No)
        button_yes = box.button(QMessageBox.Yes)
        button_yes.setText('Ok')
        button_no = box.button(QMessageBox.No)
        button_no.setText('Cancel')
        box.exec_()
        username, password = self.usernameEdit.toPlainText(), self.passwordEdit.text()
        letter, dr, name = self.letterBox.currentText(), self.directoryEdit.toPlainText(), self.nameEdit.toPlainText()
        if dr != '' and name != '' and username != '' and password != '':
            if box.clickedButton() == button_yes:
                global MESSAGE
                MESSAGE = username + "," + password
                config = cp.ConfigParser()
                config.read('mappedDrives.ini')
                sections = config.sections()
                if username not in sections:
                    # MappedDrive(letter, dr, name)
                    config.add_section(username)
                    config.set(username, 'disk', letter + name)
                    with open("mappedDrives.ini", "w+") as f:
                        config.write(f)
                        self.done.emit()
        else:
            box = QMessageBox()
            box.setIcon(QMessageBox.Warning)
            box.setWindowTitle('Missing Arguments')
            box.setText('Please fill all the text boxes')
            box.setStandardButtons(QMessageBox.Ok)
            box.setDefaultButton(QMessageBox.Ok)
            button = box.button(QMessageBox.Ok)
            button.setText('Close')
            box.exec_()


def change_message(new_message):
    global MESSAGE
    MESSAGE = new_message


def get_message():
    return MESSAGE


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())