from PyQt5 import QtGui, QtWidgets, QtCore
from Gui import MainWindow
import qdarkstyle
import Categories
from Clock import Clock


class Gui(MainWindow.Ui_MainWindow):
    def __init__(self):
        self.categories = []
        self.current_clock = None

    def setup_additional(self, main_window):
        main_window.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.clockTableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        headers = ['Clocked In:', 'Clocked Out:', 'Total Time Worked:', 'Monthly Total Time:']
        self.clockTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.clockTableWidget.verticalHeader().setVisible(False)
        self.clockTableWidget.setColumnCount(4)
        self.clockTableWidget.setHorizontalHeaderLabels(headers)
        self.clockButton.clicked.connect(self.clock_button_clicked)
        self.addCategoryButton.clicked.connect(self.add_category)
        self.load_categories()

    def add_category(self):
        category = Categories.add_category(self.clockTableWidget, self.clockButton)
        self.categories.append(category)

    def load_categories(self):
        Categories.load_categories(self.categoryBox)

    def clock_button_clicked(self):
        pass


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Gui()
    mainWindow = QtWidgets.QMainWindow()
    ui.setupUi(mainWindow)
    ui.setup_additional(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
