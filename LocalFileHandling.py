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


def add_to_csv_file(path, list_to_write, replace):
    new_list = get_list_from_csv(path)
    if replace:
        new_list.pop()
    new_list.append(list_to_write)
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in new_list:
            writer.writerow(row)


def add_dict_to_csv_file(path, dict_to_write, keyword='name'):
    list_of_dicts = get_dicts_from_csv(path)
    add_to_list_if_name_not_duplicate(list_of_dicts, dict_to_write, keyword)
    headers = dict_to_write.keys()
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(list_of_dicts)


def add_to_list_if_name_not_duplicate(dict_list, new_dict, keyword):
    for existing in dict_list:
        if existing[keyword] == new_dict[keyword]:
            break
    else:
        dict_list.append(new_dict)
    return dict_list


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
