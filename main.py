from PyQt5 import QtGui, QtWidgets, QtCore
from Gui import MainWindow
import qdarkstyle
import Categories
from Users import add_user, load_users


class Gui(MainWindow.Ui_MainWindow):
    def __init__(self):
        self.categories = []
        self.users = []
        self._current_user = None
        self._current_category = None
        self.current_clock = None

    def setup_additional(self, main_window):
        main_window.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.clockTableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        headers = ['Clocked In:', 'Clocked Out:', 'Total Time Worked:']
        self.clockTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.clockTableWidget.verticalHeader().setVisible(False)
        self.clockTableWidget.setColumnCount(3)
        self.clockTableWidget.setHorizontalHeaderLabels(headers)
        self.clockButton.clicked.connect(self.clock_button_clicked)
        self.addCategoryButton.clicked.connect(self.add_category)
        self.load_users()
        if self.userBox.currentIndex() < 0:
            self.categoryBox.setEnabled(False)
            self.addCategoryButton.setEnabled(False)
        else:
            self.current_user = self.userBox.currentData()
        if self.categoryBox.currentIndex() >= 0:
            self.current_category = self.categoryBox.currentData()
        self.userBox.currentIndexChanged.connect(self.user_box_changed)
        self.categoryBox.currentIndexChanged.connect(self.category_box_changed)
        self.addUserButton.clicked.connect(self.add_user_button_clicked)

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, value):
        self.userLabel.setText(f"User: {self.userBox.currentText()}")
        self._current_user = value
        self.load_categories()

    @property
    def current_category(self):
        return self._current_category

    @current_category.setter
    def current_category(self, value):
        self.categoryLabel.setText(f"Category: {self.categoryBox.currentText()}")
        self._current_category = value
        self.clockTableWidget.setRowCount(0)
        if value:
            self.load_clock()

    def add_user_button_clicked(self):
        user = add_user()
        if user:
            formatted = f"{user.first_name.capitalize()} {user.last_name.capitalize()}"
            self.userBox.addItem(formatted, user)
            self.userBox.setCurrentIndex(self.userBox.findText(formatted))

    def add_user_to_box(self, user, switch_focus=False):
        formatted = f"{user.first_name.capitalize()} {user.last_name.capitalize()}"
        self.userBox.addItem(formatted, user)
        if switch_focus:
            self.userBox.setCurrentIndex(self.userBox.findText(formatted))

    def load_users(self):
        self.users = load_users()
        for user in self.users:
            self.add_user_to_box(user)

    def add_category(self):
        category = Categories.add_category(self.current_user, self.clockTableWidget, self.clockButton, self.totalTimeLabel, self.totalIncomeLabel)
        if category:
            self.categories.append(category)
            self.categoryBox.addItem(category.name, category)
            self.categoryBox.setCurrentIndex(self.categoryBox.findText(category.name))

    def load_categories(self):
        self.categoryBox.clear()
        self.categories = Categories.load_categories(self.current_user, self.clockTableWidget, self.clockButton, self.totalTimeLabel, self.totalIncomeLabel)
        for category in self.categories:
            self.categoryBox.addItem(category.name, category)

    def user_box_changed(self):
        self.current_user = self.userBox.currentData()
        self.addCategoryButton.setEnabled(True)
        self.categoryBox.setEnabled(True)

    def category_box_changed(self):
        self.current_category = self.categoryBox.currentData()

    def load_clock(self):
        self.current_clock = self.current_category.clock
        self.current_clock.active = False
        self.clockTableWidget.setRowCount(0)
        self.current_clock.active = True
        self.current_clock.load()
        self.current_clock.set_button_text()

    def clock_button_clicked(self):
        if self.current_category:
            self.current_clock.clock()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Gui()
    mainWindow = QtWidgets.QMainWindow()
    ui.setupUi(mainWindow)
    ui.setup_additional(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
