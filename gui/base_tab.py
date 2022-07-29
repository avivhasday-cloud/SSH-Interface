from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QTableWidget


class BaseTab(QWidget):

    def __init__(self, parent = None, search_button_text: str = "Search", clear_button_text: str = "Clear", input_placeholder_text: str = ""):
        super(BaseTab, self).__init__(parent)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.sub_vbox = QVBoxLayout()
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText(input_placeholder_text)
        self.search_button = QPushButton(search_button_text)
        self.clear_button = QPushButton(clear_button_text)
        self.sub_vbox.addWidget(self.search_button)
        self.sub_vbox.addWidget(self.clear_button)
        self.hbox.addWidget(self.search_entry)
        self.hbox.addLayout(self.sub_vbox)
        self.vbox.addLayout(self.hbox)

    def on_clear_button_clicked(self, widgets_to_clear):
        child_widgets = self.findChildren(widgets_to_clear)
        for item in child_widgets:
            if isinstance(item, QTableWidget):
                item.clearContents()
            else:
                item.clear()
