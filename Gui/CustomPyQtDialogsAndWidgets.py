from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTreeWidget, QTreeWidgetItem, QTableWidgetItem
from PyQt5.QtCore import QDateTime, QObject, pyqtSlot, pyqtSignal, QRunnable, QThreadPool
import time
import qdarkstyle
from Gui.AssignButton import Ui_Dialog as AssignButtonUI
from Gui.EmailTemplateDialog import Ui_Dialog
from Categories import load_categories
from Exporting import GetFileLocationDialog
from utils import add_to_config, read_from_config, NoSectionError, NoOptionError
from LocalFileHandling import get_app_data_folder
import os
from Emailing import get_subject_and_body_from_text


class DialogTemplate(QDialog):
    def __init__(self, ui, parent=None):
        super(DialogTemplate, self).__init__(parent=parent)
        self.ui = ui()
        self.ui.setupUi(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


class AssignButtonDialog(DialogTemplate):
    def __init__(self, buttons, users):
        super(AssignButtonDialog, self).__init__(AssignButtonUI)
        self.ui.categoryTreeWidget = ChildDraggableTreeWidget()
        self.ui.buttonTreeWidget = ChildDroppableTreeWidget()
        self.ui.gridLayout.addWidget(self.ui.categoryTreeWidget, 1, 1)
        self.ui.gridLayout.addWidget(self.ui.buttonTreeWidget, 1, 0)
        self.ui.categoryTreeWidget.setHeaderHidden(True)
        self.ui.categoryTreeWidget.setDragEnabled(True)
        self.ui.buttonTreeWidget.setAcceptDrops(True)
        self.ui.buttonTreeWidget.setHeaderHidden(True)
        self.populate_button_tree(buttons)
        self.populate_tree(self.ui.categoryTreeWidget, self.make_users_dict(users))
        self.ui.removeCategoryPushButton.setEnabled(False)
        self.new_button_dict = {}

    def accept(self):
        try:
            for index in range(self.ui.buttonTreeWidget.topLevelItemCount()):
                button_item = self.ui.buttonTreeWidget.topLevelItem(index)
                self.new_button_dict[button_item.text(0)] = (button_item.user, button_item.category)
        except IndexError:
            pass
        super(AssignButtonDialog, self).accept()

    @staticmethod
    def make_users_dict(users):
        users_dict = {}
        for user in users:
            categories = load_categories(user)
            category_names = [category.name for category in categories]
            users_dict[f"{user.first_name}_{user.last_name}"] = category_names
        return users_dict

    def populate_button_tree(self, buttons):
        for key, values in buttons.items():
            button_item = ButtonTreeWidgetItem()
            button_item.user = values[0]
            button_item.category = values[1]
            button_item.setText(0, key)
            self.ui.buttonTreeWidget.addTopLevelItem(button_item)
            if None not in values:
                item = QTreeWidgetItem()
                item.setText(0, f"{values[0]}: {values[1]}")
                button_item.addChild(item)

    @staticmethod
    def populate_tree(tree: QTreeWidget, to_populate: dict):
        for key, values in to_populate.items():
            item = QTreeWidgetItem()
            item.setText(0, key)
            tree.addTopLevelItem(item)
            for value in values:
                if value:
                    child = QTreeWidgetItem()
                    child.setText(0, value)
                    item.addChild(child)


class TimedEmitterSignals(QObject):
    time_elapsed = pyqtSignal()
    finished = pyqtSignal()


class TimedEmitter(QRunnable):
    def __init__(self, time_between_emits, times_to_emit):
        super(TimedEmitter, self).__init__()
        self.signals = TimedEmitterSignals()
        self.time_between = time_between_emits
        self.times_to_emit = times_to_emit
        self.times_emitted = 0
        self.canceled = False

    @pyqtSlot()
    def run(self):
        while self.times_emitted < self.times_to_emit or self.times_to_emit < 0:
            if self.canceled:
                break
            time.sleep(self.time_between)
            self.signals.time_elapsed.emit()
            self.times_emitted += 1
        self.signals.finished.emit()


class ChildDraggableTreeWidget(QTreeWidget):
    def __init__(self):
        super(ChildDraggableTreeWidget, self).__init__()
        self.setDragEnabled(True)

    def startDrag(self, *args, **kwargs):
        if self.currentItem().parent():
            super(ChildDraggableTreeWidget, self).startDrag(*args, **kwargs)


class ButtonTreeWidgetItem(QTreeWidgetItem):
    def __init__(self):
        super(ButtonTreeWidgetItem, self).__init__()
        self.user = None
        self.category = None


class ChildDroppableTreeWidget(QTreeWidget):
    def __init__(self):
        super(ChildDroppableTreeWidget, self).__init__()
        self.setDragEnabled(True)

    def category_drop(self, QDropEvent):
        old_item = QDropEvent.source().currentItem()
        new_item = QTreeWidgetItem()
        button = self.itemAt(QDropEvent.pos())
        if not isinstance(button, ButtonTreeWidgetItem):
            button = button.parent()
        button.takeChildren()
        button.user = old_item.parent().text(0)
        button.category = old_item.text(0)
        new_item.setText(0, f"{button.user}: {button.category}")
        if isinstance(button, ButtonTreeWidgetItem):
            button.addChild(new_item)

    def dropEvent(self, QDropEvent):
        try:
            self.category_drop(QDropEvent)
        except AttributeError:
            pass


class EmailTemplate(QDialog):
    def __init__(self):
        super(EmailTemplate, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        try:
            path = read_from_config('EMAIL', 'template_save_path')
            with open(path, 'r') as f:
                subject, body = get_subject_and_body_from_text(f.read())
                self.ui.subjectLineEdit.setText(subject)
                self.ui.textEdit.setText(body)
        except (NoSectionError, NoOptionError):
            pass
        except FileNotFoundError:
            add_to_config('EMAIL', 'template_save_path', get_app_data_folder(''))

    @staticmethod
    def get_save_path():
        try:
            dialog = GetFileLocationDialog("email_template.txt", "Save Email Template",
                                           f"{os.path.dirname(read_from_config('EMAIL', 'template_save_path'))}/")
            path = dialog.get_save_path()
        except (NoSectionError, NoOptionError):
            dialog = GetFileLocationDialog("email_template.txt", "Save Email Template", get_app_data_folder(''))
            path = dialog.get_save_path()
        add_to_config("EMAIL", "template_save_path", path)
        return path

    def accept(self) -> None:
        path = self.get_save_path()
        try:
            with open(path, 'w') as f:
                f.write(f"@subject\n{self.ui.subjectLineEdit.text()}\n\n@body\n{self.ui.textEdit.toPlainText()}")
            super(EmailTemplate, self).accept()
        except FileNotFoundError:
            pass
