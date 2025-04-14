from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QPushButton, QMessageBox, QApplication, QLabel, QSpacerItem, QSizePolicy, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import mysql.connector

import gui.qt_config as qt_config

class ManageInventory(QWidget):
    """
    ManageInventory class to handle the management of player inventories.
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
        self.getInfoPlyers()
        self.getInventory()
        self.setup()

    def __del__(self):
        self.cursor.close()
        self.db.close()
    
    def getInfoPlyers(self):
        self.cursor.execute("SELECT * FROM Players WHERE ID = %s", (self.ID,))
        result = self.cursor.fetchone()
        self.name = result[1]
        self.level = result[2]
        self.xp = result[3]
        self.money = result[4]
        self.inventorySlot = result[5]

    def getInventory(self):
      # self.cursor.execute("SELECT * FROM Players")  # Remplace par le nom de ta table
      # rows = self.cursor.fetchall()
      # column_names = [desc[0] for desc in self.cursor.description]
      self.inventory_table = QTableWidget()
      # self.inventory_table.setRowCount(len(rows))
      # self.inventory_table.setColumnCount(len(column_names))
      # self.inventory_table.setHorizontalHeaderLabels(column_names)
      # for i, row in enumerate(rows):
      #     for j, value in enumerate(row):
      #         self.inventory_table.setItem(i, j, QTableWidgetItem(str(value)))

    def setup(self):
        backButton = QPushButton("Back")
        backButton.setFixedWidth(500)

        addItemButton = QPushButton("Add item")
        addItemButton.setEnabled(False)
        addItemButton.setFixedWidth(500)

        clearButton = QPushButton("Clear Inventory")
        clearButton.setFixedWidth(500)

        self.nameLabel = QLabel(f"Hello <u>{self.name}</u>, with a level of {self.level}, you get {self.inventorySlot} slots")
    
        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Manage Inventory"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.nameLabel, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Here is your inventory:"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inventory_table, alignment=Qt.AlignCenter)
        mainLayout.addWidget(addItemButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(clearButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)

        # connect the buttons
        backButton.clicked.connect(self.on_backButton_clicked)
        clearButton.clicked.connect(self.clearInventory)

        self.show()

    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0) # Go back to the main menu

    def clearInventory(self):
        raise Exception("not yet implemented")
