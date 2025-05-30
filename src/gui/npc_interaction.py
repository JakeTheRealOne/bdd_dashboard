from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QHeaderView, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QLabel
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
        
        modify_button = QPushButton("Modify dialog")
        modify_button.setFixedWidth(500)
        modify_button.setAutoDefault(True)
        
        quest_button = QPushButton("NPC Quests")
        quest_button.setFixedWidth(500)
        quest_button.setAutoDefault(True)
        
        buy_sell_button = QPushButton("Buy/Sell items")
        buy_sell_button.setFixedWidth(500)
        buy_sell_button.setAutoDefault(True)
        
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(qt_config.create_center_bold_title("Interactions with NPCs"), alignment=Qt.AlignCenter)
        main_layout.addWidget(self.table)
        main_layout.addWidget(modify_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(quest_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(buy_sell_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(back_button, alignment=Qt.AlignCenter)
        
        self.setLayout(main_layout)
        
        back_button.clicked.connect(self.on_back_button_clicked)
        modify_button.clicked.connect(self.on_modify_button_clicked)
        quest_button.clicked.connect(self.on_quest_button_clicked)
        buy_sell_button.clicked.connect(self.on_buy_sell_button_clicked)
        
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
        layout.addWidget(qt_config.create_center_bold_title("NPC Quests"), alignment=Qt.AlignCenter)
            
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
                                
                                
    def on_buy_sell_button_clicked(self):
        row_selected = self.table.currentRow()
        name = ""
        if row_selected != -1:
            name = self.table.item(row_selected, 0).text()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a NPC to view to buy or sell items.")
            return
        
        if hasattr(self, 'show_buy_sell_item_widget') and self.show_buy_sell_item_widget is not None:
            self.stacked_widget.removeWidget(self.show_buy_sell_item_widget)
            self.show_buy_sell_item_widget.deleteLater()
            self.show_buy_sell_item_widget = None
        
        self.cursor.execute("SELECT * FROM NPCItemInventories WHERE NPCName = %s;", (name,))
        NPC_result_raw = self.cursor.fetchall()

        NPC_result = []
        for row in NPC_result_raw:
            self.cursor.execute("SELECT Price FROM Items WHERE Name = %s;", (row[1],))
            base_price = self.cursor.fetchone()[0]
            quantity = row[-1]
            total_price = base_price * quantity
            
            npc_name = row[0]
            item_name = row[1]
            
            NPC_result.append([npc_name, item_name, quantity, total_price])

        if not NPC_result:
            NPC_result = [(name, "No items available", "")]
        
        self.cursor.execute("SELECT ItemName, SlotIDX FROM PlayerInventories WHERE PlayerID = %s;", (self.ID,))
        player_result_raw = self.cursor.fetchall()

        if player_result_raw:
            player_result = []
            for row in player_result_raw:
                self.cursor.execute("SELECT Price FROM Items WHERE Name = %s;", (row[0],))
                price = self.cursor.fetchone()[0]            
                item_name = row[0]
                slot_idx = row[1]
                player_result.append([item_name, price, slot_idx])            
        else:
            player_result = [["No items available"]]
        
        back_button = QPushButton("Back")
        back_button.setFixedWidth(500)
        back_button.setAutoDefault(True)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self))
        
        NPC_table = QTableWidget()
        NPC_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        NPC_table.setWordWrap(True)
        NPC_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        NPC_table.setRowCount(len(NPC_result))
        NPC_table.setColumnCount(5)
        NPC_table.setHorizontalHeaderLabels(["NPC Name", "Item", "Quantity", "Price", "Action"])
        
        player_table = QTableWidget()
        player_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        player_table.setWordWrap(True)
        player_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        player_table.setRowCount(len(player_result))
        player_table.setColumnCount(3)
        player_table.setHorizontalHeaderLabels(["Item", "Price", "Action"])
        
        for row_idx, row_data in enumerate(NPC_result):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                
                NPC_table.setItem(row_idx, col_idx, item)
                
            buy_button = QPushButton("Buy")
            buy_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            buy_button.setAutoDefault(True)
            buy_button.clicked.connect(lambda _, r=row_data: self.buy_item(r[1], r[2], name))
            NPC_table.setCellWidget(row_idx, 4, buy_button) 
            
        for row_idx, row_data in enumerate(player_result):
            for col_idx, value in enumerate(row_data):
                if col_idx < 2: # Need only the first two columns, not the slot index
                    item = QTableWidgetItem(str(value))
                    item.setFlags(Qt.ItemIsEnabled)
                    item.setTextAlignment(Qt.AlignCenter)
                    player_table.setItem(row_idx, col_idx, item)
                
            sell_button = QPushButton("Sell")
            buy_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            sell_button.setAutoDefault(True)
            sell_button.clicked.connect(lambda _, r=row_data: self.sell_item(r[0], name, r[2]))
            
            if row_data[0] == "No items available":
                sell_button.setEnabled(False)
            player_table.setCellWidget(row_idx, 2, sell_button)

            
        header = NPC_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        
        header = player_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        
        self.show_buy_sell_item_widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(qt_config.create_center_bold_title("Buy or Sell items"), alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("NPC Items"), alignment=Qt.AlignCenter)
        layout.addWidget(NPC_table)
        layout.addWidget(QLabel("Player Items"), alignment=Qt.AlignCenter)
        layout.addWidget(player_table)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.show_buy_sell_item_widget.setLayout(layout)
        self.stacked_widget.addWidget(self.show_buy_sell_item_widget)
        self.stacked_widget.setCurrentWidget(self.show_buy_sell_item_widget)
        
    def buy_item(self, item_name, quantity, npc_name):
        self.cursor.execute("SELECT Price FROM Items WHERE Name = %s;", (item_name,))
        price = self.cursor.fetchone()

        self.cursor.execute("SELECT Money FROM Players WHERE ID = %s;", (self.ID,))
        money = self.cursor.fetchone()

        if price is None or money is None or money[0] < price[0] * int(quantity):
            QMessageBox.warning(self, "Not enough money", "You don't have enough money to buy this item.")
            return

        self.cursor.execute("DELETE FROM NPCItemInventories WHERE NPCName = %s AND ItemName = %s and Quantity = %s;", (npc_name, item_name, quantity))
        
        items = []
        for i in range(int(quantity)):
            self.getInventory()        
            index = self._next_free_item()
            if index == len(self.inventory):
                QMessageBox.warning(self, "Inventory Full", "Your inventory is full. Please clear some space.")
                self.db.commit()
                return
            self.cursor.execute("INSERT INTO PlayerInventories (PlayerID, ItemName, SlotIDX) VALUES (%s, %s, %s);", (self.ID, item_name, index))
            self.inventory[index] = item_name
            items.append(item_name)

        self.cursor.execute("UPDATE Players SET Money = Money - %s WHERE ID = %s;", (price[0] * int(quantity), self.ID))
        
        self.db.commit()
        self.on_buy_sell_button_clicked()
        QMessageBox.information(self, "Item Bought", f"You have bought the item: {item_name}")
        
    
    def sell_item(self, item, npc_name, slot_idx):
        self.cursor.execute("DELETE FROM PlayerInventories WHERE PlayerID = %s AND ItemName = %s AND SlotIDX = %s;", (self.ID, item, slot_idx))
        
        self.cursor.execute("SELECT * FROM NPCItemInventories WHERE NPCName = %s AND ItemName = %s;", (npc_name, item))
        result = self.cursor.fetchone()
        if result:
            new_quantity = result[2] + 1
            self.cursor.execute("UPDATE NPCItemInventories SET Quantity = %s WHERE NPCName = %s AND ItemName = %s;", (new_quantity, npc_name, item))
        else:    
            self.cursor.execute("INSERT INTO NPCItemInventories (NPCName, ItemName, Quantity) VALUES (%s, %s, %s);", (npc_name, item, 1))
            
        self.cursor.execute("SELECT Price FROM Items WHERE Name = %s;", (item,))
        price = self.cursor.fetchone()
        if price is None:
            QMessageBox.warning(self, "Error", "Item not found in the database.")
            return
        
        self.cursor.execute("UPDATE Players SET Money = Money + %s WHERE ID = %s;", (price[0], self.ID))


        self.db.commit()
        self.on_buy_sell_button_clicked()
        QMessageBox.information(self, "Item Sold", f"You have sold the item: {item}")
        
        
    def _next_free_item(self):
        for i in range(len(self.inventory)):
            if self.inventory[i] is None:
                return i
        return len(self.inventory)
    
    
    def getInventory(self):
        self.cursor.execute("SELECT InventorySlot FROM Players WHERE ID = %s;", (self.ID,))
        inventorySlot = self.cursor.fetchone()[0]
        
        self.inventory = [None] * inventorySlot
        self.cursor.execute("SELECT * FROM PlayerInventories;")
        rows = self.cursor.fetchall()
              
        self.occuped_slots = 0

        for row in rows:
            if row[0] == self.ID:
               self.inventory[row[2]] = row[1]
               self.occuped_slots += 1