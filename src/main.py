import mysql.connector
import sys
from PyQt5.QtWidgets import QApplication

from src.gui import login
from src.database import create

def main():
    db = mysql.connector.connect(
        host="localhost",
        user="rootuser",
        password="rootuser",
    )

    cursor = db.cursor()
    create.create_database_and_tables(db, cursor)
    cursor.close()  
    db.close()
    
    app = QApplication(sys.argv)
    login_screen = login.Login()
    login_screen.run()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
