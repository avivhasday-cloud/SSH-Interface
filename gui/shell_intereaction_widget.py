from gui.base_tab import BaseTab
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit


class ShellInteractionWidget(BaseTab):

    def __init__(self, parent = None):
        super(ShellInteractionWidget, self).__init__(parent, "Run", "Clear", "Enter your command here....")
        self.shell_text_output_box = QTextEdit()
        self.shell_text_output_box.setReadOnly(True)
        self.vbox.addWidget(self.shell_text_output_box)
        self.clear_button.clicked.connect(lambda: self.on_clear_button_clicked((QTextEdit, QLineEdit)))
        self.setLayout(self.vbox)