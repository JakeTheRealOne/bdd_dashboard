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

    with open(csvPath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        itemData = []
        weaponData = []
        armorData = []
        potionData = []
        artefactData = []

        for row in reader:
            try:
                Type = row['Type']

                Name = row['Nom']

                Price = row['Prix']

                if not Price.isdigit():
                    continue
                
                
                Property = row['Propriétés']
                
                itemData.append((Name, int(Price)))


                if(Type == "Arme"):
                    Property = Property.removeprefix("Puissance d'attaque: ")
                    if not Property.isdigit():
                        continue
                    weaponData.append((Name, int(Property)))

                elif Type == "Armure":
                    Property = Property.removeprefix("Défense: ")
                    if not Property.isdigit():
                        continue
                    armorData.append((Name, int(Property)))

                elif Type == "Artefact":
                    artefactData.append((Name, Property))

                elif Type == "Potion":
                    potionData.append((Name, Property))
                
                else:
                    continue

                
                

            except:
                continue


    query = '''
        INSERT INTO Items (Name, Price)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            Name = VALUES(Name),
            Price = VALUES(Price)
    '''

    queryWeapon = '''
        INSERT INTO Weapons (Name, Power)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            Name = VALUES(Name),
            Power = VALUES(Power)
    '''
    
    queryArmor = '''
        INSERT INTO Armors (Name, Defence)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            Name = VALUES(Name),
            Defence = VALUES(Defence)
    '''

    queryPotion = '''
        INSERT INTO Potions (Name, Boost)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            Name = VALUES(Name),
            Boost = VALUES(Boost)
    '''

    queryArtefact = '''
        INSERT INTO Artefacts (Name, Effect)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            Name = VALUES(Name),
            Effect = VALUES(Effect)
    '''


    cursor.executemany(query, itemData)
    print(f"Inserted {len(itemData)} rows into Items table.")
    cursor.executemany(queryWeapon, weaponData)
    print(f"Inserted {len(weaponData)} rows into Weapons table.")
    cursor.executemany(queryArmor, armorData)
    print(f"Inserted {len(armorData)} rows into Armors table.")
    cursor.executemany(queryPotion, potionData)
    print(f"Inserted {len(potionData)} rows into Potions table.")
    cursor.executemany(queryArtefact, artefactData)
    print(f"Inserted {len(artefactData)} rows into Artefacts table.")
    db.commit()


def insertMonstersData(db, cursor):
    monster_xml = ElemTree.parse('./data/monstres.xml')
    root = monster_xml.getroot() 

    count = 0
    for monstre in root.findall('monstre'):
        try:
            nom = monstre.find('nom').text
            attaque = int(monstre.find('attaque').text)
            defense = int(monstre.find('defense').text)
            vie = int(monstre.find('vie').text)

            cursor.execute('''
                INSERT IGNORE INTO Monsters (Name, Damage, Defence, MonsterHealth)
                VALUES (%s, %s, %s, %s)
                ''', (
                    nom,
                    attaque,
                    defense,
                    vie
                ))
            if cursor.rowcount == 1:
                count += 1

        except:
            continue

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

        except:
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
        INSERT IGNORE INTO Characters (Name, Strenght, Agility, Intelligence, Health, Mana, Class, Username)
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
    insertMonstersData(db, cursor)
    insertQuestsData(db, cursor)
    insertItemsData(db, cursor)
    insertCharactersData(db, cursor)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()