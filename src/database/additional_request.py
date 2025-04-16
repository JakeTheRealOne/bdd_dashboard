import mysql.connector

import create
import insert

def playersMostGold(cursor):
    cursor.execute('''
    SELECT p.Name, p.Money 
    FROM Players p 
    ORDER BY p.Money DESC LIMIT 10;''')

def playerMostCharactersSameClass(cursor):
    cursor.execute('''
    SELECT p.Name, c.Class, COUNT(*) AS nbCharacters
    FROM Players p
    JOIN Characters c ON p.Name = c.Username
    GROUP BY p.Name, c.Class
    ORDER BY nbCharacters DESC
    LIMIT 1;
    ''')

def NPCMostInventoryValue(cursor):
    cursor.execute('''       
    SELECT npc.Name, SUM(items.Price * npcItemInvento.Quantity) AS TotalValue
    FROM NPCs npc
    JOIN NPCItemInventories npcItemInvento ON npc.Name = npcItemInvento.NPCName
    JOIN Items items ON npcItemInvento.ItemName = items.Name
    GROUP BY npc.Name
    ORDER BY TotalValue DESC
    LIMIT 1;
    ''')

def addAdditionalRequests(cursor):
    playersMostGold(cursor)
    print("Top 10 players with the most gold:\n")
    print(f"{'Rank':<5}{'Player':<20}{'Gold':<15}")
    print("-" * 30)
    for index, (playerName, gold) in enumerate(cursor.fetchall(), start=1):
        print(f"{index:<5}{playerName:<20}{gold:<15}")
    print("\n")

    playerMostCharactersSameClass(cursor)
    print("Player with the most characters of the same class:\n")
    print(f"{'Rank':<5}{'Player':<20}{'Class':<10}{'Nb Characters':<10}")
    print("-" * 50)
    result = cursor.fetchone()
    if result:
        playerName, classe, nbCharacters = result
        print(f"{'1':<5}{playerName:<20}{classe:<15}{nbCharacters:<10}")
    print("\n")

    NPCMostInventoryValue(cursor)
    print("NPC with the most valuable inventory:\n")
    print(f"{'Rank':<5}{'NPC':<40}{'Total Value Gold':<15}")
    print("-" * 65)
    result = cursor.fetchone()
    if result:
        npcName, totalValue = result
        print(f"{'1':<5}{npcName:<40}{totalValue:<15}")
    print("\n")
    



def main():
    db = mysql.connector.connect(
        host='localhost',
        user='rootuser',
        password='rootuser',
    )

    cursor = db.cursor()
    
    create.createDatabaseAndTables(db, cursor)
    cursor.execute("USE rpg;")

    addAdditionalRequests(cursor)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()