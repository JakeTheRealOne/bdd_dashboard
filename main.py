import mysql.connector

# Create the database and tables if they don't exist
def createDatabaseAndTables(cursor):
    # Create the database if it doesn't exist and use it
    cursor.execute("CREATE DATABASE IF NOT EXISTS rpg;")
    cursor.execute("USE rpg;")

    # Create the table Players if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Players (ID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR (255), Level INT, XP INT, Money INT);")

    # Create the table Characters if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Characters (ID INT, Name VARCHAR(255), Strenght INT, Agility INT, Intelligence INT, Health INT, Mana INT, Class INT, PRIMARY KEY (ID, Name), FOREIGN KEY (ID) REFERENCES Players(ID));")

    # Create the table Monsters if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Monsters (Name VARCHAR (255) PRIMARY KEY, Damage INT, MonsterHealth INT, Defence INT);")

    # Create the table LootingTable if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS LootingTable (Name VARCHAR (255) PRIMARY KEY, Quantity INT, DropRate INT, FOREIGN KEY (Name) REFERENCES Monsters(Name));")

def main():
    db = mysql.connector.connect(
        host="localhost",
        user="rootuser",
        password="rootuser",
    )

    cursor = db.cursor()

    createDatabaseAndTables(cursor)

    for row in cursor.fetchall():
        print(row)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()