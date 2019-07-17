from Gui.AddButtonDialog import Ui_Dialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QRunnable, QThreadPool
from PyQt5 import QtWidgets, QtCore
from scapy.all import *
import qdarkstyle
import time


class AddButtonDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super(AddButtonDialog, self).__init__(parent=parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		self.timed_emitter = TimedEmitter(1, 4)
		self.reset_labels()
		self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
		# self.ui.buttonBox.setEnabled(False)
		self.thread_pool = QThreadPool()
		self.button_identifier = ButtonIdentifier(self.thread_pool)
		self.button_identifier.signals.run_another_iteration.connect(self.restart)
		self.button_identifier.signals.found_one.connect(self.found_one)
		self.button_identifier.signals.identified_certain.connect(self.identified)
		self.thread_pool.start(self.button_identifier)
		self.ui.startButton.clicked.connect(self.start)
		self.position = 0
		self.exec()

	def reset_labels(self):
		labels = [self.ui.oneLabel, self.ui.twoLabel, self.ui.threeLabel, self.ui.goLabel]
		for label in labels:
			self.deactivate_label(label)
		self.ui.startButton.setEnabled(True)
		self.timed_emitter = TimedEmitter(1, 4)
		self.timed_emitter.signals.time_elapsed.connect(self.labels_change)
		self.timed_emitter.signals.finished.connect(self.get_addresses)
		self.position = 0

	def restart(self):
		print('\nrestarted')
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
		print(f"Identified {address} as the button")

	def found_one(self, address):
		self.ui.listWidget.addItem(address)

	def deactivate_label(self, label):
		label.setStyleSheet("QLabel{color: grey;}")

	def activate_label(self, label):
		label.setStyleSheet("QLabel{color: #287399;}")


class TimedEmitterSignals(QObject):
	time_elapsed = pyqtSignal()
	finished = pyqtSignal()


class TimedEmitter(QRunnable):
	def __init__(self, time_between_emits, times_to_emit):
		super(TimedEmitter, self).__init__()
		self.signals = TimedEmitterSignals()
		self.time_between = time_between_emits
		self.times_to_emit = times_to_emit
		self.times_emitted = 0

	@pyqtSlot()
	def run(self):
		while self.times_emitted < self.times_to_emit:
			time.sleep(self.time_between)
			self.signals.time_elapsed.emit()
			self.times_emitted += 1
		self.signals.finished.emit()


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
		self.sniffer = SnifferThread()
		self.sniffer.signals.found_one.connect(self.found_one)
		self.possible_addresses = []
		self.times_did_not_find_any = 0
		self.current_iteration = 0
		self.should_go = False
		self.identified = False
		self.thread_pool = thread_pool

	def get_addresses_for(self, seconds=6):
		self.thread_pool.start(self.sniffer)
		time.sleep(seconds)
		print('got addresses')

	def found_one(self, address):
		self.signals.found_one.emit(address)
		self.possible_addresses[self.current_iteration].append(address)

	def try_to_identify(self):
		addresses_that_exist_in_all_iterations = self.get_values_that_exist_in_all_lists(self.possible_addresses)
		print('test', addresses_that_exist_in_all_iterations, self.possible_addresses)
		if addresses_that_exist_in_all_iterations:
			length = len(addresses_that_exist_in_all_iterations)
			if length == 1:
				print(self.current_iteration)
				if self.current_iteration > 1:
					self.signals.identified_certain.emit(addresses_that_exist_in_all_iterations[0])
					return True
				else:
					self.signals.identified_possible.emit(addresses_that_exist_in_all_iterations[0])
			elif length == 0:
				self.signals.restart.emit('There was a problem, please try again.')

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

	@pyqtSlot()
	def run(self):
		while True:
			while self.should_go:
				self.possible_addresses.append([])
				self.get_addresses_for()
				if self.try_to_identify():
					self.should_go = False
					self.identified = True
					break
				if len(self.possible_addresses[self.current_iteration]) == 0:
					print('did not find any')
					self.times_did_not_find_any += 1
					if self.times_did_not_find_any > 2:
						self.signals.restart.emit('Did not find any possibilities, please try again')
					else:
						self.signals.did_not_find_any_addresses.emit()
				else:
					self.current_iteration += 1
					self.signals.run_another_iteration.emit()
				print('ran')
			if self.identified:
				break
			time.sleep(.1)


class SnifferSignals(QObject):
	found_one = pyqtSignal(str)


class SnifferThread(QRunnable):
	def __init__(self):
		super(SnifferThread, self).__init__()
		self.signals = SnifferSignals()

	@pyqtSlot()
	def run(self):
		self.signals.found_one.emit(sniff(prn=self.found_one_callback, filter="arp", store=0))

	def found_one_callback(self, pkt):
		address = arp_monitor_callback(pkt)
		if address:
			self.signals.found_one.emit(address)


def arp_monitor_callback(pkt):
	if ARP in pkt and pkt[ARP].op in (1, 2):
		print(pkt[ARP].hwsrc)
		return pkt[ARP].hwsrc
