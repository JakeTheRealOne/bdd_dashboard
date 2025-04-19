from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QAbstractItemView, QHeaderView, QLabel, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector

import gui.qt_config as qt_config

class ManageQuests(QWidget):
    """
    ManageAccount class to handle the management of player accounts.
    """

    def __init__(self, parent, stackedWidget, ID):
        super().__init__(parent)
        self.stackedWidget = stackedWidget
        self.stackedWidget.addWidget(self)
        self.ID = ID
        self.db = mysql.connector.connect(
            host="localhost",
            user="rootuser",
            password="rootuser",
            database="rpg"
        )
        self.cursor = self.db.cursor()
        self.setup()
        
        
    def setup(self):
        backButton = QPushButton("Back")
        backButton.setFixedWidth(500)
        backButton.setAutoDefault(True)
        
        showAcceptedQuestsButton = QPushButton("Show Accepted Quests")
        showAcceptedQuestsButton.setFixedWidth(500)
        showAcceptedQuestsButton.setAutoDefault(True)

        self.questTable = QTableWidget()
        self.questTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.mainLayout.addWidget(qt_config.createCenterBoldTitle("Manage your Quests"), alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(self.questTable, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(showAcceptedQuestsButton, alignment=Qt.AlignCenter)
        self.mainLayout.addWidget(backButton, alignment=Qt.AlignCenter)
        self.mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.setLayout(self.mainLayout)
        
        self.display_all_quests()

        backButton.clicked.connect(self.on_backButton_clicked)
        showAcceptedQuestsButton.clicked.connect(self.show_accepted_quests)
        
        
    def on_backButton_clicked(self):
        self.stackedWidget.setCurrentIndex(0) # Go back to the main menu
        
        
    def display_all_quests(self):
        self.cursor.execute("SELECT Name, Description, Difficulty FROM Quests")
        quests = self.cursor.fetchall()

        self.questTable.setColumnCount(4)
        self.questTable.setHorizontalHeaderLabels(["Name", "Description", "Difficulty", "Action"])
        self.questTable.setRowCount(len(quests))

        for row, (name, description, difficulty) in enumerate(quests):
            self.questTable.setItem(row, 0, QTableWidgetItem(name))
            self.questTable.setItem(row, 1, QTableWidgetItem(description))
            self.questTable.setItem(row, 2, QTableWidgetItem(str(difficulty)))

            acceptButton = QPushButton("Accept")
            acceptButton.clicked.connect(lambda _, quest=name: self.accept_quest(quest))
            self.questTable.setCellWidget(row, 3, acceptButton)
        
        self.questTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.mainLayout.insertWidget(2, self.questTable)  # On insère après le titre par exemple


    def accept_quest(self, quest_name):
        self.cursor.execute("SELECT * FROM PlayerQuests p WHERE p.QuestName = %s AND p.PlayerID=%s", (quest_name, self.ID))
        quest = self.cursor.fetchone()
        if quest:
            QMessageBox.warning(self, "Quest Already Accepted", f"You have already accepted the quest: {quest_name}")
            return        
        
        self.cursor.execute("INSERT INTO PlayerQuests (PlayerID, QuestName) VALUES (%s, %s)", (self.ID, quest_name))
        self.db.commit()
        
        QMessageBox.information(self, "Quest Accepted", f"You have accepted the quest: {quest_name}")
        
        
    def show_accepted_quests(self):
        if hasattr(self, 'showAcceptedQuestsWidget') and self.showAcceptedQuestsWidget is not None:
            self.stackedWidget.removeWidget(self.showAcceptedQuestsWidget)
            self.showAcceptedQuestsWidget.deleteLater()
            self.showAcceptedQuestsWidget = None
            
        self.showAcceptedQuestsWidget = QWidget()
        layout = QVBoxLayout()
        
        backButton = QPushButton("Back")
        backButton.setFixedWidth(500)
        backButton.setAutoDefault(True)
        backButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self))

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(qt_config.createCenterBoldTitle("Accepted Quests"), alignment=Qt.AlignCenter)
        
        self.cursor.execute("SELECT QuestName FROM PlayerQuests WHERE PlayerID = %s", (self.ID,))
        accepted_quests = self.cursor.fetchall()

        if accepted_quests:
            table = QTableWidget()
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            table.setRowCount(len(accepted_quests))
            table.setColumnCount(1)
            table.setHorizontalHeaderLabels(["Accepted Quests"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            for row, (quest_name,) in enumerate(accepted_quests):
                table.setItem(row, 0, QTableWidgetItem(quest_name))

            layout.addWidget(table, alignment=Qt.AlignCenter)
        else:
            layout.addWidget(QLabel("You have no accepted quests."), alignment=Qt.AlignCenter)

        layout.addWidget(backButton, alignment=Qt.AlignCenter)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.showAcceptedQuestsWidget.setLayout(layout)

        self.stackedWidget.addWidget(self.showAcceptedQuestsWidget)
        self.stackedWidget.setCurrentWidget(self.showAcceptedQuestsWidget)
        