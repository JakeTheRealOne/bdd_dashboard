import csv
import mysql.connector
import xml.etree.ElementTree as ElemTree
import os

import create 

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

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

            except ValueError as e:
                print(f"error in line {row}: {e}")

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

            except ValueError as e:
                print(f"error in line {row}: {e}")

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
            continue; 

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

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()