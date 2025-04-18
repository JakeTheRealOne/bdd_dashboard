import csv
import mysql.connector
import xml.etree.ElementTree as ElemTree
import json
import os
import create 

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

def insertPlayersData(db, cursor):
    csvPath = os.path.join(ROOT_DIR, 'data', 'joueurs.csv')
    with open(csvPath, "r", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    csvfile.close()

    count = 0

    for row in data:
        if not row['XP'].isdigit() or not row['Niveau'].isdigit() or not row['ID'].isdigit() or not row['SlotsInventaire'].isdigit() or not row['Monnaie'].isdigit():
            continue

        ID = int(row['ID'])
        Name = row['NomUtilisateur']
        Level = int(row['Niveau'])
        XP = int(row['XP'])
        Money = int(row['Monnaie'])
        InventorySlot = int(row['SlotsInventaire'])

        cursor.execute('''
            INSERT IGNORE INTO Players (ID, Name, Level, XP, Money, InventorySlot)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                ID,
                Name,
                Level,
                XP,
                Money,
                InventorySlot
            ))
                       
        if cursor.rowcount == 1:
            count += 1

    db.commit()
    print(f"Inserted {count} rows into Players table.")


def insertSpellsData(db, cursor):
    csvPath = os.path.join(ROOT_DIR, 'data', 'sorts.csv')
    with open(csvPath, "r", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    csvfile.close()

    count = 0

    for row in data:
        if not row['Coût en Mana'].isdigit() or not row['Temps de Recharge'].isdigit() or not row["Puissance d'Attaque"].isdigit():
            continue

        Name = row['Nom']
        ManaCost = int(row['Coût en Mana'])
        ReloadTime = int(row['Temps de Recharge'])
        Damage = int(row["Puissance d'Attaque"])

        cursor.execute('''
            INSERT IGNORE INTO Spells (Name, ManaCost, ReloadTime, Damage)
            VALUES (%s, %s, %s, %s)
            ''', (
                Name,
                ManaCost,
                ReloadTime,
                Damage
            ))
        
        if cursor.rowcount == 1:
                count += 1

    db.commit()
    print(f"Inserted {count} rows into Spells table.")


def insertItemsData(db, cursor):
    csvPath = os.path.join(ROOT_DIR, 'data', 'objets.csv')
    with open(csvPath, "r", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    csvfile.close()

    countItem = 0
    countWeapon = 0
    countArmor = 0
    countPotion = 0
    countArtefact = 0

    cursor.execute('''
                INSERT IGNORE INTO Items (Name, Price)
                VALUES ('Or', 1)
                ''')
    valide_types = ["Arme", "Armure", "Artefact", "Potion"]
    for row in data:
        try:
            Type = row['Type']

            if(Type not in valide_types):
                continue

            Name = row['Nom']

            Price = row['Prix'].strip()
            if not Price.isdigit():
                continue
            
            Property = row['Propriétés']
            
            cursor.execute('''
                INSERT IGNORE INTO Items (Name, Price, Type)
                VALUES (%s, %s, %s)
                ''', (
                    Name,
                    Price,
                    Type
                ))
            if cursor.rowcount == 1:
                countItem += 1

            if Type == "Arme":
                Property = Property.removeprefix("Puissance d'attaque: ")
                if not Property.isdigit():
                    continue
                cursor.execute('''
                    INSERT IGNORE INTO Weapons (Name, Power)
                    VALUES (%s, %s)
                    ''', (
                        Name,
                        Property
                    ))
                if cursor.rowcount == 1:
                    countWeapon += 1

            elif Type == "Armure":
                Property = Property.removeprefix("Défense: ")
                if not Property.isdigit():
                    continue
                cursor.execute('''
                    INSERT IGNORE INTO Armors (Name, Defence)
                    VALUES (%s, %s)
                    ''', (
                        Name,
                        Property
                    ))
                if cursor.rowcount == 1:
                    countArmor += 1

            elif Type == "Artefact":
                cursor.execute('''
                    INSERT IGNORE INTO Artefacts (Name, Effect)
                    VALUES (%s, %s)
                    ''', (
                        Name,
                        Property
                    ))
                if cursor.rowcount == 1:
                    countArtefact += 1

            elif Type == "Potion":
                cursor.execute('''
                    INSERT IGNORE INTO Potions (Name, Boost)
                    VALUES (%s, %s)
                    ''', (
                        Name,
                        Property
                    ))
                if cursor.rowcount == 1:
                    countPotion += 1
            
            else:
                continue         

        except Exception as e:
            continue
    
    db.commit()
    print(f"Inserted {countItem} rows into Items table.")
    print(f"Inserted {countWeapon} rows into Weapons table.")
    print(f"Inserted {countArmor} rows into Armors table.")
    print(f"Inserted {countPotion} rows into Potions table.")
    print(f"Inserted {countArtefact} rows into Artefacts table.")


def insertMonstersData(db, cursor):
    monster_xml = ElemTree.parse('./data/monstres.xml')
    root = monster_xml.getroot() 

    count = 0
    for monstre in root.findall('monstre'):
        try:
            name = monstre.find('nom').text
            attaque = int(monstre.find('attaque').text)
            defense = int(monstre.find('defense').text)
            vie = int(monstre.find('vie').text)

            cursor.execute('''
                INSERT IGNORE INTO Monsters (Name, Damage, Defence, MonsterHealth)
                VALUES (%s, %s, %s, %s)
                ''', (
                    name,
                    attaque,
                    defense,
                    vie
                ))
            if cursor.rowcount == 1:
                count += 1
        except Exception:
            continue

        for drop in monstre.find('drops'):
            try:
                drop_name = str(drop.tag).replace('_', ' ')
                quantity = int(drop.find('nombre').text)
                drop_rate = int(drop.find('probabilité').text)

                cursor.execute('''
                INSERT IGNORE INTO MonsterLoots (MonsterName, LootName, DropRate, Quantity)
                VALUES (%s, %s, %s, %s)
                ''', (
                    name,
                    drop_name,
                    drop_rate,
                    quantity
                ))


            except AttributeError:
                None
                


    db.commit()
    print(f"Inserted {count} rows into Monsters table.")


def insertQuestsData(db, cursor):
    quests_xml = ElemTree.parse('./data/quetes.xml')
    root = quests_xml.getroot()

    count = 0
    for quest in root.findall('quête'):
        try:
            name = quest.find('Nom').text
            description = quest.find('Descripion').text
            description = ' '.join(description.split())
            difficulty = int(quest.find('Difficulté').text)
            experience = int(quest.find('Expérience').text)

            cursor.execute('''
                INSERT IGNORE INTO Quests (Name, Description, Difficulty, Experience)
                VALUES (%s, %s, %s, %s)
                ''', (
                    name,
                    description,
                    difficulty,
                    experience
                ))
            if cursor.rowcount == 1:
                count += 1

            for reward in quest.find('Récompenses'):
                reward_name = ""
                quantity = 1
                if reward.tag == 'Or':
                    reward_name = 'Or'
                    quantity = int(reward.text)
                else:
                    reward_name = reward.text

                cursor.execute('''
                        INSERT IGNORE INTO Rewards (QuestName, ItemName, Quantity)
                        VALUES (%s, %s, %s)
                        ''', (
                            name,
                            reward_name,
                            quantity
                        ))
        except Exception:
            continue
    db.commit()
    print(f"Inserted {count} rows into Quests table.")
    

def insertCharactersData(db, cursor):
    jsonPath = os.path.join(ROOT_DIR, 'data', 'personnages.json')
    with open(jsonPath, "r", encoding="utf-8") as file:
        data = json.load(file)

    file.close()

    count = 0

    for p in data["personnages"]:
        if not all(isinstance(p[key], int) for key in ["Force", "Agilite", "Intelligence", "Vie", "Mana"]):
            continue # Skip if any of the required fields are not integers


        # Check if the player exists in the Players table before inserting the character
        cursor.execute("SELECT COUNT(*) FROM Players WHERE Name = %s", (p["utilisateur"],))
        if cursor.fetchone()[0] == 0:
            continue  # Ignore the character if the player does not exist

        cursor.execute('''
        INSERT IGNORE INTO Characters (Name, Strength, Agility, Intelligence, Health, Mana, Class, Username)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            p["Nom"],
            p["Force"],
            p["Agilite"],
            p["Intelligence"],
            p["Vie"],
            p["Mana"],
            p["Classe"],
            p["utilisateur"]
        ))

        if cursor.rowcount == 1:
            count += 1
        
    db.commit()
    print(f"Inserted {count} rows into Characters table.")


def insertNPCData(db, cursor):
    jsonPath = os.path.join(ROOT_DIR, 'data', 'pnjs.json')
    with open(jsonPath, "r", encoding="utf-8") as file:
        data = json.load(file)

    file.close()

    count = 0

    for p in data["PNJs"]:
        # NOM ET DIALOGUE 
        cursor.execute('''
        INSERT IGNORE INTO NPCs (Name, Dialog)
        VALUES (%s, %s)
        ''', (
            p["Nom"],
            p.get("Dialogue", "Bien le bonjour !")
        ))

        inventory = {}

        # INVENTAIRE
        for item in p["Inventaire"]:
            if item in inventory:
                inventory[item] += 1
            else:
                inventory[item] = 1

        for item in inventory: 
            cursor.execute('''
            INSERT IGNORE INTO NPCItemInventories (NPCName, ItemName)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE quantity = %s
            ''', (
                p["Nom"],
                item,
                inventory.get(item)
            ))
        
        quests_list = p.get("Qu\u00eates", [])

        for quest in quests_list:
            cursor.execute('''
            INSERT IGNORE INTO NPCQuests (NPCName, QuestName)
            VALUES (%s, %s)
            ''', (
                p["Nom"],
                quest
            ))

        if cursor.rowcount == 1:
            count += 1
        
    db.commit()

    print(f"Inserted {count} rows into Npc table.")



def main():
    db = mysql.connector.connect(
        host='localhost',
        user='rootuser',
        password='rootuser',
    )

    cursor = db.cursor()
    
    create.createDatabaseAndTables(db, cursor)
    cursor.execute("USE rpg;")

    insertPlayersData(db, cursor)
    insertSpellsData(db, cursor)
    
    insertItemsData(db, cursor)
    insertMonstersData(db, cursor)
    insertQuestsData(db, cursor)
    insertCharactersData(db, cursor)
    insertNPCData(db, cursor)
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()