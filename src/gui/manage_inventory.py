from PyQt5.QtWidgets import QWidget, QHeaderView, QVBoxLayout, QPushButton, QMessageBox, QLabel, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent
import mysql.connector

import gui.qt_config as qt_config

class ManageInventory(QWidget):
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
              item = QTableWidgetItem(row[1])
              item.setTextAlignment(Qt.AlignCenter)
              self.inventory_table.setItem(row[2], 0, item)
              self.occuped_slots += 1

      self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
      self.inventory_table.resizeRowsToContents()
      self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)
      self.clearButton.setEnabled(self.occuped_slots)


    def setup(self):
        backButton = QPushButton("Back")
        backButton.setFixedWidth(500)

        self.addItemButton = QPushButton("Add item")
        self.addItemButton.setEnabled(False)
        self.addItemButton.setFixedWidth(500)

        self.clearButton = QPushButton("Clear Inventory")
        self.clearButton.setEnabled(True)
        self.clearButton.setFixedWidth(500)

        self.nameLabel = QLabel()
        self.inventory_table = QTableWidget()
        self.inventory_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.inventory_table.cellPressed.connect(self.on_select_slot) 
        self.inventory_table.setMinimumWidth(400)

        self.item_table = QTableWidget()
        self.item_table.cellPressed.connect(self.on_select_item) 
        self.item_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.item_table.setMinimumWidth(400)

        self.item_select_cancel_button = QPushButton("Cancel")
        self.item_select_cancel_button.clicked.connect(self.hide_item_selector)

        self.item_selector_widget = QWidget()
        self.item_selector_layout = QVBoxLayout()
        self.item_selector_layout.addWidget(QLabel("Select an item to add to your inventory:"), alignment=Qt.AlignCenter)
        self.item_selector_layout.addWidget(self.item_table, alignment=Qt.AlignCenter)
        self.item_selector_layout.addWidget(self.item_select_cancel_button, alignment=Qt.AlignCenter)
        self.item_selector_widget.setLayout(self.item_selector_layout)
        self.item_selector_widget.setVisible(False)

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
        mainLayout.addWidget(self.item_selector_widget, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)

        # connect buttons
        backButton.clicked.connect(self.on_backButton_clicked)
        self.addItemButton.clicked.connect(self.on_addItemButton_clicked)
        self.clearButton.clicked.connect(self.clearInventory)

    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0)

    def on_addItemButton_clicked(self):
        self.show_item_selector()

    def show_item_selector(self):
      self.cursor.execute("SELECT * FROM Items")
      rows = self.cursor.fetchall()
      self.item_table.setRowCount(len(rows))
      self.item_table.setColumnCount(1)
      self.item_table.setHorizontalHeaderLabels(["Object Name"])
      for index in range(len(rows)):
          item = QTableWidgetItem(rows[index][0])
          item.setTextAlignment(Qt.AlignCenter)
          self.item_table.setItem(index, 0, item)

      self.item_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
      self.item_table.resizeRowsToContents()
      self.item_selector_widget.setVisible(True)

    def hide_item_selector(self):
        self.item_selector_widget.setVisible(False)

    def clearInventory(self):
        self.inventory = [None] * self.inventorySlot
        self.inventory_table.clearContents()
        self.occuped_slots = 0
        self.addItemButton.setEnabled(True)
        self.clearButton.setEnabled(False)
        self.cursor.execute("DELETE FROM PlayerInventories WHERE PlayerID = %s", (self.ID,))
        self.db.commit() 

    def showEvent(self, event: QShowEvent):
        self.getInfoPlyers()
        self.getInventory()
        self.nameLabel.setText(f"Hello <u>{self.name}</u>, with a level of {self.level}, you get {self.inventorySlot} slots")
        super().showEvent(event)

    def on_select_item(self, row, column):
        item = self.item_table.item(row, column)
        if item:
            name = item.text()
            index = self._next_free_item()
            if index == len(self.inventory):
                QMessageBox.warning(self, "Inventory error", "The inventory is full.")
                return

            self.inventory[index] = name
            item_widget = QTableWidgetItem(name)
            item_widget.setTextAlignment(Qt.AlignCenter)
            self.inventory_table.setItem(index, 0, item_widget)
            self.occuped_slots += 1
            self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)
            self.clearButton.setEnabled(self.occuped_slots)
            self.cursor.execute("INSERT INTO PlayerInventories (PlayerID, ItemName, SlotIDX) VALUES (%s, %s, %s)", (self.ID, name, index))
            self.db.commit()
            self.hide_item_selector()

    def on_select_slot(self, row, column):
        slot = self.inventory_table.item(row, column)
        if slot:
            index = row
            self.inventory[index] = None
            self.inventory_table.setItem(index, 0, QTableWidgetItem())
            self.occuped_slots -= 1
            self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)
            self.clearButton.setEnabled(self.occuped_slots)
            self.cursor.execute("DELETE FROM PlayerInventories WHERE PlayerID = %s AND SlotIDX = %s", (self.ID, index))
            self.db.commit()

    def _next_free_item(self):
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                return i
        return len(self.inventory)
