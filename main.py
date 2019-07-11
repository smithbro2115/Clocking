from PyQt5 import QtGui, QtWidgets, QtCore
from Gui import MainWindow
from utils import are_you_sure_prompt
import qdarkstyle
import Categories
from Users import add_user, load_users, delete_user, edit_user
from datetime import timedelta, datetime
from Exporting import make_invoice_excel


class Gui(MainWindow.Ui_MainWindow):
    def __init__(self):
        self.categories = []
        self.users = []
        self._current_user = None
        self._current_category = None
        self.current_clock = None
        self._global_monthly_time = timedelta()

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
        self.categoryAddAction.triggered.connect(self.add_category)
        self.categoryDeleteAction.triggered.connect(self.delete_category_clicked)
        self.categoryEditAction.triggered.connect(self.edit_category_clicked)
        self.userAddAction.triggered.connect(self.add_user_button_clicked)
        self.userDeleteAction.triggered.connect(self.delete_user_clicked)
        self.userEditAction.triggered.connect(self.edit_user_clicked)
        self.actionExport_Invoice.triggered.connect(self.export_invoice)
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
        self.globalRadioButton.clicked.connect(lambda:
                                               self.set_monthly_time_and_income(self.current_clock.total_monthly_time))

    def export_invoice(self):
        if self.current_category:
            make_invoice_excel(self.current_user, self.categories)

    @property
    def global_monthly_time(self):
        clocks = self.get_all_clocks()
        total_time = timedelta()
        for clock in clocks:
            total_time += clock.total_monthly_time
        return total_time

    @property
    def global_monthly_income(self):
        seconds_wages = []
        for clock, wage in zip(self.get_all_clocks(), self.get_all_wages()):
            seconds_wages.append((clock.total_monthly_time.seconds, wage))
        return self.calculate_global_monthly_income(seconds_wages)

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, value):
        self.userLabel.setText(f"User: {self.userBox.currentText()}")
        self._current_user = value
        if value:
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

    def delete_user_clicked(self):
        if are_you_sure_prompt(f"Are you sure you want to delete the user: {self.current_user.first_name}"):
            if delete_user(self.current_user):
                self.reset()

    def edit_user_clicked(self):
        if self.current_user:
            user = edit_user(self.current_user)
            if user:
                current_cat_index = self.categoryBox.currentIndex()
                self.reset()
                self.add_user_to_box(user, switch_focus=True)
                self.categoryBox.setCurrentIndex(current_cat_index)

    def delete_category_clicked(self):
        if self.current_category and are_you_sure_prompt(f"Are you sure you w"
                                                         f"ant to delete the category: {self.current_category.name}"):
            if Categories.delete_category(self.current_user, self.current_category):
                self.categories.remove(self.categoryBox.currentData())
                self.categoryBox.removeItem(self.categoryBox.currentIndex())
                self.reset_category()

    def edit_category_clicked(self):
        if self.current_category:
            category = Categories.edit_category(self.current_user, self.current_category)
            if category:
                self.categories.remove(self.categoryBox.currentData())
                self.categoryBox.removeItem(self.categoryBox.currentIndex())
                self.categories.append(category)
                self.categoryBox.addItem(category.name, category)
                self.categoryBox.setCurrentIndex(self.categoryBox.findText(category.name))

    def reset(self):
        self.categoryBox.clear()
        self.userBox.removeItem(self.userBox.currentIndex())
        self.userBox.setCurrentIndex(-1)
        self.reset_category()

    def reset_category(self):
        self.clockTableWidget.setRowCount(0)
        self.categoryBox.setCurrentIndex(-1)
        self.clockButton.setText('Clock In')
        self.current_category = None

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
        category = Categories.add_category(self.current_user)
        if category:
            self.categories.append(category)
            self.categoryBox.addItem(category.name, category)
            self.categoryBox.setCurrentIndex(self.categoryBox.findText(category.name))

    def load_categories(self):
        self.categoryBox.clear()
        self.categories = Categories.load_categories(self.current_user)
        for category in self.categories:
            self.categoryBox.addItem(category.name, category)

    def user_box_changed(self):
        if self.userBox.currentIndex() < 0:
            enabled = False
            self.current_user = None
        else:
            enabled = True
            self.current_user = self.userBox.currentData()
        self.addCategoryButton.setEnabled(enabled)
        self.categoryBox.setEnabled(enabled)

    def category_box_changed(self):
        self.current_category = self.categoryBox.currentData()

    def load_clock(self):
        self.current_clock = self.current_category.clock
        self.current_clock.active = False
        self.clockTableWidget.setRowCount(0)
        self.current_clock.active = True
        rows = self.current_clock.load()
        self.load_clock_data_into_table(rows)
        self.set_monthly_time_and_income(self.current_clock.total_monthly_time)
        self.set_button_text(self.current_clock.state)

    def load_clock_data_into_table(self, rows):
        for row in rows:
            self.clockTableWidget.insertRow(self.clockTableWidget.rowCount())
            for index, item in enumerate(row):
                self.set_next_item(index, item)

    def clock_button_clicked(self):
        if self.current_category:
            time = self.current_clock.clock()
            self.set_button_text(self.current_clock.state)
            self.set_monthly_time_and_income(self.current_clock.total_monthly_time)
            if self.current_clock.state:
                self.clock_in_table(time)
            else:
                self.clock_out_table(time[0], time[1])

    def set_button_text(self, state):
        if state:
            self.clockButton.setText('Clock Out')
        else:
            self.clockButton.setText('Clock In')

    def set_monthly_time_and_income(self, total):
        if self.globalRadioButton.isChecked():
            total = self.global_monthly_time
            income = self.global_monthly_income
        else:
            income = self.calculate_local_monthly_income(total.seconds)
        self.set_monthly_total_time(total)
        self.set_monthly_total_income(income)

    def set_monthly_total_time(self, total):
        seconds = total.seconds
        self.totalTimeLabel.setText(f"Total Time: {format_duration_from_seconds(seconds)}")

    def get_all_clocks(self):
        clocks = []
        for category in self.categories:
            clock = category.clock
            clocks.append(clock)
        return clocks

    def get_all_wages(self):
        wages = []
        for category in self.categories:
            wage = category.wage
            wages.append(wage)
        return wages

    def calculate_global_monthly_income(self, seconds_wages):
        total_income = 0.00
        for seconds, wage in seconds_wages:
            total_income += self.calculate_total_income(seconds, wage)
        return total_income

    def calculate_local_monthly_income(self, seconds):
        return self.calculate_total_income(seconds, self.current_category.wage)

    def calculate_total_income(self, seconds, wage):
        income = seconds / 3600 * float(wage)
        if not income:
            income = 0.00
        return income

    def set_monthly_total_income(self, income):
        self.totalIncomeLabel.setText("Total Income: " + '${:,.2f}'.format(income))

    def set_next_item(self, column, value):
        value = self.format_value(value)
        widget_item = QtWidgets.QTableWidgetItem(str(value))
        widget_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.clockTableWidget.setItem(self.clockTableWidget.rowCount() - 1, column, widget_item)

    def format_value(self, value):
        try:
            value = f"{format_time(value.time())}   |   {format_date(value.date())}"
        except AttributeError:
            try:
                value = format_duration_from_seconds_with_seconds(value.seconds)
            except AttributeError:
                pass
        return value

    def clock_in_table(self, time):
        self.clockTableWidget.insertRow(self.clockTableWidget.rowCount())
        self.set_next_item(0, time)

    def clock_out_table(self, time, total_time):
        self.set_next_item(1, time)
        self.set_next_item(2, total_time)


def format_duration_from_seconds(seconds):
    hours = seconds // 3600
    seconds = seconds - (hours*3600)
    minutes = seconds // 60
    return f"{hours}:{minutes:02}"


def format_duration_from_seconds_with_seconds(seconds):
    hours = seconds // 3600
    seconds = seconds - (hours*3600)
    minutes = seconds // 60
    seconds = seconds - (minutes*60)
    return f"{hours}:{minutes:02}:{seconds:02}"


def format_time(time):
    return f"{time.hour:01}:{time.minute:02}:{time.second:02}"


def format_date(date: datetime):
    return f"{date.month:02}-{date.day:02}-{date.year}"


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Gui()
    mainWindow = QtWidgets.QMainWindow()
    ui.setupUi(mainWindow)
    ui.setup_additional(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
