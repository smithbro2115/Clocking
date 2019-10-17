import datetime
import LocalFileHandling


class Scheduler:
    def __init__(self, scheduler_type, name, function):
        self.scheduler_type = scheduler_type
        self.name = name
        self.function = function
        self.path = f'{LocalFileHandling.get_app_data_folder("")}/{name}.yaml'

    def set_times(self, *days):
        if self.scheduler_type == 'days':
            days_with_last_used = {}
            for day in days:
                days_with_last_used[day] = 0
            self.write_to_file(days_with_last_used)

    def write_to_file(self, value):
        LocalFileHandling.save_to_yaml(self.path, value)

    def read_from_file(self):
        return LocalFileHandling.load_from_yaml(self.path)
    #
    # def set_last_used(self, day, days):
    #     days[day] = datetime.datetime.now()
    #     self.write_to_file(days)
    #     return days

    def check(self):
        try:
            days = self.read_from_file()
        except FileNotFoundError:
            pass
        else:
            current_time = datetime.datetime.now()
            new_days = {}
            for day, last_sent in days.items():
                if last_sent == 0:
                    new_days[day] = current_time
                elif current_time.day >= day and (current_time-last_sent).days > (current_time.day - day):
                    LocalFileHandling.write_to_cache('Email', 'last_sent', datetime.datetime)
                    new_days = self.get_new_dict_with_all_dates_now(days, current_time)
                    self.function()
                    break
                else:
                    new_days[day] = last_sent
            self.write_to_file(new_days)

    @staticmethod
    def get_new_dict_with_all_dates_now(days, date_time):
        new_dict = {}
        for key, _ in days.items():
            new_dict[key] = date_time
        return new_dict


class SchedulerEvent:
    def __init__(self, date_time):
        self.date_time = date_time
