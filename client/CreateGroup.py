
from protocol import *
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

class CreateGroup(QDialog):

    def __init__(self, socket, nickname):
        super().__init__()
        self.setModal(True)
        self.socket = socket
        self.nickname = nickname
        self.paintScreen()


    def paintScreen(self):
        self.setWindowTitle("Create Group")
        self.move(200, 200)
        self.setFixedSize(400, 100)
        self.show()
        self.createLayout()


    def createLayout(self):
        rootVBox = QVBoxLayout()
        self.setLayout(rootVBox)

        hbox = QHBoxLayout()
        rootVBox.addLayout(hbox)

        nameLabel = QLabel("Group Name", self)
        self.nameTextbox = QLineEdit(self)
        hbox.addWidget(nameLabel)
        hbox.addWidget(self.nameTextbox)

        createButton = QPushButton("Create", self)
        createButton.clicked.connect(self.onCreateGroupClick)
        rootVBox.addWidget(createButton)

    def onCreateGroupClick(self):

        # Check if the input field is not empty.
        if not self.nameTextbox.text() == "":
            try:

                sendData(self.socket, "groups:new", {
                    "groupName": self.nameTextbox.text(),
                    "creator": self.nickname
                })
                self.close()
            except:
                pass
