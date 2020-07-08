from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
from WindowsManagement.VirtualDisk import MappedDrive
import configparser as cp
import hashlib
import definitions

FORM = None
MESSAGE = None


class Ui_Form(QObject):
    close = pyqtSignal()
    done = pyqtSignal()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(558, 445)
        self.directortyLbl = QtWidgets.QLabel(Form)
        self.directortyLbl.setGeometry(QtCore.QRect(30, 290, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.directortyLbl.setFont(font)
        self.directortyLbl.setObjectName("directortyLbl")
        self.usernameEdit = QtWidgets.QTextEdit(Form)
        self.usernameEdit.setEnabled(True)
        self.usernameEdit.setGeometry(QtCore.QRect(120, 70, 201, 31))
        self.usernameEdit.setObjectName("usernameEdit")
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
        self.nameLbl = QtWidgets.QLabel(Form)
        self.nameLbl.setGeometry(QtCore.QRect(30, 240, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameLbl.setFont(font)
        self.nameLbl.setObjectName("nameLbl")
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
        self.passwordEdit = QtWidgets.QLineEdit(Form)
        self.passwordEdit.setEnabled(True)
        self.passwordEdit.setGeometry(QtCore.QRect(120, 110, 201, 31))
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.letterLbl = QtWidgets.QLabel(Form)
        self.letterLbl.setGeometry(QtCore.QRect(30, 190, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.letterLbl.setFont(font)
        self.letterLbl.setObjectName("letterLbl")
        self.nameEdit = QtWidgets.QTextEdit(Form)
        self.nameEdit.setGeometry(QtCore.QRect(180, 240, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameEdit.setFont(font)
        self.nameEdit.setObjectName("nameEdit")
        self.passwordLbl = QtWidgets.QLabel(Form)
        self.passwordLbl.setGeometry(QtCore.QRect(30, 110, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.passwordLbl.setFont(font)
        self.passwordLbl.setObjectName("passwordLbl")
        Form.setWindowModality(QtCore.Qt.ApplicationModal)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.browseBtn.clicked.connect(self.browseForPath)
        self.CreateBtn.clicked.connect(self.login)
        self.cancelBtn.clicked.connect(self.exit)
        self.done.connect(Form.close)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.directortyLbl.setText(_translate("Form", "Enter directory:"))
        self.letterBox.setItemText(0, _translate("Form", "U:"))
        self.letterBox.setItemText(1, _translate("Form", "Q:"))
        self.letterBox.setItemText(2, _translate("Form", "T:"))
        self.letterBox.setItemText(3, _translate("Form", "E:"))
        self.letterBox.setItemText(4, _translate("Form", "P:"))
        self.cancelBtn.setText(_translate("Form", "Cancel"))
        self.usernameLbl.setText(_translate("Form", "Username:"))
        self.nameLbl.setText(_translate("Form", "Enter Drive Name:"))
        self.browseBtn.setText(_translate("Form", "..."))
        self.CreateBtn.setText(_translate("Form", "Login"))
        self.letterLbl.setText(_translate("Form", "Enter Drive Letter:"))
        self.passwordLbl.setText(_translate("Form", "Password:"))

        global FORM
        FORM = Form

    def browseForPath(self):
        folder_dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select folder', '',
                                                                QtWidgets.QFileDialog.ShowDirsOnly)
        self.directoryEdit.setPlainText(folder_dir)

    def login(self):
        global MESSAGE
        username, password = self.usernameEdit.toPlainText(), self.passwordEdit.text()
        letter, dr, name = self.letterBox.currentText(), self.directoryEdit.toPlainText(), self.nameEdit.toPlainText()
        if dr != '' and name != '' and username != '' and password != '':
            hashed_password = hashlib.sha224(password.encode()).hexdigest()
            MESSAGE = '{0},{1},{2}'.format(username, hashed_password, definitions.MAC_ADDRESS)

            config = cp.ConfigParser()
            config.read(definitions.DRIVES_LIST_DIR)
            sections = config.sections()
            if username not in sections:
                # MappedDrive(letter, dr, name)
                config.add_section(username)
                config.set(username, 'disk', letter + name)
                config.set(username, 'password', hashed_password)
                with open(definitions.DRIVES_LIST_DIR, "w+") as f:
                    config.write(f)
            print('emited done')
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

    def exit(self):
        global FORM
        self.close.emit()
        FORM.close()

    @staticmethod
    def accountAlreadyExists():
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle('Account Exists')
        box.setText('The account you are trying to reach to is already logged in')
        box.setStandardButtons(QMessageBox.Ok)
        box.setDefaultButton(QMessageBox.Ok)
        button = box.button(QMessageBox.Ok)
        button.setText('Close')
        box.exec_()

    @staticmethod
    def wrongDetails():
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle('Wrong Details')
        box.setText('The username or password are wrong')
        box.setStandardButtons(QMessageBox.Ok)
        box.setDefaultButton(QMessageBox.Ok)
        button = box.button(QMessageBox.Ok)
        button.setText('Close')
        box.exec_()


def get_message():
    global MESSAGE
    return MESSAGE


def set_message(new_message):
    global MESSAGE
    MESSAGE = new_message


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

