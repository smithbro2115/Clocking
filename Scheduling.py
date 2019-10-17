import datetime
import LocalFileHandling
import yaml


class Scheduler:
    def __init__(self, scheduler_type):
        self.scheduler_type = scheduler_type

    def set_times(self, *days):
        if self.scheduler_type == 'days':
            days_with_last_used = {}
            for day in days:
                days_with_last_used[day] = 0
            self.write_to_file(days_with_last_used)

    @staticmethod
    def write_to_file(value):
        LocalFileHandling.save_to_yaml(f"{LocalFileHandling.get_app_data_folder('')}/scheduler.yml", value)

    @staticmethod
    def read_from_file():
        return LocalFileHandling.load_from_yaml(f"{LocalFileHandling.get_app_data_folder('')}/scheduler.yml")

    def check(self):
        try:
            days = self.read_from_file()
        except FileNotFoundError:
            pass
        else:
            current_day = datetime.datetime.now().day
            for day, last_sent in days.items():
                if datetime.datetime.now().day > day and last_sent:
                    LocalFileHandling.write_to_cache('Email', 'last_sent', datetime.datetime)


class SchedulerEvent:
    def __init__(self, date_time):
        self.date_time = date_time
