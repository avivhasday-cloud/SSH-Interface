from PyQt6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidgetItem


class FileSystemWidget(QWidget):

    def __init__(self):
        super(FileSystemWidget, self).__init__()
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(['File Name', 'File Path', 'Type', 'Permissions', 'Size', 'Last modified'])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 600)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(5, 150)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Enter path here...")
        self.search_button = QPushButton("Search")
        hbox.addWidget(self.search_entry)
        hbox.addWidget(self.search_button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def insert_file_stats_to_table(self, list_of_file_stats: [dict]):
        self.table.setRowCount(len(list_of_file_stats))
        for index, file_stats in enumerate(list_of_file_stats):
            col_index = 0
            for key, value in file_stats.items():
                self.table.setItem(index, col_index , QTableWidgetItem(str(value)))
                col_index += 1

