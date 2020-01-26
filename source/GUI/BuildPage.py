# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\nimni\PycharmProjects\Unicloud-VC\source\GUI\ui scripts\BuildPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from WindowsManagement.VirtualDisk import MappedDrive


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(555, 358)
        self.letterLbl = QtWidgets.QLabel(Form)
        self.letterLbl.setGeometry(QtCore.QRect(20, 60, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.letterLbl.setFont(font)
        self.letterLbl.setObjectName("letterLbl")
        self.letterBox = QtWidgets.QComboBox(Form)
        self.letterBox.setGeometry(QtCore.QRect(170, 60, 111, 31))
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
        self.nameLbl.setGeometry(QtCore.QRect(20, 110, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameLbl.setFont(font)
        self.nameLbl.setObjectName("nameLbl")
        self.nameEdit = QtWidgets.QTextEdit(Form)
        self.nameEdit.setGeometry(QtCore.QRect(170, 110, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameEdit.setFont(font)
        self.nameEdit.setObjectName("nameEdit")
        self.directortyLbl = QtWidgets.QLabel(Form)
        self.directortyLbl.setGeometry(QtCore.QRect(20, 160, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.directortyLbl.setFont(font)
        self.directortyLbl.setObjectName("directortyLbl")
        self.directoryEdit = QtWidgets.QTextEdit(Form)
        self.directoryEdit.setGeometry(QtCore.QRect(170, 160, 331, 31))
        self.directoryEdit.setObjectName("directoryEdit")
        self.browseBtn = QtWidgets.QToolButton(Form)
        self.browseBtn.setGeometry(QtCore.QRect(500, 170, 25, 21))
        self.browseBtn.setObjectName("browseBtn")
        self.CancelBtn = QtWidgets.QPushButton(Form)
        self.CancelBtn.setGeometry(QtCore.QRect(320, 300, 101, 41))
        self.CancelBtn.setObjectName("CancelBtn")
        self.CreateBtn = QtWidgets.QPushButton(Form)
        self.CreateBtn.setGeometry(QtCore.QRect(440, 300, 101, 41))
        self.CreateBtn.setObjectName("CreateBtn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.browseBtn.clicked.connect(self.browseForPath)
        self.CreateBtn.clicked.connect(self.buildDrive)
        self.CancelBtn.clicked.connect(Form.close)

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
        self.CancelBtn.setText(_translate("Form", "Cancel"))
        self.CreateBtn.setText(_translate("Form", "Create Drive"))

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
        if box.clickedButton() == button_yes:
            MappedDrive(self.letterBox.currentText(), self.directoryEdit.toPlainText(), self.nameEdit.toPlainText())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
