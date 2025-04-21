from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget, QMessageBox, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

import gui.qt_config as qt_config
import gui.manage_account as manage_account
import gui.manage_characters as manage_characters
import gui.manage_inventory as manage_inventory
import gui.manage_quests as manage_quests
import gui.monsters as monsters
import gui.ranking as ranking

class MainMenu(QWidget):
    """
    MainMenu class to handle the main menu of the game.
    """

    def __init__(self, ID, parent=None):
        super().__init__(parent)
        self.showMaximized()
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
        manageMonstersButton = QPushButton("Check Monsters")
        manageMonstersButton.setFixedWidth(500)
        manageMonstersButton.setAutoDefault(True)
        rankingButton = QPushButton("Ranking")
        rankingButton.setFixedWidth(500)
        rankingButton.setAutoDefault(True)
        exitButton = QPushButton("Exit")
        exitButton.setFixedWidth(500)
        exitButton.setAutoDefault(True)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.create_center_bold_title("Welcome to the Main Menu"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(manageAccountButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(manageCharactersButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(manageInventoryButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(manageQuestsButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(manageMonstersButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(rankingButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(exitButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.mainPage = QWidget()
        self.mainPage.setLayout(mainLayout)
        self.stackedWidget.addWidget(self.mainPage)

        self.stackedWidget.setCurrentWidget(self.mainPage)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)

        # connect the buttons
        exitButton.clicked.connect(self.on_exitButton_clicked)
        manageAccountButton.clicked.connect(self.on_manageAccountButton_clicked)
        manageCharactersButton.clicked.connect(self.on_manageCharactersButton_clicked)
        manageInventoryButton.clicked.connect(self.on_manageInventoryButton_clicked)
        manageQuestsButton.clicked.connect(self.on_manageQuestsButton_clicked)
        manageMonstersButton.clicked.connect(self.on_manageMonstersButton_clicked)
        rankingButton.clicked.connect(self.on_rankingButton_clicked)
        

    def on_exitButton_clicked(self):
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to exit ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()
            
    def on_rankingButton_clicked(self):
        if hasattr(self, 'ranking'):
            self.ranking.deleteLater()
            self.ranking = None
        self.ranking = ranking.Ranking(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.ranking)
        self.stackedWidget.setCurrentWidget(self.ranking)

    def on_manageAccountButton_clicked(self):
        if hasattr(self, 'manageAccount'):
            self.manageAccount.deleteLater()
            self.manageAccount = None
        self.manageAccount = manage_account.ManageAccount(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.manageAccount)
        self.stackedWidget.setCurrentWidget(self.manageAccount)

    def on_manageCharactersButton_clicked(self):
        if hasattr(self, 'manageCharacters'):
            self.manageCharacters.deleteLater()
            self.manageCharacters = None
        self.manageCharacters = manage_characters.ManageCharacters(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.manageCharacters)
        self.stackedWidget.setCurrentWidget(self.manageCharacters)

    def on_manageInventoryButton_clicked(self):
        if hasattr(self, 'manageInventory'):
            self.manageInventory.deleteLater()
            self.manageInventory = None
        self.manageInventory = manage_inventory.ManageInventory(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.manageInventory)
        self.stackedWidget.setCurrentWidget(self.manageInventory)

    def on_manageQuestsButton_clicked(self):
        if hasattr(self, 'manageQuests'):
            self.manageQuests.deleteLater()
            self.manageQuests = None
        self.manageQuests = manage_quests.ManageQuests(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.manageQuests)
        self.stackedWidget.setCurrentWidget(self.manageQuests)
        
    def on_manageMonstersButton_clicked(self):
        if hasattr(self, 'manageMonsters'):
            self.manageMonsters.deleteLater()
            self.manageMonsters = None
        self.manageMonsters = monsters.Monsters(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.manageMonsters)
        self.stackedWidget.setCurrentWidget(self.manageMonsters)
        