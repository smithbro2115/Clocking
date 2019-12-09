from PyQt5 import QtWidgets
import qdarkstyle
from Gui.PreferencesDialog import Ui_Dialog as Preference_UI
from LocalFileHandling import add_to_config, read_from_config
from configparser import NoOptionError, NoSectionError
from platform import system


class PreferenceDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PreferenceDialog, self).__init__(parent=parent)
        self.ui = Preference_UI()
        self.ui.setupUi(self)
        self.user_location_changed = False
        self.reset_clocks_after_export_changed = False
        self.dash_buttons_activated_changed = False
        self.email_invoices_changed = False
        self.email_invoices_activated = False
        self.dash_buttons_activated = None
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.ui.browseUserSaveLoationButton.clicked.connect(self.browse_for_folder)
        self.ui.emailInvoicesCheckBox.clicked.connect(self.email_invoices_clicked)
        self.previous_user_save_location = read_from_config('USERS', 'USER_SAVE_LOCATION')
        try:
            self.reset_clocks_after_export = bool(int(read_from_config('EXPORTING', 'reset_clocks_after_export')))
            self.ui.resetClocksAfterExportingInvoicesCheckBox.setChecked(self.reset_clocks_after_export)
        except (NoSectionError, NoOptionError):
            self.reset_clocks_after_export = None
        try:
            self.ui.userSaveLocationLineEdit.setText(self.previous_user_save_location)
        except KeyError:
            pass
        self.ui.userSaveLocationLineEdit.textChanged.connect(self.user_loc_changed)
        self.ui.resetClocksAfterExportingInvoicesCheckBox.clicked.connect(self.reset_clocks_export_changed)
        self.ui.amazonButtonsCheckBox.clicked.connect(self.dash_buttons_activated_changed_clicked)
        if system() == 'Darwin':
            self.ui.amazonButtonsCheckBox.setHidden(True)
        else:
            self.setup_dash_button_prefs()
        self.setup_email_invoices_prefs()

    def setup_dash_button_prefs(self):
        try:
            self.dash_buttons_activated = bool(int(read_from_config('BUTTONS', 'activated')))
            self.ui.amazonButtonsCheckBox.setChecked(self.dash_buttons_activated)
        except (NoSectionError, NoOptionError):
            self.dash_buttons_activated = None

    def setup_email_invoices_prefs(self):
        try:
            self.email_invoices_activated = bool(int(read_from_config('EMAIL', 'activated')))
            self.ui.emailInvoicesCheckBox.setChecked(self.email_invoices_activated)
        except (NoSectionError, NoOptionError):
            self.email_invoices_activated = None

    def user_loc_changed(self):
        self.user_location_changed = True

    def reset_clocks_export_changed(self):
        self.reset_clocks_after_export_changed = True

    def dash_buttons_activated_changed_clicked(self):
        self.dash_buttons_activated = self.ui.amazonButtonsCheckBox.isChecked()
        self.dash_buttons_activated_changed = True

    def email_invoices_clicked(self):
        self.email_invoices_activated = self.ui.emailInvoicesCheckBox.isChecked()
        self.email_invoices_changed = True

    def browse_for_folder(self):
        dialog = GetFolderLocationDialog(self.previous_user_save_location)
        result = dialog.get_folder_path()
        if result:
            self.ui.userSaveLocationLineEdit.setText(result)

    def accept(self):
        if self.user_location_changed:
            add_to_config('USERS', 'USER_SAVE_LOCATION', self.ui.userSaveLocationLineEdit.text())
        if self.reset_clocks_after_export_changed:
            add_to_config('EXPORTING', 'reset_clocks_after_export',
                          int(self.ui.resetClocksAfterExportingInvoicesCheckBox.isChecked()))
        if self.dash_buttons_activated_changed:
            add_to_config('BUTTONS', 'activated', int(self.ui.amazonButtonsCheckBox.isChecked()))
        if self.email_invoices_changed:
            add_to_config('EMAIL', 'activated', int(self.ui.emailInvoicesCheckBox.isChecked()))
        super(PreferenceDialog, self).accept()


class GetFolderLocationDialog(QtWidgets.QFileDialog):
    def __init__(self, default_location):
        super(GetFolderLocationDialog, self).__init__()
        self.default_location = default_location

    def get_folder_path(self):
        result = self.getExistingDirectory(caption='Select Users Save Location', directory=self.default_location)
        return result
