from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QPushButton, QMessageBox, QApplication, QLabel, QSpacerItem, QSizePolicy, QLineEdit
from PyQt5.QtCore import Qt
import mysql.connector

import gui.qt_config as qt_config

class ManageCharacters(QWidget):
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
        self.getCharactes()
        self.setup()

    def setup(self):
        backButton = QPushButton("Back")
        backButton.setFixedWidth(500)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Manage your Characters"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)

        backButton.clicked.connect(self.on_backButton_clicked)

    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0) # Go back to the main menu

    def getCharactes(self):
        self.cursor.execute("SELECT p.Name FROM Players p WHERE ID = %s", self.ID)
        name = self.cursor.fetchone()

        self.cursor.execute("SELECT * FROM Characters WHERE Username = %s", name)
        self.characters = self.cursor.fetchall()
