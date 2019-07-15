# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Josh\PycharmProjects\Clocking\Gui\AddCategoryDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_addCategoryDialog(object):
    def setupUi(self, addCategoryDialog):
        addCategoryDialog.setObjectName("addCategoryDialog")
        addCategoryDialog.resize(391, 234)
        self.gridLayout = QtWidgets.QGridLayout(addCategoryDialog)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(addCategoryDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.nameLineEdit = QtWidgets.QLineEdit(addCategoryDialog)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.gridLayout.addWidget(self.nameLineEdit, 1, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(addCategoryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(addCategoryDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(addCategoryDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.categoryNumberLineEdit = QtWidgets.QLineEdit(addCategoryDialog)
        self.categoryNumberLineEdit.setObjectName("categoryNumberLineEdit")
        self.gridLayout.addWidget(self.categoryNumberLineEdit, 3, 1, 1, 1)
        self.wageLineEdit = QtWidgets.QLineEdit(addCategoryDialog)
        self.wageLineEdit.setObjectName("wageLineEdit")
        self.gridLayout.addWidget(self.wageLineEdit, 3, 0, 1, 1)
        self.descriptionTextEdit = QtWidgets.QTextEdit(addCategoryDialog)
        self.descriptionTextEdit.setObjectName("descriptionTextEdit")
        self.gridLayout.addWidget(self.descriptionTextEdit, 5, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(addCategoryDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.retranslateUi(addCategoryDialog)
        self.buttonBox.accepted.connect(addCategoryDialog.accept)
        self.buttonBox.rejected.connect(addCategoryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(addCategoryDialog)
        addCategoryDialog.setTabOrder(self.nameLineEdit, self.wageLineEdit)
        addCategoryDialog.setTabOrder(self.wageLineEdit, self.categoryNumberLineEdit)
        addCategoryDialog.setTabOrder(self.categoryNumberLineEdit, self.descriptionTextEdit)

    def retranslateUi(self, addCategoryDialog):
        _translate = QtCore.QCoreApplication.translate
        addCategoryDialog.setWindowTitle(_translate("addCategoryDialog", "Add Category"))
        self.label.setText(_translate("addCategoryDialog", "Description:"))
        self.label_3.setText(_translate("addCategoryDialog", "Category #:"))
        self.label_2.setText(_translate("addCategoryDialog", "*Hourly Wage:"))
        self.label_4.setText(_translate("addCategoryDialog", "*Name:"))

