import re
import sys
from utils.common import PAGE
from utils.ssh_handler import SSHClient
from gui.dialog import DialogMessageBox
from gui.main_page_widget import MainWindowWidget
from gui.connection_form import ConnectionFormWidget
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget,  QLineEdit


class MainWindowUI(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindowUI, self).__init__(parent)
        self.setFixedSize(1300, 700)
        self.setWindowTitle("Remote Control Management Interface")
        self.ssh_client = None
        self.stack = QStackedWidget()
        self.form_connection_widget = ConnectionFormWidget(self)
        self.form_connection_widget.btn1.clicked.connect(self.on_connect_button_clicked)
        self.main_window_widget = MainWindowWidget()

        self.setup_onclick_functions_to_buttons()
        self.stack.addWidget(self.form_connection_widget)
        self.stack.addWidget(self.main_window_widget)
        self.stack.setCurrentIndex(PAGE.FORM_PAGE.value)
        self.setCentralWidget(self.stack)

    def _input_is_valid(self):
        return re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', self.form_connection_widget.ipEntry.text()) \
               and len(self.form_connection_widget.userEntry.text()) != 0 \
               and len(self.form_connection_widget.passwordEntry.text()) != 0

    def on_connect_button_clicked(self):
        if self._input_is_valid():
            self.ssh_client = SSHClient(ip=self.form_connection_widget.ipEntry.text(),
                                        username=self.form_connection_widget.userEntry.text(),
                                        password=self.form_connection_widget.passwordEntry.text())
            if self.ssh_client.is_connected():
                self.form_connection_widget.btn1.setText("Disconnect")
                self._clean_form([self.form_connection_widget.ipEntry, self.form_connection_widget.userEntry, self.form_connection_widget.passwordEntry])
                self.main_window_widget.init_tab_views(self.ssh_client)
                self.stack.setCurrentIndex(PAGE.MAIN_PAGE.value)
            else:
                if isinstance(self.ssh_client.connection, str):
                    dialog_message = DialogMessageBox(self.ssh_client.connection)
                    dialog_message.exec()
        else:
            dialog_message = DialogMessageBox("Input isnt valid! please check your input")
            dialog_message.exec()

    def setup_onclick_functions_to_buttons(self):
        self.main_window_widget.disconnect_button.clicked.connect(self.on_disconnect_button_clicked)
        self.main_window_widget.file_system_widget.searchButton.clicked.connect(self.on_search_button_clicked)

    @staticmethod
    def _clean_form(line_edit_list: [QLineEdit]):
        for line_edit in line_edit_list:
            line_edit.clear()

    def on_disconnect_button_clicked(self):
        def _on_disconnect_from_server(self):
            if self.ssh_client:
                self.ssh_client.disconnect()
                self.ssh_client = None
            self.stack.setCurrentIndex(PAGE.FORM_PAGE.value)
        dialog_message = DialogMessageBox("Are you sure you want to disconnect from the server?")
        dialog_message.button_box.accepted.connect(lambda: _on_disconnect_from_server(self))
        dialog_message.exec()

    def on_search_button_clicked(self):
        remote_dir = self.main_window_widget.file_system_widget.searchEntry.text()
        if self.ssh_client.is_path_exists(remote_dir):
            file_stats_list = self.ssh_client.get_files_and_folders_stats_in_remote_dir(remote_dir)
            self.main_window_widget.file_system_widget.insert_file_stats_to_table(file_stats_list)
        else:
            dialog_message = DialogMessageBox("Path is not exists in remote server")
            dialog_message.exec()
            self._clean_form([self.main_window_widget.file_system_widget.searchEntry])


def main():
    app = QApplication(sys.argv)
    win = MainWindowUI()
    win.show()
    sys.exit(app.exec())


