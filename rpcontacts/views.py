# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""

from datetime import date
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QLabel

)
from .model import ContactsModel, InventoryModel, SalesModel

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Main Menu")
        self.resize(800, 500)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.inventoryModel = InventoryModel()
        self.contactsModel = ContactsModel()
        self.salesModel = SalesModel()
        self.inventorySetupUI()
        self.cursor = QSqlQuery()
        

    def initWindow(self):
        # Create buttons
        self.inventoryButton = QPushButton("Inventory")
        self.contactsButton = QPushButton("Contacts")
        self.salesButton = QPushButton("Daily Sales")
        # Lay out the GUI...
        layout = QVBoxLayout()
        layout.addWidget(self.inventoryButton)
        self.inventoryButton.clicked.connect(self.inventorySetupUI)
        layout.addWidget(self.contactsButton)
        self.contactsButton.clicked.connect(self.contactsSetupUI)
        layout.addWidget(self.salesButton)
        self.salesButton.clicked.connect(self.salesSetupUI)
        self.layout.addLayout(layout)
        
    def contactsSetupUI(self):
        """Setup the main window's GUI."""

        self.setWindowTitle("Contacts")
        # Clear previous layout
        self.clearLayout()
        # Disable the buttons
        self.inventoryButton.setEnabled(True)
        self.contactsButton.setEnabled(False)
        self.salesButton.setEnabled(True)
        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        self.table.setColumnHidden(0, True)
        # Create buttons
        self.addButton = QPushButton("Add...")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteContact)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearContacts)
        # Lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def inventorySetupUI(self):
        """Setup the inventory window's GUI."""
        self.setWindowTitle("Inventory")
        # Clear previous layout
        self.clearLayout()
        # Disable button
        self.inventoryButton.setEnabled(False)
        self.contactsButton.setEnabled(True)
        self.salesButton.setEnabled(True)
        # Create the inventory table view widget
        self.table = QTableView()
        self.table.setModel(self.inventoryModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        self.table.setColumnHidden(0, True)
        # Create buttons
        self.addButton = QPushButton("Add...")
        self.addButton.clicked.connect(self.openAddDialog_i)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteOrder)
        self.clearAllButton = QPushButton("Paid")
        self.clearAllButton.clicked.connect(self.paid)
        # Lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def salesSetupUI(self):
        """Setup the sales window's GUI."""
        today = date.today()
        today = today.strftime("%b-%d-%Y")
        self.setWindowTitle(f"Sales for {today}")
        # Clear previous layout
        self.clearLayout()
        # Disable buton
        self.inventoryButton.setEnabled(True)
        self.contactsButton.setEnabled(True)
        self.salesButton.setEnabled(False)


        # Create the sales table
        self.salesTable = QTableView()
        self.salesTable.setModel(self.salesModel.model)
        self.salesTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.salesTable.resizeColumnsToContents()
        self.salesTable.setColumnHidden(0, True)
        r = self.salesTable.currentIndex()
        self.cursor.exec("select total from sales")
        x =[]
        z= 0
        while self.cursor.next():
            y = self.cursor.value(0)
            x.append(float(y))
        for i in x:
            z+=i
        self.totals = QLabel(f"Total: {round(z,2)}")
        # Lay out the GUI
        layout = QVBoxLayout()

        self.layout.addWidget(self.salesTable)
        self.layout.addWidget(self.totals)
        self.layout.addLayout(layout)



    def openAddDialog(self):
        """Open the Add Contact dialog."""
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()

    def openAddDialog_i(self):
        """Open the Add Contact dialog."""
        dialog = AddDialog_i(self)
        if dialog.exec() == QDialog.Accepted:
            self.inventoryModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()
            result = self.cursor.exec(f"select * from contacts where phone = '{dialog.c_data[1]}'")
            x =''
            while self.cursor.next():
                x = (self.cursor.value(0))
            if x == '':
                self.contactsModel.addContact(dialog.c_data)

    def deleteContact(self):
        """Delete the selected contact from the database."""
        row = self.table.currentIndex().row()
        if row < 0:
            return
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            f"Do you want to remove the selected contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.deleteContact(row)

    def deleteOrder(self):
            """Delete the selected row from the database."""
            row = self.table.currentIndex().row()
            r = self.table.currentIndex()
            x = ''
            x = r.sibling(row, 5).data()

            if row < 0:
                return
            if x == '':
                messageBox = QMessageBox.warning(
                    self,
                    "Warning!",
                    "Order is not Paid",
                    QMessageBox.Ok
                )

            else:
                messageBox = QMessageBox.warning(
                    self,
                    "Warning!",
                    "Do you want to remove the selected Order?",
                    QMessageBox.Ok | QMessageBox.Cancel,
                )

                if messageBox == QMessageBox.Ok:
                    self.inventoryModel.deleteContact(row)

    def paid(self):
        row = self.table.currentIndex().row()
        r = self.table.currentIndex()
        today = date.today()
        today = today.strftime("%b-%d-%Y")
        x = []
        y = r.sibling(row,0).data()
        self.cursor.exec(f"update inventory set datePaid = '{today}' where id = {y}")
        x.append(r.sibling(row, 1).data())
        x.append(r.sibling(row, 2).data())
        x.append(r.sibling(row, 4).data())
        if row < 0:
            return
        self.inventoryModel.updateModel()
        self.salesModel.addEntry(x)


    def clearContacts(self):
        """Remove all contacts from the database."""
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to Clear All",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.clearContacts()

    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.initWindow()



class AddDialog(QDialog):
    """Add Contact dialog."""
    def __init__(self, parent=None):

        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()


    def setupUI(self):
        """Setup the Add Contact dialog's GUI."""

        # Create line edits for data fields
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        self.phoneField = QLineEdit()
        self.phoneField.setObjectName("Phone")
        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Name:", self.nameField)
        layout.addRow("Phone:", self.phoneField)
        self.layout.addLayout(layout)
        # Add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """Accept the data provided through the dialog."""
        self.data = []
        s
        for field in (self.nameField, self.phoneField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}",
                )
                self.data = None  # Reset .data
                return

            self.data.append(field.text())

        if not self.data:
            return

        super().accept()


class AddDialog_i(QDialog):
    """Add Inventory dialog."""
    def __init__(self, parent=None):

        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Add Order")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.cursor = QSqlQuery()
        self.setupUI()


    def setupUI(self):
        """Setup the Add Order dialog's GUI."""

        # Create line edits for data fields
        self.orderField = QLineEdit()
        self.orderField.setObjectName("Order #")
        self.cursor.exec("SELECT orderNum FROM inventory ORDER BY ID DESC LIMIT 1")
        while self.cursor.next():
            y = int(self.cursor.value(0))
            y += 1
            self.orderField.setText(f"{y}")
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        self.phoneField = QLineEdit()
        self.phoneField.setObjectName("Phone")
        self.totalField = QLineEdit()
        self.totalField.setObjectName("Total")
        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Order #:", self.orderField)
        layout.addRow("Name:", self.nameField)
        layout.addRow("Phone:", self.phoneField)
        layout.addRow("Total:", self.totalField)
        self.layout.addLayout(layout)
        # Add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """Accept the data provided through the dialog."""
        self.data = []
        self.c_data = []
        phone = self.phoneField.text()
        if len(phone) == 10:
            phone = "("+phone[:3]+") "+phone[3:6]+"-"+phone[6:]
            self.phoneField.setText(phone)

        for field in (self.orderField, self.nameField, self.phoneField, self.totalField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a {field.objectName()}",
                )
                self.data = None  # Reset .data
                return

            self.data.append(field.text())

        if not self.data:
            return
        self.c_data.append(self.nameField.text())
        self.c_data.append(self.phoneField.text())
        super().accept()

