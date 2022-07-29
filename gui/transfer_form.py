import os.path
from PyQt6 import QtGui
from utils.common import STAGE
from utils.ssh_handler import SSHClient
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QCheckBox, QLabel, QHBoxLayout


class TransferFormWidget(QWidget):

    def __init__(self):
        super(TransferFormWidget, self).__init__()
        self.vbox_layout = QVBoxLayout()
        self.hbox_layout = QHBoxLayout()
        self.setFixedWidth(800)

        self.local_path_entry = QLineEdit()
        self.local_path_entry.setFixedHeight(30)
        self.local_path_entry.setPlaceholderText("Enter local path here...")

        self.remote_path_entry = QLineEdit()
        self.remote_path_entry.setFixedHeight(30)
        self.remote_path_entry.setPlaceholderText("Enter remote path here...")

        self.recursive_checkbox = QCheckBox("Recursive")
        self.rth_checkbox = QCheckBox("Remote to local host")

        self.transfer_button = QPushButton("Begin Transfer")
        self.stage = QLabel(f"Stage: {STAGE.IDLE.name}")
        self.stage_font = QtGui.QFont("sans serif", 20)
        self.stage_font.setBold(True)
        self.stage.setFont(self.stage_font)

        self.vbox_layout.addWidget(self.local_path_entry)
        self.vbox_layout.addWidget(self.remote_path_entry)
        self.vbox_layout.addWidget(self.recursive_checkbox)
        self.vbox_layout.addWidget(self.rth_checkbox)
        self.vbox_layout.addWidget(self.transfer_button)

        self.hbox_layout.addLayout(self.vbox_layout)
        self.hbox_layout.addWidget(self.stage)
        self.setLayout(self.hbox_layout)

    def set_stage_status(self, stage: str):
        self.stage.setText(f"Stage: {stage}")

    @staticmethod
    def is_item_checked(item: QCheckBox):
        return item.isChecked()

    def validate_input(self, ssh_client: SSHClient):
        local_path = self.local_path_entry.text()
        remote_path = self.remote_path_entry.text()
        is_remote_path_exists = ssh_client.is_path_exists(remote_path) if ssh_client.is_connected() else False
        return os.path.exists(local_path) and is_remote_path_exists