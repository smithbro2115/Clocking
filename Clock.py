from datetime import datetime, timedelta
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from LocalFileHandling import add_to_csv_file, get_list_from_csv, add_file_if_it_does_not_exist, \
    make_folder_if_it_does_not_exist


class Clock:
    def __init__(self, user, table: QTableWidget, button: QPushButton, time_label, income_label, category):
        self.user = user
        self._state = False
        self.active = False
        self.current_time = None
        self.table = table
        self.category = category
        self.time_label = time_label
        self.income_label = income_label
        self.file_path = f"{make_folder_if_it_does_not_exist(user.directory, 'Clocks')}/{self.category.name}.csv"
        add_file_if_it_does_not_exist(self.file_path)
        self.button = button
        self._total_monthly_time = timedelta()
        self.load()

    @property
    def total_monthly_time(self):
        return self._total_monthly_time

    @total_monthly_time.setter
    def total_monthly_time(self, value: timedelta):
        self.time_label.setText(f"Total Time: {format_time_from_seconds(value.seconds)}")
        income = value.seconds/3600*float(self.category.wage)
        if not income:
            income = 0.00
        self.income_label.setText("Total Income: " + '${:,.2f}'.format(income))
        self._total_monthly_time = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.set_button_text()

    def set_button_text(self):
        if self.active:
            if self.state:
                self.button.setText("Clock Out")
            else:
                self.button.setText("Clock In")

    def clock(self):
        if self.state:
            self.clock_out()
        else:
            self.clock_in()

    def clock_in(self):
        self.table.insertRow(self.table.rowCount())
        date_time = datetime.now()
        self.current_time = date_time
        self.set_next_item(0, date_time)
        self.save(self.current_time, "0:00:00", timedelta())
        self.state = True

    def clock_out(self):
        date_time = datetime.now()
        self.set_next_item(1, date_time)
        total_time = date_time - self.current_time
        self.set_next_item(2, total_time)
        self.total_monthly_time += total_time
        self.save(self.current_time, date_time, total_time, replace=True)
        self.state = False

    def set_next_item(self, column, value):
        self.table.setItem(self.table.rowCount() - 1, column, QTableWidgetItem(str(value)))

    def convert_to_days(self, time_delta):
        return time_delta/timedelta(days=1)

    def save(self, clock_in_time, clock_out_time, total_time, replace=False):
        add_to_csv_file(self.file_path, [str(clock_in_time), str(clock_out_time),
                                         str(self.convert_to_days(total_time))], replace)

    def reset(self):
        self.total_monthly_time = timedelta()

    def load(self):
        self.reset()
        rows = get_list_from_csv(self.file_path)
        for row in rows:
            self.table.insertRow(self.table.rowCount())
            row[2] = timedelta(days=float(row[2]))
            for index, item in enumerate(row):
                self.set_next_item(index, item)
            self.total_monthly_time += row[2]
        self.check_if_clocked_in(rows)

    def check_if_clocked_in(self, rows):
        try:
            if rows[-1][1] == "0:00:00":
                self.state = True
                self.current_time = datetime.strptime(rows[-1][0], '%Y-%m-%d %H:%M:%S.%f')
        except IndexError:
            pass


def format_time_from_seconds(seconds):
    hours = seconds // 3600
    seconds = seconds - (hours*3600)
    minutes = seconds // 60
    return f"{hours}:{minutes:02}"
