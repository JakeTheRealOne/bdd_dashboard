from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget, QMessageBox, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

import gui.qt_config as qt_config
import gui.manage_account as manage_account
import gui.manage_characters as manage_characters
import gui.manage_inventory as manage_inventory
import gui.manage_quests as manage_quests

class MainMenu(QWidget):
    """
    MainMenu class to handle the main menu of the game.
    """

    def __init__(self, ID, parent=None):
        super().__init__(parent)
        self.ID = ID
        self.setup()

    def setup(self):
        self.stackedWidget = QStackedWidget()

        manageAccountButton = QPushButton("Manage Account")
        manageAccountButton.setFixedWidth(500)
        manageAccountButton.setAutoDefault(True)
        manageCharactersButton = QPushButton("Manage Characters")
        manageCharactersButton.setFixedWidth(500)
        manageCharactersButton.setAutoDefault(True)
        manageInventoryButton = QPushButton("Manage inventory")
        manageInventoryButton.setFixedWidth(500)
        manageInventoryButton.setAutoDefault(True)
        manageQuestsButton = QPushButton("Manage Quests")
        manageQuestsButton.setFixedWidth(500)
        manageQuestsButton.setAutoDefault(True)
        exitButton = QPushButton("Exit")
        exitButton.setFixedWidth(500)
        exitButton.setAutoDefault(True)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Welcome to the Main Menu"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(manageAccountButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(manageCharactersButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(manageInventoryButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(manageQuestsButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(exitButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.mainPage = QWidget()
        self.mainPage.setLayout(mainLayout)
        self.stackedWidget.addWidget(self.mainPage)

        self.manageAccount = manage_account.ManageAccount(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.manageAccount)

        self.manageCharacters = manage_characters.ManageCharacters(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.manageCharacters)

        self.manageInventory = manage_inventory.ManageInventory(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.manageInventory)
        
        self.manageQuests = manage_quests.ManageQuests(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.manageQuests)

        self.stackedWidget.setCurrentWidget(self.mainPage)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)
        self.showMaximized()

        # connect the buttons
        exitButton.clicked.connect(self.on_exitButton_clicked)
        manageAccountButton.clicked.connect(self.on_manageAccountButton_clicked)
        manageCharactersButton.clicked.connect(self.on_manageCharactersButton_clicked)
        manageInventoryButton.clicked.connect(self.on_manageInventoryButton_clicked)
        manageQuestsButton.clicked.connect(self.on_manageQuestsButton_clicked)
        

    def on_exitButton_clicked(self):
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to exit ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def on_manageAccountButton_clicked(self):
        self.stackedWidget.setCurrentWidget(self.manageAccount)

    def on_manageCharactersButton_clicked(self):
        self.stackedWidget.setCurrentWidget(self.manageCharacters)

    def on_manageInventoryButton_clicked(self):
        self.stackedWidget.setCurrentWidget(self.manageInventory)

    def on_manageQuestsButton_clicked(self):
        self.stackedWidget.setCurrentWidget(self.manageQuests)