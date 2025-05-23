from PyQt5.QtWidgets import (
    QWidget,
    QHeaderView,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QLineEdit,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent, QBrush, QColor, QFont
import mysql.connector

from . import qt_config


class AddObject(QWidget):
    """
    Allows user to set name and property for a new object in the database
    """

    def __init__(self, parent, stackedWidget, ID):
        super().__init__(parent)
        self.stackedWidget = stackedWidget
        self.ID = ID
        self.db = mysql.connector.connect(
            host="localhost", user="rootuser", password="rootuser", database="rpg"
        )
        self.db.start_transaction(isolation_level="READ COMMITTED")
        self.cursor = self.db.cursor()
        self.setup()

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def setup(self):
        backButton = QPushButton("Back")
        backButton.setFixedWidth(300)
        backButton.setAutoDefault(True)

        confirmButton = QPushButton("Confirm")
        confirmButton.setFixedWidth(300)
        confirmButton.setAutoDefault(True)

        self.type_combo = QComboBox()
        self.type_combo.setFixedWidth(300)
        self.type_combo.addItem("Arme")
        self.type_combo.addItem("Armure")
        self.type_combo.addItem("Potion")
        self.type_combo.addItem("Artefact")
        self.property_field = QLineEdit()
        self.property_label = QLabel("property")
        self.property_field.setFixedWidth(300)
        self.price_field = QLineEdit()
        self.price_label = QLabel("price")
        self.price_field.setFixedWidth(300)
        self.name_field = QLineEdit()
        self.name_label = QLabel("name")
        self.name_field.setFixedWidth(300)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        mainLayout.addWidget(
            qt_config.create_center_bold_title("Add an object"),
            alignment=Qt.AlignCenter,
        )
        mainLayout.addWidget(
            QLabel("Be careful: adding an object is permanent"),
            alignment=Qt.AlignCenter,
        )
        mainLayout.addWidget(self.type_combo, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.name_label, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.name_field, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.property_label, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.property_field, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.price_label, alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.price_field, alignment=Qt.AlignCenter)
        mainLayout.addWidget(confirmButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.setLayout(mainLayout)

        # connect buttons
        self.type_combo.currentTextChanged.connect(self.update_type)
        self.name_field.textChanged.connect(self.reset_name_error)
        self.property_field.textChanged.connect(self.reset_property_error)
        self.price_field.textChanged.connect(self.reset_price_error)
        backButton.clicked.connect(self.on_backButton_clicked)
        confirmButton.clicked.connect(self.on_confirmButton_clicked)

    def update_type(self, new_type: str):
        self.reset_name_error()
        self.reset_property_error()
        self.reset_price_error()
        self.type_combo.setCurrentText(new_type)
        self.property_field.setText("")
        self.name_field.setText("")
        self.price_field.setText("")
        if new_type == "Artefact":
            self.property_field.setText("Effet: ")

    def reset_name_error(self):
        self.name_field.setStyleSheet("border: 2px solid transparent;")
        self.name_label.setStyleSheet("color: black;")
        self.name_label.setText("name")

    def reset_property_error(self):
        self.property_field.setStyleSheet("border: 2px solid transparent;")
        self.property_label.setStyleSheet("color: black;")
        self.property_label.setText("property")

    def reset_price_error(self):
        self.price_field.setStyleSheet("border: 2px solid transparent;")
        self.price_label.setStyleSheet("color: black;")
        self.price_label.setText("price")

    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.count() - 1)

    def on_confirmButton_clicked(self):
        # 1. retrieve datas

        name = self.name_field.text()
        prop = self.property_field.text()
        price = self.price_field.text()
        tp = self.type_combo.currentText()

        # 2. check if the datas are valid

        property_error_msg = "unknown"
        property_value = 0
        name_error_msg = "unknown"
        price_value = 0
        price_error_msg = "unknown"
        is_name_valid = True
        is_property_valid = True
        is_price_valid = True
        is_db_passed = True

        if not len(name):
            is_name_valid = False
            name_error_msg = "is empty"
        elif self._exists_in_db(name):
            is_name_valid = False
            name_error_msg = "two items can't have the same name"

        try:
            if tp == "Arme" or tp == "Armure":
                property_value = int(prop)
                if property_value < 0:
                    is_property_valid = False
                    property_error_msg = "can't be negative"
            else:
                property_value = prop
        except:
            is_property_valid = False
            property_error_msg = "invalid format"

        try:
            price_value = int(price)
        except:
            is_price_valid = False
            price_error_msg = "invalid format"
        if price_value <= 0:
            is_price_valid = False
            price_error_msg = "can't be negative"

        # 3. If valid: update in db and leave, else show error message
        try:
            if is_name_valid and is_property_valid and is_price_valid:
                valide_types = ["Arme", "Armure", "Artefact", "Potion"]
                self._insert(name, property_value, price_value, tp)
                self.on_backButton_clicked()
        except:
            is_db_passed = False
            raise

        if not is_name_valid or not is_db_passed:
            self.name_field.setStyleSheet("border: 2px solid #D64F4F;")
            self.name_label.setStyleSheet("color: #B52121;")
            self.name_label.setText("name - " + name_error_msg)
        if not is_property_valid or not is_db_passed:
            self.property_field.setStyleSheet("border: 2px solid #D64F4F;")
            self.property_label.setStyleSheet("color: #B52121;")
            self.property_label.setText("property - " + property_error_msg)
        if not is_price_valid or not is_db_passed:
            self.price_field.setStyleSheet("border: 2px solid #D64F4F;")
            self.price_label.setStyleSheet("color: #B52121;")
            self.price_label.setText("price - " + price_error_msg)

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)

    def _exists_in_db(self, object_name: str) -> bool:
        """
        Check if an item exists in the database
        """
        self.cursor.execute(
            "SELECT 1 FROM Items WHERE Name = %s LIMIT 1", (object_name,)
        )
        return self.cursor.fetchone() is not None

    def _insert(self, name: str, prop, price: int, tp: str) -> bool:
        """
        Insert an item in the database
        """
        self.cursor.execute(
            "INSERT INTO Items (Name, Price, Type) VALUES (%s, %s, %s)",
            (name, price, tp),
        )
        table = (
            "Weapons"
            if tp == "Arme"
            else (
                "Armors"
                if tp == "Armure"
                else "Artefacts" if tp == "Artefact" else "Potions"
            )
        )
        prop_name = (
            "Power"
            if tp == "Arme"
            else (
                "Defence"
                if tp == "Armure"
                else "Effect" if tp == "Artefact" else "Boost"
            )
        )
        query = f"INSERT INTO `{table}` (Name, `{prop_name}`) VALUES (%s, %s)"
        self.cursor.execute(query, (name, prop))
        self.db.commit()
