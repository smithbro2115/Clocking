from LocalFileHandling import get_app_data_folder


class Company:
    def __init__(self, name='', phone_number='', email='', address='', motto=''):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.motto = motto
        self.directory = get_app_data_folder('Companies')
        self.file_path = f"{self.directory}/{name}_company.csv"
