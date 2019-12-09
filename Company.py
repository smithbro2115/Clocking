from LocalFileHandling import get_app_data_folder, add_dict_to_list_csv_file, add_file_if_it_does_not_exist, \
    get_dicts_from_csv
import os


class Company:
    def __init__(self, name='', phone_number='', email='', address='', motto=''):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.motto = motto
        self.directory = get_app_data_folder('Companies')
        self.file_path = f"{self.directory}/company_company.csv"

    @property
    def info(self):
        return {'name': self.name, 'phone_number': self.phone_number, 'email': self.email, 'address': self.address,
                'motto': self.motto}

    def save(self):
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
        add_file_if_it_does_not_exist(self.file_path)
        add_dict_to_list_csv_file(self.file_path, self.info, keyword='name')

    def edit(self):
        os.remove(self.file_path)
        add_file_if_it_does_not_exist(self.file_path)
        self.save()


def load_companies(path):
    add_file_if_it_does_not_exist(path)
    raw_companies = get_dicts_from_csv(path)
    companies = []
    for raw_company in raw_companies:
        company = Company(**raw_company)
        companies.append(company)
    return companies


def make_company_from_dialog(dialog):
    ui = dialog.ui
    return Company(ui.nameLineEdit.text(), ui.phoneLineEdit.text(), ui.emailLineEdit.text(),
                   ui.addressPlainTextEdit.toPlainText(), ui.mottoLineEdit.text())
