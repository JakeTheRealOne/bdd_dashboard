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
        self.manageAccountButton.setFixedWidth(500)
        self.exitButton = QPushButton("Exit")
        self.exitButton.setFixedWidth(500)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(self.manageAccountButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.exitButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        
        self.setLayout(mainLayout)

        # connect the buttons
        self.exitButton.clicked.connect(self.on_exitButton_clicked)

        self.show()

    def on_exitButton_clicked(self):
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to exit ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()