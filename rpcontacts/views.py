# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""

from PyQt5.QtCore import Qt
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

)
from .model import ContactsModel, InventoryModel, SalesModel

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("RP Contacts")
        self.resize(550, 250)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.inventoryModel = InventoryModel()
        self.contactsModel = ContactsModel()
        self.salesModel = SalesModel()
        self.initWindow()

    def initWindow(self):
        # Create buttons
        self.inventoryButton = QPushButton("Inventory")
        self.contactsButton = QPushButton("Contacts")
        self.salesButton = QPushButton("Sales")
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
        # Create buttons
        self.addButton = QPushButton("Add...")
        self.addButton.clicked.connect(self.openAddDialog_i)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteOrder)
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

    def salesSetupUI(self):
        """Setup the sales window's GUI."""
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
        # Lay out the GUI
        layout = QVBoxLayout()
        self.layout.addWidget(self.salesTable)
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

    def deleteContact(self):
        """Delete the selected contact from the database."""
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.deleteContact(row)

    def deleteOrder(self):
            """Delete the selected contact from the database."""
            row = self.table.currentIndex().row()
            if row < 0:
                return

            messageBox = QMessageBox.warning(
                self,
                "Warning!",
                "Do you want to remove the selected contact?",
                QMessageBox.Ok | QMessageBox.Cancel,
            )

            if messageBox == QMessageBox.Ok:
                self.inventoryModel.deleteContact(row)


    def clearContacts(self):
        """Remove all contacts from the database."""
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all your contacts?",
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
        self.jobField = QLineEdit()
        self.jobField.setObjectName("Job")
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")
        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Name:", self.nameField)
        layout.addRow("Job:", self.jobField)
        layout.addRow("Email:", self.emailField)
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
        for field in (self.nameField, self.jobField, self.emailField):
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
        self.orderField = QLineEdit()
        self.orderField.setObjectName("Order")
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
        for field in (self.orderField, self.nameField, self.phoneField, self.totalField):
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

