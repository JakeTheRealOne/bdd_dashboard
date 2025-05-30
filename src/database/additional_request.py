import mysql.connector

from . import insert

def players_most_gold(cursor):
    cursor.execute('''
    SELECT p.Name, p.Money 
    FROM Players p 
    ORDER BY p.Money DESC LIMIT 10;
    ''')


def player_most_characters_same_class(cursor):
    cursor.execute('''
    SELECT p.Name, c.Class, COUNT(*) AS nbCharacters
    FROM Players p
    JOIN Characters c ON p.ID = c.PlayerID
    GROUP BY p.Name, c.Class
    ORDER BY nbCharacters DESC LIMIT 1;
    ''')


def quest_biggest_reward_by_level(cursor):
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


def NPC_most_inventory_value(cursor):
    cursor.execute('''       
    SELECT npc.Name, SUM(i.Price * npcII.Quantity) AS TotalValue
    FROM NPCs npc
    JOIN NPCItemInventories npcII ON npc.Name = npcII.NPCName
    JOIN Items i ON npcII.ItemName = i.Name
    GROUP BY npc.Name
    ORDER BY TotalValue DESC LIMIT 1;
    ''')


def most_rewarded_item_type(cursor):
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
    ORDER BY apparitions desc LIMIT 1;
    ''')


def most_rewarding_monster(cursor):
    cursor.execute('''
    SELECT (MonsterCost/MonsterHealth) AS Ratio, Name
    FROM (
        SELECT SUM(ItemPrice * lootQuantity) as MonsterCost, MonsterName
        FROM
        (
            SELECT 
                items.Name as ItemName,
                items.Price as ItemPrice,
                loot.MonsterName as MonsterName,
                loot.Quantity as lootQuantity
            FROM Items items
            JOIN MonsterLoots loot ON items.Name = loot.LootName
        ) as subrequest
        GROUP BY MonsterName
    ) as monsterHealthAndPrice
    JOIN Monsters monsters on monsters.Name = MonsterName
    ORDER BY Ratio desc;
    ''')


def text_underline(text):
    return f"<u>{text}</u>"


def add_additional_requests():
    db = mysql.connector.connect(
        host='localhost',
        user='rootuser',
        password='rootuser',
        database='rpg'
    )

    cursor = db.cursor()
    
    result_request = ""
    
    result_request += text_underline("Top 10 players with the most gold:\n")
    result_request += (f"{'Rank':<5}{'Player':<20}{'Gold':<5}\n")
    result_request += ("-" * 30 + "\n")
    players_most_gold(cursor)
    for index, (player_name, gold) in enumerate(cursor.fetchall(), start=1):
        result_request += (f"{index:<5}{player_name:<20}{gold:<5}\n")
    result_request += "\n"

    player_most_characters_same_class(cursor)
    result_request += text_underline("Player with the most characters of the same class:\n")
    result_request += (f"{'Rank':<5}{'Player':<20}{'Class':<10}{'Nb Characters':<12}\n")
    result_request += ("-" * 47 + "\n")
    result = cursor.fetchone()
    if result:
        player_name, classe, nb_characters = result
        result_request += (f"{'1':<5}{player_name:<20}{classe:<10}{nb_characters:<12}\n")
    result_request += "\n"

    quest_biggest_reward_by_level(cursor)
    result_request += text_underline("Quest with the biggest reward by level:\n")
    result_request += (f"{'Quest Name':<40}{'Level':<15}{'Gold':<5}\n")
    result_request += ("-" * 60 + "\n")
    for quest_name, level, total_gold in cursor.fetchall():
        result_request += (f"{quest_name:<40}{level:<15}{total_gold:<5}\n")
    result_request += "\n"

    NPC_most_inventory_value(cursor)
    result_request += text_underline("NPC with the most valuable inventory:\n")
    result_request += (f"{'Rank':<5}{'NPC':<40}{'Gold inventory value':<17}\n")
    result_request += ("-" * 63 + "\n")
    result = cursor.fetchone()
    if result:
        npc_name, total_value = result
        result_request += (f"{'1':<5}{npc_name:<40}{total_value:<17}\n")
    result_request += "\n"

    
    most_rewarded_item_type(cursor)
    result_request += text_underline("Most Rewarded Item Type rewarded by difficulty 5 quests:\n")
    result_request += (f"{'Item Type':<20}{'Number of apparition'}\n")
    result_request += ("-" * 40 + "\n")
    result = cursor.fetchone()
    if result:
        item_type, apparition_number = result
        result_request += (f"{item_type:<20}{apparition_number}\n")
    result_request += "\n"

    most_rewarding_monster(cursor)
    result_request += text_underline("Ranking of the Most Rewarding Monster (in term of gold total price and health):\n")
    result_request += (f"{'Item':<30}{'Ration gold/life'}\n")
    result_request += ("-" * 45 + "\n")
    result = cursor.fetchall()
    if result:
        for ratio, item_name in result:
            result_request += (f"{item_name:<30}{ratio}\n")
    result_request += "\n"
    
    cursor.close()
    db.close()
    
    return f"<pre>{result_request}</pre>"
