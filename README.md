# Database Project

This project is written in Python and uses a graphical interface using PyQt5. It interacts with a MySQL database using the `mysql-connector-python` package.

## Members

- Bilal Vandenberge
- Lucas Verbeiren
- Ethan Van Ruyskensvelde
- Rares Radu-Loghin

## Prerequisites

Make sure you have Python 3 installed on your system:

```sh
python3 --version
```

You also need to install MySQL (or MariaDB) to run the project. If you don't have it installed, you can do so with the following command (for Arch Linux):

```sh
sudo pacman -S mysql
```

## Installation

Install the required dependencies using `pip`:

```sh
pip install pyqt5 mysql-connector-python
```

## Running the Application

You can run the program with:

```sh
python3 -m src.main
```

### Troubleshooting

On Wayland desktop environments, running the program with `QT_QPA_PLATFORM=xcb` is recommended:

```sh
QT_QPA_PLATFORM=xcb python3 -m src.main
```

## Database Management Scripts

Three utility scripts are provided to manage the database:

### Create the database and its tables

```sh
python3 -m src.database.create
```

### Delete the database

```sh
python3 -m src.database.delete
```

### Insert data into the database

```sh
python3 -m src.database.insert
```

This script will populate the database using data from files in the `data/` folder at the root of the project.

## Create Your Own MySQL Database to Run This Project

To run the project, you'll need to set up your own MySQL (or MariaDB) database and user. Follow the steps below:

1. **Install MySQL** (or MariaDB) on your system if you haven't already done so.

2. **Create a new MySQL user** and grant privileges by running the following commands in your terminal:

    ```sh
    sudo mysql -e "CREATE USER 'rootuser'@'localhost' IDENTIFIED BY 'rootuser';"
    sudo mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'rootuser'@'localhost' WITH GRANT OPTION;"
    sudo mysql -e "FLUSH PRIVILEGES;"
    ```

    **For windows**
    ```sh
    mysql -u root -p -e "CREATE USER 'rootuser'@'localhost' IDENTIFIED BY 'rootuser';"
    mysql -u root -p -e "GRANT ALL PRIVILEGES ON *.* TO 'rootuser'@'localhost' WITH GRANT OPTION;"
    mysql -u root -p -e "FLUSH PRIVILEGES;"
    ```

This will create a user `rootuser` with the password `rootuser` and grant it full privileges on your MySQL instance. This user (`rootuser`) will be used throughout the project for database interaction.
