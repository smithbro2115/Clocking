from Clock import Clock
from Gui.AddCategoryDialog import Ui_addCategoryDialog
from PyQt5 import QtWidgets, QtGui
import qdarkstyle
from LocalFileHandling import get_app_data_folder, add_dict_to_csv_file, get_dicts_from_csv, \
    add_file_if_it_does_not_exist, make_folder_if_it_does_not_exist


class AddCategoryDialog(QtWidgets.QDialog):
    def __init__(self, default_wage, parent=None):
        super(AddCategoryDialog, self).__init__(parent=parent)
        self.ui = Ui_addCategoryDialog()
        self.ui.setupUi(self)
        self.ui.wageLineEdit.setValidator(QtGui.QDoubleValidator())
        self.ui.wageLineEdit.setText(str(default_wage))
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
    def __init__(self, name, wage, category_number, description, user, time_label, income_label):
        self.name = name
        self.wage = wage
        self.category_number = category_number
        self.description = description
        self.clock = Clock(user, time_label, income_label, self)
        self.file_path = f"{make_folder_if_it_does_not_exist(user.directory, 'Categories')}/Categories.csv"
        add_file_if_it_does_not_exist(self.file_path)
        self.save()

    def save(self):
        info = {'name': self.name, 'wage': self.wage,
                'category_number': self.category_number, 'description': self.description}
        add_dict_to_csv_file(self.file_path, info)


def add_category(user, time_label, income_label):
    dialog = AddCategoryDialog(user.default_wage)
    if not dialog.result():
        return None
    return Category(dialog.ui.nameLineEdit.text(), dialog.ui.wageLineEdit.text(),
                    dialog.ui.categoryNumberLineEdit.text(), dialog.ui.descriptionTextEdit.toPlainText(),
                    user, time_label, income_label)


def load_categories(user, time_label, income_label):
    path = f"{make_folder_if_it_does_not_exist(user.directory, 'Categories')}/Categories.csv"
    add_file_if_it_does_not_exist(path)
    raw_categories = get_dicts_from_csv(path)
    categories = []
    for raw_category in raw_categories:
        category = Category(user=user, time_label=time_label, income_label=income_label,
                            **raw_category)
        categories.append(category)
    return categories


