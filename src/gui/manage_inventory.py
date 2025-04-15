from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QPushButton, QMessageBox, QApplication, QLabel, QSpacerItem, QSizePolicy, QLineEdit, QTableWidget, QTableWidgetItem, QDialog
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
      self.occuped_slots = 0
      for row in rows:
        if row[0] == self.ID:
          self.inventory[row[2]] = row[1]
          self.inventory_table.setItem(row[2], 0, QTableWidgetItem(row[1]))
          self.occuped_slots += 1
      self.inventory_table.resizeColumnsToContents()
      self.inventory_table.resizeRowsToContents()
      self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)


    def setup(self):
        backButton = QPushButton("Back")
        backButton.setFixedWidth(500)

        self.addItemButton = QPushButton("Add item")
        self.addItemButton.setEnabled(False)
        self.addItemButton.setFixedWidth(500)

        self.clearButton = QPushButton("Clear Inventory")
        self.clearButton.setEnabled(True)
        self.clearButton.setFixedWidth(500)

        self.nameLabel = QLabel(f"Hello <u>{self.name}</u>, with a level of {self.level}, you get {self.inventorySlot} slots")
        self.inventory_table = QTableWidget()
        self.inventory_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.inventory_table.cellPressed.connect(self.on_select_slot) 
        self.item_table = QTableWidget()
        self.item_table.cellPressed.connect(self.on_select_item) 
        self.item_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.item_dialog = QDialog()
        self.item_dialog.setWindowTitle("Item selector")
        dialog_layout = QVBoxLayout()
        dialog_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        dialog_layout.addWidget(QLabel("Select an item to add to your inventory:"), alignment=Qt.AlignCenter)
        dialog_layout.addWidget(self.item_table, alignment=Qt.AlignCenter)
        dialog_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.item_dialog.setLayout(dialog_layout)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Manage Inventory"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.nameLabel, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Here is your inventory:"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inventory_table, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Click on a slot to drop its item"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.addItemButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.clearButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)

        # connect the buttons
        backButton.clicked.connect(self.on_backButton_clicked)
        self.addItemButton.clicked.connect(self.on_addItemButton_clicked)
        self.clearButton.clicked.connect(self.clearInventory)

    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0) # Go back to the main menu

    def on_addItemButton_clicked(self):
        index = self._next_free_item()
        if index is len(self.inventory):
          QMessageBox.warning(self, "Inventory error", "The inventory is full.")
          return
        name = self._select_item()
        if name is None:
          return

        self.inventory[index] = name
        self.inventory_table.setItem(index, 0, QTableWidgetItem(name))
        self.inventory_table.resizeColumnsToContents()
        self.inventory_table.resizeRowsToContents()
        self.occuped_slots += 1
        self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)
        self.clearButton.setEnabled(self.occuped_slots)
        self.cursor.execute("INSERT INTO PlayerInventories (PlayerID, ItemName, SlotIDX) VALUES (%s, %s, %s)", (self.ID, name, index))
        self.db.commit()

    def clearInventory(self):
        self.inventory = [None] * self.inventorySlot
        self.inventory_table.clearContents()
        self.occuped_slots = 0
        self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)
        self.clearButton.setEnabled(self.occuped_slots)
        self.cursor.execute("DELETE FROM PlayerInventories WHERE PlayerID = %s", (self.ID,))
        self.db.commit() 
 

    def showEvent(self, event: QShowEvent):
        self.getInfoPlyers()
        self.getInventory()
        self.nameLabel.setText(f"Hello <u>{self.name}</u>, with a level of {self.level}, you get {self.inventorySlot} slots")

        super().showEvent(event)
      
    def _select_item(self) -> str:
      # Get the name of an item from the Items table (or None if none selected)
      self.cursor.execute("SELECT * FROM Items")
      rows = self.cursor.fetchall()
      self.item_table.setRowCount(len(rows))
      self.item_table.setColumnCount(1)
      self.item_table.setHorizontalHeaderLabels(["Object Name"])
      for index in range(len(rows)):
        self.item_table.setItem(index, 0, QTableWidgetItem(rows[index][0]))
      self.item_table.resizeColumnsToContents()
      self.item_table.resizeRowsToContents()
      
      self.selected_item = None
      self.item_dialog.exec()

      return self.selected_item # TESTING VALUE

    def _next_free_item(self) -> int:
      # Return the index of the next free slot in the inventory (or len(inventory) if no free space)
      for i in range(len(self.inventory)):
        if self.inventory[i] is None:
          return i
      return len(self.inventory)

    def on_select_item(self, row, column) -> int:
        item = self.item_table.item(row, column)
        if item:
            self.selected_item = item.text()
            self.item_dialog.accept()

    def on_select_slot(self, row, column) -> int:
        slot = self.inventory_table.item(row, column)
        if slot:
            index = row
            self.inventory[index] = None
            self.inventory_table.setItem(index, 0, QTableWidgetItem())
            self.inventory_table.resizeColumnsToContents()
            self.inventory_table.resizeRowsToContents()
            self.occuped_slots -= 1
            self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)
            self.clearButton.setEnabled(self.occuped_slots)
            self.cursor.execute("DELETE FROM PlayerInventories WHERE PlayerID = %s AND SlotIDX = %s", (self.ID, index))
            self.db.commit()
