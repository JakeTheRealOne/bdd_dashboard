# 📦 Database Project

This project is written in Python and uses a graphical interface using PyQt5. It interacts with a MySQL database using the `mysql-connector-python` package.

## 👥 Members

- Bilal Vandenberge
- Lucas Verbeiren
- Ethan Van Ruyskensvelde
- Rares Radu-Loghin

## ✅ Prerequisites

Make sure you have Python 3 installed on your system:

```sh
python3 --version
```

## 📦 Installation

Install the required dependencies using `pip`:

```sh
pip install pyqt5 mysql-connector-python
```

## 🚀 Running the Application

You can run the program with:

```sh
python3 -m src.main
```

## 🛠️ Database Management Scripts

Three utility scripts are provided to manage the database:

### 📌 Create the database and its tables

```sh
python3 -m src.database.create
```

### 🗑️ Delete the database

```sh
python3 -m src.database.delete
```

### 📥 Insert data into the database

```sh
python3 -m src.database.insert
```

This script will populate the database using data from files in the `data/` folder.
