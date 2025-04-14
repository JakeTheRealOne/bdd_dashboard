from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QPushButton, QMessageBox, QApplication, QLabel, QSpacerItem, QSizePolicy, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent
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
        self.db.start_transaction(isolation_level='READ COMMITTED')
        self.cursor = self.db.cursor()
        self.getInfoPlyers()
        self.setup()
        self.getInventory()

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
      self.inventory = [None] * self.inventorySlot
      self.cursor.execute("SELECT * FROM PlayerInventories")
      rows = self.cursor.fetchall()
      self.inventory_table.setRowCount(self.inventorySlot)
      self.inventory_table.setColumnCount(1)
      self.inventory_table.setHorizontalHeaderLabels(["Object Name"])
      i = 0
      for row in rows:
        if row[0] == self.ID:
          self.inventory[row[2]] = row[1]
          self.inventory_table.setItem(row[2], 0, QTableWidgetItem(row[1]))
          i += 1
      self.addItemButton.setEnabled(i != self.inventorySlot)


    def setup(self):
        backButton = QPushButton("Back")
        backButton.setFixedWidth(500)

        self.addItemButton = QPushButton("Add item")
        self.addItemButton.setEnabled(False)
        self.addItemButton.setFixedWidth(500)

        clearButton = QPushButton("Clear Inventory")
        clearButton.setFixedWidth(500)

        self.nameLabel = QLabel(f"Hello <u>{self.name}</u>, with a level of {self.level}, you get {self.inventorySlot} slots")
        self.inventory_table = QTableWidget()    

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Manage Inventory"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.nameLabel, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Here is your inventory:"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inventory_table, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.addItemButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(clearButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)

        # connect the buttons
        backButton.clicked.connect(self.on_backButton_clicked)
        self.addItemButton.clicked.connect(self.on_addItemButton_clicked)
        clearButton.clicked.connect(self.clearInventory)

    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0) # Go back to the main menu

    def on_addItemButton_clicked(self):
        name = self._select_item()
        if name is None:
          return
        index = self._next_free_item()
        if index is len(self.inventory):
          QMessageBox.warning(self, "Inventory error", "The inventory is full.")
          return

        self.inventory[index] = name
        self.inventory_table.setItem(index, 0, QTableWidgetItem(name))
        self.cursor.execute("INSERT INTO PlayerInventories (PlayerID, ItemName, SlotIDX) VALUES (%s, %s, %s)", (self.ID, name, index))
        self.db.commit()

    def clearInventory(self):
        raise Exception("not yet implemented")

    def showEvent(self, event: QShowEvent):
        self.getInfoPlyers()
        self.getInventory()
        self.nameLabel.setText(f"Hello <u>{self.name}</u>, with a level of {self.level}, you get {self.inventorySlot} slots")

        super().showEvent(event)
      
    def _select_item(self) -> str:
      # Get the name of an item from the Items table (or None if none selected)
      return "Arc en bois" # TESTING VALUE

    def _next_free_item(self) -> int:
      # Return the index of the next free slot in the inventory (or len(inventory) if no free space)
      for i in range(len(self.inventory)):
        if self.inventory[i] is None:
          return i
      return len(self.inventory)