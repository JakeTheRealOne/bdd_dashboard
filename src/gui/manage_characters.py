from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QTableWidget, QLabel, QPushButton, QSpacerItem, QSizePolicy, QTableWidgetItem, QMessageBox, QLineEdit, QFormLayout, QHeaderView
from PyQt5.QtCore import Qt
import mysql.connector

from . import qt_config

class ManageCharacters(QWidget):

    def __init__(self, parent, stackedWidget, ID):
        super().__init__(parent)
        self.stacked_widget = stackedWidget
        self.stacked_widget.addWidget(self)
        self.ID = ID
        self.db = mysql.connector.connect(
            host="localhost",
            user="rootuser",
            password="rootuser",
            database="rpg"
        )
        self.cursor = self.db.cursor()

        self.cursor.execute("SELECT p.Name FROM Players p WHERE ID = %s;", (self.ID,))
        result = self.cursor.fetchone()
        self.username = result[0]

        self.setup()


    def showEvent(self, event):
        super().showEvent(event)
        self.getCharactes()


    def setup(self):
        backButton = QPushButton("Back")
        backButton.setFixedWidth(500)
        backButton.setAutoDefault(True)

        addButton = QPushButton("Add Character")
        addButton.setFixedWidth(500)
        addButton.setAutoDefault(True)
        modifyButton = QPushButton("Modify Character")
        modifyButton.setFixedWidth(500)
        modifyButton.setAutoDefault(True)
        
        show_all_characters_button = QPushButton("Show All Characters")
        show_all_characters_button.setFixedWidth(500)
        show_all_characters_button.setAutoDefault(True)

        self.table = QTableWidget()
        self.table.setFixedSize(500, 250)

        self.nameInput = QLineEdit()
        self.nameInput.setMaxLength(255)
        self.nameInput.setFixedWidth(500)
        self.nameInput.setPlaceholderText("Name")
        self.nameInput.setAlignment(Qt.AlignCenter)
        self.strengthInput = QSpinBox()
        self.strengthInput.setMinimum(0)
        self.strengthInput.setMaximum(100)
        self.strengthInput.setAlignment(Qt.AlignCenter)
        self.agilityInput = QSpinBox()
        self.agilityInput.setMinimum(0)
        self.agilityInput.setMaximum(100)
        self.agilityInput.setAlignment(Qt.AlignCenter)
        self.intelligenceInput = QSpinBox()
        self.intelligenceInput.setMinimum(0)
        self.intelligenceInput.setMaximum(100)
        self.intelligenceInput.setAlignment(Qt.AlignCenter)
        self.healthInput = QSpinBox()
        self.healthInput.setMinimum(0)
        self.healthInput.setMaximum(100)
        self.healthInput.setAlignment(Qt.AlignCenter)
        self.manaInput = QSpinBox()
        self.manaInput.setMinimum(0)
        self.manaInput.setMaximum(100)
        self.manaInput.setAlignment(Qt.AlignCenter)
        self.classInput = QLineEdit()
        self.classInput.setMaxLength(255)
        self.classInput.setFixedWidth(500)
        self.classInput.setAlignment(Qt.AlignCenter)
        self.classInput.setPlaceholderText("Class")

        characterForm = QFormLayout()
        characterForm.addRow("", self.nameInput)
        characterForm.addRow("", self.classInput)

        formWidget = QWidget()
        formWidget.setLayout(characterForm)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        mainLayout.addWidget(qt_config.create_center_bold_title("Manage your Characters"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.table, alignment=Qt.AlignCenter)
        mainLayout.addWidget(formWidget, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Strength"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.strengthInput, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Agility"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.agilityInput, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Intelligence"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.intelligenceInput, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Health"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.healthInput, alignment=Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Mana"), alignment=Qt.AlignCenter)
        mainLayout.addWidget(self.manaInput, alignment=Qt.AlignCenter)
        mainLayout.addWidget(addButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(modifyButton, alignment=Qt.AlignCenter)
        mainLayout.addWidget(show_all_characters_button, alignment=Qt.AlignCenter)
        mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)

        backButton.clicked.connect(self.on_backButton_clicked)
        addButton.clicked.connect(self.on_addButton_clicked)
        modifyButton.clicked.connect(self.on_modifyButton_clicked)
        show_all_characters_button.clicked.connect(self.show_all_characters)


    def on_backButton_clicked(self):
        self.clearAll()
        self.stacked_widget.setCurrentIndex(0) # Go back to the main menu


    def clearAll(self):
        self.nameInput.clear()
        self.classInput.clear()
        self.strengthInput.setValue(0)
        self.agilityInput.setValue(0)
        self.intelligenceInput.setValue(0)
        self.healthInput.setValue(0)
        self.manaInput.setValue(0)


    def getCharactes(self):
        self.cursor.execute("SELECT * FROM Characters WHERE PlayerID = %s;", (self.ID,))
        result = self.cursor.fetchall()

        if not result:
            QMessageBox.information(self, "No character", "You don't have any character yet !")
            self.table.setRowCount(0)            
            return

        self.table.setRowCount(len(result))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Name", "Strength", "Agility", "Intelligence", "Health", "Mana", "Class"])

        for rowIdx, rowData in enumerate(result):
            for colIdx, value in enumerate(rowData):
                if colIdx >= 7:
                  continue

                item = QTableWidgetItem(str(value))

                if colIdx == 0:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                
                self.table.setItem(rowIdx, colIdx, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)


    def on_addButton_clicked(self):
        name = self.nameInput.text()
        strength = self.strengthInput.value()
        agility = self.agilityInput.value()
        intelligence = self.intelligenceInput.value()
        health = self.healthInput.value()
        mana = self.manaInput.value()
        classe = self.classInput.text()

        if not name and not classe:
                QMessageBox.warning(self, "Error", "Please fill in all fields!")

        # Insert the new character into the database
        else:
            self.cursor.execute("SELECT c.Name FROM Characters c WHERE c.PlayerID = %s AND c.Name = %s;", (self.ID, name))
            result = self.cursor.fetchone()
            if result:
                QMessageBox.warning(self, "Error", "You have already a Character with this name !")
                return

            self.cursor.execute(
                "INSERT INTO Characters (Name, Strength, Agility, Intelligence, Health, Mana, Class, PlayerID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                (name, strength, agility, intelligence, health, mana, classe, self.ID)
            )
            self.db.commit()
            QMessageBox.information(self, "Success", "Character added successfully!")
            self.getCharactes()


    def on_modifyButton_clicked(self):
        selectedRow = self.table.currentRow()

        if selectedRow != -1:  # Ensure a character is selected
            name = self.table.item(selectedRow, 0).text()
            strength = self.table.item(selectedRow, 1).text()
            agility = self.table.item(selectedRow, 2).text()
            intelligence = self.table.item(selectedRow, 3).text()
            health = self.table.item(selectedRow, 4).text()
            mana = self.table.item(selectedRow, 5).text()
            classe = self.table.item(selectedRow, 6).text()

            if not (name and strength and agility and intelligence and health and mana and classe):
                QMessageBox.warning(self, "Error", "Please fill in all fields!")
            
            elif not all(stat.isdigit() for stat in [strength, agility, intelligence, health, mana]):
                QMessageBox.warning(self, "Error", "Strength, Agility, Intelligence, Health and Mana must be numbers!")
            
            else:
                self.cursor.execute(
                    """UPDATE Characters SET 
                        Strength = %s, Agility = %s, Intelligence = %s, Health = %s, Mana = %s, Class = %s 
                        WHERE PlayerID = %s AND Name = %s;""",
                    (strength, agility, intelligence, health, mana, classe, self.ID, name)
                )
                self.db.commit()
                QMessageBox.information(self, "Success", "Character updated successfully!")
                self.getCharactes()

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

        for rowIdx, rowData in enumerate(result):
            for colIdx, value in enumerate(rowData):
                if colIdx >= 7:
                  continue

                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)


                # Username and name column is non-editable
                if colIdx == 0:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                
                self.table_characters.setItem(rowIdx, colIdx, item)

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
        classe = self.table_characters.item(row, 6).text()

        if not (name and strength and agility and intelligence and health and mana and classe):
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
        elif not all(stat.isdigit() for stat in [strength, agility, intelligence, health, mana]):
            QMessageBox.warning(self, "Error", "Strength, Agility, Intelligence, Health and Mana must be numbers!")
        else:
            self.cursor.execute("UPDATE Characters SET Strength = %s, Agility = %s, Intelligence = %s, Health = %s, Mana = %s, Class = %s WHERE PlayerID = %s AND Name = %s;", (strength, agility, intelligence, health, mana, classe, self.ID, name))
            self.db.commit()
            QMessageBox.information(self, "Success", "Character updated successfully!")
        