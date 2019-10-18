from PyQt5 import QtWidgets, QtCore
from Gui import MainWindow
from utils import are_you_sure_prompt, make_dir, ChoiceDialog, resource_path, copy_file_to_directory, start_program,\
    close_program, delete_file, error_dialog
import getpass
import qdarkstyle
import Categories
from time import sleep
from platform import system
from Gui.CustomPyQtDialogsAndWidgets import AssignButtonDialog, TimedEmitter, EmailTemplate, AssignDatesDialog, \
    SavePathDialog, UsersToEmailDialog
from Clock import get_new_date_time, DateAndTimeContextMenu, delete_clock
from Users import add_user, load_users, delete_user, edit_user_dialog, move_user
from datetime import timedelta, datetime
from Preferences import PreferenceDialog
from configparser import NoSectionError, NoOptionError
from LocalFileHandling import delete_directory, read_from_config, get_app_data_folder, add_to_config, \
    add_to_dict_from_csv_file, read_dict_from_csv_file, convert_string_tuple_into_tuple_dict, save_dict_to_csv_file, \
    write_to_cache, read_from_cache
import Scheduling
if system() == 'Windows':
    from Buttons import AddButtonDialog


PLATFORM = system()


class Gui(MainWindow.Ui_MainWindow):
    def __init__(self):
        self.categories = []
        self.users = []
        self._current_user = None
        self._current_category = None
        self.current_clock = None
        self.buttons_activated = False
        self.buttons_file_path = f"{get_app_data_folder('Buttons')}/Buttons.csv"
        self._global_monthly_time = timedelta()
        self.background_thread_pool = QtCore.QThreadPool()
        self.update_thread = TimedEmitter(2, -1)
        self.email_scheduler_thread = TimedEmitter(30, -1)
        self.email_scheduler = Scheduling.Scheduler('days', 'email_scheduler', lambda: print('triggered'))

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
        self.clockTableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.clockTableWidget.customContextMenuRequested.connect(self.table_right_clicked)
        self.clockTableWidget.setStyleSheet("""QTableWidget::item:hover { background: transparent; }""")
        self.actionEdit_User.triggered.connect(self.edit_user_clicked)
        self.actionSet_Email_Template.triggered.connect(self.set_email_template_clicked)
        self.actionAssign_Days_to_Send_Emails.triggered.connect(self.assign_email_dates_clicked)
        self.clockTableWidget.itemDoubleClicked.connect(self.clock_table_select_clicked)
        self.actionClock.triggered.connect(self.clock_button_clicked)
        self.actionExport_Invoice.triggered.connect(lambda: self.export_invoice_triggered(self.current_user, self.categories))
        self.actionExport_All_Invoices.triggered.connect(self.export_all_invoices)
        self.actionSet_Default_Invoice_Path.triggered.connect(self.set_default_invoice_path)
        self.actionPreferences.triggered.connect(self.preferences_clicked)
        self.actionAdd_Button.triggered.connect(self.add_button_action_triggered)
        self.actionSetup_Emailing.triggered.connect(self.setup_emailing)
        self.actionSet_Users_Invoices_to_Email.triggered.connect(self.set_users_to_email_triggered)
        self.actionAssign_Buttons.triggered.connect(self.assign_buttons_action_triggered)
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
        self.try_to_recall_last_used_settings()
        self.update_thread.signals.time_elapsed.connect(self.update_table)
        self.email_scheduler_thread.signals.time_elapsed.connect(self.email_scheduler.check)
        self.background_thread_pool.start(self.update_thread)
        try:
            if bool(int(read_from_config('EMAIL', 'activated'))):
                self.background_thread_pool.start(self.email_scheduler_thread)
        except (NoOptionError, NoSectionError):
            pass
        if system() == 'Darwin':
            self.menubar.removeAction(self.menubar.actions()[2])

    def __del__(self):
        self.update_thread.canceled = True
        self.email_scheduler_thread.canceled = True

    def try_to_recall_last_used_settings(self):
        try:
            user_name = read_from_cache('LAST_USED', 'user')
            category = read_from_cache('LAST_USED', 'category')
            self.userBox.setCurrentIndex(self.userBox.findText(user_name))
            self.categoryBox.setCurrentIndex(self.categoryBox.findText(category))
        except(NoOptionError, NoSectionError):
            pass

    def activate_dash_buttons(self):
        try:
            if not bool(int(read_from_config("BUTTONS", 'setup'))):
                path = resource_path('Clocking Buttons.exe')
                new_path = copy_file_to_directory(path, self.get_startup_folder())
                start_program(new_path)
                add_to_config('BUTTONS', 'setup', 1)
        except(NoSectionError, NoOptionError):
                path = resource_path('Clocking Buttons.exe')
                new_path = copy_file_to_directory(path, self.get_startup_folder())
                start_program(new_path)
                add_to_config('BUTTONS', 'setup', 1)

    def deactivate_dash_buttons(self):
        if bool(int(read_from_config("BUTTONS", 'setup'))):
            path = f"{self.get_startup_folder()}/Clocking Buttons.exe"
            close_program("Clocking Buttons.exe")
            sleep(.5)
            delete_file(path)
            add_to_config('BUTTONS', 'setup', 0)

    def get_startup_folder(self):
        USER_NAME = getpass.getuser()
        return r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME

    def add_button_action_triggered(self):
        dialog = AddButtonDialog()
        if dialog.result():
            add_to_dict_from_csv_file(self.buttons_file_path, {dialog.address: (None, None)})

    def assign_buttons_action_triggered(self):
        buttons = convert_string_tuple_into_tuple_dict(read_dict_from_csv_file(self.buttons_file_path))
        dialog = AssignButtonDialog(buttons, self.users)
        dialog.exec_()
        if dialog.result():
            save_dict_to_csv_file(self.buttons_file_path, dialog.new_button_dict)

    def table_right_clicked(self, point):
        item = self.clockTableWidget.itemAt(point)
        if item:
            DateAndTimeContextMenu(self.clockTableWidget.mapToGlobal(point), item,
                                   self.clock_table_edit_triggered, self.clock_table_delete_triggered)

    def export_invoice_triggered(self, user, categories):
        from Exporting import make_invoice_excel, GetFileLocationDialog, get_file_invoice_name
        if self.current_category:
            file_location_dialog = GetFileLocationDialog(get_file_invoice_name(user), caption='Export Invoice')
            result = file_location_dialog.get_save_path()
            if result:
                delete_clocks_dialog = ChoiceDialog('Do you want to reset all the clocks for this user?', 'EXPORTING',
                                                    'reset_clocks_after_export')
                if delete_clocks_dialog.result():
                    make_invoice_excel(user, categories, path=result)
                    self.handle_delete_clocks(user, delete_clocks_dialog.yes_or_no)

    def handle_delete_clocks(self, user, result):
        if result:
            if user == self.current_user:
                self.reset_current_clocks()
            else:
                self.delete_all_users_clocks(user)

    def export_all_invoices(self):
        self.export_invoices(self.users)

    @staticmethod
    def export_invoices(users):
        from Exporting import make_invoice_excel, GetFileLocationDialog, get_file_invoice_name, get_invoice_folder_name
        folder_name = get_invoice_folder_name()
        dialog = GetFileLocationDialog(folder_name, "Export Invoices")
        path = dialog.get_save_path()
        make_dir(path)
        if path:
            for user in users:
                make_invoice_excel(user, Categories.load_categories(user), path=f"{path}/{get_file_invoice_name(user)}")

    @staticmethod
    def set_default_invoice_path():
        dialog = SavePathDialog()
        result = dialog.exec_()
        if result:
            add_to_config('INVOICE', 'save_path', dialog.save_path)
        return result

    def set_users_to_email_triggered(self):
        dialog = UsersToEmailDialog(self.users)
        return dialog.exec_()

    def setup_emailing(self):
        result = self.set_email_template_clicked()
        if not result:
            return None
        result = self.set_default_invoice_path()
        if not result:
            return None
        result = self.assign_email_dates_clicked()
        if not result:
            return None
        result = self.set_users_to_email_triggered()
        if result:
            add_to_config('EMAIL', 'activated', 1)

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
            seconds_wages.append((clock.total_monthly_time.total_seconds(), wage))
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

    def set_email_template_clicked(self):
        dialog = EmailTemplate()
        return dialog.exec_()

    def assign_email_dates_clicked(self):
        dialog = AssignDatesDialog()
        dialog.exec_()
        if dialog.result():
            self.email_scheduler.set_times(*dialog.selected_dates)
            return True

    def clock_table_select_clicked(self, item):
        self.clock_table_edit_triggered(item.row(), item.column(), item.data(QtCore.Qt.UserRole))

    def clock_table_edit_triggered(self, row_number, column, data):
        new_date_time = get_new_date_time(data)
        if isinstance(new_date_time, datetime):
            try:
                row = self.current_clock.edit_clock_time(row_number, column, new_date_time)
            except RuntimeError as e:
                error_dialog(str(e))
            else:
                if row:
                    for index, item in enumerate(row):
                        self.set_next_item(row_number, index, item)
                    self.set_monthly_time_and_income(self.current_clock.total_monthly_time)

    def clock_table_delete_triggered(self, row):
        if are_you_sure_prompt('Are you sure you want to delete this row?'):
            self.current_clock.delete_row(row)
            self.clockTableWidget.removeRow(row)
            self.set_monthly_time_and_income(self.current_clock.total_monthly_time)

    def preferences_clicked(self):
        dialog = PreferenceDialog()
        dialog.exec()
        if dialog.result():
            if dialog.user_location_changed:
                self.move_users(dialog.previous_user_save_location)
            if dialog.dash_buttons_activated_changed:
                if dialog.dash_buttons_activated:
                    self.activate_dash_buttons()
                else:
                    self.deactivate_dash_buttons()
            if dialog.email_invoices_changed:
                if dialog.email_invoices_activated:
                    self.email_scheduler_thread = TimedEmitter(30, -1)
                    self.email_scheduler_thread.signals.time_elapsed.connect(self.email_scheduler.check)
                    self.background_thread_pool.start(self.email_scheduler_thread)
                else:
                    self.email_scheduler_thread.canceled = True

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
            user = edit_user_dialog(self.current_user)
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
        self.set_monthly_time_and_income(timedelta())
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

    def update_table(self):
        try:
            original_state = self.current_clock.state
            data = self.get_table_positional_data()
            self.load_clock()
            self.set_table_positional_data(data)
            return original_state != self.current_clock.state
        except AttributeError:
            pass

    def get_table_positional_data(self):
        current_index = self.clockTableWidget.currentIndex()
        current_scroll = self.clockTableWidget.verticalScrollBar().sliderPosition()
        return current_index, current_scroll

    def set_table_positional_data(self, data):
        self.clockTableWidget.setCurrentIndex(data[0])
        self.clockTableWidget.verticalScrollBar().setSliderPosition(data[1])

    def load_clock(self):
        self.current_clock = self.current_category.clock
        self.current_clock.active = False
        self.clockTableWidget.setRowCount(0)
        self.current_clock.active = True
        rows = self.current_clock.load()
        self.current_clock.check_if_clocked_in(rows)
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
            if self.update_table():
                result = are_you_sure_prompt("This clock has already been modified somewhere else, "
                                             "are you sure you want to do this?")
                if result:
                    self.clock()
            else:
                self.clock()

    def clock(self):
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
            income = self.calculate_local_monthly_income(total.total_seconds())
        self.set_monthly_total_time(total)
        self.set_monthly_total_income(income)

    def set_monthly_total_time(self, total):
        seconds = total.total_seconds()
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
        try:
            return self.calculate_total_income(seconds, self.current_category.wage)
        except AttributeError:
            return self.calculate_total_income(seconds, 0)

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
                value = format_duration_from_seconds_with_seconds(value.total_seconds())
            except AttributeError:
                pass
        if value == "0:00:00":
            return ""
        return value

    def clock_in_table(self, time):
        self.clockTableWidget.insertRow(self.clockTableWidget.rowCount())
        self.set_next_item(self.clockTableWidget.rowCount() - 1, 0, time)

    def clock_out_table(self, time, total_time):
        self.set_next_item(self.clockTableWidget.rowCount() - 1, 1, time)
        self.set_next_item(self.clockTableWidget.rowCount() - 1, 2, total_time)

    def delete_all_users_clocks(self, user):
        categories = Categories.load_categories(user)
        for clock in [category.clock for category in categories]:
            delete_clock(clock)

    def reset_current_clocks(self):
        self.delete_all_users_clocks(self.current_user)
        current_user_index = self.userBox.currentIndex()
        current_category_index = self.categoryBox.currentIndex()
        self.userBox.clear()
        self.load_users()
        self.userBox.setCurrentIndex(current_user_index)
        self.reset_category()
        self.categoryBox.setCurrentIndex(current_category_index)


def format_duration_from_seconds(seconds):
    hours = seconds // 3600
    seconds = seconds - (hours*3600)
    minutes = seconds // 60
    return f"{round(hours)}:{round(minutes):02}"


def format_duration_from_seconds_with_seconds(seconds):
    hours = seconds // 3600
    seconds = seconds - (hours*3600)
    minutes = seconds // 60
    seconds = seconds - (minutes*60)
    return f"{round(hours)}:{round(minutes):02}:{round(seconds):02}"


def format_time(time):
    return f"{time.hour:01}:{time.minute:02}:{time.second:02}"


def format_date(date: datetime):
    return f"{date.month:02}-{date.day:02}-{date.year}"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, gui_ui):
        super(MainWindow, self).__init__()
        self.ui = gui_ui

    def closeEvent(self, *args, **kwargs):
        if self.ui.current_category:
            write_to_cache('LAST_USED', 'user', f"{self.ui.current_user.first_name} {self.ui.current_user.last_name}")
            write_to_cache('LAST_USED', 'category', self.ui.current_category.name)
        super(MainWindow, self).close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Gui()
    mainWindow = MainWindow(ui)
    ui.setupUi(mainWindow)
    ui.setup_additional(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
