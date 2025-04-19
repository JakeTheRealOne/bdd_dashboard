import mysql.connector
import sys
from PyQt5.QtWidgets import QApplication

from gui import login
from database import create

def main():
    db = mysql.connector.connect(
        host="localhost",
        user="rootuser",
        password="rootuser",
    )

    cursor = db.cursor()
    create.createDatabaseAndTables(db, cursor)
    cursor.close()  
    db.close()
    
    app = QApplication(sys.argv)
    loginScreen = login.Login()
    loginScreen.run()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()