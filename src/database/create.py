import mysql.connector

def create_database_and_tables(db, cursor):
    """
    Create the database and tables if they don't exist
    """
    
    # Create the database if it doesn't exist and use it
    cursor.execute("CREATE DATABASE IF NOT EXISTS rpg;")
    cursor.execute("USE rpg;")

    # Create the table Players if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Players (ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR (255) UNIQUE, Level INT DEFAULT 0, XP INT DEFAULT 0, Money INT DEFAULT 0, InventorySlot INT DEFAULT 5);")

    # Create the table Characters if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Characters (Name VARCHAR(255) PRIMARY KEY, Strength INT DEFAULT 0, Agility INT DEFAULT 0, Intelligence INT DEFAULT 0, Health INT DEFAULT 0, Mana INT DEFAULT 0, Class VARCHAR(255), Username VARCHAR(255), FOREIGN KEY (Username) REFERENCES Players(Name));")

    # Create the table Monsters if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Monsters (Name VARCHAR (255) PRIMARY KEY, Damage INT DEFAULT 0, MonsterHealth INT DEFAULT 0, Defence INT DEFAULT 0);")

    # Create the table Spells if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Spells (Name VARCHAR (255) PRIMARY KEY, ManaCost INT DEFAULT 0, ReloadTime INT DEFAULT 0, Damage INT DEFAULT 0);")
    
    # Create the table Quests if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Quests (Name VARCHAR (255) PRIMARY KEY, Description VARCHAR (255), Difficulty INT DEFAULT 0, Experience INT DEFAULT 0);")

    # Create the table Items if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Items (Name VARCHAR (225) PRIMARY KEY, Price INT DEFAULT 0, Type VARCHAR (255)) ;")

    # Create the table Weapons if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Weapons (Name VARCHAR (225) PRIMARY KEY, Power INT DEFAULT 0);")

    # Create the table Armors if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Armors (Name VARCHAR (225) PRIMARY KEY, Defence INT DEFAULT 0) ;")
 
    # Create the table Potions if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Potions (Name VARCHAR (225) PRIMARY KEY, Boost VARCHAR (225));")
    
    # Create the table Artefacts if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Artefacts (Name VARCHAR (225) PRIMARY KEY, Effect VARCHAR (225));")

    # Create the table NPCs if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS NPCs (Name VARCHAR (225) PRIMARY KEY, Dialog TEXT);")

    # Create the table NPCItemInventories if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS NPCItemInventories (NPCName VARCHAR (225), ItemName VARCHAR (225), Quantity INT DEFAULT 1," \
    "PRIMARY KEY (NPCName, ItemName), FOREIGN KEY (NPCName) REFERENCES NPCs(Name), FOREIGN KEY (ItemName) REFERENCES Items(Name)) ;")

    # Create the table NPCQuests if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS NPCQuests (NPCName VARCHAR (225), QuestName VARCHAR (225), " \
    "PRIMARY KEY (NPCName, QuestName), FOREIGN KEY (NPCName) REFERENCES NPCs(Name), FOREIGN KEY (QuestName) REFERENCES Quests(Name));")
    
    # Create the table PlayerQuests if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS PlayerQuests (PlayerID INT, QuestName VARCHAR(255)," \
    "PRIMARY KEY (PlayerID, QuestName), FOREIGN KEY (PlayerID) REFERENCES Players(ID), FOREIGN KEY (QuestName) REFERENCES Quests(Name));")

    # Create the table MonsterLoots if it doesen't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS MonsterLoots (MonsterName VARCHAR (255), LootName VARCHAR (255), DropRate INT DEFAULT 0, Quantity INT DEFAULT 0," \
    "PRIMARY KEY (MonsterName, LootName), FOREIGN KEY (MonsterName) REFERENCES Monsters(Name), FOREIGN KEY (LootName) REFERENCES Items(Name));")

    # Create the table Rewards if it doesen't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Rewards (QuestName VARCHAR (255), ItemName VARCHAR (255), Quantity INT DEFAULT 1," \
    "PRIMARY KEY (QuestName, ItemName), FOREIGN KEY (QuestName) REFERENCES Quests(Name), FOREIGN KEY (ItemName) REFERENCES Items(Name));")

    # Create the table PlayerInventories if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PlayerInventories (
            PlayerID INT,
            ItemName VARCHAR(225),
            SlotIDX INT,
            PRIMARY KEY (PlayerID, SlotIDX),
            FOREIGN KEY (PlayerID) REFERENCES Players(ID) ON DELETE CASCADE,
            FOREIGN KEY (ItemName) REFERENCES Items(Name)
        );
    """)

    # Create the table PlayerArmors if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PlayerArmors (
            PlayerID INT,
            ArmorName VARCHAR(255),
            PRIMARY KEY (PlayerID),
            FOREIGN KEY (PlayerID) REFERENCES Players(ID) ON DELETE CASCADE,
            FOREIGN KEY (ArmorName) REFERENCES Armors(Name)
        );
    """)

    # Create the table PlayerWeapons if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PlayerWeapons (
            PlayerID INT,
            WeaponName VARCHAR(255),
            PRIMARY KEY (PlayerID),
            FOREIGN KEY (PlayerID) REFERENCES Players(ID) ON DELETE CASCADE,
            FOREIGN KEY (WeaponName) REFERENCES Weapons(Name)
        );
    """)

    db.commit()

def main():
    db = mysql.connector.connect(
        host="localhost",
        user="rootuser",
        password="rootuser",
    )

    cursor = db.cursor()
    create_database_and_tables(db, cursor)
    print("Database and tables created successfully.")
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()