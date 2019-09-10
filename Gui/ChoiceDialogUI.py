# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Employee Folders\Josh\Programs\Clocking\Gui\ChoiceDialogUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChoiceDialog(object):
    def setupUi(self, ChoiceDialog):
        ChoiceDialog.setObjectName("ChoiceDialog")
        ChoiceDialog.resize(382, 95)
        self.gridLayout = QtWidgets.QGridLayout(ChoiceDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.messageLabel = QtWidgets.QLabel(ChoiceDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.messageLabel.setFont(font)
        self.messageLabel.setObjectName("messageLabel")
        self.gridLayout.addWidget(self.messageLabel, 0, 0, 1, 2)
        self.rememberRadioButton = QtWidgets.QRadioButton(ChoiceDialog)
        self.rememberRadioButton.setObjectName("rememberRadioButton")
        self.gridLayout.addWidget(self.rememberRadioButton, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.yesPushButton = QtWidgets.QPushButton(ChoiceDialog)
        self.yesPushButton.setObjectName("yesPushButton")
        self.horizontalLayout.addWidget(self.yesPushButton)
        self.noPushButton = QtWidgets.QPushButton(ChoiceDialog)
        self.noPushButton.setObjectName("noPushButton")
        self.horizontalLayout.addWidget(self.noPushButton)
        self.cancelPushButton = QtWidgets.QPushButton(ChoiceDialog)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.retranslateUi(ChoiceDialog)
        QtCore.QMetaObject.connectSlotsByName(ChoiceDialog)

    def retranslateUi(self, ChoiceDialog):
        _translate = QtCore.QCoreApplication.translate
        ChoiceDialog.setWindowTitle(_translate("ChoiceDialog", "Dialog"))
        self.messageLabel.setText(_translate("ChoiceDialog", "Message"))
        self.rememberRadioButton.setText(_translate("ChoiceDialog", "Remember"))
        self.yesPushButton.setText(_translate("ChoiceDialog", "Yes"))
        self.noPushButton.setText(_translate("ChoiceDialog", "No"))
        self.cancelPushButton.setText(_translate("ChoiceDialog", "Cancel"))

