from datetime import datetime, timedelta
from LocalFileHandling import add_to_csv_file, get_list_from_csv, add_file_if_it_does_not_exist, \
    make_folder_if_it_does_not_exist, save_list_to_csv
from Gui.DateAndTimeEdit import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QMenu
from PyQt5.QtCore import QDateTime, Qt


class Clock:
    def __init__(self, user, category):
        self.user = user
        self.state = False
        self.active = False
        self.current_time = None
        self.category = category
        add_file_if_it_does_not_exist(self.file_path)
        self._total_monthly_time = timedelta()
        self.load()

    @property
    def file_path(self):
        return f"{make_folder_if_it_does_not_exist(self.user.directory, 'Clocks')}/{self.category.name}.csv"

    @property
    def total_monthly_time(self):
        return self._total_monthly_time

    @total_monthly_time.setter
    def total_monthly_time(self, value: timedelta):
        self._total_monthly_time = value

    def clock(self):
        if self.state:
            return self.clock_out()
        else:
            return self.clock_in()

    def clock_in(self):
        date_time = datetime.now()
        self.current_time = date_time
        self.save_row(self.current_time, "0:00:00", timedelta())
        self.state = True
        return date_time

    def clock_out(self):
        date_time = datetime.now()
        total_time = date_time - self.current_time
        self.total_monthly_time += total_time
        self.save_row(self.current_time, date_time, total_time, replace=True)
        self.state = False
        return date_time, total_time

    def convert_to_days(self, time_delta):
        return time_delta/timedelta(days=1)

    def save_row(self, clock_in_time, clock_out_time, total_time, replace=False):
        add_to_csv_file(self.file_path, [str(clock_in_time), str(clock_out_time),
                                         str(self.convert_to_days(total_time))], replace)

    def save(self, rows):
        save_list_to_csv(self.file_path, rows)

    def edit_row(self, row_number, old_rows, new_row):
        old_rows[row_number] = new_row
        self.save(old_rows)

    def edit_clock_time(self, row_number, column_number, new_time: datetime):
        old_rows = get_list_from_csv(self.file_path)
        row = old_rows[row_number]
        parsed_row = self.parse_row(row)
        parsed_row[column_number] = new_time
        total_time = parsed_row[1] - parsed_row[0]
        if total_time.seconds >= 0:
            parsed_row[2] = total_time
            row[column_number] = str(new_time)
            print(parsed_row)
            row[2] = str(self.convert_to_days(total_time))
            self.edit_row(row_number, old_rows, row)
            return parsed_row

    def reset(self):
        self.total_monthly_time = timedelta()

    def load(self):
        self.reset()
        rows = get_list_from_csv(self.file_path)
        for row in rows:
            row = self.parse_row(row)
            self.total_monthly_time += row[2]
        return rows

    def parse_row(self, row):
        row[0] = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
        try:
            row[1] = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            self.state = True
            self.current_time = row[0]
        row[2] = timedelta(days=float(row[2]))
        return row

    def check_if_clocked_in(self, rows):
        try:
            if rows[-1][1] == "0:00:00":
                self.state = True
                self.current_time = datetime.strptime(rows[-1][0], '%Y-%m-%d %H:%M:%S.%f')
                return True
        except IndexError:
            return False


def format_time_from_seconds(seconds):
    hours = seconds // 3600
    seconds = seconds - (hours*3600)
    minutes = seconds // 60
    return f"{hours}:{minutes:02}"


class DateAndTimeEditDialog(QDialog):
    def __init__(self, old_date_time: datetime, parent=None):
        super(DateAndTimeEditDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        qdate = QDateTime()
        qdate.setSecsSinceEpoch(old_date_time.timestamp())
        self.ui.dateTimeEdit.setDateTime(qdate)

    def get_edited_time(self):
        self.exec()
        date_time_qt = self.ui.dateTimeEdit.dateTime()
        return date_time_qt.toPyDateTime()


def get_new_date_time(parent):
    old_time = parent.data(Qt.UserRole)
    dialog = DateAndTimeEditDialog(old_time)
    new_time = dialog.get_edited_time()
    if dialog.result():
        return new_time
    return old_time
