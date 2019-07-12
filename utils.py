from Gui.AreYouSureDialog import Ui_Dialog
from Gui.CannotExcept import Ui_Dialog as CannotUi
from PyQt5 import QtWidgets
import qdarkstyle
import os


def disconnect_all_signals(*args):
    if len(args) > 1:
        for slot in args:
            disconnect_all_signals(slot)
    else:
        try:
            args[0].disconnect()
        except TypeError:
            pass


class AreYouSureDialog(QtWidgets.QDialog):
    def __init__(self, msg, parent=None):
        super(AreYouSureDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.msgLabel.setText(msg)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.exec()


class CannotExceptDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CannotExceptDialog, self).__init__(parent=parent)
        self.ui = CannotUi()
        self.ui.setupUi(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.exec()


def are_you_sure_prompt(msg):
    dialog = AreYouSureDialog(msg)
    return dialog.result()


def cannot_except_dialog():
    CannotExceptDialog()


def does_folder_exist(path):
    return os.path.exists(path)


def make_dir(directory):
    if not does_folder_exist(directory):
        os.makedirs(directory)
    return directory
