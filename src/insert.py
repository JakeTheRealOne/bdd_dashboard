import csv
import mysql.connector
import os

import create 

def insertPlayersData(db, cursor):
    cursor.execute("USE rpg;")

    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    csvPath = os.path.join(ROOT_DIR, 'data', 'joueurs.csv')

    with open(csvPath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        players_data = []
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
                players_data.append((ID, Name, Level, XP, Money, InventorySlot))
            except ValueError as e:
                print(f"error in line {row}: {e}")

    # Insertion des données
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

    cursor.executemany(query, players_data)

    db.commit()

    print(f"Inserted {len(players_data)} rows into Players table.")

def main():
    db = mysql.connector.connect(
        host='localhost',
        user='rootuser',
        password='rootuser',
    )

    cursor = db.cursor()

    cursor.execute("DROP DATABASE IF EXISTS rpg;")
    create.createDatabaseAndTables(db, cursor)
    insertPlayersData(db, cursor)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()