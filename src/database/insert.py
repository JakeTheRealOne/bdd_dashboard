import csv
import mysql.connector
import xml.etree.ElementTree as ElemTree
import json
import os

from . import create

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

def insert_players_data(db, cursor):
    csv_path = os.path.join(ROOT_DIR, 'data', 'joueurs.csv')
    with open(csv_path, "r", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    csvfile.close()

    count = 0

    for row in data:
        if not row['XP'].isdigit() or not row['Niveau'].isdigit() or not row['ID'].isdigit() or not row['SlotsInventaire'].isdigit() or not row['Monnaie'].isdigit():
            continue

        id = int(row['ID'])
        name = row['NomUtilisateur']
        level = int(row['Niveau'])
        xp = int(row['XP'])
        money = int(row['Monnaie'])
        inventory_slot = int(row['SlotsInventaire'])

        cursor.execute('''
            INSERT IGNORE INTO Players (ID, Name, Level, XP, Money, InventorySlot)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                id,
                name,
                level,
                xp,
                money,
                inventory_slot
            ))
                       
        if cursor.rowcount == 1:
            count += 1

    db.commit()
    print(f"Inserted {count} rows into Players table.")


def insert_spells_data(db, cursor):
    csv_path = os.path.join(ROOT_DIR, 'data', 'sorts.csv')
    with open(csv_path, "r", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    csvfile.close()

    count = 0

    for row in data:
        if not row['Coût en Mana'].isdigit() or not row['Temps de Recharge'].isdigit() or not row["Puissance d'Attaque"].isdigit():
            continue

        name = row['Nom']
        mana_cost = int(row['Coût en Mana'])
        reload_time = int(row['Temps de Recharge'])
        damage = int(row["Puissance d'Attaque"])

        cursor.execute('''
            INSERT IGNORE INTO Spells (Name, ManaCost, ReloadTime, Damage)
            VALUES (%s, %s, %s, %s)
            ''', (
                name,
                mana_cost,
                reload_time,
                damage
            ))
        
        if cursor.rowcount == 1:
                count += 1

    db.commit()
    print(f"Inserted {count} rows into Spells table.")


def insert_items_data(db, cursor):
    csv_path = os.path.join(ROOT_DIR, 'data', 'objets.csv')
    with open(csv_path, "r", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    csvfile.close()

    count_item = 0
    count_weapon = 0
    count_armor = 0
    count_potion = 0
    count_artefact = 0

    cursor.execute('''
                INSERT IGNORE INTO Items (Name, Price)
                VALUES ('Or', 1)
                ''')
    valide_types = ["Arme", "Armure", "Artefact", "Potion"]
    for row in data:
        try:
            type = row['Type']

            if(type not in valide_types):
                continue

            name = row['Nom']

            price = row['Prix'].strip()
            if not price.isdigit():
                continue
            
            property = row['Propriétés']
            
            cursor.execute('''
                INSERT IGNORE INTO Items (Name, Price, Type)
                VALUES (%s, %s, %s)
                ''', (
                    name,
                    price,
                    type
                ))
            if cursor.rowcount == 1:
                count_item += 1

            if type == "Arme":
                property = property.removeprefix("Puissance d'attaque: ")
                if not property.isdigit():
                    continue
                cursor.execute('''
                    INSERT IGNORE INTO Weapons (Name, Power)
                    VALUES (%s, %s)
                    ''', (
                        name,
                        property
                    ))
                if cursor.rowcount == 1:
                    count_weapon += 1

            elif type == "Armure":
                property = property.removeprefix("Défense: ")
                if not property.isdigit():
                    continue
                cursor.execute('''
                    INSERT IGNORE INTO Armors (Name, Defence)
                    VALUES (%s, %s)
                    ''', (
                        name,
                        property
                    ))
                if cursor.rowcount == 1:
                    count_armor += 1

            elif type == "Artefact":
                cursor.execute('''
                    INSERT IGNORE INTO Artefacts (Name, Effect)
                    VALUES (%s, %s)
                    ''', (
                        name,
                        property
                    ))
                if cursor.rowcount == 1:
                    count_artefact += 1

            elif type == "Potion":
                cursor.execute('''
                    INSERT IGNORE INTO Potions (Name, Boost)
                    VALUES (%s, %s)
                    ''', (
                        name,
                        property
                    ))
                if cursor.rowcount == 1:
                    count_potion += 1
            
            else:
                continue         

        except Exception as e:
            continue
    
    db.commit()
    print(f"Inserted {count_item} rows into Items table.")
    print(f"Inserted {count_weapon} rows into Weapons table.")
    print(f"Inserted {count_armor} rows into Armors table.")
    print(f"Inserted {count_potion} rows into Potions table.")
    print(f"Inserted {count_artefact} rows into Artefacts table.")


def insert_monsters_data(db, cursor):
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


def insert_quests_data(db, cursor):
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
    

def insert_characters_data(db, cursor):
    json_path = os.path.join(ROOT_DIR, 'data', 'personnages.json')
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    file.close()

    count = 0

    for p in data["personnages"]:
        if not all(isinstance(p[key], int) for key in ["Force", "Agilite", "Intelligence", "Vie", "Mana"]):
            continue # Skip if any of the required fields are not integers


        # Check if the player exists in the Players table before inserting the character
        cursor.execute("SELECT ID FROM Players WHERE Name = %s", (p["utilisateur"],))
        result = cursor.fetchone()
        if result is None:
            continue
        my_id = result[0]

        cursor.execute('''
        INSERT IGNORE INTO Characters (Name, Strength, Agility, Intelligence, Health, Mana, Class, PlayerID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            p["Nom"],
            p["Force"],
            p["Agilite"],
            p["Intelligence"],
            p["Vie"],
            p["Mana"],
            p["Classe"],
            my_id
        ))

        if cursor.rowcount == 1:
            count += 1
        
    db.commit()
    print(f"Inserted {count} rows into Characters table.")


def insert_NPC_data(db, cursor):
    json_path = os.path.join(ROOT_DIR, 'data', 'pnjs.json')
    with open(json_path, "r", encoding="utf-8") as file:
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
    
    create.create_database_and_tables(db, cursor)
    cursor.execute("USE rpg;")

    insert_players_data(db, cursor)
    insert_spells_data(db, cursor)
    insert_items_data(db, cursor)
    insert_monsters_data(db, cursor)
    insert_quests_data(db, cursor)
    insert_characters_data(db, cursor)
    insert_NPC_data(db, cursor)
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
