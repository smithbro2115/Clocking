from datetime import datetime, timedelta
from LocalFileHandling import add_to_csv_file, get_list_from_csv, add_file_if_it_does_not_exist, \
    make_folder_if_it_does_not_exist


class Clock:
    def __init__(self, user, time_label, income_label, category):
        self.user = user
        self.state = False
        self.active = False
        self.current_time = None
        self.category = category
        self.time_label = time_label
        self.income_label = income_label
        self.file_path = f"{make_folder_if_it_does_not_exist(user.directory, 'Clocks')}/{self.category.name}.csv"
        add_file_if_it_does_not_exist(self.file_path)
        self._total_monthly_time = timedelta()
        self.load()

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
        self.save(self.current_time, "0:00:00", timedelta())
        self.state = True
        return date_time

    def clock_out(self):
        date_time = datetime.now()
        total_time = date_time - self.current_time
        self.total_monthly_time += total_time
        self.save(self.current_time, date_time, total_time, replace=True)
        self.state = False
        return date_time, total_time

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