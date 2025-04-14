'''
Brief:    Print all the tables and columns of the RPG database
Authors:
  * Bilal Vandenberge
  * Lucas Verbeiren
  * Ethan Van Ruyskensvelde
  * Rares Radu-Loghin
Date:     2025
Context:  Project INFO-H303
'''

import mysql.connector

def main() -> None:
  db = mysql.connector.connect(
    host='localhost',
    user='rootuser',
    password='rootuser',
    database='rpg'
  )
  cursor = db.cursor()

  cursor.execute('SHOW TABLES')
  tables = cursor.fetchall()
  for (table_name,) in tables:
    print(f'\033[31;1;4mTable\033[0m: {table_name}')
    cursor.execute(f'SHOW COLUMNS FROM `{table_name}`')
    columns = cursor.fetchall()     
    for i in range(len(columns)):
      char = '└' if i == len(columns) - 1 else '├'
      column = columns[i]
      print(f'{char}{column[0]}')
    print()

  cursor.close()
  db.close()

if __name__ == '__main__':
  main()