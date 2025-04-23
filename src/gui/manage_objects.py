from PyQt5.QtWidgets import QWidget, QHeaderView, QVBoxLayout, QPushButton, QMessageBox, QLabel, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent
import mysql.connector

from . import qt_config

class ManageObjects(QWidget):
    """
    Allows user to modify object properties
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
        self.getWeapons()

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

    def getWeapons(self):
      self.cursor.execute("SELECT * FROM Weapons")
      self.weapons = self.cursor.fetchall()
      
      self.weapons_table.setRowCount(len(self.weapons))
      self.weapons_table.setColumnCount(2)
      self.weapons_table.setHorizontalHeaderLabels(["Weapon Name", "Power"])

      for i in range(len(self.weapons)):
          col1 = QTableWidgetItem(self.weapons[i][0])
          col2 = QTableWidgetItem(str(self.weapons[i][1]))
          col1.setTextAlignment(Qt.AlignCenter)
          col2.setTextAlignment(Qt.AlignCenter)
          self.weapons_table.setItem(i, 0, col1)
          self.weapons_table.setItem(i, 1, col2)

      self.weapons_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
      self.weapons_table.resizeRowsToContents()
      # self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)
      # self.clearButton.setEnabled(self.occuped_slots)


    def setup(self):
        backButton = QPushButton("Back")
        backButton.setFixedWidth(500)
        backButton.setAutoDefault(True)

        self.nameLabel = QLabel()
        self.weapons_table = QTableWidget()
        self.weapons_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.weapons_table.setMinimumWidth(400)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.create_center_bold_title("Manage objects"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Here is all registered weapons:"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.weapons_table, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Click on a property to modify its value"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)

        # connect buttons
        backButton.clicked.connect(self.on_backButton_clicked)

    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0)

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

    def showEvent(self, event: QShowEvent):
        self.getInfoPlyers()
        self.getWeapons()
        super().showEvent(event)

    def _next_free_item(self):
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                return i
        return len(self.inventory)
