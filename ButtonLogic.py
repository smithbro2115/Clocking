from LocalFileHandling import get_app_data_folder, add_file_if_it_does_not_exist, read_dict_from_csv_file, \
	convert_string_tuple_into_tuple_dict
from Categories import Category, load_categories
from Users import load_user, get_user_path_from_user_name
from Buttons import sniff_for_arps, arp_monitor_callback
import time
from plyer import notification
from main import format_duration_from_seconds, format_time
from utils import resource_path


class ButtonListener:
	def __init__(self):
		self.time_since_last_clocked = 0
		sniff_for_arps(self.found_arp)

	@property
	def file_path(self):
		return f"{get_app_data_folder('Buttons')}/Buttons.csv"

	def found_arp(self, pkt):
		try:
			if time.time() - self.time_since_last_clocked > 2:
				address = arp_monitor_callback(pkt)
				category = self.get_assigned_category(address)
				clock_time = category.clock.clock()
				self.time_since_last_clocked = time.time()
				self.send_notification(category.clock.state, clock_time)
		except AttributeError:
			pass

	def get_assigned_category(self, address) -> Category:
		button_assignments = self.get_button_assignments()
		print(button_assignments)
		try:
			user_name, category_name = button_assignments[address]
			user = load_user(get_user_path_from_user_name(user_name))[0]
			category = find_category_from_key_value(load_categories(user), 'name', category_name)
			return category
		except KeyError:
			pass

	def send_notification(self, clocked_in, clock_time):
		if clocked_in:
			self.notify('Clocked In!', f'Clocked in at: {format_time(clock_time)}')
		else:
			self.notify('Clocked Out!', f'Clocked out at: {format_time(clock_time[0])}, for a total work time of: '
						f'{format_duration_from_seconds(clock_time[1].total_seconds())}')

	def notify(self, title, message):
		manual_icon = "C:/Users/Josh/PycharmProjects/Clocking/clock_icon.ico"
		auto = resource_path('clock_icon.ico').replace('\\', '/')
		notification.notify(title=title, message=message, timeout=10, app_name="Clocking", app_icon=auto)

	def get_button_assignments(self) -> dict:
		add_file_if_it_does_not_exist(self.file_path)
		return convert_string_tuple_into_tuple_dict(read_dict_from_csv_file(self.file_path))


def find_category_from_key_value(categories, key, value):
	for category in categories:
		try:
			if category.__dict__[key] == value:
				return category
		except KeyError:
			continue


button_listener = ButtonListener()
