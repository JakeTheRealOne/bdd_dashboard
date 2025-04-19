from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QPushButton, QMessageBox, QApplication, QLabel, QSpacerItem, QSizePolicy, QLineEdit
from PyQt5.QtCore import Qt
import mysql.connector

import gui.qt_config as qt_config

class ManageAccount(QWidget):
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
        self.getInfoPlyers()
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

    def setup(self):
        backButton = QPushButton("Back")
        backButton.setFixedWidth(500)
        backButton.setAutoDefault(True)

        deleteAccountButton = QPushButton("Delete Account")
        deleteAccountButton.setFixedWidth(500)
        deleteAccountButton.setAutoDefault(True)

        self.inputName = QLineEdit()
        self.inputName.setFixedWidth(500)
        self.inputName.setPlaceholderText("Enter a new name")
        self.inputName.setAlignment(Qt.AlignCenter)
        self.inputName.setMaxLength(255)
        
        self.inputLevel = QSpinBox()
        self.inputLevel.setMinimum(0)
        self.inputLevel.setValue(self.level)  

        self.inputXP = QSpinBox()
        self.inputXP.setMinimum(0)
        self.inputXP.setValue(self.xp)

        self.inputMoney = QSpinBox()
        self.inputMoney.setMinimum(0)
        self.inputMoney.setMaximum(10000)
        self.inputMoney.setValue(self.money)

        self.nameLabel = QLabel(f"Hello <u>{self.name}</u> with the ID <u>{self.ID}</u> !")
        self.inventoryLabel = QLabel(f"Inventory Slot : <u>{self.inventorySlot}</u>")

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Manage Account"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.nameLabel, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Here is your account info :"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inputName, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Change your level :"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inputLevel, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Change your XP :"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inputXP, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Change your money :"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inputMoney, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inventoryLabel, alignment=Qt.AlignCenter)
        mainLayout.addWidget(deleteAccountButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)

        # connect the buttons
        backButton.clicked.connect(self.on_backButton_clicked)
        deleteAccountButton.clicked.connect(self.deleteAccount)
        self.inputName.returnPressed.connect(self.on_changeAccountButton_clicked)
        self.inputLevel.valueChanged.connect(self.on_changeAccountButton_clicked)
        self.inputXP.valueChanged.connect(self.on_changeAccountButton_clicked)
        self.inputMoney.valueChanged.connect(self.on_changeAccountButton_clicked)

    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0) # Go back to the main menu

    def deleteAccount(self):
        reply = QMessageBox.question(self, "Quit", "Are you sure you delete your account ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM Characters WHERE Username = %s", (self.name,))
            self.cursor.execute("DELETE FROM Players WHERE ID = %s", (self.ID,))
            self.db.commit()
            QApplication.quit()

    def on_changeAccountButton_clicked(self):
        newName = self.inputName.text()
        newLevel = self.inputLevel.value()
        newXP = self.inputXP.value()
        newMoney = self.inputMoney.value()

        if not newName:
            newName = self.name

        newInventorySlot = 5 + min(27, 2 * newLevel)
        self.inventorySlot = newInventorySlot

        # Update the account info in the database
        self.cursor.execute("UPDATE Players SET Name = %s, Level = %s, XP = %s, Money = %s, InventorySlot = %s WHERE ID = %s", (newName, newLevel, newXP, newMoney, newInventorySlot, self.ID))
        self.db.commit()

        self.getInfoPlyers()
        self.nameLabel.setText(f"Hello <u>{self.name}</u> with the ID <u>{self.ID}<u/> !")
        self.inventoryLabel.setText(f"Inventory Slot : <u>{self.inventorySlot}</u>")
