import csv
import mysql.connector
import xml.etree.ElementTree as ElemTree
import json
import os
import create 

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

def insertPlayersData(db, cursor):
    csvPath = os.path.join(ROOT_DIR, 'data', 'joueurs.csv')

    with open(csvPath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        playersData = []
        for row in reader:
            try:
                if not row['XP'].isdigit() or not row['Niveau'].isdigit() or not row['ID'].isdigit() or not row['SlotsInventaire'].isdigit() or not row['Monnaie'].isdigit():
                    continue

                ID = int(row['ID'])
                Name = row['NomUtilisateur']
                Level = int(row['Niveau'])
                XP = int(row['XP'])
                Money = int(row['Monnaie'])
                InventorySlot = int(row['SlotsInventaire'])
                playersData.append((ID, Name, Level, XP, Money, InventorySlot))

            except:
                continue

    # Prepare the SQL query to insert data into the Players table (update the existing player if the ID already exists)
    query = '''
        INSERT INTO Players (ID, Name, Level, XP, Money, InventorySlot)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Name = VALUES(Name),
            Level = VALUES(Level),
            XP = VALUES(XP),
            Money = VALUES(Money),
            InventorySlot = VALUES(InventorySlot)
    '''

    cursor.executemany(query, playersData)

    db.commit()
    csvfile.close()

    print(f"Inserted {len(playersData)} rows into Players table.")


def insertSpellsData(db, cursor):
    csvPath = os.path.join(ROOT_DIR, 'data', 'sorts.csv')

    with open(csvPath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        spellsData = []
        for row in reader:
            try:
                if not row['Coût en Mana'].isdigit() or not row['Temps de Recharge'].isdigit() or not row["Puissance d'Attaque"].isdigit():
                    continue

                Name = row['Nom']
                ManaCost = int(row['Coût en Mana'])
                ReloadTime = int(row['Temps de Recharge'])
                Damage = int(row["Puissance d'Attaque"])
                spellsData.append((Name, ManaCost, ReloadTime, Damage))

            except:
                 continue 

    # Prepare the SQL query to insert data into the Spells table (update the existing spell if the Name already exists)
    query = '''
        INSERT INTO Spells (Name, ManaCost, ReloadTime, Damage)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Name = VALUES(Name),
            ManaCost = VALUES(ManaCost),
            ReloadTime = VALUES(ReloadTime),
            Damage = VALUES(Damage)
    '''

    cursor.executemany(query, spellsData)

    db.commit()
    csvfile.close()

    print(f"Inserted {len(spellsData)} rows into Spells table.")


def insertMonstersData(db, cursor):
    monster_xml = ElemTree.parse('./data/monstres.xml')
    root = monster_xml.getroot() 
    monstres_data = []
    for monstre in root.findall('monstre'):
        try:
            nom = monstre.find('nom').text
            attaque = int(monstre.find('attaque').text)
            defense = int(monstre.find('defense').text)
            vie = int(monstre.find('vie').text)
            monstres_data.append((nom, attaque, defense, vie))
        except:
            continue 

    query = '''
        INSERT INTO Monsters (Name, Damage, Defence, MonsterHealth)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Name = VALUES(Name),
            Damage = VALUES(Damage),
            Defence = VALUES(Defence),
            MonsterHealth = VALUES(MonsterHealth)
    '''
    cursor.executemany(query, monstres_data)

    db.commit()

    print(f"Inserted {len(monstres_data)} rows into Monsters table.")


def insertQuestsData(db, cursor):
    quests_xml = ElemTree.parse('./data/quetes.xml')
    root = quests_xml.getroot()
    quests_data = []
    for quest in root.findall('quête'):
        try:
            name = quest.find('Nom').text
            description = quest.find('Descripion').text
            description = ' '.join(description.split())

            difficulty = int(quest.find('Difficulté').text)
            experience = int(quest.find('Expérience').text)
            quests_data.append((name, description, difficulty, experience))
        except:
            continue

    query = '''
        INSERT INTO Quests (Name, Description, Difficulty, Experience)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Name = VALUES(Name),
            Description = VALUES(Description),
            Difficulty = VALUES(Difficulty),
            Experience = VALUES(Experience)
    '''
    cursor.executemany(query, quests_data)
    db.commit()
    print(f"Inserted {len(quests_data)} rows into Quests table.")
    
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

        # Check if the character was inserted successfully
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
    insertCharactersData(db, cursor)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()