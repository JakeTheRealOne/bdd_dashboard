from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLineEdit, QStackedWidget, QMessageBox, QApplication, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt

class MainMenu(QWidget):
    """
    MainMenu class to handle the main menu of the game.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup()

    def setup(self):
        self.manageAccountButton = QPushButton("Manage Account")
        self.startButton.setFixedWidth(500)
        self.exitButton = QPushButton("Exit")
        self.exitButton.setFixedWidth(500)

        # main page
        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(self.manageAccountButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.exitButton, alignment=Qt.AlignCenter)
        
        self.setLayout(mainLayout)

        self.show()

    def on_exit