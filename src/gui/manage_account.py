from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QPushButton, QMessageBox, QApplication, QLabel, QSpacerItem, QSizePolicy, QLineEdit
from PyQt5.QtCore import Qt
import mysql.connector

from . import qt_config

class ManageAccount(QWidget):

    def __init__(self, parent, stacked_widget, id):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.id = id
        self.db = mysql.connector.connect(
            host="localhost",
            user="rootuser",
            password="rootuser",
            database="rpg"
        )
        self.cursor = self.db.cursor()
        self.getInfoPlyers()
        self.setup()

    def __del__(self):
        self.cursor.close()
        self.db.close()
    
    def getInfoPlyers(self):
        self.cursor.execute("SELECT * FROM Players WHERE ID = %s", (self.id,))
        result = self.cursor.fetchone()
        self.name = result[1]
        self.level = result[2]
        self.xp = result[3]
        self.money = result[4]
        self.inventory_slot = result[5]

    def setup(self):
        back_button = QPushButton("Back")
        back_button.setFixedWidth(500)
        back_button.setAutoDefault(True)

        delete_account_button = QPushButton("Delete Account")
        delete_account_button.setFixedWidth(500)
        delete_account_button.setAutoDefault(True)

        self.input_name = QLineEdit()
        self.input_name.setFixedWidth(500)
        self.input_name.setPlaceholderText("A new name")
        self.input_name.setAlignment(Qt.AlignCenter)
        self.input_name.setMaxLength(255)
        
        self.input_level = QSpinBox()
        self.input_level.setMinimum(0)
        self.input_level.setMaximum(100000000)
        self.input_level.setValue(self.level)

        self.input_xp = QSpinBox()
        self.input_xp.setMinimum(0)
        self.input_xp.setMaximum(100000000)
        self.input_xp.setValue(self.xp)

        self.input_money = QSpinBox()
        self.input_money.setMinimum(0)
        self.input_money.setMaximum(100000000)
        self.input_money.setValue(self.money)

        self.name_label = QLabel(f"Hello <u>{self.name}</u> with the ID <u>{self.id}</u> !")
        self.inventory_label = QLabel(f"Inventory Slot : <u>{self.inventory_slot}</u>")

        main_layout = QVBoxLayout()
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(qt_config.create_center_bold_title("Manage Account"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.name_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(QLabel("Here is your account info :"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.input_name, alignment=Qt.AlignCenter)
        main_layout.addWidget(QLabel("Change your level :"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.input_level, alignment=Qt.AlignCenter)
        main_layout.addWidget(QLabel("Change your XP :"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.input_xp, alignment=Qt.AlignCenter)
        main_layout.addWidget(QLabel("Change your money :"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.input_money, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.inventory_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(delete_account_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(back_button, alignment=Qt.AlignCenter)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)

        # connect the buttons
        back_button.clicked.connect(self.on_back_button_clicked)
        delete_account_button.clicked.connect(self.delete_account)
        self.input_name.returnPressed.connect(self.on_change_account_button_clicked)
        self.input_level.valueChanged.connect(self.on_change_account_button_clicked)
        self.input_xp.valueChanged.connect(self.on_change_account_button_clicked)
        self.input_money.valueChanged.connect(self.on_change_account_button_clicked)

        back_button.setFocus()

    def on_back_button_clicked(self):
        self.stacked_widget.setCurrentIndex(0) # Go back to the main menu

    def delete_account(self):
        reply = QMessageBox.question(self, "Quit", "Are you sure you delete your account ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM Characters WHERE Username = %s", (self.name,))
            self.cursor.execute("DELETE FROM Players WHERE ID = %s", (self.id,))
            self.db.commit()
            QApplication.quit()

    def on_change_account_button_clicked(self):
        new_name = self.input_name.text()
        new_level = self.input_level.value()
        new_xp = self.input_xp.value()
        new_money = self.input_money.value()

        if not new_name:
            new_name = self.name

        new_inventory_slot = 5 + min(27, 2 * new_level)
        self.inventory_slot = new_inventory_slot

        # Update the account info in the database
        try:
          self.cursor.execute("UPDATE Players SET Name = %s, Level = %s, XP = %s, Money = %s, InventorySlot = %s WHERE ID = %s", (new_name, new_level, new_xp, new_money, new_inventory_slot, self.id))
          self.db.commit()
        except mysql.connector.errors.IntegrityError:
          reply = QMessageBox.critical(self, "Error", "One or more entries are invalid.")
          raise
        except: 
          pass

        self.cursor.execute("DELETE FROM PlayerInventories WHERE PlayerID = %s AND SlotIDX >= %s", (self.ID, self.inventorySlot))
        self.db.commit()

        self.getInfoPlyers()
        self.name_label.setText(f"Hello <u>{self.name}</u> with the ID <u>{self.id}<u/> !")
        self.inventory_label.setText(f"Inventory Slot : <u>{self.inventory_slot}</u>")
