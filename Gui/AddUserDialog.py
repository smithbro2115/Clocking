# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Josh\PycharmProjects\Clocking\Gui\AddUserDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddUserDialog(object):
    def setupUi(self, AddUserDialog):
        AddUserDialog.setObjectName("AddUserDialog")
        AddUserDialog.resize(512, 218)
        self.gridLayout = QtWidgets.QGridLayout(AddUserDialog)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.lastNameLineEdit = QtWidgets.QLineEdit(AddUserDialog)
        self.lastNameLineEdit.setObjectName("lastNameLineEdit")
        self.gridLayout.addWidget(self.lastNameLineEdit, 1, 1, 1, 1)
        self.firstNameLineEdit = QtWidgets.QLineEdit(AddUserDialog)
        self.firstNameLineEdit.setObjectName("firstNameLineEdit")
        self.gridLayout.addWidget(self.firstNameLineEdit, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddUserDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(AddUserDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(AddUserDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(AddUserDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(AddUserDialog)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.label = QtWidgets.QLabel(AddUserDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.wageLineEdit = QtWidgets.QLineEdit(AddUserDialog)
        self.wageLineEdit.setObjectName("wageLineEdit")
        self.gridLayout.addWidget(self.wageLineEdit, 7, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(AddUserDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.addressTextEdit = QtWidgets.QTextEdit(AddUserDialog)
        self.addressTextEdit.setObjectName("addressTextEdit")
        self.gridLayout.addWidget(self.addressTextEdit, 5, 0, 1, 2)
        self.phoneLineEdit = QtWidgets.QLineEdit(AddUserDialog)
        self.phoneLineEdit.setObjectName("phoneLineEdit")
        self.gridLayout.addWidget(self.phoneLineEdit, 3, 0, 1, 1)
        self.emailLineEdit = QtWidgets.QLineEdit(AddUserDialog)
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.gridLayout.addWidget(self.emailLineEdit, 3, 1, 1, 1)

        self.retranslateUi(AddUserDialog)
        self.buttonBox.accepted.connect(AddUserDialog.accept)
        self.buttonBox.rejected.connect(AddUserDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddUserDialog)
        AddUserDialog.setTabOrder(self.firstNameLineEdit, self.lastNameLineEdit)
        AddUserDialog.setTabOrder(self.lastNameLineEdit, self.phoneLineEdit)
        AddUserDialog.setTabOrder(self.phoneLineEdit, self.emailLineEdit)
        AddUserDialog.setTabOrder(self.emailLineEdit, self.addressTextEdit)
        AddUserDialog.setTabOrder(self.addressTextEdit, self.wageLineEdit)

    def retranslateUi(self, AddUserDialog):
        _translate = QtCore.QCoreApplication.translate
        AddUserDialog.setWindowTitle(_translate("AddUserDialog", "Add User"))
        self.label_5.setText(_translate("AddUserDialog", "*Email Address"))
        self.label_6.setText(_translate("AddUserDialog", "*Address"))
        self.label_2.setText(_translate("AddUserDialog", "*Last Name:"))
        self.label_3.setText(_translate("AddUserDialog", "Default Pay:"))
        self.label.setText(_translate("AddUserDialog", "*First Name:"))
        self.label_4.setText(_translate("AddUserDialog", "*Phone Number"))

