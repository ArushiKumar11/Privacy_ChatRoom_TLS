

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QListWidget, QPushButton, QVBoxLayout
from protocol import sendData

class GroupInvite(QDialog):

    def __init__(self, socket, groupName):
        super().__init__()
        self.setModal(True)
        self.socket = socket
        self.groupName = groupName
        self.paintScreen()

        sendData(self.socket, "groups:inviteList", {
            "groupName": self.groupName
        })


    def paintScreen(self):
        self.setWindowTitle("Invite Friends")
        self.setFixedSize(250, 500)
        self.show()
        self.createLayout()


    def createLayout(self):
        rootVBox = QVBoxLayout()
        self.setLayout(rootVBox)

        inviteTitle = QLabel("Invite Clients", self)
        inviteTitle.setFont(QFont("Arial", 14))
        rootVBox.addWidget(inviteTitle)

        self.clientList = QListWidget()
        self.clientList.itemClicked.connect(self.onClientSelected)
        rootVBox.addWidget(self.clientList)

        inviteButton = QPushButton("Invite", self)
        inviteButton.clicked.connect(self.onInviteClick)
        rootVBox.addWidget(inviteButton)

    def addClientToList(self, client):
        self.clientList.addItem(client)

    def onClientSelected(self, client):
        self.selectedClient = client.text()

    def onInviteClick(self):
        try:

            sendData(self.socket, "groups:invite", {
                "groupName": self.groupName,
                "client": self.selectedClient
            })
            self.close()
        except Exception as e:
            pass