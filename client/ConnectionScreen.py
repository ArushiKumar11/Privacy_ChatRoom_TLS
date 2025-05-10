
import ssl
import socket
from PyQt5 import QtCore
from DashboardScreen import DashboardScreen
from PyQt5.QtWidgets import QLabel, QGridLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QWidget

class ConnectionScreen(QWidget):


    def __init__(self) -> None:
        super().__init__()
        self.paintScreen()


    def paintScreen(self):
        self.setWindowTitle("Setup Connection")
        self.move(200, 200)
        self.setFixedSize(400, 180)
        self.show()
        self.createLayout()


    def createLayout(self):
        grid = QGridLayout()
        hbox = QHBoxLayout()

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addLayout(hbox)
        
        ipAddressLabel = QLabel("IP Address", self)
        ipAddressLabel.setAlignment(QtCore.Qt.AlignRight)
        self.ipAddressTextbox = QLineEdit(self)
        self.ipAddressTextbox.setText("localhost")
        grid.addWidget(ipAddressLabel, 0, 0)
        grid.addWidget(self.ipAddressTextbox, 0, 1)

        portLabel = QLabel("Port", self)
        portLabel.setAlignment(QtCore.Qt.AlignRight)
        self.portTextbox = QLineEdit(self)
        self.portTextbox.setText("9988")
        grid.addWidget(portLabel, 1, 0)
        grid.addWidget(self.portTextbox, 1, 1)

        nicknameLabel = QLabel("Nick Name", self)
        nicknameLabel.setAlignment(QtCore.Qt.AlignRight)
        self.nicknameTextbox = QLineEdit(self)
        grid.addWidget(nicknameLabel, 2, 0)
        grid.addWidget(self.nicknameTextbox, 2, 1)

        connectButton = QPushButton("Connect", self)
        connectButton.clicked.connect(self.onConnectClick)
        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.close)
        hbox.addWidget(connectButton)
        hbox.addWidget(cancelButton)

        self.setLayout(vbox)

    def onConnectClick(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket = context.wrap_socket(mySocket, server_hostname=self.ipAddressTextbox.text())
            mySocket.connect((self.ipAddressTextbox.text(), int(self.portTextbox.text())))
            dashboard = DashboardScreen(mySocket, self.nicknameTextbox.text())
            dashboard.exec_()
            mySocket.close()
        except:
            return