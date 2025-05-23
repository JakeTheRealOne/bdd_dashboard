from PyQt5.QtWidgets import (
    QWidget,
    QHeaderView,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent, QBrush, QColor, QFont
import mysql.connector

from . import qt_config
from . import add_object


class ManageObjects(QWidget):
    """
    Allows user to modify item properties
    """

    def __init__(self, parent, stackedWidget, ID):
        super().__init__(parent)
        self.stackedWidget = stackedWidget
        self.ID = ID
        self.db = mysql.connector.connect(
            host="localhost", user="rootuser", password="rootuser", database="rpg"
        )
        self.db.start_transaction(isolation_level="READ COMMITTED")
        self.cursor = self.db.cursor()
        self.setup()
        self.getWeapons()
        self.getArmors()
        self.getPotions()
        self.getArtefacts()

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def _price_of(self, item: str) -> int:
        """
        Get the price of an item, or 0 if it doesn't exist
        """
        self.cursor.execute("SELECT Price FROM Items WHERE Name = %s;", (item,))
        return self.cursor.fetchone()[0] or 0

    def getWeapons(self):
        self.weapons_table.cellChanged.disconnect()
        self.cursor.execute("SELECT * FROM Weapons")
        self.weapons = [list(e) for e in self.cursor.fetchall()]

        self.weapons_table.setRowCount(len(self.weapons))
        self.weapons_table.setColumnCount(3)
        self.weapons_table.setHorizontalHeaderLabels(["Weapon Name", "Power", "Price"])

        for i in range(len(self.weapons)):
            col1 = QTableWidgetItem(self.weapons[i][0])
            col1.setFlags(col1.flags() & ~Qt.ItemIsEditable)
            col1.setTextAlignment(Qt.AlignCenter)
            col2 = QTableWidgetItem(str(self.weapons[i][1]))
            col2.setTextAlignment(Qt.AlignCenter)
            col3 = QTableWidgetItem(str(self._price_of(self.weapons[i][0])))
            col3.setTextAlignment(Qt.AlignCenter)
            self.weapons_table.setItem(i, 2, col3)
            self.weapons_table.setItem(i, 0, col1)
            self.weapons_table.setItem(i, 1, col2)

        self.weapons_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.weapons_table.resizeRowsToContents()
        self.weapons_table.cellChanged.connect(self.on_weaponCell_changed)
        # self.addItemButton.setEnabled(self.occuped_slots != self.inventorySlot)
        # self.clearButton.setEnabled(self.occuped_slots)

    def getArmors(self):
        self.armors_table.cellChanged.disconnect()
        self.cursor.execute("SELECT * FROM Armors")
        self.armors = [list(e) for e in self.cursor.fetchall()]

        self.armors_table.setRowCount(len(self.armors))
        self.armors_table.setColumnCount(3)
        self.armors_table.setHorizontalHeaderLabels(["Armor Name", "Defence", "Price"])

        for i in range(len(self.armors)):
            col1 = QTableWidgetItem(self.armors[i][0])
            col1.setFlags(col1.flags() & ~Qt.ItemIsEditable)
            col2 = QTableWidgetItem(str(self.armors[i][1]))
            col1.setTextAlignment(Qt.AlignCenter)
            col2.setTextAlignment(Qt.AlignCenter)
            col3 = QTableWidgetItem(str(self._price_of(self.armors[i][0])))
            col3.setTextAlignment(Qt.AlignCenter)
            self.armors_table.setItem(i, 2, col3)
            self.armors_table.setItem(i, 0, col1)
            self.armors_table.setItem(i, 1, col2)

        self.armors_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.armors_table.resizeRowsToContents()
        self.armors_table.cellChanged.connect(self.on_armorCell_changed)

    def getPotions(self):
        self.cursor.execute("SELECT * FROM Potions")
        self.potions = [list(e) for e in self.cursor.fetchall()]

        self.potions_table.setRowCount(len(self.potions))
        self.potions_table.setColumnCount(3)
        self.potions_table.setHorizontalHeaderLabels(["Potion Name", "Boost", "Price"])

        for i in range(len(self.potions)):
            col1 = QTableWidgetItem(self.potions[i][0])
            col1.setFlags(col1.flags() & ~Qt.ItemIsEditable)
            col2 = QTableWidgetItem(self.potions[i][1])
            col1.setTextAlignment(Qt.AlignCenter)
            col2.setTextAlignment(Qt.AlignCenter)
            col3 = QTableWidgetItem(str(self._price_of(self.potions[i][0])))
            col3.setTextAlignment(Qt.AlignCenter)
            self.potions_table.setItem(i, 2, col3)
            self.potions_table.setItem(i, 0, col1)
            self.potions_table.setItem(i, 1, col2)

        self.potions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.potions_table.resizeRowsToContents()

    def getArtefacts(self):
        self.cursor.execute("SELECT * FROM Artefacts")
        self.artefacts = [list(e) for e in self.cursor.fetchall()]

        self.artefacts_table.setRowCount(len(self.artefacts))
        self.artefacts_table.setColumnCount(3)
        self.artefacts_table.setHorizontalHeaderLabels(
            ["Artefact Name", "Effect", "Price"]
        )

        for i in range(len(self.artefacts)):
            col1 = QTableWidgetItem(self.artefacts[i][0])
            col1.setFlags(col1.flags() & ~Qt.ItemIsEditable)
            col2 = QTableWidgetItem(self.artefacts[i][1])
            col1.setTextAlignment(Qt.AlignCenter)
            col2.setTextAlignment(Qt.AlignCenter)
            col3 = QTableWidgetItem(str(self._price_of(self.artefacts[i][0])))
            col3.setTextAlignment(Qt.AlignCenter)
            self.artefacts_table.setItem(i, 2, col3)
            self.artefacts_table.setItem(i, 0, col1)
            self.artefacts_table.setItem(i, 1, col2)

        self.artefacts_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.artefacts_table.resizeRowsToContents()

    def setup(self):
        self.addPage = add_object.AddObject(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.addPage)

        backButton = QPushButton("Back")
        backButton.setFixedWidth(400)
        backButton.setAutoDefault(True)

        add_weapon_button = QPushButton("Add")
        add_weapon_button.setFixedWidth(300)
        add_weapon_button.setAutoDefault(True)

        add_armor_button = QPushButton("Add")
        add_armor_button.setFixedWidth(300)
        add_armor_button.setAutoDefault(True)

        add_potion_button = QPushButton("Add")
        add_potion_button.setFixedWidth(300)
        add_potion_button.setAutoDefault(True)

        add_artefact_button = QPushButton("Add")
        add_artefact_button.setFixedWidth(300)
        add_artefact_button.setAutoDefault(True)

        self.weapons_table = QTableWidget()
        self.weapons_table.horizontalHeader().setStretchLastSection(False)
        self.weapons_table.setMinimumWidth(400)
        self.weapons_table.cellChanged.connect(self.on_weaponCell_changed)
        self.armors_table = QTableWidget()
        self.armors_table.horizontalHeader().setStretchLastSection(False)
        self.armors_table.setMinimumWidth(400)
        self.armors_table.cellChanged.connect(self.on_armorCell_changed)
        self.potions_table = QTableWidget()
        self.potions_table.horizontalHeader().setStretchLastSection(False)
        self.potions_table.setMinimumWidth(400)
        self.potions_table.cellChanged.connect(self.on_potionCell_changed)
        self.artefacts_table = QTableWidget()
        self.artefacts_table.horizontalHeader().setStretchLastSection(False)
        self.artefacts_table.setMinimumWidth(400)
        self.artefacts_table.cellChanged.connect(self.on_artefactCell_changed)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        mainLayout.addWidget(
            qt_config.create_center_bold_title("Manage objects"),
            alignment=Qt.AlignCenter,
        )
        mainLayout.addWidget(
            QLabel("Click on a property to modify its value"), alignment=Qt.AlignCenter
        )
        mainLayout.addWidget(
            QLabel("Here is all registered weapons:"), alignment=Qt.AlignCenter
        )
        mainLayout.addWidget(self.weapons_table, alignment=Qt.AlignCenter)
        mainLayout.addWidget(add_weapon_button, alignment=Qt.AlignCenter)
        mainLayout.addWidget(
            QLabel("Here is all registered armors:"), alignment=Qt.AlignCenter
        )
        mainLayout.addWidget(self.armors_table, alignment=Qt.AlignCenter)
        mainLayout.addWidget(add_armor_button, alignment=Qt.AlignCenter)
        mainLayout.addWidget(
            QLabel("Here is all registered potions:"), alignment=Qt.AlignCenter
        )
        mainLayout.addWidget(self.potions_table, alignment=Qt.AlignCenter)
        mainLayout.addWidget(add_potion_button, alignment=Qt.AlignCenter)
        mainLayout.addWidget(
            QLabel("Here is all registered artefacts:"), alignment=Qt.AlignCenter
        )
        mainLayout.addWidget(self.artefacts_table, alignment=Qt.AlignCenter)
        mainLayout.addWidget(add_artefact_button, alignment=Qt.AlignCenter)
        mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.setLayout(mainLayout)

        # connect buttons
        backButton.clicked.connect(self.on_backButton_clicked)
        add_weapon_button.clicked.connect(self.on_addWeapon_clicked)
        add_armor_button.clicked.connect(self.on_addArmor_clicked)
        add_potion_button.clicked.connect(self.on_addPotion_clicked)
        add_artefact_button.clicked.connect(self.on_addArtefact_clicked)

    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0)

    def on_weaponCell_changed(self, row, col):
        if col == 2:
            name = self.weapons[row][0]
            item = self.weapons_table.item(row, col)
            try:
                value = int(item.text())
                if value <= 0:
                    raise TypeError("Price cannot be negative")
            except:
                item.setForeground(QBrush(QColor("red")))
                font = QFont()
                font.setBold(True)
                item.setFont(font)
            else:
                item.setForeground(QBrush(QColor("Black")))
                font = QFont()
                item.setFont(font)
                self._update_price(name, value)
        elif col == 1:
            item = self.weapons_table.item(row, col)
            string = item.text()
            try:
                value = int(string)
                if value < 0:
                    raise TypeError("Cannot convert to positive integer")
            except:
                item.setForeground(QBrush(QColor("red")))
                font = QFont()
                font.setBold(True)
                item.setFont(font)
            else:
                item.setForeground(QBrush(QColor("Black")))
                font = QFont()
                item.setFont(font)
                self.weapons[row][1] = value
                self.cursor.execute(
                    "UPDATE Weapons SET Power = %s WHERE Name = %s",
                    self.weapons[row][::-1],
                )
                self.db.commit()

    def on_armorCell_changed(self, row, col):
        if col == 2:
            name = self.armors[row][0]
            item = self.armors_table.item(row, col)
            try:
                value = int(item.text())
                if value <= 0:
                    raise TypeError("Price cannot be negative")
            except:
                item.setForeground(QBrush(QColor("red")))
                font = QFont()
                font.setBold(True)
                item.setFont(font)
            else:
                item.setForeground(QBrush(QColor("Black")))
                font = QFont()
                item.setFont(font)
                self._update_price(name, value)
        elif col == 1:
            item = self.armors_table.item(row, col)
            string = item.text()
            try:
                value = int(string)
                if value < 0:
                    raise TypeError("Cannot convert to positive integer")
            except:
                item.setForeground(QBrush(QColor("red")))
                font = QFont()
                font.setBold(True)
                item.setFont(font)
            else:
                item.setForeground(QBrush(QColor("Black")))
                font = QFont()
                item.setFont(font)
                self.armors[row][1] = value
                self.cursor.execute(
                    "UPDATE Armors SET Defence = %s WHERE Name = %s",
                    self.armors[row][::-1],
                )
                self.db.commit()

    def on_potionCell_changed(self, row, col):
        if col == 2:
          name = self.potions[row][0]
          item = self.potions_table.item(row, col)
          try:
            value = int(item.text())
            if value <= 0:
              raise TypeError("Price cannot be negative")
          except:
              item.setForeground(QBrush(QColor("red")))
              font = QFont()
              font.setBold(True)
              item.setFont(font)
          else:
            item.setForeground(QBrush(QColor("Black")))
            font = QFont()
            item.setFont(font)
            self._update_price(name, value)
        elif col == 1:
            item = self.potions_table.item(row, col)
            string = item.text()
            self.potions[row][1] = string
            self.cursor.execute(
                "UPDATE Potions SET Boost = %s WHERE Name = %s",
                self.potions[row][::-1],
            )
            self.db.commit()


    def on_artefactCell_changed(self, row, col):
        if col == 2:
          name = self.artefacts[row][0]
          item = self.artefacts_table.item(row, col)
          try:
            value = int(item.text())
            if value <= 0:
              raise TypeError("Price cannot be negative")
          except:
              item.setForeground(QBrush(QColor("red")))
              font = QFont()
              font.setBold(True)
              item.setFont(font)
          else:
            item.setForeground(QBrush(QColor("Black")))
            font = QFont()
            item.setFont(font)
            self._update_price(name, value)
        elif col == 1:
            item = self.artefacts_table.item(row, col)
            string = item.text()
            self.artefacts[row][1] = string
            self.cursor.execute(
                "UPDATE Artefacts SET Effect = %s WHERE Name = %s",
                self.artefacts[row][::-1],
            )
            self.db.commit()

    def on_addArmor_clicked(self):
        self.addPage.update_type("Armure")
        self.stackedWidget.setCurrentWidget(self.addPage)

    def on_addWeapon_clicked(self):
        self.addPage.update_type("Arme")
        self.stackedWidget.setCurrentWidget(self.addPage)

    def on_addPotion_clicked(self):
        self.addPage.update_type("Potion")
        self.stackedWidget.setCurrentWidget(self.addPage)

    def on_addArtefact_clicked(self):
        self.addPage.update_type("Artefact")
        self.stackedWidget.setCurrentWidget(self.addPage)

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

        self.item_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.item_table.resizeRowsToContents()
        self.item_selector_widget.setVisible(True)

    def hide_item_selector(self):
        self.item_selector_widget.setVisible(False)

    def showEvent(self, event: QShowEvent):
        self.getWeapons()
        self.getArmors()
        self.getPotions()
        self.getArtefacts()
        super().showEvent(event)

    def _next_free_item(self):
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                return i
        return len(self.inventory)

    def _update_price(self, item, price):
        """
        Update the price of an item
        """
        self.cursor.execute(
            "UPDATE Items SET Price = %s  WHERE Name = %s",
            (price, item),
        )
        self.db.commit()
