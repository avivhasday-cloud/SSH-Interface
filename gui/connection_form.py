from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QLabel, QFormLayout, QLineEdit, QWidget, QPushButton

class ConnectionFormWidget(QWidget):

    def __init__(self, parent):
        super(ConnectionFormWidget, self).__init__(parent)
        layout = QFormLayout()
        self.ip_entry = QLineEdit()
        self.user_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn1 = QPushButton(self)
        self.btn1.setText("Connect")
        layout.addRow("IP: ", self.ip_entry)
        layout.addRow("Username: ", self.user_entry)
        layout.addRow("Password: ", self.password_entry)
        layout.addWidget(self.btn1)
        self.setLayout(layout)



