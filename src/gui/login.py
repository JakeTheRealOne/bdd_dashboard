from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QStackedWidget, QMessageBox, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
import mysql.connector

import gui.qt_config as qt_config
import gui.main_menu as main_menu

class Login(QWidget):
    """
    Login class to handle the login and registration of players.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = mysql.connector.connect(
            host="localhost",
            user="rootuser",
            password="rootuser",
            database="rpg"
        )
        self.cursor = self.db.cursor()
        self.setup()
    
    def __del__(self):
        self.cursor.close()
        self.db.close()

    def run(self):
        self.show()

    def setup(self):
        self.stackedWidget = QStackedWidget()
        self.mainPage = QWidget()
        self.loginPage = QWidget()
        self.registerPage = QWidget()

        self.exitButton = QPushButton("Exit")
        self.exitButton.setFixedWidth(500)
        self.loginButton = QPushButton("Login")
        self.loginButton.setFixedWidth(500)
        self.registerButton = QPushButton("Register")
        self.registerButton.setFixedWidth(500)
        self.backButtonLogin = QPushButton("Back")
        self.backButtonLogin.setFixedWidth(500)
        self.backButtonRegister = QPushButton("Back")
        self.backButtonRegister.setFixedWidth(500)

        self.sendButtonRegister = QPushButton("Send")
        self.sendButtonRegister.setFixedWidth(500)
        self.sendButtonLogin = QPushButton("Send")
        self.sendButtonLogin.setFixedWidth(500)

        self.usernameInputRegister = QLineEdit()
        self.usernameInputRegister.setFixedWidth(500)
        self.usernameInputRegister.setAlignment(Qt.AlignCenter)
        self.usernameInputLogin = QLineEdit()
        self.usernameInputLogin.setFixedWidth(500)
        self.usernameInputLogin.setAlignment(Qt.AlignCenter)


        # main page
        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.createCenterBoldTitle("Welcome to the RPG !"))
        mainLayout.addWidget(self.registerButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.loginButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.exitButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.mainPage.setLayout(mainLayout)

        # register page
        registerPageLayout = QVBoxLayout()
        registerPageLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        registerPageLayout.addWidget(qt_config.createCenterBoldTitle("Register"))
        registerPageLayout.addWidget(self.usernameInputRegister, alignment=Qt.AlignCenter)
        registerPageLayout.addWidget(self.sendButtonRegister, alignment=Qt.AlignCenter)
        registerPageLayout.addWidget(self.backButtonRegister, alignment=Qt.AlignCenter)
        registerPageLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.registerPage.setLayout(registerPageLayout)

        # login page
        loginPageLayout = QVBoxLayout()
        loginPageLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        loginPageLayout.addWidget(qt_config.createCenterBoldTitle("Login"))
        loginPageLayout.addWidget(self.usernameInputLogin, alignment=Qt.AlignCenter)
        loginPageLayout.addWidget(self.sendButtonLogin, alignment=Qt.AlignCenter)
        loginPageLayout.addWidget(self.backButtonLogin, alignment=Qt.AlignCenter)
        loginPageLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.loginPage.setLayout(loginPageLayout)

        # Add the pages to stackedWidget
        self.stackedWidget.addWidget(self.mainPage)
        self.stackedWidget.addWidget(self.registerPage)
        self.stackedWidget.addWidget(self.loginPage)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)

        # Connect buttons
        self.exitButton.clicked.connect(self.on_exitButton_clicked)
        self.loginButton.clicked.connect(self.on_loginButton_clicked)
        self.registerButton.clicked.connect(self.on_registerButton_clicked)
        self.backButtonLogin.clicked.connect(self.on_backButtonLogin_clicked)
        self.backButtonRegister.clicked.connect(self.on_backButtonRegister_clicked)
        self.sendButtonRegister.clicked.connect(self.on_sendButtonRegister_clicked)
        self.sendButtonLogin.clicked.connect(self.on_sendButtonLogin_clicked)
        self.usernameInputLogin.returnPressed.connect(self.on_sendButtonLogin_clicked)
        self.usernameInputRegister.returnPressed.connect(self.on_sendButtonRegister_clicked)

    def on_exitButton_clicked(self):
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to exit ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def on_loginButton_clicked(self):
        self.stackedWidget.setCurrentWidget(self.loginPage)

    def on_registerButton_clicked(self):
        self.stackedWidget.setCurrentWidget(self.registerPage)

    def on_backButtonLogin_clicked(self):
        self.clearInputs()
        self.stackedWidget.setCurrentWidget(self.mainPage)

    def on_backButtonRegister_clicked(self):
        self.clearInputs()
        self.stackedWidget.setCurrentWidget(self.mainPage)

    def on_sendButtonRegister_clicked(self):
        username = self.usernameInputRegister.text()

        # Check if name lenght is valid
        if not (0 < len(username) < 256):
            QMessageBox.warning(self, "Register failed", "Username length is invalid.")
            return

        # Check in db to not create 2 accounts with the same name
        self.cursor.execute("SELECT * FROM Players WHERE Name = ('"+ username +"');")
        result = self.cursor.fetchone()
        if result:
            QMessageBox.warning(self, "Register failed", "Username is already taken.")

        else:
            self.cursor.execute("INSERT INTO Players (Name) VALUES ('"+ username +"');")
            result = self.cursor.fetchone()
            if not result:
                self.db.commit()
                QMessageBox.information(self, "Register successful", "You have successfully registered.")
                self.stackedWidget.setCurrentWidget(self.loginPage)

        self.clearInputs()

    def on_sendButtonLogin_clicked(self):
        username = self.usernameInputLogin.text()

        # Check if name lenght is valid
        if not (0 < len(username) < 256):
            QMessageBox.warning(self, "Register failed", "Username length is invalid.")
            return

        self.cursor.execute("SELECT p.ID FROM Players p WHERE Name = ('"+ username +"');")
        result = self.cursor.fetchone()
        if result:
            self.db.commit()
            self.clearInputs()
            QMessageBox.information(self, "Login successful", "You have successfully logged in.")
            mainMenu = main_menu.MainMenu(result[0], self)
            self.stackedWidget.addWidget(mainMenu)
            self.stackedWidget.setCurrentWidget(mainMenu) # show the main menu

        else:
            self.clearInputs()
            QMessageBox.warning(self, "Login failed", "Username does not exist.")

    def clearInputs(self):
        self.usernameInputRegister.clear()
        self.usernameInputLogin.clear()
