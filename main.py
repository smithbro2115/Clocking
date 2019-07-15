from PyQt5 import QtGui, QtWidgets, QtCore
from Gui import MainWindow
from utils import are_you_sure_prompt, make_dir
import qdarkstyle
import Categories
from Clock import get_new_date_time
from Users import add_user, load_users, delete_user, edit_user, move_user
from datetime import timedelta, datetime
from Exporting import make_invoice_excel, GetFileLocationDialog, get_file_invoice_name, get_invoice_folder_name
from Preferences import PreferenceDialog
from configparser import NoSectionError
from LocalFileHandling import delete_directory, read_from_config, get_app_data_folder, add_to_config


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
        self.actionAdd_Category_2.triggered.connect(self.add_category)
        self.actionDelete_Category.triggered.connect(self.delete_category_clicked)
        self.actionEdit_Category.triggered.connect(self.edit_category_clicked)
        self.userAddAction_2.triggered.connect(self.add_user_button_clicked)
        self.actionDelete_User.triggered.connect(self.delete_user_clicked)
        self.actionEdit_User.triggered.connect(self.edit_user_clicked)
        self.clockTableWidget.itemDoubleClicked.connect(self.clock_table_edit_triggered)
        self.actionClock.triggered.connect(self.clock_button_clicked)
        self.actionExport_Invoice.triggered.connect(lambda: self.export_invoice(self.current_user, self.categories))
        self.actionExport_All_Invoices.triggered.connect(self.export_all_invoices)
        self.actionPreferences.triggered.connect(self.preferences_clicked)
        self.load_users()
        self.load_config()
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

    def export_invoice(self, user, categories):
        if self.current_category:
            dialog = GetFileLocationDialog(get_file_invoice_name(user))
            result = dialog.get_save_path()
            if result:
                make_invoice_excel(user, categories, path=result)

    def export_all_invoices(self):
        self.export_invoices(self.users)

    def export_invoices(self, users):
        folder_name = get_invoice_folder_name()
        dialog = GetFileLocationDialog(folder_name)
        path = dialog.get_save_path()
        make_dir(path)
        if path:
            for user in users:
                make_invoice_excel(user, Categories.load_categories(user), path=f"{path}/{get_file_invoice_name(user)}")

    def load_config(self):
        try:
            return f"{read_from_config('USERS', 'USER_SAVE_LOCATION')}"
        except NoSectionError:
            app_data_folder = get_app_data_folder('')
            add_to_config('USERS', 'USER_SAVE_LOCATION', app_data_folder)
            return app_data_folder

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

    def clock_table_edit_triggered(self, item):
        row_number = item.row()
        new_date_time = get_new_date_time(item)
        if isinstance(new_date_time, datetime):
            row = self.current_clock.edit_clock_time(row_number, item.column(), new_date_time)
            for index, item in enumerate(row):
                self.set_next_item(row_number, index, item)

    def preferences_clicked(self):
        dialog = PreferenceDialog()
        dialog.exec()
        if dialog.result():
            if dialog.user_location_changed:
                self.move_users(dialog.previous_user_save_location)

    def move_users(self, old_directory):
        current_user = self.userBox.currentIndex()
        current_category = self.categoryBox.currentIndex()
        self.reset()
        self.userBox.clear()
        path = read_from_config('USERS', 'USER_SAVE_LOCATION')
        for user in self.users:
            move_user(user, path, old_directory)
        delete_directory(f"{old_directory}/Users")
        self.load_users()
        self.userBox.setCurrentIndex(current_user)
        self.categoryBox.setCurrentIndex(current_category)

    def add_user_button_clicked(self):
        user = add_user()
        if user:
            self.users.append(user)
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
                self.set_next_item(self.clockTableWidget.rowCount() - 1, index, item)

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

    def set_next_item(self, row, column, value):
        formatted_value = self.format_value(value)
        widget_item = QtWidgets.QTableWidgetItem(str(formatted_value))
        widget_item.setData(QtCore.Qt.UserRole, value)
        widget_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.clockTableWidget.setItem(row, column, widget_item)

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
        self.set_next_item(self.clockTableWidget.rowCount() - 1, 0, time)

    def clock_out_table(self, time, total_time):
        self.set_next_item(self.clockTableWidget.rowCount() - 1, 1, time)
        self.set_next_item(self.clockTableWidget.rowCount() - 1, 2, total_time)


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
