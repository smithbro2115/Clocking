from PyQt5 import QtWidgets
from Gui.PreferencesDialog import Ui_Dialog as Preference_UI
from LocalFileHandling import add_to_config, read_from_config


class PreferenceDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PreferenceDialog, self).__init__(parent=parent)
        self.ui = Preference_UI()
        self.ui.setupUi(self)
        self.user_location_changed = False
        try:
            self.ui.userSaveLocationLineEdit.setText(read_from_config('USER_SAVE_LOCATION'))
        except KeyError:
            pass
        self.ui.userSaveLocationLineEdit.textChanged.connect(self.user_loc_changed)

    def user_loc_changed(self):
        self.user_location_changed = True

    def accept(self):
        if self.user_location_changed:
            add_to_config('USER_SAVE_LOCATION', self.ui.userSaveLocationLineEdit.text())
        super(PreferenceDialog, self).accept()
