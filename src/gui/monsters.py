from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QAbstractItemView, QHeaderView, QScrollArea, QAbstractScrollArea, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector

import gui.qt_config as qt_config

class Monsters(QWidget):
    """
    ManageAccount class to handle the management of player accounts.
    """

    def __init__(self, parent, stackedWidget, ID):
        super().__init__(parent)
        self.stackedWidget = stackedWidget
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
        
        self.monsters_table = QTableWidget()
        self.monsters_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.monsters_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.monsters_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)


        scroll_area = QScrollArea()
        scroll_area.setWidget(self.monsters_table)
        scroll_area.setWidgetResizable(True)  # Allow the table to resize

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Manage your Quests"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(scroll_area, alignment=Qt.AlignCenter)
        mainLayout.addWidget(back_button, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.setLayout(mainLayout)
        
        back_button.clicked.connect(self.on_backButton_clicked)
        
        self.display_all_monsters()
        
        
    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0)
        
        
    def display_all_monsters(self):
        self.cursor.execute("SELECT * FROM Monsters")
        monsters = self.cursor.fetchall()

        self.monsters_table.setRowCount(len(monsters))
        self.monsters_table.setColumnCount(4)
        self.monsters_table.setHorizontalHeaderLabels(["Name", "Damage", "Health", "Defence"])

        for i, monster in enumerate(monsters):
            for j, value in enumerate(monster):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                self.monsters_table.setItem(i, j, item)
                
        header = self.monsters_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) 
    