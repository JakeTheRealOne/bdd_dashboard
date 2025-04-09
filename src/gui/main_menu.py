from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget, QMessageBox, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

import gui.qt_config as qt_config
import gui.manage_account as manage_account

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

        self.manageAccountButton = QPushButton("Manage Account")
        self.manageAccountButton.setFixedWidth(500)
        self.exitButton = QPushButton("Exit")
        self.exitButton.setFixedWidth(500)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Welcome to the Main Menu"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.manageAccountButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.exitButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.mainPage = QWidget()
        self.mainPage.setLayout(mainLayout)
        self.stackedWidget.addWidget(self.mainPage)

        self.manageAccount = manage_account.ManageAccount(self, self.stackedWidget, self.ID)
        self.stackedWidget.addWidget(self.manageAccount)

        self.stackedWidget.setCurrentWidget(self.mainPage)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)
        self.show()

        # connect the buttons
        self.exitButton.clicked.connect(self.on_exitButton_clicked)
        self.manageAccountButton.clicked.connect(self.on_manageAccountButton_clicked)

    def on_exitButton_clicked(self):
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to exit ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def on_manageAccountButton_clicked(self):
        self.stackedWidget.setCurrentWidget(self.manageAccount)
