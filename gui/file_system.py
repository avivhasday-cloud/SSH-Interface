from gui.base_tab import BaseTab
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit


class FileSystemWidget(BaseTab):

    def __init__(self):
        super(FileSystemWidget, self).__init__(input_placeholder_text="Enter your path here...")
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(['File Name', 'File Path', 'Type', 'Permissions', 'Size', 'Last modified'])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 600)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(5, 150)
        self.vbox.addWidget(self.table)
        self.clear_button.clicked.connect(lambda : self.on_clear_button_clicked((QTableWidget, QLineEdit)))
        self.setLayout(self.vbox)

    def insert_file_stats_to_table(self, list_of_file_stats: [dict]):
        self.table.setRowCount(len(list_of_file_stats))
        for index, file_stats in enumerate(list_of_file_stats):
            col_index = 0
            for key, value in file_stats.items():
                self.table.setItem(index, col_index , QTableWidgetItem(str(value)))
                col_index += 1

