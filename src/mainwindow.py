# -*- coding: utf-8 -*-
"""
Name: Juniper log grabber
Author: Martin Bo Kristensen Grønholdt, Rickie Ljungberg, Kasper Soelberg.
Version: 1.0 (2017-03-26)

Main window.
"""

import socket
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QApplication, \
    QLabel, QLineEdit, QPlainTextEdit, QInputDialog, QMessageBox, QTableWidget
from PyQt5.QtGui import QStandardItemModel
from paramiko.ssh_exception import AuthenticationException, \
    BadHostKeyException

from vjuniper import VJuniper


class MainWindow(QWidget):
    """
    Class encapsulates the main window.
    """

    def __init__(self):
        """
        Constructor, creates the UI.
        """
        # Call the parent constructor.
        super().__init__()

        # Create header labels for the table
        header_table_labels = ["Time", "Name", "Process", "Event", "Message"]
        # Create the labels.
        ip_label = QLabel('Juniper IP address:')
        search_pattern_label = QLabel('Search pattern:')

        # Create the IP and file name edits.
        self.__ip_edit = QLineEdit()
        # self.ip_edit.setInputMask('000.000.000.000')
        self.__ip_edit.setPlaceholderText('127.0.0.1:22')
        self.__search_pattern_edit = QLineEdit()
        self.__search_pattern_edit.setPlaceholderText(
            'Enter search pattern')

        # Create log table widget
        table_model = QStandardItemModel()
        table_model.setHorizontalHeaderLabels(header_table_labels)
        self.__log_table = QTableWidget(1, 5)
        self.__log_table.setModel(table_model)

        # Create the buttons
        get_button = QPushButton("Get logs")
        # Connect the get config button to the handler.
        get_button.clicked.connect(self.getLogsClicked)

        quit_button = QPushButton("Quit")
        # Close the window on clicking "Quit"
        quit_button.clicked.connect(self.close)

        # Create a grid layout
        grid = QGridLayout()
        grid.setSpacing(10)

        # Place the labels in the top row.
        grid.addWidget(ip_label, 0, 0, 1, 1)
        grid.addWidget(search_pattern_label, 0, 2, 1, 1)

        # Place the edit fields on the next line.
        grid.addWidget(self.__ip_edit, 1, 0, 1, 2)
        grid.addWidget(self.__search_pattern_edit, 1, 2, 1, 4)

        # Add log table to layout
        grid.addWidget(self.__log_table, 2, 0, 2, 6)
        # Place the buttons at the second row, with some cells between them for
        # spacing.
        grid.addWidget(get_button, 4, 3)
        grid.addWidget(quit_button, 4, 5)

        # Set the layout of this widget
        self.setLayout(grid)

        # Set title
        self.setWindowTitle('Log grabber')
        # Show window
        self.show()

        # Create the VSRX instance used to talk to the Juniper device.
        self.__vjuniper = VJuniper()

    def error(self, msg):
        """
        Open a message box for errors.
        :param msg: The error message.
        """
        # Create an instance.
        mb = QMessageBox()
        # Set the window title.
        mb.setWindowTitle('Error')
        # Set the window content text
        mb.setText(msg)
        # Show the message box.
        mb.exec()

    def getLogsClicked(self):
        """
        Get the logs from the router and show them in the GUI.
        """
        log_data = [
            ["Apr 11 10:27:25", "router1", "mgd[3606]", "UI_DBASE_LOGIN_EVENT", "User 'barbara' entering configuration mode"],
            ["Apr 11 10:32:22", "router1", "mgd[3606]", "UI_DBASE_LOGOUT_EVENT", "User 'barbara' exiting configuration mode"],
            ["Apr 11 11:36:15", "router1", "mgd[3606]", "UI_COMMIT", "User 'root' performed commit: no comment"],
            ["Apr 11 11:46:37", "router1", "mib2d[2905]", "SNMP_TRAP_LINK_DOWN", "ifIndex 82, ifAdminStatus up(1), ifOperStatus down(2), ifName at-1/0/0"]
        ]
