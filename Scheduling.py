import datetime
import LocalFileHandling


# TODO Add compensating for later days of the month


class Scheduler:
    def __init__(self, scheduler_type, name, function):
        self.scheduler_type = scheduler_type
        self.name = name
        self.function = function
        self.path = f'{LocalFileHandling.get_app_data_folder("")}/{name}.yaml'
        self.config_path = f'{LocalFileHandling.get_app_data_folder("")}/{name}_config.yaml'
        try:
            self._compensate = self.read_from_file(self.config_path)
        except FileNotFoundError:
            self._compensate = False
        self.compensate = self._compensate

    @property
    def compensate(self):
        return self._compensate

    @compensate.setter
    def compensate(self, value):
        self.write_to_file(value, self.config_path)
        self._compensate = value

    def set_times(self, *days):
        if self.scheduler_type == 'days':
            days_with_last_used = {}
            for day in days:
                days_with_last_used[day] = 0
            self.write_to_file(days_with_last_used, self.path)

    @staticmethod
    def write_to_file(value, path):
        LocalFileHandling.save_to_yaml(path, value)

    @staticmethod
    def read_from_file(path):
        return LocalFileHandling.load_from_yaml(path)
    #
    # def set_last_used(self, day, days):
    #     days[day] = datetime.datetime.now()
    #     self.write_to_file(days)
    #     return days

    def check(self):
        try:
            days = self.read_from_file(self.path)
        except FileNotFoundError:
            pass
        else:
            current_time = datetime.datetime.now()
            new_days = {}
            for day, last_sent in days.items():
                if last_sent == 0:
                    new_days[day] = current_time
                else:
                    condition, current_time = self.check_condition(day, current_time, last_sent)
                    if condition:
                        new_days = self.get_new_dict_with_all_dates_now(days, current_time)
                        self.function()
                        break
                    else:
                        new_days[day] = last_sent
            self.write_to_file(new_days, self.path)

    def check_condition(self, day, current_time, last_sent):
        conditions = []
        day = self.check_if_day_is_out_of_range(day)
        if self.compensate:
            current_time = self.weekend_condition(day, current_time)
        conditions.append(self.passed_day_condition(day, current_time))
        conditions.append(self.already_sent_condition(day, current_time, last_sent))
        return False not in conditions, current_time

    @staticmethod
    def check_if_day_is_out_of_range(day):
        current_date = datetime.datetime.now()
        try:
            datetime.datetime(current_date.year, current_date.month, day)
            return day
        except ValueError:
            return last_day_of_month(current_date).day

    @staticmethod
    def weekend_condition(day, current_time: datetime.datetime):
        new_time = datetime.datetime(current_time.year, current_time.month, day, current_time.hour, current_time.minute)
        if new_time.weekday() == 5 or new_time.weekday() == 6 and current_time.weekday() == 4:
            return new_time
        return current_time

    @staticmethod
    def passed_day_condition(day, current_time: datetime.datetime):
        return current_time.day >= day

    @staticmethod
    def already_sent_condition(day, current_time: datetime.datetime, last_sent):
        return (current_time - last_sent).days > (current_time.day - day)

    @staticmethod
    def get_new_dict_with_all_dates_now(days, date_time):
        new_dict = {}
        for key, _ in days.items():
            new_dict[key] = date_time
        return new_dict


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

