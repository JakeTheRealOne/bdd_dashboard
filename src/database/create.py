import mysql.connector

def createDatabaseAndTables(db, cursor):
    """
    Create the database and tables if they don't exist
    """
    
    # Create the database if it doesn't exist and use it
    cursor.execute("CREATE DATABASE IF NOT EXISTS rpg;")
    cursor.execute("USE rpg;")

    # Create the table Players if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Players (ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR (255), Level INT DEFAULT 0, XP INT DEFAULT 0, Money INT DEFAULT 0, InventorySlot INT DEFAULT 0);")

    # Create the table Characters if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Characters (ID INT, Name VARCHAR(255), Strenght INT DEFAULT 0, Agility INT DEFAULT 0, Intelligence INT DEFAULT 0, Health INT DEFAULT 0, Mana INT DEFAULT 0, Class INT DEFAULT 0, PRIMARY KEY (ID, Name), FOREIGN KEY (ID) REFERENCES Players(ID));")

    # Create the table Monsters if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Monsters (Name VARCHAR (255) PRIMARY KEY, Damage INT DEFAULT 0, MonsterHealth INT DEFAULT 0, Defence INT DEFAULT 0);")

    # Create the table LootingTable if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS LootingTable (Name VARCHAR (255) PRIMARY KEY, Quantity INT DEFAULT 0, DropRate INT DEFAULT 0, FOREIGN KEY (Name) REFERENCES Monsters(Name));")

    # Create the table Spells if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Spells (Name VARCHAR (255) PRIMARY KEY, ManaCost INT DEFAULT 0, ReloadTime INT DEFAULT 0, Damage INT DEFAULT 0);")
    
    # Create the table Quests if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Quests (Name VARCHAR (255) PRIMARY KEY, Description VARCHAR (255), Difficulty INT DEFAULT 0, Experience INT DEFAULT 0);")

    db.commit()

def main():
    db = mysql.connector.connect(
        host="localhost",
        user="rootuser",
        password="rootuser",
    )

    cursor = db.cursor()
    createDatabaseAndTables(db, cursor)
    print("Database and tables created successfully.")
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()