from datetime import datetime, timedelta
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from LocalFileHandling import get_app_data_folder, add_to_csv_file, get_list_from_csv, add_file_if_it_does_not_exist


class Clock:
    def __init__(self, table: QTableWidget, button: QPushButton, category):
        self.state = False
        self.current_time = None
        self.table = table
        self.category = category
        self.file_path = f"{get_app_data_folder('Clocks')}/{self.category}.csv"
        add_file_if_it_does_not_exist(self.file_path)
        self.button = button
        self._total_monthly_time = timedelta()
        self.load()

    @property
    def total_monthly_time(self):
        return self._total_monthly_time

    @total_monthly_time.setter
    def total_monthly_time(self, value):
        self.table.setItem(0, 3, QTableWidgetItem(str(value)))
        self._total_monthly_time = value

    def clock(self):
        if self.state:
            self.clock_out()
            self.button.setText("Clock In")
        else:
            self.clock_in()
            self.button.setText("Clock Out")

    def clock_in(self):
        self.table.insertRow(self.table.rowCount())
        date_time = datetime.now()
        self.current_time = date_time
        self.set_next_item(0, date_time)
        self.state = True

    def clock_out(self):
        date_time = datetime.now()
        self.set_next_item(1, date_time)
        total_time = date_time - self.current_time
        self.set_next_item(2, total_time)
        self.total_monthly_time += total_time
        self.save(self.current_time, date_time, total_time)
        self.state = False

    def set_next_item(self, column, value):
        self.table.setItem(self.table.rowCount() - 1, column, QTableWidgetItem(str(value)))

    def convert_to_days(self, time_delta):
        return time_delta/timedelta(days=1)

    def save(self, clock_in_time, clock_out_time, total_time):
        add_to_csv_file(self.file_path, [str(clock_in_time), str(clock_out_time),
                                         str(self.convert_to_days(total_time))])

    def load(self):
        rows = get_list_from_csv(self.file_path)
        for row in rows:
            self.table.insertRow(self.table.rowCount())
            row[2] = timedelta(days=float(row[2]))
            for index, item in enumerate(row):
                self.set_next_item(index, item)
            self.total_monthly_time += row[2]
