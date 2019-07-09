from Clock import Clock
from Gui.AddCategoryDialog import Ui_addCategoryDialog
from PyQt5 import QtWidgets, QtGui
import qdarkstyle
from LocalFileHandling import get_app_data_folder, add_dict_to_csv_file, get_dicts_from_csv, \
    add_file_if_it_does_not_exist


class AddCategoryDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddCategoryDialog, self).__init__(parent=parent)
        self.ui = Ui_addCategoryDialog()
        self.ui.setupUi(self)
        self.ui.wageLineEdit.setValidator(QtGui.QDoubleValidator())
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

    def accept(self):
        if self.check_if_filled(self.required_fields):
            super(AddCategoryDialog, self).accept()


class Category:
    def __init__(self, name, wage, category_number, description, table, button):
        self.name = name
        self.wage = wage
        self.category_number = category_number
        self.description = description
        self.clock = Clock(table, button, self.name)
        self.file_path = f"{get_app_data_folder('Categories')}/Categories.csv"
        add_file_if_it_does_not_exist(self.file_path)
        self.save()

    def save(self):
        info = {'name': self.name, 'wage': self.wage,
                'category_number': self.category_number, 'description': self.description}
        add_dict_to_csv_file(self.file_path, info)


def add_category(table, button):
    dialog = AddCategoryDialog()
    return Category(dialog.ui.nameLineEdit.text(), dialog.ui.wageLineEdit.text(),
                    dialog.ui.categoryNumberLineEdit.text(), dialog.ui.descriptionTextEdit.toPlainText(), table, button)


def load_categories(combo_box):
    path = f"{get_app_data_folder('Categories')}/Categories.csv"
    add_file_if_it_does_not_exist(path)
    print(get_dicts_from_csv(path))


