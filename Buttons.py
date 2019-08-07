from Gui.AddButtonDialog import Ui_Dialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QRunnable, QThreadPool
from PyQt5 import QtWidgets
from Gui.CustomPyQtDialogsAndWidgets import TimedEmitter
from scapy.all import *
from utils import error_dialog
import qdarkstyle
import time


class AddButtonDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super(AddButtonDialog, self).__init__(parent=parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		self.ui.addPushButton.setEnabled(False)
		self.ui.addPushButton.clicked.connect(self.accept)
		self.ui.cancelPushButton.clicked.connect(self.reject)
		self.timed_emitter = TimedEmitter(1, 4)
		self.address = None
		self.reset_labels()
		self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
		self.thread_pool = QThreadPool()
		self.button_identifier = None
		self.make_button_identifier()
		self.ui.startButton.clicked.connect(self.start)
		self.position = 0
		self.exec_()

	def reset_labels(self):
		labels = [self.ui.oneLabel, self.ui.twoLabel, self.ui.threeLabel, self.ui.goLabel]
		for label in labels:
			self.deactivate_label(label)
		self.ui.startButton.setEnabled(True)
		self.timed_emitter = TimedEmitter(1, 4)
		self.timed_emitter.signals.time_elapsed.connect(self.labels_change)
		self.timed_emitter.signals.finished.connect(self.get_addresses)
		self.position = 0

	def reset(self, msg):
		error_dialog(msg)
		self.make_button_identifier()
		self.reset_labels()
		self.ui.listWidget.clear()

	def make_button_identifier(self):
		self.button_identifier = ButtonIdentifier(self.thread_pool)
		self.button_identifier.signals.run_another_iteration.connect(self.restart)
		self.button_identifier.signals.found_one.connect(self.found_one)
		self.button_identifier.signals.identified_certain.connect(self.identified)
		self.button_identifier.signals.restart.connect(self.reset)
		self.thread_pool.start(self.button_identifier)

	def restart(self):
		self.reset_labels()
		self.start()

	def start(self):
		self.ui.startButton.setEnabled(False)
		self.thread_pool.start(self.timed_emitter)

	def labels_change(self):
		self.position += 1
		if self.position == 1:
			self.activate_label(self.ui.threeLabel)
		elif self.position == 2:
			self.activate_label(self.ui.twoLabel)
		elif self.position == 3:
			self.activate_label(self.ui.oneLabel)
		elif self.position == 4:
			self.activate_label(self.ui.goLabel)

	def get_addresses(self):
		self.button_identifier.should_go = True

	def identified(self, address):
		self.ui.buttonAddressLabel.setText(f"Button Address: {address}")
		self.address = address
		self.ui.addPushButton.setEnabled(True)
		self.ui.startButton.setEnabled(False)
		del self.button_identifier
		self.timed_emitter.canceled = True

	def found_one(self, address):
		self.ui.listWidget.addItem(address)

	def deactivate_label(self, label):
		label.setStyleSheet("QLabel{color: grey;}")

	def activate_label(self, label):
		label.setStyleSheet("QLabel{color: #287399;}")


class ButtonIdentifierSignals(QObject):
	found_one = pyqtSignal(str)
	identified_possible = pyqtSignal(str)
	identified_certain = pyqtSignal(str)
	did_not_find_any_addresses = pyqtSignal()
	restart = pyqtSignal(str)
	run_another_iteration = pyqtSignal()


class ButtonIdentifier(QRunnable):
	def __init__(self, thread_pool):
		super(ButtonIdentifier, self).__init__()
		self.signals = ButtonIdentifierSignals()
		self.go = False
		self.thread_pool = thread_pool
		self.sniffer = SnifferThread(8)
		self.sniffer.signals.found_one.connect(self.found_one)
		self.thread_pool.start(self.sniffer)
		self.possible_addresses = []
		self.times_did_not_find_any = 0
		self.current_iteration = 0
		self.should_go = False
		self.identified = False
		self.error = False

	def __del__(self):
		self.sniffer.stop()

	def get_addresses_for(self, seconds=8):
		self.sniffer.should_go = True
		time.sleep(seconds)
		# del self.sniffer

	def found_one(self, address):
		self.signals.found_one.emit(address)
		self.possible_addresses[self.current_iteration].append(address)
		self.possible_addresses[self.current_iteration] = list(set(self.possible_addresses[self.current_iteration]))

	def try_to_identify(self):
		addresses_that_exist_in_all_iterations = self.get_values_that_exist_in_all_lists(self.possible_addresses)
		if addresses_that_exist_in_all_iterations:
			length = len(addresses_that_exist_in_all_iterations)
			if length == 1:
				if self.current_iteration > 1:
					self.signals.identified_certain.emit(addresses_that_exist_in_all_iterations[0])
					return True
				else:
					self.signals.identified_possible.emit(addresses_that_exist_in_all_iterations[0])
			elif length == 0:
				self.signals.restart.emit('There was a problem, please try again.')
				self.error = True
		else:
			self.signals.restart.emit('There was a problem, please try again.')
			self.error = True

	@staticmethod
	def get_values_that_exist_in_all_lists(list_of_lists):
		new_list = []
		for index, list_ in enumerate(list_of_lists):
			if index == 0:
				new_list = list_
			else:
				new_list = set(new_list) & set(list_)
		if len(new_list) > 0:
			return list(new_list)

	def did_not_find_any_addresses(self):
		self.times_did_not_find_any += 1
		if self.times_did_not_find_any > 2:
			self.signals.restart.emit('Did not find any possibilities, please try again')
		else:
			self.signals.did_not_find_any_addresses.emit()

	def get_addresses(self):
		self.possible_addresses.append([])
		self.get_addresses_for()
		if self.try_to_identify():
			self.should_go = False
			self.identified = True
			return None
		if self.error:
			self.should_go = False
			return None
		if len(self.possible_addresses[self.current_iteration]) == 0:
			self.did_not_find_any_addresses()
		else:
			self.current_iteration += 1
			self.signals.run_another_iteration.emit()
		self.should_go = False

	@pyqtSlot()
	def run(self):
		while True:
			if self.should_go:
				self.get_addresses()
			if self.identified:
				break

			time.sleep(.1)


class SnifferSignals(QObject):
	found_one = pyqtSignal(str)


class SnifferThread(QRunnable):
	def __init__(self, timeout):
		super(SnifferThread, self).__init__()
		self.signals = SnifferSignals()
		self.timeout = timeout
		self.should_go = False
		self._stop = False

	def stop(self):
		self._stop = True

	@pyqtSlot()
	def run(self):
		while not self._stop:
			while self.should_go:
				sniff(prn=self.found_one_callback, filter="arp", store=0, timeout=self.timeout)
				self.should_go = False
			time.sleep(.1)

	def found_one_callback(self, pkt):
		address = arp_monitor_callback(pkt)
		if address:
			self.signals.found_one.emit(address)


def arp_monitor_callback(pkt):
	if ARP in pkt and pkt[ARP].op in (1, 2):
		return pkt[ARP].hwsrc


def sniff_for_arps(call_back):
	sniff(prn=call_back, filter="arp", store=0)
