from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QSpinBox, QPushButton, QMessageBox, QApplication, QLabel, QSpacerItem, QSizePolicy, QLineEdit)
from PyQt5.QtCore import Qt
import mysql.connector

import qt_config

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

        changeAccountButton = QPushButton("Change Account Info")
        changeAccountButton.setFixedWidth(500)

        deleteAccountButton = QPushButton("Delete Account")
        deleteAccountButton.setFixedWidth(500)

        self.inputName = QLineEdit()
        self.inputName.setFixedWidth(500)
        self.inputName.setPlaceholderText("Enter a new name")
        self.inputName.setAlignment(Qt.AlignCenter)
        self.inputName.setMaxLength(255)
        
        self.inputLevel = QSpinBox()
        self.inputLevel.setMinimum(-1)
        self.inputLevel.setValue(-1)  

        self.inputXP = QSpinBox()
        self.inputXP.setMinimum(-1)
        self.inputXP.setValue(-1)

        self.inputMoney = QSpinBox()
        self.inputMoney.setMinimum(-1)
        self.inputMoney.setMaximum(1000000)
        self.inputMoney.setValue(-1)

        self.inputInventorySlot = QSpinBox()
        self.inputInventorySlot.setMinimum(-1)
        self.inputInventorySlot.setValue(-1)

        self.nameLabel = QLabel(f"Hello {self.name} with the ID {self.ID} !")
        self.statsLabel = QLabel(f"Your Level : {self.level}, your XP : {self.xp}, your money : {self.money} and your Inventory Slot : {self.inventorySlot}")

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Manage Account"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.nameLabel, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Here is your account info :"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.statsLabel, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inputName, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Change your level :"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inputLevel, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Change your XP :"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inputXP, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Change your money :"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inputMoney, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Change your Inventory Slot :"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.inputInventorySlot, alignment=Qt.AlignCenter)
        mainLayout.addWidget(changeAccountButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(deleteAccountButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)

        # connect the buttons
        backButton.clicked.connect(self.on_backButton_clicked)
        deleteAccountButton.clicked.connect(self.deleteAccount)
        changeAccountButton.clicked.connect(self.on_changeAccountButton_clicked)

        self.show()

    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0) # Go back to the main menu

    def deleteAccount(self):
        self.cursor.execute("DELETE FROM Players WHERE ID = %s", (self.ID,))
        self.db.commit()

        # Close the program after deleting the account
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to exit ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def on_changeAccountButton_clicked(self):
        newName = self.inputName.text()
        if not newName:
            newName = self.name

        newLevel = self.inputLevel.value()
        if newLevel == -1:
            newLevel = self.level

        newXP = self.inputXP.value()
        if newXP == -1:
            newXP = self.xp

        newMoney = self.inputMoney.value()
        if newMoney == -1:
            newMoney = self.money

        newInventorySlot = self.inputInventorySlot.value()
        if newInventorySlot == -1:
            newInventorySlot = self.inventorySlot

        # Update the account info in the database
        self.cursor.execute("UPDATE Players SET Name = %s, Level = %s, XP = %s, Money = %s, InventorySlot = %s WHERE ID = %s", (newName, newLevel, newXP, newMoney, newInventorySlot, self.ID))
        self.db.commit()

        self.getInfoPlyers()
        self.nameLabel.setText(f"Hello {self.name} with the ID {self.ID} !")
        self.statsLabel.setText(f"Your Level : {self.level}, your XP : {self.xp}, your money : {self.money} and your Inventory Slot : {self.inventorySlot}")

        # Show a message box to confirm the changes
        QMessageBox.information(self, "Success", "Your account info has been updated successfully.")