from Gui.AreYouSureDialog import Ui_Dialog
from Gui.CannotExcept import Ui_Dialog as CannotUi
from Gui.ChoiceDialogUI import Ui_ChoiceDialog as ChoiceUi
from Gui.Error import Ui_Dialog as ErrorUi
from PyQt5 import QtWidgets
from LocalFileHandling import add_to_config, read_from_config
import qdarkstyle
import os
from configparser import NoSectionError, NoOptionError
import sys
from shutil import copyfile
import subprocess


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


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, msg, parent=None):
        super(ErrorDialog, self).__init__(parent=parent)
        self.ui = ErrorUi()
        self.ui.setupUi(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.ui.messageLabel.setText(msg)
        self.exec()


class ChoiceDialog(QtWidgets.QDialog):
    def __init__(self, message, remember_category, remember_option, window_title='Question', parent=None):
        super(ChoiceDialog, self).__init__(parent=parent)
        self.ui = ChoiceUi()
        self.ui.setupUi(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.ui.messageLabel.setText(message)
        self.setWindowTitle(window_title)
        self.remember_category = remember_category
        self.remember_option = remember_option
        self.ui.yesPushButton.clicked.connect(self.yes_button_clicked)
        self.ui.noPushButton.clicked.connect(self.no_button_clicked)
        self.ui.cancelPushButton.clicked.connect(self.reject)
        self.yes_or_no = False
        if self.check_if_remembered():
            self.accept()
        else:
            self.exec_()

    def no_button_clicked(self):
        self.yes_or_no = False
        self.accept()

    def yes_button_clicked(self):
        self.yes_or_no = True
        self.accept()

    def check_if_remembered(self):
        try:
            remembered_option = bool(int(read_from_config(self.remember_category, self.remember_option)))
            if remembered_option:
                self.yes_or_no = True
            else:
                self.yes_or_no = False
            return True
        except (NoSectionError, NoOptionError):
            pass

    def remember(self):
        add_to_config(self.remember_category, self.remember_option, int(self.yes_or_no))

    def accept(self):
        if self.ui.rememberRadioButton.isChecked():
            self.remember()
        super(ChoiceDialog, self).accept()


def are_you_sure_prompt(msg):
    dialog = AreYouSureDialog(msg)
    return dialog.result()


def cannot_except_dialog():
    CannotExceptDialog()


def error_dialog(msg):
    ErrorDialog(msg)


def does_folder_exist(path):
    return os.path.exists(path)


def make_dir(directory):
    if not does_folder_exist(directory):
        os.makedirs(directory)
    return directory


def copy_file_to_directory(path, new_path):
    new_path = f"{new_path}/{os.path.basename(path)}".replace('\\', '/')
    path = path.replace('\\', '/')
    copyfile(path, new_path)
    return new_path


def delete_file(path):
    os.remove(path)


def start_program(path):
    os.startfile(path)


def close_program(name):
    os.system(f'TASKKILL /F /IM "{name}"')


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)
