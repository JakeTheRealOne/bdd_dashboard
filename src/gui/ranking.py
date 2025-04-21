from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QAbstractItemView, QHeaderView, QScrollArea, QAbstractScrollArea, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import mysql.connector

from . import qt_config

class Ranking(QWidget):
    """
    ManageAccount class to handle the management of player accounts.
    """

    def __init__(self, parent, stackedWidget, ID):
        super().__init__(parent)
        self.stacked_widget = stackedWidget
        self.stacked_widget.addWidget(self)
        self.ID = ID
        self.db = mysql.connector.connect(
            host="localhost",
            user="rootuser",
            password="rootuser",
            database="rpg"
        )
        self.cursor = self.db.cursor()
        self.setup()
        
        
    def setup(self):
        back_button = QPushButton("Back")
        back_button.setFixedWidth(500)
        back_button.setAutoDefault(True)
        
        self.ranking_table = QTableWidget()
        self.ranking_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ranking_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ranking_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)


        scroll_area = QScrollArea()
        scroll_area.setWidget(self.ranking_table)
        scroll_area.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(qt_config.create_center_bold_title("Ranking (ordered by level, then by XP)"), alignment=Qt.AlignCenter)
        main_layout.addWidget(scroll_area, alignment=Qt.AlignCenter)
        main_layout.addWidget(back_button, alignment=Qt.AlignCenter)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.setLayout(main_layout)
        
        back_button.clicked.connect(self.on_back_button_clicked)
        
        self.display_ranking()
        
        
    def on_back_button_clicked(self):
        self.stacked_widget.setCurrentIndex(0)
        
        
    def display_ranking(self):
        self.cursor.execute("SELECT p.Name, p.Level, p.XP, p.Money, p.InventorySlot FROM Players p ORDER BY p.Level DESC, p.XP DESC;")
        result = self.cursor.fetchall()

        self.ranking_table.setRowCount(len(result))
        self.ranking_table.setColumnCount(5)
        self.ranking_table.setHorizontalHeaderLabels(["Name", "Level", "XP", "Money", "Inventory Slot"])

        for i, row in enumerate(result):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                self.ranking_table.setItem(i, j, item)
                
        header = self.ranking_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
