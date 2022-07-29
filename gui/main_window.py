import re
import sys
from datetime import datetime
from utils.common import PAGE, STAGE
from utils.ssh_handler import SSHClient
from gui.dialog import DialogMessageBox
from gui.transfer_form import TransferFormWidget
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

    def _input_is_valid(self, widget) -> bool:
        is_valid = False
        if isinstance(widget, ConnectionFormWidget):
            is_valid = widget.validate_input()
        elif isinstance(widget, TransferFormWidget):
            is_valid = widget.validate_input(self.ssh_client)
        return is_valid

    def on_connect_button_clicked(self):
        if self._input_is_valid(self.form_connection_widget):
            self.ssh_client = SSHClient(ip=self.form_connection_widget.ip_entry.text(),
                                        username=self.form_connection_widget.user_entry.text(),
                                        password=self.form_connection_widget.password_entry.text())
            if self.ssh_client.is_connected():
                self.form_connection_widget.btn1.setText("Disconnect")
                self._clean_form([self.form_connection_widget.ip_entry, self.form_connection_widget.user_entry, self.form_connection_widget.password_entry])
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
        self.main_window_widget.file_system_widget.execute_button.clicked.connect(self.on_search_button_clicked)
        self.main_window_widget.shell_interaction_widget.execute_button.clicked.connect(self.on_run_command_button_clicked)
        self.main_window_widget.transfer_form_widget.transfer_button.clicked.connect(self.on_begin_transfer_button_clicked)

    @staticmethod
    def _clean_form(line_edit_list: [QLineEdit]):
        for line_edit in line_edit_list:
            line_edit.clear()

    def on_run_command_button_clicked(self):
        if self.ssh_client.is_connected:
            command = self.main_window_widget.shell_interaction_widget.input_entry.text()
            stdout_lines, stderr_lines = self.ssh_client.run_command(command)
            datetime_str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            if len(stdout_lines) > 0:
                text = "\n".join(stdout_lines)
                output = f"{datetime_str} Output:\n {text}"
                self.main_window_widget.shell_interaction_widget.shell_text_output_box.append(output)
            elif len(stderr_lines) > 0:
                text = "\n".join(stderr_lines)
                output = f"{datetime_str} Error:\n {text}"
                self.main_window_widget.shell_interaction_widget.shell_text_output_box.append(output)

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
        remote_dir = self.main_window_widget.file_system_widget.input_entry.text()
        if self.ssh_client.is_path_exists(remote_dir):
            file_stats_list = self.ssh_client.get_files_and_folders_stats_in_remote_dir(remote_dir)
            self.main_window_widget.file_system_widget.insert_file_stats_to_table(file_stats_list)
        else:
            dialog_message = DialogMessageBox("Path is not exists in remote server")
            dialog_message.exec()
            self._clean_form([self.main_window_widget.file_system_widget.input_entry])

    def on_begin_transfer_button_clicked(self):
        if self._input_is_valid(self.main_window_widget.transfer_form_widget):
            is_recursive = self.main_window_widget.transfer_form_widget.is_item_checked(self.main_window_widget.transfer_form_widget.recursive_checkbox)
            remote_to_local_host = self.main_window_widget.transfer_form_widget.is_item_checked(self.main_window_widget.transfer_form_widget.rth_checkbox)
            local_path = self.main_window_widget.transfer_form_widget.local_path_entry.text()
            remote_path = self.main_window_widget.transfer_form_widget.remote_path_entry.text()
            if self.ssh_client.is_connected():
                self.main_window_widget.transfer_form_widget.set_stage_status(STAGE.ONGOING_TRANSFER.name)
                self.ssh_client.transfer_files(local_path=local_path, remote_path=remote_path, host_to_local=remote_to_local_host, recursive=is_recursive)
                self.main_window_widget.transfer_form_widget.set_stage_status(STAGE.DONE.name)
        else:
            dialog_message = DialogMessageBox("Input isnt valid, please check that the given paths exists!")
            dialog_message.exec()


def main():
    app = QApplication(sys.argv)
    win = MainWindowUI()
    win.show()
    sys.exit(app.exec())


