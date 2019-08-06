from LocalFileHandling import get_app_data_folder, add_file_if_it_does_not_exist, read_dict_from_csv_file
from Categories import Category, load_categories
from Users import load_user, get_user_path_from_user_name


class ButtonListener:
    def __init__(self):
        self.sniff()

    @property
    def file_path(self):
        return f"{get_app_data_folder('Buttons')}/Buttons.csv"

    def sniff(self):
        pass

    def found_arp(self, address: str):
        try:
            category = self.get_assigned_category(address)
            category.clock.clock()
        except AttributeError:
            pass

    def get_assigned_category(self, address) -> Category:
        button_assignments = self.get_button_assignments()
        try:
            user_name, category_name = button_assignments[address]
            user = load_user(get_user_path_from_user_name(user_name))
            category_dict = self.find_dict_from_key_value(load_categories(user), 'name', category_name)
            return Category(user=user, **category_dict)
        except KeyError:
            pass

    @staticmethod
    def find_dict_from_key_value(dicts, key, value):
        for dict_ in dicts:
            try:
                if dict_[key] == value:
                    return dict_
            except KeyError:
                continue

    def get_button_assignments(self) -> dict:
        add_file_if_it_does_not_exist(self.file_path)
        return get_dict_from_csv(self.file_path)


class ButtonAdder:
    def __init__(self):
        pass
