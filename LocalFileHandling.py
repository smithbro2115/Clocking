import pickle
import os
import csv


def pickle_obj(path, obj):
    with open(f"{path}.pkl", 'wb') as f:
        try:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        except TypeError as e:
            raise AttributeError(e)


def load_pickle_obj(path):
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except EOFError:
        return []


def add_to_csv_file(path, list_to_write):
    new_list = get_list_from_csv(path)
    new_list.append(list_to_write)
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in new_list:
            writer.writerow(row)


def add_dict_to_csv_file(path, dict_to_write):
    list_of_dicts = get_dicts_from_csv(path)
    list_of_dicts.append(dict_to_write)
    print(list_of_dicts)
    headers = dict_to_write.keys()
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(list_of_dicts)


def get_list_from_csv(path):
    with open(path, mode='r') as file:
        return list(csv.reader(file))


def get_dicts_from_csv(path):
    with open(path, mode='r') as file:
        raw_dicts = csv.DictReader(file)
        list_of_dicts = []
        for raw_dict in raw_dicts:
            list_of_dicts.append(dict(raw_dict))
        return list_of_dicts


def make_folder_if_it_does_not_exist(src, folder):
    new_src = src.replace('\\', '/')
    directory = f"{new_src}/{folder}"
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass
    return directory


def get_app_data_folder(folder):
    app_data_path = os.getenv('APPDATA')
    clocking_path = make_folder_if_it_does_not_exist(app_data_path, 'Clocking')
    return make_folder_if_it_does_not_exist(clocking_path, folder)


def add_file_if_it_does_not_exist(path):
    open(path, 'a').close()


def check_if_file_exists(path):
    try:
        open(path, 'r')
        return True
    except FileNotFoundError:
        return False
