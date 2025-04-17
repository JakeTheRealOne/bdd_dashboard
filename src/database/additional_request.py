import mysql.connector

import create

def playersMostGold(cursor):
    cursor.execute('''
    SELECT p.Name, p.Money 
    FROM Players p 
    ORDER BY p.Money DESC LIMIT 10;
                   ''')


def playerMostCharactersSameClass(cursor):
    cursor.execute('''
    SELECT p.Name, c.Class, COUNT(*) AS nbCharacters
    FROM Players p
    JOIN Characters c ON p.Name = c.Username
    GROUP BY p.Name, c.Class
    ORDER BY nbCharacters DESC
    LIMIT 1;
    ''')


def questBiggestRewardByLevel(cursor):
    cursor.execute('''
    WITH QuestGold AS (
    SELECT q.Name AS QuestName, q.Difficulty, SUM(i.Price * r.Quantity) AS TotalGold
    FROM Quests q
    JOIN Rewards r ON q.Name = r.QuestName
    JOIN Items i ON r.ItemName = i.Name
    GROUP BY q.Name, q.Difficulty
    ),
    RankedQuests AS (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY Difficulty ORDER BY TotalGold DESC) AS `rank`
        FROM QuestGold
    )
    SELECT QuestName, Difficulty, TotalGold
    FROM RankedQuests
    WHERE `rank` = 1;
    ''')


def NPCMostInventoryValue(cursor):
    cursor.execute('''       
    SELECT npc.Name, SUM(i.Price * npcII.Quantity) AS TotalValue
    FROM NPCs npc
    JOIN NPCItemInventories npcII ON npc.Name = npcII.NPCName
    JOIN Items i ON npcII.ItemName = i.Name
    GROUP BY npc.Name
    ORDER BY TotalValue DESC
    LIMIT 1;
    ''')


def mostRewardedItemType(cursor):
    cursor.execute('''
                   SELECT item.Type, COUNT(*) as apparitions
                   FROM Items item
                   WHERE item.Name in (

                   SELECT reward.ItemName
                   FROM Rewards reward
                   WHERE reward.ItemName <> 'Or' AND
                        reward.QuestName in (
                        SELECT quest.Name
                        FROM Quests quest
                        WHERE quest.Difficulty = 5
                   )
                   )
                   GROUP BY item.Type
                   ORDER BY apparitions desc
                   LIMIT 1;
    ''')


def print_underline(text):
    print("\033[4m" + text + "\033[0m")


def addAdditionalRequests(cursor):
    print_underline("Top 10 players with the most gold:\n")
    print(f"{'Rank':<5}{'Player':<20}{'Gold':<5}")
    print("-" * 30)
    playersMostGold(cursor)
    for index, (playerName, gold) in enumerate(cursor.fetchall(), start=1):
        print(f"{index:<5}{playerName:<20}{gold:<5}")
    print("\n")

    playerMostCharactersSameClass(cursor)
    print_underline("Player with the most characters of the same class:\n")
    print(f"{'Rank':<5}{'Player':<20}{'Class':<10}{'Nb Characters':<12}")
    print("-" * 47)
    result = cursor.fetchone()
    if result:
        playerName, classe, nbCharacters = result
        print(f"{'1':<5}{playerName:<20}{classe:<10}{nbCharacters:<12}")
    print("\n")

    questBiggestRewardByLevel(cursor)
    print_underline("Quest with the biggest reward by level:\n")
    print(f"{'Quest Name':<40}{'Level':<15}{'Gold':<5}")
    print("-" * 60)
    for questName, level, totalGold in cursor.fetchall():
        print(f"{questName:<40}{level:<15}{totalGold:<5}")
    print("\n")

    NPCMostInventoryValue(cursor)
    print_underline("NPC with the most valuable inventory:\n")
    print(f"{'Rank':<5}{'NPC':<40}{'Gold inventory value':<17}")
    print("-" * 63)
    result = cursor.fetchone()
    if result:
        npcName, totalValue = result
        print(f"{'1':<5}{npcName:<40}{totalValue:<17}")
    print("\n")

    
    mostRewardedItemType(cursor)
    print_underline("Most Rewarded Item Type rewarded by difficulty 5 quests:\n")
    print(f"{'Item Type':<20}{'Number of apparition'}")
    print("-" * 40)
    result = cursor.fetchone()
    if result:
        itemType, apparition_number = result
        print(f"{itemType:<20}{apparition_number}")
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