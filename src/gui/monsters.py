from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QAbstractItemView, QHeaderView, QScrollArea, QAbstractScrollArea, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import mysql.connector

from . import qt_config

class Monsters(QWidget):

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
        
        self.monsters_table = QTableWidget()
        self.monsters_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.monsters_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.monsters_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)


        scroll_area = QScrollArea()
        scroll_area.setWidget(self.monsters_table)
        scroll_area.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(qt_config.create_center_bold_title("Monsters"), alignment=Qt.AlignCenter)
        main_layout.addWidget(scroll_area, alignment=Qt.AlignCenter)
        main_layout.addWidget(back_button, alignment=Qt.AlignCenter)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.setLayout(main_layout)
        
        back_button.clicked.connect(self.on_back_button_clicked)
        
        self.display_all_monsters()
        
        
    def on_back_button_clicked(self):
        self.stacked_widget.setCurrentIndex(0)
        
        
    def display_all_monsters(self):
        self.cursor.execute("SELECT * FROM Monsters")
        monsters = self.cursor.fetchall()

        self.monsters_table.setRowCount(len(monsters))
        self.monsters_table.setColumnCount(4)
        self.monsters_table.setHorizontalHeaderLabels(["Name", "Damage", "Health", "Defence"])

        for i, monster in enumerate(monsters):
            for j, value in enumerate(monster):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignCenter)
                self.monsters_table.setItem(i, j, item)
                
        header = self.monsters_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.monsters_table.cellClicked.connect(self.show_monster_loot)


    def show_monster_loot(self, row):
        if hasattr(self, 'show_monster_loot_widget') and self.show_monster_loot_widget is not None:
            self.stacked_widget.removeWidget(self.show_monster_loot_widget)
            self.show_monster_loot_widget.deleteLater()
            self.show_monster_loot_widget = None
            
        self.show_monster_loot_widget = QWidget()
        layout = QVBoxLayout()
        
        back_button = QPushButton("Back")
        back_button.setFixedWidth(500)
        back_button.setAutoDefault(True)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self))
        
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(qt_config.create_center_bold_title("Monster Loots"), alignment=Qt.AlignCenter)
        
        monster = self.monsters_table.item(row, 0)
        
        self.cursor.execute("SELECT * FROM MonsterLoots WHERE MonsterName = %s", (monster.text(),))
        results = self.cursor.fetchall()
                
        if results:
            table = QTableWidget()
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            table.setRowCount(len(results))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["Monster Name", "Loot Name", "Drop Rate", "Quantity"])
            
            for row, (name, loot, drop, quant) in enumerate(results):                       
                monster_name = QTableWidgetItem(name)
                monster_name.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 0, monster_name)
                
                loot_name = QTableWidgetItem(loot)
                loot_name.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 1, loot_name)
                
                drop_rate = QTableWidgetItem(str(drop) + "%")
                drop_rate.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 2, drop_rate)
                
                quantity = QTableWidgetItem(str(quant))
                quantity.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 3, quantity)
                
            header = table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)       
            layout.addWidget(table, alignment=Qt.AlignCenter)
                
        else:
            no_loot_label = QLabel("No loot available for this monster.")
            no_loot_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_loot_label, alignment=Qt.AlignCenter)
            
        layout.addWidget(back_button, alignment=Qt.AlignCenter)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.show_monster_loot_widget.setLayout(layout)

        self.stacked_widget.addWidget(self.show_monster_loot_widget)
        self.stacked_widget.setCurrentWidget(self.show_monster_loot_widget)
            