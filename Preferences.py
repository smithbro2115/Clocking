from PyQt5 import QtWidgets
import qdarkstyle
from Gui.PreferencesDialog import Ui_Dialog as Preference_UI
from LocalFileHandling import add_to_config, read_from_config


class PreferenceDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PreferenceDialog, self).__init__(parent=parent)
        self.ui = Preference_UI()
        self.ui.setupUi(self)
        self.user_location_changed = False
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.ui.browseUserSaveLoationButton.clicked.connect(self.browse_for_folder)
        self.previous_user_save_location = read_from_config('USERS', 'USER_SAVE_LOCATION')
        try:
            self.ui.userSaveLocationLineEdit.setText(self.previous_user_save_location)
        except KeyError:
            pass
        self.ui.userSaveLocationLineEdit.textChanged.connect(self.user_loc_changed)

    def user_loc_changed(self):
        self.user_location_changed = True

    def browse_for_folder(self):
        dialog = GetFolderLocationDialog(self.previous_user_save_location)
        result = dialog.get_folder_path()
        if result:
            self.ui.userSaveLocationLineEdit.setText(result)

    def accept(self):
        if self.user_location_changed:
            add_to_config('USERS', 'USER_SAVE_LOCATION', self.ui.userSaveLocationLineEdit.text())
        super(PreferenceDialog, self).accept()


class GetFolderLocationDialog(QtWidgets.QFileDialog):
    def __init__(self, default_location):
        super(GetFolderLocationDialog, self).__init__()
        self.default_location = default_location

    def get_folder_path(self):
        result = self.getExistingDirectory(caption='Select Users Save Location', directory=self.default_location)
        return result
