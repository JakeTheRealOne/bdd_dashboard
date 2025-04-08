from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QStackedWidget, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt

import qt_config

class ManageAccount(QWidget):
    """
    ManageAccount class to handle the management of player accounts.
    """

    def __init__(self, parent, stackedWidget, username):
        super().__init__(parent)
        self.username = username
        self.stackedWidget = stackedWidget
        self.setup()

    def setup(self):
        self.exitButton = QPushButton("Back")
        self.exitButton.setFixedWidth(500)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Manage Account"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.exitButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)

        # connect the buttons
        self.exitButton.clicked.connect(self.on_backButton_clicked)

        self.show()

    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0) # Go back to the main menu
