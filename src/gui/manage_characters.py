from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QTableWidget, QLabel, QPushButton, QSpacerItem, QSizePolicy, QTableWidgetItem, QMessageBox, QLineEdit, QFormLayout, QHeaderView
from PyQt5.QtCore import Qt
import mysql.connector

from . import qt_config

class ManageCharacters(QWidget):

    def __init__(self, parent, stacked_widget, id):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.stacked_widget.addWidget(self)
        self.id = id
        self.db = mysql.connector.connect(
            host="localhost",
            user="rootuser",
            password="rootuser",
            database="rpg"
        )
        self.cursor = self.db.cursor()

        self.cursor.execute("SELECT p.Name FROM Players p WHERE ID = %s;", (self.id,))
        result = self.cursor.fetchone()
        self.username = result[0]

        self.setup()


    def showEvent(self, event):
        super().showEvent(event)
        self.get_characters()


    def setup(self):
        back_button = QPushButton("Back")
        back_button.setFixedWidth(500)
        back_button.setAutoDefault(True)

        add_button = QPushButton("Add Character")
        add_button.setFixedWidth(500)
        add_button.setAutoDefault(True)
        modify_button = QPushButton("Modify Character")
        modify_button.setFixedWidth(500)
        modify_button.setAutoDefault(True)
        
        show_all_characters_button = QPushButton("Show All Characters")
        show_all_characters_button.setFixedWidth(500)
        show_all_characters_button.setAutoDefault(True)

        self.table = QTableWidget()
        self.table.setFixedSize(500, 250)

        self.name_input = QLineEdit()
        self.name_input.setMaxLength(255)
        self.name_input.setFixedWidth(500)
        self.name_input.setPlaceholderText("Name")
        self.name_input.setAlignment(Qt.AlignCenter)
        self.strength_input = QSpinBox()
        self.strength_input.setMinimum(0)
        self.strength_input.setMaximum(100)
        self.strength_input.setAlignment(Qt.AlignCenter)
        self.agility_input = QSpinBox()
        self.agility_input.setMinimum(0)
        self.agility_input.setMaximum(100)
        self.agility_input.setAlignment(Qt.AlignCenter)
        self.intelligence_input = QSpinBox()
        self.intelligence_input.setMinimum(0)
        self.intelligence_input.setMaximum(100)
        self.intelligence_input.setAlignment(Qt.AlignCenter)
        self.health_input = QSpinBox()
        self.health_input.setMinimum(0)
        self.health_input.setMaximum(100)
        self.health_input.setAlignment(Qt.AlignCenter)
        self.mana_input = QSpinBox()
        self.mana_input.setMinimum(0)
        self.mana_input.setMaximum(100)
        self.mana_input.setAlignment(Qt.AlignCenter)
        self.class_input = QLineEdit()
        self.class_input.setMaxLength(255)
        self.class_input.setFixedWidth(500)
        self.class_input.setAlignment(Qt.AlignCenter)
        self.class_input.setPlaceholderText("Class")

        character_form = QFormLayout()
        character_form.addRow("", self.name_input)
        character_form.addRow("", self.class_input)

        form_widget = QWidget()
        form_widget.setLayout(character_form)

        main_layout = QVBoxLayout()
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(qt_config.create_center_bold_title("Manage your Characters"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.table, alignment=Qt.AlignCenter)
        main_layout.addWidget(form_widget, alignment=Qt.AlignCenter)
        main_layout.addWidget(QLabel("Strength"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.strength_input, alignment=Qt.AlignCenter)
        main_layout.addWidget(QLabel("Agility"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.agility_input, alignment=Qt.AlignCenter)
        main_layout.addWidget(QLabel("Intelligence"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.intelligence_input, alignment=Qt.AlignCenter)
        main_layout.addWidget(QLabel("Health"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.health_input, alignment=Qt.AlignCenter)
        main_layout.addWidget(QLabel("Mana"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.mana_input, alignment=Qt.AlignCenter)
        main_layout.addWidget(add_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(modify_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(show_all_characters_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(back_button, alignment=Qt.AlignCenter)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)

        back_button.clicked.connect(self.on_back_button_clicked)
        add_button.clicked.connect(self.on_add_button_clicked)
        modify_button.clicked.connect(self.on_modify_button_clicked)
        show_all_characters_button.clicked.connect(self.show_all_characters)


    def on_back_button_clicked(self):
        self.clear_all()
        self.stacked_widget.setCurrentIndex(0) # Go back to the main menu


    def clear_all(self):
        self.name_input.clear()
        self.class_input.clear()
        self.strength_input.setValue(0)
        self.agility_input.setValue(0)
        self.intelligence_input.setValue(0)
        self.health_input.setValue(0)
        self.mana_input.setValue(0)


    def get_characters(self):
        self.cursor.execute("SELECT * FROM Characters WHERE PlayerID = %s;", (self.id,))
        result = self.cursor.fetchall()

        if not result:
            QMessageBox.information(self, "No character", "You don't have any character yet !")
            self.table.setRowCount(0)            
            return

        self.table.setRowCount(len(result))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Name", "Strength", "Agility", "Intelligence", "Health", "Mana", "Class"])

        for row_idx, row_data in enumerate(result):
            for col_idx, value in enumerate(row_data):
                if col_idx >= 7:
                  continue

                item = QTableWidgetItem(str(value))

                if col_idx == 0:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                self.table.setItem(row_idx, col_idx, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)


    def on_add_button_clicked(self):
        name = self.name_input.text()
        strength = self.strength_input.value()
        agility = self.agility_input.value()
        intelligence = self.intelligence_input.value()
        health = self.health_input.value()
        mana = self.mana_input.value()
        classe = self.class_input.text()

        if not name and not classe:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")

        # Insert the new character into the database
        else:
            self.cursor.execute("SELECT c.Name FROM Characters c WHERE c.PlayerID = %s AND c.Name = %s;", (self.id, name))
            result = self.cursor.fetchone()
            if result:
                QMessageBox.warning(self, "Error", "You have already a Character with this name !")
                return

            self.cursor.execute(
                "INSERT INTO Characters (Name, Strength, Agility, Intelligence, Health, Mana, Class, PlayerID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                (name, strength, agility, intelligence, health, mana, classe, self.id)
            )
            self.db.commit()
            QMessageBox.information(self, "Success", "Character added successfully!")
            self.get_characters()


    def on_modify_button_clicked(self):
        selected_row = self.table.currentRow()

        if selected_row != -1:  # Ensure a character is selected
            name = self.table.item(selected_row, 0).text()
            strength = self.table.item(selected_row, 1).text()
            agility = self.table.item(selected_row, 2).text()
            intelligence = self.table.item(selected_row, 3).text()
            health = self.table.item(selected_row, 4).text()
            mana = self.table.item(selected_row, 5).text()
            classe = self.table.item(selected_row, 6).text()

            if not (name and strength and agility and intelligence and health and mana and classe):
                QMessageBox.warning(self, "Error", "Please fill in all fields!")
            
            elif not all(stat.isdigit() for stat in [strength, agility, intelligence, health, mana]):
                QMessageBox.warning(self, "Error", "Strength, Agility, Intelligence, Health and Mana must be numbers!")
            
            else:
                self.cursor.execute(
                    """UPDATE Characters SET 
                        Strength = %s, Agility = %s, Intelligence = %s, Health = %s, Mana = %s, Class = %s 
                        WHERE PlayerID = %s AND Name = %s;""",
                    (strength, agility, intelligence, health, mana, classe, self.id, name)
                )
                self.db.commit()
                QMessageBox.information(self, "Success", "Character updated successfully!")
                self.get_characters()

        else:
            QMessageBox.warning(self, "No Selection", "Please select a character to modify.")
            
    
    def show_all_characters(self):
        self.cursor.execute("SELECT * FROM Characters;")
        result = self.cursor.fetchall()

        if not result:
            QMessageBox.information(self, "No character", "There is no character !")
            return
        
        
        if hasattr(self, 'show_show_all_characters') and self.show_show_all_characters is not None:
            self.stacked_widget.removeWidget(self.show_show_all_characters)
            self.show_show_all_characters.deleteLater()
            self.show_show_all_characters = None

        self.table_characters = QTableWidget()
        self.table_characters.setRowCount(len(result))
        self.table_characters.setColumnCount(7)
        self.table_characters.setHorizontalHeaderLabels(["Name", "Strength", "Agility", "Intelligence", "Health", "Mana", "Class"])
        self.table_characters.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for row_idx, row_data in enumerate(result):
            for col_idx, value in enumerate(row_data):
                if col_idx >= 7:
                  continue

                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)

                # Username and name column is non-editable
                if col_idx == 0:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                self.table_characters.setItem(row_idx, col_idx, item)

        header = self.table_characters.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        back_button = QPushButton("Back")
        back_button.setFixedWidth(500)
        back_button.setAutoDefault(True)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self))
        
        modify_button = QPushButton("Modify Character")
        modify_button.setFixedWidth(500)
        modify_button.setAutoDefault(True)
        modify_button.clicked.connect(self.modify_character)
        
        layout = QVBoxLayout()
        layout.addWidget(qt_config.create_center_bold_title("All Characters"))
        layout.addWidget(self.table_characters)
        layout.addWidget(modify_button, alignment=Qt.AlignCenter)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)
        
        self.show_show_all_characters = QWidget()
        self.show_show_all_characters.setLayout(layout)
        
        self.stacked_widget.addWidget(self.show_show_all_characters)
        self.stacked_widget.setCurrentWidget(self.show_show_all_characters)
        
        
    def modify_character(self):
        row = self.table_characters.currentRow()
        
        name = self.table_characters.item(row, 0).text()
        strength = self.table_characters.item(row, 1).text()
        agility = self.table_characters.item(row, 2).text()
        intelligence = self.table_characters.item(row, 3).text()
        health = self.table_characters.item(row, 4).text()
        mana = self.table_characters.item(row, 5).text()
        role = self.table_characters.item(row, 6).text()
        username = self.table_characters.item(row, 7).text()

        if not (name and strength and agility and intelligence and health and mana and role):
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
        elif not all(stat.isdigit() for stat in [strength, agility, intelligence, health, mana]):
            QMessageBox.warning(self, "Error", "Strength, Agility, Intelligence, Health and Mana must be numbers!")
        else:
            self.cursor.execute("UPDATE Characters SET Strength = %s, Agility = %s, Intelligence = %s, Health = %s, Mana = %s, Class = %s WHERE PlayerID = %s AND Name = %s;", (strength, agility, intelligence, health, mana, role, self.id, name))
            self.db.commit()
            QMessageBox.information(self, "Success", "Character updated successfully!")
