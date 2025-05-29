from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QAbstractItemView, QHeaderView, QLabel, QAbstractScrollArea, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector

from . import qt_config

class ManageQuests(QWidget):

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
        self.setup()
        
        
    def setup(self):
        back_button = QPushButton("Back")
        back_button.setFixedWidth(500)
        back_button.setAutoDefault(True)
        
        show_accepted_quests_button = QPushButton("Show Accepted Quests")
        show_accepted_quests_button.setFixedWidth(500)
        show_accepted_quests_button.setAutoDefault(True)

        self.quest_table = QTableWidget()
        self.quest_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.quest_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.quest_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.main_layout = QVBoxLayout()
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.main_layout.addWidget(qt_config.create_center_bold_title("Manage your Quests"), alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.quest_table)
        self.main_layout.addWidget(show_accepted_quests_button, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(back_button, alignment=Qt.AlignCenter)
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.setLayout(self.main_layout)
        
        self.display_all_quests()

        back_button.clicked.connect(self.on_back_button_clicked)
        show_accepted_quests_button.clicked.connect(self.show_accepted_quests)
        
        
    def on_back_button_clicked(self):
        self.stacked_widget.setCurrentIndex(0) # Go back to the main menu
        
        
    def display_all_quests(self):
        self.cursor.execute("SELECT Name, Description, Difficulty FROM Quests;")
        quests = self.cursor.fetchall()

        self.quest_table.setColumnCount(4)
        self.quest_table.setHorizontalHeaderLabels(["Name", "Description", "Difficulty", "Action"])
        self.quest_table.setRowCount(len(quests))
        header = self.quest_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Name
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Description
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Difficulty
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Action

        for row, (name, description, difficulty) in enumerate(quests):
            name_item = QTableWidgetItem(name)
            name_item.setTextAlignment(Qt.AlignCenter)
            self.quest_table.setItem(row, 0, name_item)
            
            desc_item = QTableWidgetItem(description)
            desc_item.setTextAlignment(Qt.AlignCenter)
            self.quest_table.setItem(row, 1, desc_item)

            item = QTableWidgetItem(str(difficulty))
            item.setTextAlignment(Qt.AlignCenter)
            self.quest_table.setItem(row, 2, item)

            accept_button = QPushButton("Accept")
            accept_button.clicked.connect(lambda _, quest=name: self.accept_quest(quest))
            self.quest_table.setCellWidget(row, 3, accept_button)
        
        self.main_layout.insertWidget(2, self.quest_table)


    def accept_quest(self, quest_name):
        self.cursor.execute("SELECT * FROM PlayerQuests p WHERE p.QuestName = %s AND p.PlayerID=%s;", (quest_name, self.id))
        quest = self.cursor.fetchone()
        if quest:
            QMessageBox.warning(self, "Quest Already Accepted", f"You have already accepted the quest: {quest_name}")
            return        
        
        self.cursor.execute("INSERT INTO PlayerQuests (PlayerID, QuestName) VALUES (%s, %s);", (self.id, quest_name))
        self.db.commit()
        
        QMessageBox.information(self, "Quest Accepted", f"You have accepted the quest: {quest_name}")
        
        
    def show_accepted_quests(self):
        if hasattr(self, 'showAcceptedQuestsWidget') and self.show_accepted_quests_widget is not None:
            self.stacked_widget.removeWidget(self.show_accepted_quests_widget)
            self.show_accepted_quests_widget.deleteLater()
            self.show_accepted_quests_widget = None
            
        self.show_accepted_quests_widget = QWidget()
        layout = QVBoxLayout()
        
        back_button = QPushButton("Back")
        back_button.setFixedWidth(500)
        back_button.setAutoDefault(True)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self))

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(qt_config.create_center_bold_title("Accepted Quests"), alignment=Qt.AlignCenter)
        
        self.cursor.execute("SELECT QuestName FROM PlayerQuests WHERE PlayerID = %s;", (self.id,))
        accepted_quests = self.cursor.fetchall()

        if accepted_quests:
            table = QTableWidget()
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            table.setRowCount(len(accepted_quests))
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Accepted Quests", "Validate", "Delete"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

            for row, (quest_name,) in enumerate(accepted_quests):
                table.setItem(row, 0, QTableWidgetItem(quest_name))
                
                validate_button = QPushButton("Validate")
                validate_button.clicked.connect(lambda _, quest_name=quest_name: self.validate_quest(quest_name))
                table.setCellWidget(row, 1, validate_button)
                
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, quest_name=quest_name: self.delete_quest(quest_name))
                table.setCellWidget(row, 2, delete_button)

            layout.addWidget(table, alignment=Qt.AlignCenter)
        else:
            layout.addWidget(QLabel("You have no accepted quests."), alignment=Qt.AlignCenter)

        layout.addWidget(back_button, alignment=Qt.AlignCenter)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.show_accepted_quests_widget.setLayout(layout)

        self.stacked_widget.addWidget(self.show_accepted_quests_widget)
        self.stacked_widget.setCurrentWidget(self.show_accepted_quests_widget)
        
        
    def validate_quest(self, quest_name):       
        self.cursor.execute("SELECT r.ItemName, r.Quantity FROM Rewards r WHERE r.QuestName = %s;", (quest_name,))
        rewards = self.cursor.fetchall()

        Or = 0
        items = []
        for item, quantity in rewards:
            for _ in range(quantity):
                if item == "Or":
                    self.cursor.execute("UPDATE Players SET Money = Money + 1 WHERE ID = %s;", (self.id,))
                    Or += 1
                else:
                    self.getInventory()        
                    index = self._next_free_item()
                    if index == len(self.inventory):
                        QMessageBox.warning(self, "Inventory Full", "Your inventory is full. Please clear some space.")
                        break
                    self.cursor.execute("INSERT INTO PlayerInventories (PlayerID, ItemName, SlotIDX) VALUES (%s, %s, %s);", (self.id, item, index))
                    self.inventory[index] = item
                    items.append(item)
      
        self.cursor.execute("DELETE FROM PlayerQuests WHERE PlayerID = %s AND QuestName = %s;", (self.id, quest_name))
        self.db.commit()
        
        if items:
            QMessageBox.information(self, "Quest Validated", f"You have successfully validated the quest: {quest_name}. You received {Or} gold and the items: {', '.join(items)}")

        else:
            QMessageBox.information(self, "Quest Validated", f"You have successfully validated the quest: {quest_name}. You received {Or} gold.")
        
        self.show_accepted_quests()


    def delete_quest(self, quest_name):
        self.cursor.execute("DELETE FROM PlayerQuests WHERE PlayerID = %s AND QuestName = %s;", (self.id, quest_name))
        self.db.commit()
        
        QMessageBox.information(self, "Quest Deleted", f"You have successfully deleted the quest: {quest_name}")
        
        self.show_accepted_quests()
            
            
    def getInventory(self):
        self.cursor.execute("SELECT InventorySlot FROM Players WHERE ID = %s;", (self.id,))
        inventory_slot = self.cursor.fetchone()[0]
        
        self.inventory = [None] * inventory_slot
        self.cursor.execute("SELECT * FROM PlayerInventories;")
        rows = self.cursor.fetchall()
              
        self.occupied_slots = 0

        for row in rows:
            if row[0] == self.id:
               self.inventory[row[2]] = row[1]
               self.occupied_slots += 1
            
            
    def _next_free_item(self):
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                return i
        return len(self.inventory)
