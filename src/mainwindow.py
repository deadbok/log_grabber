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
    QLabel, QLineEdit, QPlainTextEdit, QInputDialog, QMessageBox
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

        # Create the labels.
        ip_label = QLabel('Juniper IP address:')
        file_name_label = QLabel('Configuration file name:')
        config_label = QLabel('Configuration:')

        # Create the IP and file name edits.
        self.__ip_edit = QLineEdit()
        # self.ip_edit.setInputMask('000.000.000.000')
        self.__ip_edit.setPlaceholderText('127.0.0.1:22')
        self.__file_name_edit = QLineEdit()
        self.__file_name_edit.setPlaceholderText(
            'Leave empty to only view the config')

        # Create the configuration file view.
        self.__config_edit = QPlainTextEdit()
        # Do not allow editing the configuration.
        self.__config_edit.setReadOnly(True)

        # Create the buttons
        get_button = QPushButton("Get configuration")
        # Connect the get config button to the handler.
        get_button.clicked.connect(self.getConfigClicked)

        quit_button = QPushButton("Quit")
        # Close the window on clicking "Quit"
        quit_button.clicked.connect(self.close)

        # Create a grid layout
        grid = QGridLayout()
        grid.setSpacing(10)

        # Place the labels in the top row.
        grid.addWidget(ip_label, 0, 0, 1, 1)
        grid.addWidget(file_name_label, 0, 2, 1, 1)

        # Place the edit fields on the next line.
        grid.addWidget(self.__ip_edit, 1, 0, 1, 2)
        grid.addWidget(self.__file_name_edit, 1, 2, 1, 4)

        # Place the configuration view label on the next line.
        grid.addWidget(config_label, 2, 0)

        # Place the configuration view.
        grid.addWidget(self.__config_edit, 3, 0, 1, 6)

        # Place the buttons at the second row, with some cells between them for
        # spacing.
        grid.addWidget(get_button, 4, 3)
        grid.addWidget(quit_button, 4, 5)

        # Set the layout of this widget
        self.setLayout(grid)

        # Set title
        self.setWindowTitle('Juniper configuration snatcher')
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

    def getConfigClicked(self):
        pass