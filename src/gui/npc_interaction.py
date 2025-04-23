from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QHeaderView, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import mysql.connector

from . import qt_config

class NPCInteraction(QWidget):

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
        self.setup()
        
        
    def setup(self):
        back_button = QPushButton("Back")
        back_button.setFixedWidth(500)
        back_button.setAutoDefault(True)
        
        modify_button = QPushButton("Modify")
        modify_button.setFixedWidth(500)
        modify_button.setAutoDefault(True)
        
        quest_button = QPushButton("NPC Quests")
        quest_button.setFixedWidth(500)
        quest_button.setAutoDefault(True)
        
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(qt_config.create_center_bold_title("Interactions with NPCs"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.table)
        main_layout.addWidget(modify_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(quest_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(back_button, alignment=Qt.AlignCenter)
        
        self.setLayout(main_layout)
        
        back_button.clicked.connect(self.on_back_button_clicked)
        modify_button.clicked.connect(self.on_modify_button_clicked)
        quest_button.clicked.connect(self.on_quest_button_clicked)
        
        self.get_NPCs()
                
        
    def on_back_button_clicked(self):
        self.stacked_widget.setCurrentIndex(0)
        
        
    def get_NPCs(self):
        self.cursor.execute("SELECT * FROM NPCs;")
        result = self.cursor.fetchall()
        
        self.table.setRowCount(len(result))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["NPC Name", "Dialog"])
        
        for row_idx, row_data in enumerate(result):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)

                # NPC Name column is non-editable
                if col_idx == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                else:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
                
                self.table.setItem(row_idx, col_idx, item)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        
    def on_modify_button_clicked(self):
        row_selected = self.table.currentRow()

        if row_selected != -1:  # Ensure a character is selected
            name = self.table.item(row_selected, 0).text()
            dialog = self.table.item(row_selected, 1).text()

            if not dialog:
                QMessageBox.warning(self, "Error", "Please fill in the dialog!")
            
            else:
                self.cursor.execute(
                    """UPDATE NPCs SET Dialog = %s WHERE Name = %s;""",
                    (dialog, name)
                )
                self.db.commit()
                QMessageBox.information(self, "Success", "NPC updated successfully!")
                self.get_NPCs()

        else:
            QMessageBox.warning(self, "No Selection", "Please select a NPC to modify the dialog.")
            
            
    def on_quest_button_clicked(self):
        row_selected = self.table.currentRow()
        name = ""
        if row_selected != -1:
            name = self.table.item(row_selected, 0).text()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a NPC to view the quest.")
            return
        
        if hasattr(self, 'show_npc_quest_widget') and self.show_npc_quest_widget is not None:
            self.stacked_widget.removeWidget(self.show_npc_quest_widget)
            self.show_npc_quest_widget.deleteLater()
            self.show_npc_quest_widget = None
            
        self.show_npc_quest_widget = QWidget()
        layout = QVBoxLayout()
        
        back_button = QPushButton("Back")
        back_button.setFixedWidth(500)
        back_button.setAutoDefault(True)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self))
        
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(qt_config.create_center_bold_title("Monster Loots"), alignment=Qt.AlignCenter)
            
        self.cursor.execute("SELECT * FROM NPCQuests WHERE NPCName = %s;", (name,))
        result = self.cursor.fetchall()
        if not result:
            QMessageBox.warning(self, "No Quests", "This NPC has no quests.")
            return
        
        table = QTableWidget()
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setWordWrap(True)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setRowCount(len(result))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["NPC Name", "Quest", "Action"])
        
        for row_idx, row_data in enumerate(result):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                
                table.setItem(row_idx, col_idx, item)
                
            accept_button = QPushButton("Accept Quest")
            accept_button.setFixedWidth(200)
            accept_button.setAutoDefault(True)
            accept_button.clicked.connect(lambda _, r=row_idx: self.accept_quest(result[r][1]))
            table.setCellWidget(row_idx, 2, accept_button)
                
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        layout.addWidget(table)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.show_npc_quest_widget.setLayout(layout)
        self.stacked_widget.addWidget(self.show_npc_quest_widget)
        self.stacked_widget.setCurrentWidget(self.show_npc_quest_widget)
        
        
    def accept_quest(self, quest_name):
        self.cursor.execute("SELECT * FROM PlayerQuests p WHERE p.QuestName = %s AND p.PlayerID=%s;", (quest_name, self.ID))
        quest = self.cursor.fetchone()
        if quest:
            QMessageBox.warning(self, "Quest Already Accepted", f"You have already accepted the quest: {quest_name}")
            return        
        
        self.cursor.execute("INSERT INTO PlayerQuests (PlayerID, QuestName) VALUES (%s, %s);", (self.ID, quest_name))
        self.db.commit()
        
        QMessageBox.information(self, "Quest Accepted", f"You have accepted the quest: {quest_name}")
                                