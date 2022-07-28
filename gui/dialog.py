from typing import Callable
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class DialogMessageBox(QDialog):

    def __init__(self, message):
        super().__init__()

        self.setWindowTitle("Message Alert")
        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.button_box = QDialogButtonBox(QBtn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        vbox_layout = QVBoxLayout()
        message_label = QLabel(message)
        vbox_layout.addWidget(message_label)
        vbox_layout.addWidget(self.button_box)
        self.setLayout(vbox_layout)

    def on_accept(self, function: Callable):
        return function()


