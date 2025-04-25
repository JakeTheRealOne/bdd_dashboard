from PyQt5.QtWidgets import QWidget, QHeaderView, QVBoxLayout, QPushButton, QMessageBox, QLabel, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent
import mysql.connector

from . import qt_config

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
      self.inventory_table.setColumnCount(3)
      self.inventory_table.setHorizontalHeaderLabels(["Object Name", "Equip", "Delete"])

      self.occuped_slots = 0

      for row in rows:
          if row[0] == self.ID:
              self.inventory[row[2]] = row[1]
              item = QTableWidgetItem(row[1])
              item.setTextAlignment(Qt.AlignCenter)
              self.inventory_table.setItem(row[2], 0, item)
              use_button = QPushButton("Equip")
              use_button.setFixedWidth(200)
              use_button.setAutoDefault(True)
              use_button.clicked.connect(lambda _, r=row[2]: self.on_useItem_clicked(r))
              del_button = QPushButton("Delete")
              del_button.setFixedWidth(200)
              del_button.setAutoDefault(True)
              del_button.clicked.connect(lambda _, r=row[2]: self.on_delItem_clicked(r))
              self.inventory_table.setCellWidget(row[2], 1, use_button)
              self.inventory_table.setCellWidget(row[2], 2, del_button)
              self.occuped_slots += 1

      self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
      self.inventory_table.resizeRowsToContents()
      self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)
      self.clearButton.setEnabled(self.occuped_slots)

      self.equip = [None, None]
      self.cursor.execute("SELECT ArmorName FROM PlayerArmors WHERE PlayerArmors.PlayerID = %s", (self.ID,))
      result = self.cursor.fetchall()
      if result and result[0]:
        self.equip[0] = result[0][0]
        item = QTableWidgetItem(result[0][0])
        item.setTextAlignment(Qt.AlignCenter)
        self.equip_table.setItem(0, 0, item)

      self.cursor.execute("SELECT WeaponName FROM PlayerWeapons WHERE PlayerWeapons.PlayerID = %s", (self.ID,))
      result = self.cursor.fetchall()
      if result and result[0]:
        self.equip[1] = result[0][0]
        item = QTableWidgetItem(result[0][0])
        item.setTextAlignment(Qt.AlignCenter)
        self.equip_table.setItem(0, 1, item)
      self.equip_table.resizeRowsToContents()

    def setup(self):
        backButton = QPushButton("Back")
        backButton.setFixedWidth(500)
        backButton.setAutoDefault(True)

        self.addItemButton = QPushButton("Collect item")
        self.addItemButton.setEnabled(False)
        self.addItemButton.setAutoDefault(True)
        self.addItemButton.setFixedWidth(500)

        self.clearButton = QPushButton("Clear Inventory")
        self.clearButton.setEnabled(True)
        self.clearButton.setAutoDefault(True)
        self.clearButton.setFixedWidth(500)

        self.nameLabel = QLabel()

        self.equip_table = QTableWidget()
        self.equip_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.equip_table.setMinimumWidth(200)
        self.equip_table.setRowCount(2)
        self.equip_table.setColumnCount(1)
        self.equip_table.setVerticalHeaderLabels(["Armor on body", "Weapon in hand"])
        self.equip_table.resizeRowsToContents()

        self.inventory_table = QTableWidget()
        self.inventory_table.setEditTriggers(QTableWidget.NoEditTriggers)
        # self.inventory_table.cellPressed.connect(self.on_select_slot) 
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
        mainLayout.addWidget(qt_config.create_center_bold_title("Manage Inventory"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.nameLabel, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Here is your equipements:"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.equip_table, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Here is your inventory:"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inventory_table, alignment=Qt.AlignCenter)
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

    def on_select_item(self, row):
        item = self.item_table.item(row, 0)
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
            use_button = QPushButton("Equip")
            use_button.setFixedWidth(200)
            use_button.setAutoDefault(True)
            use_button.clicked.connect(lambda _, r=index: self.on_useItem_clicked(r))
            del_button = QPushButton("Drop")
            del_button.setFixedWidth(200)
            del_button.setAutoDefault(True)
            del_button.clicked.connect(lambda _, r=index: self.on_delItem_clicked(r))
            self.inventory_table.setCellWidget(index, 1, use_button)
            self.inventory_table.setCellWidget(index, 2, del_button)
            self.occuped_slots += 1
            self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)
            self.clearButton.setEnabled(self.occuped_slots)
            self.cursor.execute("INSERT INTO PlayerInventories (PlayerID, ItemName, SlotIDX) VALUES (%s, %s, %s)", (self.ID, name, index))
            self.db.commit()
            self.hide_item_selector()

    def on_delItem_clicked(self, row):
        slot = self.inventory_table.item(row, 0)
        if slot:
            index = row
            self.inventory[index] = None
            self.inventory_table.setItem(index, 0, QTableWidgetItem())
            self.inventory_table.setCellWidget(index, 1, None)
            self.inventory_table.setCellWidget(index, 2, None)
            self.occuped_slots -= 1
            self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)
            self.clearButton.setEnabled(self.occuped_slots)
            self.cursor.execute("DELETE FROM PlayerInventories WHERE PlayerID = %s AND SlotIDX = %s", (self.ID, index))
            self.db.commit()

    def on_useItem_clicked(self, row):
        slot = self.inventory_table.item(row, 0)
        if not slot:
            return        
        index = row
        name = slot.text()
        if self._is_armor(name):
            old = self.equip[0]
            self.equip[0] = name
            item = QTableWidgetItem(name)
            item.setTextAlignment(Qt.AlignCenter)
            self.equip_table.setItem(0, 0, item)
            item2 = QTableWidgetItem(old)
            item2.setTextAlignment(Qt.AlignCenter)
            self.inventory_table.setItem(row, 0, item2)
            self.inventory[row] = old
            if old is None:
              self.inventory_table.setCellWidget(row, 1, None)
              self.inventory_table.setCellWidget(row, 2, None)
              self.cursor.execute("""
                  DELETE FROM PlayerInventories
                  WHERE PlayerID = %s AND SlotIDX = %s
              """, (self.ID, index))
            else:
              self.cursor.execute("""
                  INSERT INTO PlayerInventories (PlayerID, ItemName, SlotIDX)
                  VALUES (%s, %s, %s)
                  ON DUPLICATE KEY UPDATE ItemName = VALUES(ItemName)
              """, (self.ID, old, index))
            self.cursor.execute("""
                INSERT INTO PlayerArmors (PlayerID, ArmorName)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE ArmorName = VALUES(ArmorName)
            """, (self.ID, name))
            self.db.commit()
        elif self._is_weapon(name):
            old = self.equip[1]
            self.equip[1] = name
            self.inventory[row] = old
            item = QTableWidgetItem(name)
            item.setTextAlignment(Qt.AlignCenter)
            self.equip_table.setItem(0, 1, item)
            item2 = QTableWidgetItem(old)
            item2.setTextAlignment(Qt.AlignCenter)
            self.inventory_table.setItem(row, 0, item2)
            if old is None:
              self.inventory_table.setCellWidget(row, 1, None)
              self.inventory_table.setCellWidget(row, 2, None)
              self.cursor.execute("""
                  DELETE FROM PlayerInventories
                  WHERE PlayerID = %s AND SlotIDX = %s
              """, (self.ID, index))
            else:
              self.cursor.execute("""
                  INSERT INTO PlayerInventories (PlayerID, ItemName, SlotIDX)
                  VALUES (%s, %s, %s)
                  ON DUPLICATE KEY UPDATE ItemName = VALUES(ItemName)
              """, (self.ID, old, index))
            self.cursor.execute("""
                INSERT INTO PlayerWeapons (PlayerID, WeaponName)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE WeaponName = VALUES(WeaponName)
            """, (self.ID, name))
            self.db.commit()


    def _next_free_item(self):
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                return i
        return len(self.inventory)

    def _is_armor(self, object: str) -> bool:
        self.cursor.execute("SELECT * FROM Armors WHERE Name = %s", (object,))
        result = bool(self.cursor.fetchall())
        return result

    def _is_weapon(self, object: str) -> bool:
        self.cursor.execute("SELECT * FROM Weapons WHERE Name = %s", (object,))
        result = bool(self.cursor.fetchall())
        return result