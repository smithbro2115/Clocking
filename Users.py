from Gui.AddUserDialog import Ui_AddUserDialog
from PyQt5 import QtWidgets, QtGui
import qdarkstyle
from utils import cannot_except_dialog
from LocalFileHandling import get_app_data_folder, add_dict_to_csv_file, add_file_if_it_does_not_exist, \
    make_folder_if_it_does_not_exist, get_dicts_from_csv
import os


class AddUserDialog(QtWidgets.QDialog):
    def __init__(self, first_name='', last_name='', default_wage='', parent=None):
        super(AddUserDialog, self).__init__(parent=parent)
        self.ui = Ui_AddUserDialog()
        self.ui.setupUi(self)
        self.ui.wageLineEdit.setValidator(QtGui.QDoubleValidator())
        self.ui.firstNameLineEdit.setFocus()
        self.required_fields = [self.ui.firstNameLineEdit, self.ui.lastNameLineEdit]
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.ui.firstNameLineEdit.setText(first_name)
        self.ui.lastNameLineEdit.setText(last_name)
        self.ui.wageLineEdit.setText(str(default_wage))
        self.exec_()

    def check_if_filled(self, fields):
        try:
            for field in fields:
                if not field.text():
                    return False
            return True
        except TypeError:
            if not fields.text():
                return False
            return True

    def check_for_bad_characters(self):
        bad_letters = ['/', '\\']
        for bad in bad_letters:
            if bad in (self.ui.firstNameLineEdit.text()or self.ui.lastNameLineEdit.text()):
                cannot_except_dialog()
                return True
        return False

    def accept(self):
        if self.check_if_filled(self.required_fields) and not self.check_for_bad_characters():
            super(AddUserDialog, self).accept()


class User:
    def __init__(self, first_name, last_name, default_wage=0.0):
        self.first_name = first_name
        self.last_name = last_name
        self.default_wage = default_wage
        make_folder_if_it_does_not_exist(get_app_data_folder('Users'), f"{self.first_name}_{self.last_name}")
        self.directory = f"{get_app_data_folder('Users')}/{self.first_name}_{self.last_name}"
        self.file_path = f"{self.directory}/{self.first_name}_{self.last_name}_user.csv"
        add_file_if_it_does_not_exist(self.file_path)
        self.save()

    @property
    def info(self):
        return {'first_name': self.first_name, 'last_name': self.last_name, 'default_wage': self.default_wage}

    def save(self):
        add_dict_to_csv_file(self.file_path, self.info, keyword='last_name')


def add_user():
    dialog = AddUserDialog()
    return make_user(dialog)


def make_user(dialog):
    if not dialog.result():
        return None
    try:
        user = User(dialog.ui.firstNameLineEdit.text(), dialog.ui.lastNameLineEdit.text(),
                    float(dialog.ui.wageLineEdit.text()))
    except ValueError:
        user = User(dialog.ui.firstNameLineEdit.text(), dialog.ui.lastNameLineEdit.text())
    return user


def get_user_file_paths():
    path = f"{get_app_data_folder('Users')}"
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('user.csv'):
                paths.append(os.path.join(root, file))
    return paths


def load_user(path):
    add_file_if_it_does_not_exist(path)
    raw_users = get_dicts_from_csv(path)
    users = []
    for raw_user in raw_users:
        user = User(**raw_user)
        users.append(user)
    return users


def load_users():
    paths = get_user_file_paths()
    users = []
    for path in paths:
        users.extend(load_user(path))
    return users


def delete_user(user):
    import shutil
    try:
        shutil.rmtree(user.directory)
        return True
    except Exception:
        return False


def edit_user(user):
    import shutil
    dialog = AddUserDialog(**user.info)
    print(dialog.result())
    if not dialog.result():
        return None
    os.remove(user.file_path)
    new_directory = f"{get_app_data_folder('Users')}/{dialog.ui.firstNameLineEdit.text()}_" \
        f"{dialog.ui.lastNameLineEdit.text()}"
    shutil.move(user.directory, new_directory)
    return make_user(dialog)
