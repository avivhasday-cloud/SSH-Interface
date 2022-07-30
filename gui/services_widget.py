from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QFrame


class ServicesWidget(QWidget):

    def __init__(self):
        super(ServicesWidget, self).__init__()
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

    def init_service_widgets(self, services_dict: [dict]) ->  [QVBoxLayout]:
        services_layout_list = list()
        for service_dict in services_dict:
            vbox_layout = QVBoxLayout()
            frame = QFrame()
            frame.setFixedWidth(400)
            for key, value in service_dict.items():
                font = QtGui.QFont("Times", 20)
                font.setBold(True)
                label = QLabel(f"{value}")
                if key == 'status':
                    color = "color: green;" if value == 'running' else "color: red;"
                    label.setStyleSheet(color)
                vbox_layout.addWidget(label)
                frame.setLayout(vbox_layout)
                frame.setStyleSheet('border: 1px solid black;')
            services_layout_list.append(frame)
        for idx, frame in enumerate(services_layout_list):
            self.grid_layout.addWidget(frame)


