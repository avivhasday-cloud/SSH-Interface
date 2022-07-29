from utils.ssh_handler import SSHClient
from gui.file_system import FileSystemWidget
from gui.system_stats import SystemStatsWidget
from gui.shell_intereaction_widget import ShellInteractionWidget
from PyQt6.QtWidgets import QTabWidget, QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout


class MainWindowWidget(QWidget):

    def __init__(self):
        super(MainWindowWidget, self).__init__()
        vbox_main_layout = QVBoxLayout()
        vbox_sub_layout = QVBoxLayout()
        hbox_layout = QHBoxLayout()
        self.disconnect_button = QPushButton("Disconnect")
        self.shutdown_button = QPushButton("Shutdown")
        self.file_system_widget = FileSystemWidget()
        self.system_monitor = QWidget()
        self.shell_interaction_widget = ShellInteractionWidget()


        vbox_sub_layout.addWidget(self.disconnect_button)
        vbox_sub_layout.addWidget(self.shutdown_button)

        self.tab_widget = QTabWidget()
        label3 = QLabel("SSH Remote Client program")
        hbox_layout.addLayout(vbox_sub_layout)
        hbox_layout.addWidget(label3)
        vbox_main_layout.addLayout(hbox_layout)
        vbox_main_layout.addWidget(self.tab_widget)
        self.setLayout(vbox_main_layout)

    def init_tab_views(self, ssh_client: SSHClient):
        vbox_layout = QVBoxLayout()
        if ssh_client:
            disk_stats_list, ram_stats = ssh_client.get_system_stats(['/'])
            ram_stats_widget = SystemStatsWidget("RAM", ram_stats)
            disk_stats_widget_list = [SystemStatsWidget("DISK", disk_stats) for disk_stats in disk_stats_list]
            vbox_layout.addWidget(ram_stats_widget)
            for disk_stats_widget in disk_stats_widget_list:
                vbox_layout.addWidget(disk_stats_widget)
            self.system_monitor.setLayout(vbox_layout)
        self.tab_widget.addTab(self.file_system_widget, "Browser")
        self.tab_widget.addTab(self.system_monitor, "Monitor")
        self.tab_widget.addTab(self.shell_interaction_widget, "Shell")