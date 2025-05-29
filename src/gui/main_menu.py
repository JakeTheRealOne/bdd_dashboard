from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget, QMessageBox, QApplication, QSpacerItem, QSizePolicy, QTextEdit, QLabel
from PyQt5.QtCore import Qt

import src.database.additional_request as additional_request

from . import qt_config
from . import manage_account
from . import manage_characters
from . import manage_inventory
from . import manage_quests
from . import manage_objects
from . import monsters
from . import ranking
from . import npc_interaction

class MainMenu(QWidget):

    def __init__(self, id, parent=None):
        super().__init__(parent)
        self.showMaximized()
        self.id = id
        self.setup()
        

    def setup(self):
        self.stacked_widget = QStackedWidget()

        manage_account_button = QPushButton("Manage Account")
        manage_account_button.setFixedWidth(500)
        manage_account_button.setAutoDefault(True)
        manage_characters_button = QPushButton("Manage Characters")
        manage_characters_button.setFixedWidth(500)
        manage_characters_button.setAutoDefault(True)
        manage_inventory_button = QPushButton("Manage inventory")
        manage_inventory_button.setFixedWidth(500)
        manage_inventory_button.setAutoDefault(True)
        manage_quests_button = QPushButton("Manage Quests")
        manage_quests_button.setFixedWidth(500)
        manage_quests_button.setAutoDefault(True)
        manage_monsters_button = QPushButton("Check Monsters")
        manage_monsters_button.setFixedWidth(500)
        manage_monsters_button.setAutoDefault(True)
        interaction_NPC_button = QPushButton("Interactions with NPCs")
        interaction_NPC_button.setFixedWidth(500)
        interaction_NPC_button.setAutoDefault(True)
        manage_objects_button = QPushButton("Manage Objects")
        manage_objects_button.setFixedWidth(500)
        manage_objects_button.setAutoDefault(True)
        ranking_button = QPushButton("Ranking")
        ranking_button.setFixedWidth(500)
        ranking_button.setAutoDefault(True)
        manage_additional_requests_button = QPushButton("Additional Requests")
        manage_additional_requests_button.setFixedWidth(500)
        manage_additional_requests_button.setAutoDefault(True)
        exit_button = QPushButton("Exit")
        exit_button.setFixedWidth(500)
        exit_button.setAutoDefault(True)

        main_layout = QVBoxLayout()
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(qt_config.create_center_bold_title("Welcome to the Main Menu"), alignment=Qt.AlignCenter)
        main_layout.addWidget(manage_account_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(manage_characters_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(manage_inventory_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(manage_quests_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(manage_monsters_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(manage_objects_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(interaction_NPC_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(ranking_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(manage_additional_requests_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(exit_button, alignment=Qt.AlignCenter)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.main_page = QWidget()
        self.main_page.setLayout(main_layout)
        self.stacked_widget.addWidget(self.main_page)

        self.stacked_widget.setCurrentWidget(self.main_page)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # connect the buttons
        exit_button.clicked.connect(self.on_exit_button_clicked)
        manage_account_button.clicked.connect(self.on_manage_account_button_clicked)
        manage_characters_button.clicked.connect(self.on_manage_characters_button_clicked)
        manage_inventory_button.clicked.connect(self.on_manage_inventory_button_clicked)
        manage_quests_button.clicked.connect(self.on_manage_quests_button_clicked)
        manage_monsters_button.clicked.connect(self.on_manage_monsters_button_clicked)
        manage_objects_button.clicked.connect(self.on_manage_objects_button_clicked)
        interaction_NPC_button.clicked.connect(self.on_interaction_NPC_button_clicked)
        ranking_button.clicked.connect(self.on_ranking_button_clicked)
        manage_additional_requests_button.clicked.connect(self.on_manage_additional_requests_button_clicked)
        

    def on_exit_button_clicked(self):
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to exit ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()
            
            
    def on_ranking_button_clicked(self):
        if hasattr(self, 'ranking'):
            self.ranking.deleteLater()
            self.ranking = None
            
        self.ranking = ranking.Ranking(self, self.stacked_widget, self.id)
        self.stacked_widget.addWidget(self.ranking)
        self.stacked_widget.setCurrentWidget(self.ranking)


    def on_manage_account_button_clicked(self):
        if hasattr(self, 'manageAccount'):
            self.manage_account.deleteLater()
            self.manage_account = None
            
        self.manage_account = manage_account.ManageAccount(self, self.stacked_widget, self.id)
        self.stacked_widget.addWidget(self.manage_account)
        self.stacked_widget.setCurrentWidget(self.manage_account)


    def on_manage_characters_button_clicked(self):
        if hasattr(self, 'manageCharacters'):
            self.manage_characters.deleteLater()
            self.manage_characters = None
            
        self.manage_characters = manage_characters.ManageCharacters(self, self.stacked_widget, self.id)
        self.stacked_widget.addWidget(self.manage_characters)
        self.stacked_widget.setCurrentWidget(self.manage_characters)


    def on_manage_inventory_button_clicked(self):
        if hasattr(self, 'manageInventory'):
            self.manage_inventory.deleteLater()
            self.manage_inventory = None
            
        self.manage_inventory = manage_inventory.ManageInventory(self, self.stacked_widget, self.id)
        self.stacked_widget.addWidget(self.manage_inventory)
        self.stacked_widget.setCurrentWidget(self.manage_inventory)


    def on_manage_quests_button_clicked(self):
        if hasattr(self, 'manageQuests'):
            self.manage_quests.deleteLater()
            self.manage_quests = None
            
        self.manage_quests = manage_quests.ManageQuests(self, self.stacked_widget, self.id)
        self.stacked_widget.addWidget(self.manage_quests)
        self.stacked_widget.setCurrentWidget(self.manage_quests)
        
        
    def on_manage_monsters_button_clicked(self):
        if hasattr(self, 'manageMonsters'):
            self.manage_monsters.deleteLater()
            self.manage_monsters = None
            
        self.manage_monsters = monsters.Monsters(self, self.stacked_widget, self.id)
        self.stacked_widget.addWidget(self.manage_monsters)
        self.stacked_widget.setCurrentWidget(self.manage_monsters)

    def on_manage_objects_button_clicked(self):
        if hasattr(self, 'manageObjects'):
            self.manage_objects.deleteLater()
            self.manage_objects = None
        self.manage_objects = manage_objects.ManageObjects(self, self.stacked_widget, self.id)
        self.stacked_widget.addWidget(self.manage_objects)
        self.stacked_widget.setCurrentWidget(self.manage_objects)

    def on_manage_additional_requests_button_clicked(self):
        if hasattr(self, 'additionalRequestsPage'):
            self.additional_requests_page.deleteLater()
            self.additional_requests_page = None

        back_button = QPushButton("Back")
        back_button.setFixedWidth(500)
        back_button.setAutoDefault(True)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_page))

        self.additional_requests_page = QWidget()

        layout = QVBoxLayout()
        
        results_text = additional_request.add_additional_requests()
        results_display = QTextEdit()
        results_display.setHtml(results_text)
        results_display.setReadOnly(True)
        
        layout.addWidget(qt_config.create_center_bold_title("Additional Requests"), alignment=Qt.AlignCenter)
        layout.addWidget(results_display)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.additional_requests_page.setLayout(layout)

        self.stacked_widget.addWidget(self.additional_requests_page)
        self.stacked_widget.setCurrentWidget(self.additional_requests_page)
        
        
    def on_interaction_NPC_button_clicked(self):
        if hasattr(self, 'interactionNPC'):
            self.interaction_NPC.deleteLater()
            self.interaction_NPC = None
            
        self.interaction_NPC = npc_interaction.NPCInteraction(self, self.stacked_widget, self.id)
        self.stacked_widget.addWidget(self.interaction_NPC)
        self.stacked_widget.setCurrentWidget(self.interaction_NPC)
        
