import pickle
import os
import csv
import configparser


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


def save_list_to_csv(path, list_to_write):
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in list_to_write:
            writer.writerow(row)


def add_dict_to_csv_file(path, dict_to_write, keyword='name'):
    list_of_dicts = get_dicts_from_csv(path)
    add_to_list_if_name_not_duplicate(list_of_dicts, dict_to_write, keyword)
    save_dicts_to_csv_file(path, list_of_dicts)


def save_dicts_to_csv_file(path, dicts_to_save):
    try:
        headers = dicts_to_save[0].keys()
    except IndexError:
        headers = {}
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(dicts_to_save)


def replace_dicts_from_csv(path, old_dict, new_dict):
    delete_dict_from_csv(path, old_dict)
    add_dict_to_csv_file(path, new_dict)


def delete_dict_from_csv(path, dict_to_delete):
    list_of_dicts = get_dicts_from_csv(path)
    for existing_dict in list_of_dicts:
        if existing_dict == dict_to_delete:
            list_of_dicts.remove(existing_dict)
            save_dicts_to_csv_file(path, list_of_dicts)
            return True
    return False


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


def add_to_config(category, option, value):
    config_path = f"{get_app_data_folder('')}/config.ini"
    config = configparser.ConfigParser()
    try_to_add_section_to_config(config, category)
    config.read(config_path)
    config.set(category, str(option), str(value))
    with open(config_path, 'w') as config_file:
        config.write(config_file)


def try_to_add_section_to_config(config, section):
    try:
        config.add_section(section)
    except configparser.DuplicateSectionError:
        pass


def read_from_config(category, option):
    config_path = f"{get_app_data_folder('')}/config.ini"
    config = configparser.ConfigParser()
    config.read(config_path)
    return config.get(category, option)


def does_folder_exist(path):
    return os.path.exists(path)


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


def delete_directory(directory):
    import shutil
    try:
        shutil.rmtree(directory)
        return True
    except Exception:
        return False
