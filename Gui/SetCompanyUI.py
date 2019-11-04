# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Programming\Clocking\Gui\SetCompanyUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(388, 282)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.phoneLineEdit = QtWidgets.QLineEdit(Dialog)
        self.phoneLineEdit.setObjectName("phoneLineEdit")
        self.gridLayout.addWidget(self.phoneLineEdit, 1, 1, 1, 1)
        self.emailLineEdit = QtWidgets.QLineEdit(Dialog)
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.gridLayout.addWidget(self.emailLineEdit, 3, 0, 1, 1)
        self.nameLineEdit = QtWidgets.QLineEdit(Dialog)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.gridLayout.addWidget(self.nameLineEdit, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.mottoLineEdit = QtWidgets.QLineEdit(Dialog)
        self.mottoLineEdit.setObjectName("mottoLineEdit")
        self.gridLayout.addWidget(self.mottoLineEdit, 3, 1, 1, 1)
        self.addressPlainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.addressPlainTextEdit.setObjectName("addressPlainTextEdit")
        self.gridLayout.addWidget(self.addressPlainTextEdit, 5, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.nameLineEdit, self.phoneLineEdit)
        Dialog.setTabOrder(self.phoneLineEdit, self.emailLineEdit)
        Dialog.setTabOrder(self.emailLineEdit, self.mottoLineEdit)
        Dialog.setTabOrder(self.mottoLineEdit, self.addressPlainTextEdit)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Set Company"))
        self.label.setText(_translate("Dialog", "*Company Name:"))
        self.label_4.setText(_translate("Dialog", "Company Motto:"))
        self.label_2.setText(_translate("Dialog", "*Company Phone Number:"))
        self.label_3.setText(_translate("Dialog", "*Company Email:"))
        self.label_5.setText(_translate("Dialog", "*Company Address:"))

