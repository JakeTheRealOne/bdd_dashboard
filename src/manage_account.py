from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QMessageBox, QApplication, QLabel, QSpacerItem, QSizePolicy)
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

        deleteAccountButton = QPushButton("Delete Account")
        deleteAccountButton.setFixedWidth(500)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Manage Account"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel(f"Hello {self.name} with the ID {self.ID} !"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Here is your account info :"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel(f"Your Level : {self.level}, your XP : {self.xp}, your money : {self.money} and your Inventory Slot : {self.inventorySlot}"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(deleteAccountButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)

        # connect the buttons
        backButton.clicked.connect(self.on_backButton_clicked)
        deleteAccountButton.clicked.connect(self.deleteAccount)

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