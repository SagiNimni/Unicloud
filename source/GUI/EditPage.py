# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\nimni\PycharmProjects\Unicloud-VC\source\GUI\ui scripts\EditPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QFont
from GUI.AddAccount import Ui_Form as ac
from executables.utillty import handle_remove_readonly
import shutil
import ntpath
import configparser as cp


class Ui_Form(object):
    def setupUi(self, Form, currentDrive: list):
        self.currentDrive = currentDrive
        Form.setObjectName("Form")
        Form.resize(562, 414)
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.setFont(font)
        self.addAccount = QtWidgets.QToolButton(Form)
        self.addAccount.setGeometry(QtCore.QRect(500, 40, 25, 19))
        self.addAccount.setObjectName("addAccount")
        self.RemoveAccount = QtWidgets.QToolButton(Form)
        self.RemoveAccount.setGeometry(QtCore.QRect(500, 60, 25, 19))
        self.RemoveAccount.setObjectName("RemoveAccount")
        self.RemoveAccount.setEnabled(False)
        self.accountList = QtWidgets.QListWidget(Form)
        self.accountList.setGeometry(QtCore.QRect(70, 40, 431, 221))
        self.accountList.setObjectName("accountList")
        self.ApplyBtn = QtWidgets.QPushButton(Form)
        self.ApplyBtn.setGeometry(QtCore.QRect(434, 352, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        font.setPointSize(12)
        self.ApplyBtn.setFont(font)
        self.ApplyBtn.setObjectName("ApplyBtn")
        self.CancelBtn = QtWidgets.QPushButton(Form)
        self.CancelBtn.setGeometry(QtCore.QRect(300, 350, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        font.setPointSize(12)
        self.CancelBtn.setFont(font)
        self.CancelBtn.setObjectName("CancelBtn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.refreshList()

        self.addAccount.clicked.connect(self.openAddAccountWindow)
        self.CancelBtn.clicked.connect(Form.close)
        self.RemoveAccount.clicked.connect(self.removeAccount)
        self.accountList.itemActivated.connect(self.enableRemove)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.addAccount.setText(_translate("Form", "+"))
        self.RemoveAccount.setText(_translate("Form", "-"))
        self.ApplyBtn.setText(_translate("Form", "Apply"))
        self.CancelBtn.setText(_translate("Form", "Cancel"))

    def enableRemove(self):
        self.RemoveAccount.setEnabled(True)

    def openAddAccountWindow(self):
        self.addAccountWindow = QtWidgets.QWidget()
        self.ui = ac()
        self.ui.setupUi(self.addAccountWindow, self.currentDrive)
        self.addAccountWindow.show()

    def removeAccount(self):
        drive_type, username, path = self.accountList.currentItem().text().split('   ')
        shutil.rmtree(path, ignore_errors=False, onerror=handle_remove_readonly)
        config = cp.ConfigParser()
        config.read('mappedDrives.ini')
        section = self.currentDrive[0] + self.currentDrive[1]
        with open("mappedDrives.ini", 'w+') as f:
            try:
                for key, value in config.items(section, raw=True):
                    path_check, _ = ntpath.split(value)
                    if path_check == path:
                        number = key[-1::]
                        value = config[section]['account' + str(eval(number + "+1"))]
                        path, _ = ntpath.split(value)
                        config.set(section, 'account' + number, value)
            except KeyError:
                config.remove_option(section, 'account' + number)
                config.write(f)
                f.close()

                list_items = self.accountList.selectedItems()
                for item in list_items:
                    self.accountList.takeItem(self.accountList.row(item))
            except Exception as e:
                print(e)

    def refreshList(self):
        config = cp.ConfigParser()
        config.read("mappedDrives.ini")
        section = self.currentDrive[0] + self.currentDrive[1]
        for i in range(1, 10):
            try:
                path = config[section]["account" + str(i)]
                folder_name, _ = ntpath.split(path)
                config2 = cp.ConfigParser()
                config2.read(path)
                cloud_type = eval("Cloud('{0}').name".format(config2['accountSettings']['type']))
                username = config2['accountSettings']['username']
                new_item = "{0}:   {1}   {2}".format(cloud_type, username, folder_name)
                item = self.accountList.findItems(new_item, Qt.Qt.MatchFlag.MatchRecursive)
                if not item:
                    item = QtWidgets.QListWidgetItem(new_item)
                    item.setFont(QFont("Segoe UI", 12, QFont.StyleItalic))
                    item.setTextAlignment(QtCore.Qt.AlignLeft)
                    self.accountList.addItem(item)
            except KeyError:
                break


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
