from Gui.AddUserDialog import Ui_AddUserDialog
from PyQt5 import QtWidgets, QtGui
import qdarkstyle
from utils import cannot_except_dialog, make_dir
from LocalFileHandling import get_app_data_folder, add_dict_to_list_csv_file, add_file_if_it_does_not_exist, \
	make_folder_if_it_does_not_exist, get_dicts_from_csv, read_from_config, add_to_config, does_folder_exist, \
	delete_directory
import os
from configparser import NoSectionError


class AddUserDialog(QtWidgets.QDialog):
	def __init__(self, first_name='', last_name='', default_wage='',
					phone_number='', email='', address='', parent=None, email_invoice=False, **kwargs):
		super(AddUserDialog, self).__init__(parent=parent)
		self.ui = Ui_AddUserDialog()
		self.ui.setupUi(self)
		self.ui.wageLineEdit.setValidator(QtGui.QDoubleValidator())
		self.ui.firstNameLineEdit.setFocus()
		self.required_fields = [self.ui.firstNameLineEdit, self.ui.lastNameLineEdit, self.ui.addressTextEdit,
								self.ui.phoneLineEdit, self.ui.emailLineEdit]
		self.fields_to_check_for_bad_characters = [self.ui.firstNameLineEdit, self.ui.lastNameLineEdit]
		self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
		self.ui.firstNameLineEdit.setText(first_name)
		self.ui.lastNameLineEdit.setText(last_name)
		self.ui.wageLineEdit.setText(str(default_wage))
		self.ui.phoneLineEdit.setText(phone_number)
		self.ui.emailLineEdit.setText(email)
		self.ui.addressTextEdit.setText(address)
		self.ui.emailInvoinceCheckBox.setChecked(email_invoice)
		self.exec_()

	@staticmethod
	def check_if_filled(fields):
		try:
			for field in fields:
				try:
					text = field.text()
				except AttributeError:
					text = field.toPlainText()
				if not text:
					return False
			return True
		except TypeError:
			if not fields.text():
				return False
			return True

	def check_for_bad_characters(self):
		bad_letters = ['/', '\\']
		for bad in bad_letters:
			for field in self.fields_to_check_for_bad_characters:
				if bad in field.text():
					cannot_except_dialog()
					return True
		return False

	def accept(self):
		if self.check_if_filled(self.required_fields) and not self.check_for_bad_characters():
			super(AddUserDialog, self).accept()


class User:
	def __init__(self, first_name, last_name, phone_number, email, address, default_wage=0.0, **kwargs):
		self.first_name = first_name
		self.last_name = last_name
		self.default_wage = default_wage
		self.phone_number = phone_number
		self.email = email
		self.address = address
		try:
			self.email_invoice = kwargs['email_invoice'] == 'True' or kwargs['email_invoice'] is True
		except KeyError:
			self.email_invoice = False
		make_dir(self.directory)
		self.file_path = f"{self.directory}/{self.first_name}_{self.last_name}_user.csv"
		add_file_if_it_does_not_exist(self.file_path)
		self.save()

	@property
	def full_name(self):
		return f"{self.first_name} {self.last_name}"

	@property
	def directory(self):
		try:
			return f"{read_from_config('USERS', 'USER_SAVE_LOCATION')}/Users/{self.first_name}_{self.last_name}"
		except NoSectionError:
			make_folder_if_it_does_not_exist(get_app_data_folder(''), f"{self.first_name}_{self.last_name}")
			add_to_config('USERS', 'USER_SAVE_LOCATION', get_app_data_folder(''))
			return f"{get_app_data_folder('')}/{self.first_name}_{self.last_name}"

	@property
	def info(self):
		return {'first_name': self.first_name, 'last_name': self.last_name, 'default_wage': self.default_wage,
				'phone_number': self.phone_number, 'email': self.email, 'address': self.address,
				'email_invoice': self.email_invoice}

	def save(self):
		add_dict_to_list_csv_file(self.file_path, self.info, keyword='last_name')

	def edit(self):
		os.remove(self.file_path)
		add_file_if_it_does_not_exist(self.file_path)
		self.save()


def add_user():
	dialog = AddUserDialog()
	return make_user(dialog)


def make_user(dialog):
	if not dialog.result():
		return None
	try:
		user = User(dialog.ui.firstNameLineEdit.text(), dialog.ui.lastNameLineEdit.text(),
					dialog.ui.phoneLineEdit.text(), dialog.ui.emailLineEdit.text(),
					dialog.ui.addressTextEdit.toPlainText(), float(dialog.ui.wageLineEdit.text()),
					email_invoice=dialog.ui.emailInvoinceCheckBox.isChecked())
	except ValueError:
		user = User(dialog.ui.firstNameLineEdit.text(), dialog.ui.lastNameLineEdit.text(),
					dialog.ui.phoneLineEdit.text(), dialog.ui.emailLineEdit.text(),
					dialog.ui.addressTextEdit.toPlainText(), email_invoice=dialog.ui.emailInvoinceCheckBox.isChecked())
	return user


def get_user_file_paths():
	try:
		path = f"{read_from_config('USERS', 'USER_SAVE_LOCATION')}"
	except NoSectionError:
		return []
	else:
		paths = []
		for root, dirs, files in os.walk(path):
			for file in files:
				if file.endswith('user.csv'):
					paths.append(os.path.join(root, file))
		return paths


def load_user(path):
	add_file_if_it_does_not_exist(path)
	raw_users = get_dicts_from_csv(path)
	users = []
	for raw_user in raw_users:
		user = User(**raw_user)
		users.append(user)
	return users


def load_users():
	paths = get_user_file_paths()
	users = []
	for path in paths:
		users.extend(load_user(path))
	return users


def delete_user(user):
	return delete_directory(user.directory)


def move_user(user, location, old_location):
	import shutil
	old_info = user.info
	os.remove(user.file_path)
	new_directory = f"{location}/Users"
	old_location = f"{old_location}/Users"
	shutil.move(old_location, new_directory)
	return User(**old_info)


def edit_user_dialog(user):
	import shutil
	dialog = AddUserDialog(**user.info)
	if not dialog.result():
		return None
	os.remove(user.file_path)
	new_directory = f"{read_from_config('USERS', 'USER_SAVE_LOCATION')}/Users/{dialog.ui.firstNameLineEdit.text()}_" \
		f"{dialog.ui.lastNameLineEdit.text()}"
	shutil.move(user.directory, new_directory)
	return make_user(dialog)


def get_user_path_from_user_name(user_name):
	user_name = f"{user_name}_user.csv"
	for user_path in get_user_file_paths():
		if user_path.endswith(user_name):
			return user_path
