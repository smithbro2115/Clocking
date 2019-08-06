from Clock import Clock, delete_clock
from Gui.AddCategoryDialog import Ui_addCategoryDialog
from PyQt5 import QtWidgets, QtGui
import qdarkstyle
from utils import cannot_except_dialog, make_dir
import os
from LocalFileHandling import add_dict_to_list_csv_file, get_dicts_from_csv, \
    add_file_if_it_does_not_exist, make_folder_if_it_does_not_exist, delete_dict_from_csv


class AddCategoryDialog(QtWidgets.QDialog):
    def __init__(self, default_wage, wage=None, name='', category_number='', description='', parent=None):
        super(AddCategoryDialog, self).__init__(parent=parent)
        self.ui = Ui_addCategoryDialog()
        self.ui.setupUi(self)
        self.ui.wageLineEdit.setValidator(QtGui.QDoubleValidator())
        if not wage:
            self.ui.wageLineEdit.setText(str(default_wage))
        else:
            self.ui.wageLineEdit.setText(str(wage))
        self.ui.nameLineEdit.setText(name)
        self.ui.categoryNumberLineEdit.setText(category_number)
        self.ui.descriptionTextEdit.setText(description)
        self.required_fields = [self.ui.nameLineEdit, self.ui.wageLineEdit]
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
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
            if bad in self.ui.nameLineEdit.text():
                cannot_except_dialog()
                return True
        return False

    def accept(self):
        if self.check_if_filled(self.required_fields) and not self.check_for_bad_characters():
            super(AddCategoryDialog, self).accept()


class Category:
    def __init__(self, name, wage, category_number, description, user):
        self.name = name
        self.wage = wage
        self.category_number = category_number
        self.description = description
        self.clock = Clock(user, self)
        self.user = user
        add_file_if_it_does_not_exist(self.file_path)
        self.save()

    @property
    def file_path(self):
        return f"{make_folder_if_it_does_not_exist(self.user.directory, 'Categories')}/Categories.csv"

    @property
    def info(self):
        return {'name': self.name, 'wage': self.wage,
                'category_number': self.category_number, 'description': self.description}

    def save(self):
        add_dict_to_list_csv_file(self.file_path, self.info)


def add_category(user):
    dialog = AddCategoryDialog(user.default_wage)
    if not dialog.result():
        return None
    return Category(dialog.ui.nameLineEdit.text(), dialog.ui.wageLineEdit.text(),
                    dialog.ui.categoryNumberLineEdit.text(), dialog.ui.descriptionTextEdit.toPlainText(),
                    user)


def load_categories(user):
    path = f"{make_dir(f'{user.directory}/Categories')}/Categories.csv"
    add_file_if_it_does_not_exist(path)
    raw_categories = get_dicts_from_csv(path)
    categories = []
    for raw_category in raw_categories:
        category = Category(user=user, **raw_category)
        categories.append(category)
    return categories


def delete_category(user, category):
    path = f"{make_folder_if_it_does_not_exist(user.directory, 'Categories')}/Categories.csv"
    add_file_if_it_does_not_exist(path)
    delete_clock(category.clock)
    return delete_dict_from_csv(path, category.info)


def edit_category(user, category):
    old_clock_path = category.clock.file_path
    dialog = AddCategoryDialog(user.default_wage, **category.info)
    if not dialog.result():
        return None
    delete_dict_from_csv(category.file_path, category.info)
    category.name = dialog.ui.nameLineEdit.text()
    os.rename(old_clock_path, category.clock.file_path)
    return Category(dialog.ui.nameLineEdit.text(), dialog.ui.wageLineEdit.text(),
                    dialog.ui.categoryNumberLineEdit.text(), dialog.ui.descriptionTextEdit.toPlainText(), user)
