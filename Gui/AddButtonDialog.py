# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Employee Folders\Josh\Programs\Clocking\Gui\AddButtonDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(422, 197)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setMaximumSize(QtCore.QSize(120, 16777215))
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 2, 1, 2, 1)
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.buttonAddressLabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonAddressLabel.setFont(font)
        self.buttonAddressLabel.setObjectName("buttonAddressLabel")
        self.gridLayout.addWidget(self.buttonAddressLabel, 3, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.twoLabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.twoLabel.setFont(font)
        self.twoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.twoLabel.setObjectName("twoLabel")
        self.gridLayout_2.addWidget(self.twoLabel, 0, 1, 1, 1)
        self.oneLabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.oneLabel.setFont(font)
        self.oneLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.oneLabel.setObjectName("oneLabel")
        self.gridLayout_2.addWidget(self.oneLabel, 0, 2, 1, 1)
        self.goLabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.goLabel.setFont(font)
        self.goLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.goLabel.setObjectName("goLabel")
        self.gridLayout_2.addWidget(self.goLabel, 0, 3, 1, 1)
        self.threeLabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.threeLabel.setFont(font)
        self.threeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.threeLabel.setObjectName("threeLabel")
        self.gridLayout_2.addWidget(self.threeLabel, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 2, 0, 1, 1)
        self.startButton = QtWidgets.QPushButton(Dialog)
        self.startButton.setObjectName("startButton")
        self.gridLayout.addWidget(self.startButton, 1, 0, 1, 2)
        self.horizontalWidget = QtWidgets.QWidget(Dialog)
        self.horizontalWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addPushButton = QtWidgets.QPushButton(self.horizontalWidget)
        self.addPushButton.setMaximumSize(QtCore.QSize(65, 16777215))
        self.addPushButton.setObjectName("addPushButton")
        self.horizontalLayout.addWidget(self.addPushButton)
        self.cancelPushButton = QtWidgets.QPushButton(self.horizontalWidget)
        self.cancelPushButton.setMaximumSize(QtCore.QSize(65, 16777215))
        self.cancelPushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.gridLayout.addWidget(self.horizontalWidget, 4, 0, 1, 2)
        self.gridLayout.setColumnStretch(0, 5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Button"))
        self.label.setText(_translate("Dialog", "Hit your amazon button on GO!"))
        self.buttonAddressLabel.setText(_translate("Dialog", "Button Address:"))
        self.twoLabel.setText(_translate("Dialog", "2"))
        self.oneLabel.setText(_translate("Dialog", "1"))
        self.goLabel.setText(_translate("Dialog", "GO"))
        self.threeLabel.setText(_translate("Dialog", "3"))
        self.startButton.setText(_translate("Dialog", "Start"))
        self.addPushButton.setText(_translate("Dialog", "Add"))
        self.cancelPushButton.setText(_translate("Dialog", "Cancel"))

