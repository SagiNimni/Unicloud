from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject
import configparser as cp
from GUI.errors import BlankSpaceError
from BuildDiskDrive import buildSkeleton
import definitions


class Ui_Form(QObject):
    done = pyqtSignal()
    MESSAGE = None

    def setupUi(self, Form, currentDrive: list):
        self.currentDrive = currentDrive
        Form.setObjectName("Form")
        Form.resize(562, 415)
        self.typeEdit = QtWidgets.QComboBox(Form)
        self.typeEdit.setGeometry(QtCore.QRect(130, 80, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.typeEdit.setFont(font)
        self.typeEdit.setObjectName("typeEdit")
        self.typeEdit.addItem("")
        self.typeEdit.addItem("")
        self.typeEdit.addItem("")
        self.typeLbl = QtWidgets.QLabel(Form)
        self.typeLbl.setGeometry(QtCore.QRect(30, 80, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.typeLbl.setFont(font)
        self.typeLbl.setObjectName("typeLbl")
        self.usernameLbl = QtWidgets.QLabel(Form)
        self.usernameLbl.setEnabled(True)
        self.usernameLbl.setGeometry(QtCore.QRect(30, 180, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.usernameLbl.setFont(font)
        self.usernameLbl.setObjectName("usernameLbl")
        self.usernameEdit = QtWidgets.QTextEdit(Form)
        self.usernameEdit.setEnabled(True)
        self.usernameEdit.setGeometry(QtCore.QRect(130, 180, 201, 31))
        self.usernameEdit.setObjectName("usernameEdit")
        self.browseBtn = QtWidgets.QToolButton(Form)
        self.browseBtn.setEnabled(True)
        self.browseBtn.setGeometry(QtCore.QRect(330, 240, 25, 19))
        self.browseBtn.setObjectName("browseBtn")
        self.credantialsEdit = QtWidgets.QLineEdit(Form)
        self.credantialsEdit.setEnabled(True)
        self.credantialsEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.credantialsEdit.setGeometry(QtCore.QRect(130, 230, 201, 31))
        self.credantialsEdit.setObjectName("credantialsEdit")
        self.credantialsLbl = QtWidgets.QLabel(Form)
        self.credantialsLbl.setEnabled(True)
        self.credantialsLbl.setGeometry(QtCore.QRect(30, 230, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.credantialsLbl.setFont(font)
        self.credantialsLbl.setObjectName("credantialsLbl")
        self.passwordLbl = QtWidgets.QLabel(Form)
        self.passwordLbl.setGeometry(QtCore.QRect(30, 230, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.passwordLbl.setFont(font)
        self.passwordLbl.setObjectName("passwordLbl")
        self.passwordLbl.close()
        self.doneBtn = QtWidgets.QPushButton(Form)
        self.doneBtn.setGeometry(QtCore.QRect(440, 360, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doneBtn.setFont(font)
        self.doneBtn.setObjectName("doneBtn")
        self.cancelBtn = QtWidgets.QPushButton(Form)
        self.cancelBtn.setGeometry(QtCore.QRect(320, 360, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cancelBtn.setFont(font)
        self.cancelBtn.setObjectName("cancelBtn")
        self.tokenLbl = QtWidgets.QLabel(Form)
        self.tokenLbl.setGeometry(QtCore.QRect(30, 230, 91, 31))
        self.tokenLbl.close()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tokenLbl.setFont(font)
        self.tokenLbl.setObjectName("tokenLbl")
        self.nameLbl = QtWidgets.QLabel(Form)
        self.nameLbl.setEnabled(True)
        self.nameLbl.setGeometry(QtCore.QRect(20, 280, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameLbl.setFont(font)
        self.nameLbl.setObjectName("nameLbl")
        self.nameEdit = QtWidgets.QTextEdit(Form)
        self.nameEdit.setEnabled(True)
        self.nameEdit.setGeometry(QtCore.QRect(130, 280, 201, 31))
        Form.setWindowModality(QtCore.Qt.ApplicationModal)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.browseBtn.clicked.connect(self.browseForPath)
        self.typeEdit.currentTextChanged.connect(self.changeCloudType)
        self.doneBtn.clicked.connect(self.addAccountApproved)
        self.doneBtn.clicked.connect(Form.close)
        self.cancelBtn.clicked.connect(Form.close)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.typeEdit.setItemText(0, _translate("Form", "Google Drive"))
        self.typeEdit.setItemText(1, _translate("Form", "Dropbox"))
        self.typeEdit.setItemText(2, _translate("Form", "Mega Upload"))
        self.typeLbl.setText(_translate("Form", "Cloud Type:"))
        self.usernameLbl.setText(_translate("Form", "Username:"))
        self.browseBtn.setText(_translate("Form", "..."))
        self.credantialsLbl.setText(_translate("Form", "Credantials:"))
        self.passwordLbl.setText(_translate("Form", "Password:"))
        self.doneBtn.setText(_translate("Form", "Done"))
        self.cancelBtn.setText(_translate("Form", "Cancel"))
        self.tokenLbl.setText(_translate("Form", "Token Key:"))
        self.nameLbl.setText(_translate("Form", "Folder Name:"))

    def changeCloudType(self):
        def check_previous_type():
            if self.passwordLbl.isVisible():
                return "Mega Upload"
            elif self.credantialsLbl.isVisible():
                return "Google Drive"
            elif self.tokenLbl.isVisible():
                return "Dropbox"

        current_type = self.typeEdit.currentText()
        previous_type = check_previous_type()
        if previous_type == "Mega Upload":
            self.passwordLbl.close()
            if current_type == "Google Drive":
                self.credantialsLbl.show()
                self.browseBtn.show()
            elif current_type == "Dropbox":
                self.tokenLbl.show()
        elif previous_type == "Google Drive":
            self.browseBtn.close()
            self.credantialsLbl.close()
            if current_type == "Mega Upload":
                self.passwordLbl.show()
            elif current_type == "Dropbox":
                self.tokenLbl.show()
        elif previous_type == "Dropbox":
            self.tokenLbl.close()
            if current_type == "Google Drive":
                self.credantialsLbl.show()
                self.browseBtn.show()
            elif current_type == "Mega Upload":
                self.passwordLbl.show()

    def browseForPath(self):
        cred_dir, _ = QtWidgets.QFileDialog.getOpenFileUrl(None, 'Inset Credantials', '', 'credantials files (*.json)')
        self.credantialsEdit.setPlainText(cred_dir.path()[1:])

    def addAccountApproved(self):
        try:
            if self.credantialsEdit.text() == '':
                raise BlankSpaceError
            if self.usernameEdit.toPlainText() == '':
                raise BlankSpaceError
            if self.nameEdit.toPlainText() == '':
                raise BlankSpaceError
            account_directory = self.currentDrive[0] + "/" + self.nameEdit.toPlainText()
            cloud_type = self.typeEdit.currentText().replace(' ', '')
            credentials = self.credantialsEdit.text()
            username = self.usernameEdit.toPlainText()
            self.MESSAGE = 'add,' + username + ',' + credentials + ',' + cloud_type + ',' + self.nameEdit.toPlainText()
            buildSkeleton.establishUnicloudConnectionToFolder(account_directory, username, credentials, cloud_type)
        except BlankSpaceError:
            box = QMessageBox()
            box.setIcon(QMessageBox.Warning)
            box.setWindowTitle('Missing Arguments')
            box.setText('Please fill all the text boxes')
            box.setStandardButtons(QMessageBox.Ok)
            box.setDefaultButton(QMessageBox.Ok)
            button = box.button(QMessageBox.Ok)
            button.setText('Close')
            box.exec_()
            return
        except FileNotFoundError:
            box = QMessageBox()
            box.setIcon(QMessageBox.Warning)
            box.setWindowTitle('credentials error')
            box.setText("The credntials path you entered doesn't exist")
            box.setStandardButtons(QMessageBox.Ok)
            box.setDefaultButton(QMessageBox.Ok)
            button = box.button(QMessageBox.Ok)
            button.setText('Close')
            box.exec_()
            return
        except Exception as e:
            box = QMessageBox()
            box.setIcon(QMessageBox.Warning)
            box.setWindowTitle('Error')
            box.setText(str(e))
            box.setStandardButtons(QMessageBox.Ok)
            box.setDefaultButton(QMessageBox.Ok)
            button = box.button(QMessageBox.Ok)
            button.setText('Close')
            box.exec_()
            return

        config = cp.ConfigParser()
        config.read(definitions.DRIVES_LIST_DIR)
        section = self.currentDrive[1]
        key = None
        try:
            for i in range(1, 10):
                key = 'account' + str(i)
                config[section][key]
        except KeyError:
            config.set(section, key, account_directory + "/account.ini")
            with open(definitions.DRIVES_LIST_DIR, 'w+') as f:
                config.write(f)
                f.close()
            self.done.emit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
