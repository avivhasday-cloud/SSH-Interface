from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout


class SystemStatsWidget(QFrame):

    def __init__(self, name: str,  system_stats: dict):
        super(SystemStatsWidget, self).__init__()
        self.name_label = QLabel(name)
        self.setStyleSheet('border:1px solid black')
        self.stats_labels = [QLabel(f"{key}: {value}") for key, value in system_stats.items()]
        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(self.name_label)
        for stat_label in self.stats_labels:
            vbox_layout.addWidget(stat_label)
        self.setLayout(vbox_layout)
