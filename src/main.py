import mysql.connector
import sys
from PyQt5.QtWidgets import QApplication

import login
import create

def main():
    db = mysql.connector.connect(
        host="localhost",
        user="rootuser",
        password="rootuser",
    )

    cursor = db.cursor()

    create.createDatabaseAndTables(db, cursor)

    app = QApplication(sys.argv)
    loginScreen = login.Login()
    loginScreen.show()

    cursor.close()
    db.close()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()