# -*- coding: utf-8 -*-
# rpcontacts/database.py


"""This module provides a database connection."""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def _createContactsTable():
    """Create the contacts table in the database."""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            job VARCHAR(50),
            email VARCHAR(40) NOT NULL
        )
        """
    )

def _createInventoryTable():
    """Create the contacts table in the database."""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            orderNum VARCHAR(40) NOT NULL,
            name VARCHAR(50) NOT NULL,
            phone VARCHAR(40),
            total VARCHAR(40) NOT NULL
        )
        """
    )

def _createSalesTable():
    """Creates sales table in the database."""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS sales (
            ordernum INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            total VARCHAR(40)
        )
        """
    )

def createAllTables():
    """Function that creates all tables from main once a connection is stablished"""
    _createContactsTable()
    _createSalesTable()
    _createInventoryTable()

def createConnection(databaseName):
    """Create and open a database connection."""
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():

        QMessageBox.warning(
            None,
            ""
            "project_db.sqlite",
            f"Database Error: {connection.lastError().text()}",

        )
        return False

    return True