from PyQt6.QtWidgets import QLabel, QFormLayout, QLineEdit, QWidget, QPushButton

class ConnectionFormWidget(QWidget):

    def __init__(self, parent):
        super(ConnectionFormWidget, self).__init__(parent)
        layout = QFormLayout()
        self.ipEntry = QLineEdit()
        self.userEntry = QLineEdit()
        self.passwordEntry = QLineEdit()
        self.passwordEntry.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn1 = QPushButton(self)
        self.btn1.setText("Connect")
        layout.addRow("IP: ", self.ipEntry)
        layout.addRow("Username: ", self.userEntry)
        layout.addRow("Password: ", self.passwordEntry)
        layout.addWidget(self.btn1)
        self.setLayout(layout)



