# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Employee Folders\Josh\Programs\PreferencesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(470, 96)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(1)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.userSaveLocationLineEdit = QtWidgets.QLineEdit(self.frame)
        self.userSaveLocationLineEdit.setObjectName("userSaveLocationLineEdit")
        self.gridLayout_2.addWidget(self.userSaveLocationLineEdit, 0, 0, 1, 1)
        self.browseUserSaveLoationButton = QtWidgets.QToolButton(self.frame)
        self.browseUserSaveLoationButton.setObjectName("browseUserSaveLoationButton")
        self.gridLayout_2.addWidget(self.browseUserSaveLoationButton, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 1, 1, 2)
        self.resetClocksAfterExportingInvoicesCheckBox = QtWidgets.QCheckBox(Dialog)
        self.resetClocksAfterExportingInvoicesCheckBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.resetClocksAfterExportingInvoicesCheckBox.setObjectName("resetClocksAfterExportingInvoicesCheckBox")
        self.gridLayout.addWidget(self.resetClocksAfterExportingInvoicesCheckBox, 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Preferences"))
        self.label.setText(_translate("Dialog", "User Save Location:"))
        self.browseUserSaveLoationButton.setText(_translate("Dialog", "..."))
        self.resetClocksAfterExportingInvoicesCheckBox.setText(_translate("Dialog", "Reset Clocks After Exporting Invoice"))

