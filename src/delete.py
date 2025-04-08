import mysql.connector

def main():
    db = mysql.connector.connect(
        host="localhost",
        user="rootuser",
        password="rootuser",
    )

    cursor = db.cursor()

    cursor.execute("DROP DATABASE IF EXISTS rpg;")

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()