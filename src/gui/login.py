from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QStackedWidget, QMessageBox, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
import mysql.connector

from . import qt_config
from . import main_menu

class Login(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.showMaximized()
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
        self.stacked_widget = QStackedWidget()
        self.main_page = QWidget()
        self.login_page = QWidget()
        self.register_page = QWidget()

        exit_button = QPushButton("Exit")
        exit_button.setFixedWidth(500)
        exit_button.setAutoDefault(True)
        login_button = QPushButton("Login")
        login_button.setFixedWidth(500)
        login_button.setAutoDefault(True)
        register_button = QPushButton("Register")
        register_button.setFixedWidth(500)
        register_button.setAutoDefault(True)
        back_button_login = QPushButton("Back")
        back_button_login.setFixedWidth(500)
        back_button_login.setAutoDefault(True)
        back_button_register = QPushButton("Back")
        back_button_register.setFixedWidth(500)
        back_button_register.setAutoDefault(True)

        send_button_register = QPushButton("Send")
        send_button_register.setFixedWidth(500)
        send_button_register.setAutoDefault(True)
        send_button_login = QPushButton("Send")
        send_button_login.setAutoDefault(True)
        send_button_login.setFixedWidth(500)

        self.username_input_register = QLineEdit()
        self.username_input_register.setFixedWidth(500)
        self.username_input_register.setAlignment(Qt.AlignCenter)
        self.username_input_login = QLineEdit()
        self.username_input_login.setFixedWidth(500)
        self.username_input_login.setAlignment(Qt.AlignCenter)


        # main page
        main_layout = QVBoxLayout()
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(qt_config.create_center_bold_title("Welcome to the RPG !"))
        main_layout.addWidget(register_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(login_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(exit_button, alignment=Qt.AlignCenter)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.main_page.setLayout(main_layout)

        # register page
        register_page_layout = QVBoxLayout()
        register_page_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        register_page_layout.addWidget(qt_config.create_center_bold_title("Register"))
        register_page_layout.addWidget(self.username_input_register, alignment=Qt.AlignCenter)
        register_page_layout.addWidget(send_button_register, alignment=Qt.AlignCenter)
        register_page_layout.addWidget(back_button_register, alignment=Qt.AlignCenter)
        register_page_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.register_page.setLayout(register_page_layout)

        # login page
        login_page_layout = QVBoxLayout()
        login_page_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        login_page_layout.addWidget(qt_config.create_center_bold_title("Login"))
        login_page_layout.addWidget(self.username_input_login, alignment=Qt.AlignCenter)
        login_page_layout.addWidget(send_button_login, alignment=Qt.AlignCenter)
        login_page_layout.addWidget(back_button_login, alignment=Qt.AlignCenter)
        login_page_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.login_page.setLayout(login_page_layout)

        # Add the pages to stacked_widget
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.login_page)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Connect buttons
        exit_button.clicked.connect(self.on_exit_button_clicked)
        login_button.clicked.connect(self.on_login_button_clicked)
        register_button.clicked.connect(self.on_register_button_clicked)
        back_button_login.clicked.connect(self.on_back_button_login_clicked)
        back_button_register.clicked.connect(self.on_back_button_register_clicked)
        send_button_register.clicked.connect(self.on_send_button_register_clicked)
        send_button_login.clicked.connect(self.on_send_button_login_clicked)
        self.username_input_login.returnPressed.connect(self.on_send_button_login_clicked)
        self.username_input_register.returnPressed.connect(self.on_send_button_register_clicked)

    def on_exit_button_clicked(self):
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to exit ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def on_login_button_clicked(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def on_register_button_clicked(self):
        self.stacked_widget.setCurrentWidget(self.register_page)

    def on_back_button_login_clicked(self):
        self.clear_inputs()
        self.stacked_widget.setCurrentWidget(self.main_page)

    def on_back_button_register_clicked(self):
        self.clear_inputs()
        self.stacked_widget.setCurrentWidget(self.main_page)

    def on_send_button_register_clicked(self):
        username = self.username_input_register.text()

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
                self.stacked_widget.setCurrentWidget(self.login_page)
                self.username_input_login.setFocus()

        self.clear_inputs()

    def on_send_button_login_clicked(self):
        username = self.username_input_login.text()

        # Check if name lenght is valid
        if not (0 < len(username) < 256):
            QMessageBox.warning(self, "Register failed", "Username length is invalid.")
            return

        self.cursor.execute("SELECT p.ID FROM Players p WHERE Name = ('"+ username +"');")
        result = self.cursor.fetchone()
        if result:
            self.db.commit()
            self.clear_inputs()
            QMessageBox.information(self, "Login successful", "You have successfully logged in.")
            mainMenu = main_menu.MainMenu(result[0], self)
            self.stacked_widget.addWidget(mainMenu)
            self.stacked_widget.setCurrentWidget(mainMenu) # show the main menu

        else:
            self.clear_inputs()
            QMessageBox.warning(self, "Login failed", "Username does not exist.")
            self.username_input_login.setFocus()

    def clear_inputs(self):
        self.username_input_register.clear()
        self.username_input_login.clear()
