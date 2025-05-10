import ssl
import time
import socket
import threading
from protocol import *

port = 9988
hostname = "127.0.0.1"

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
context.load_verify_locations("cert.pem")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((hostname, port))
server.listen()
server = context.wrap_socket(server, server_side=True)

print(f"Status - Server starting on {hostname}:{port}.")

clientData = {}
clientSockets = {}
groups = {}

def sendToClient(nickname, payloadType, payload):
    socket = findClientSocket(nickname)
    sendData(socket, payloadType, payload)

def findClientSocket(nickname):
    for client in clientSockets:
        if clientSockets[client].get("nickname") == nickname:
            return client

def send1v1RequestToClient(request):
    name = request.get("receiver")
    sendToClient(name, "1v1:request", request)

def removeClient(clientSocket):
    nickname = clientSockets[clientSocket].get("nickname")
    print(f"Client is leaving: {nickname}")
    clientSockets.pop(clientSocket)
    clientData.pop(nickname)

def broadcast(payloadType, payload):
    for client in clientSockets:
        sendData(client, payloadType, payload)

def addClientToGroup(groupName, nickname):
    groups[groupName]["clients"].append(nickname)

def broadcastMessageToGroup(payloadType, payload):
    for client in groups[payload["groupName"]]["clients"]:
        socket = findClientSocket(client)
        sendData(socket, payloadType, payload)

def broadcastDashboardLists():
    broadcast("dashboard:update", {
        "users": clientData,
        "groups": groups
    })

def sendGroupInviteList(clientSocket, payload):
    joinedClients = groups[payload["groupName"]]["clients"]
    inviteList = []
    for client in clientData:
        if client not in joinedClients:
            inviteList.append(client)
    sendData(clientSocket, "groups:inviteList", {
        "clients": inviteList
    })

def sendGroupInvite(payload):
    clientSocket = findClientSocket(payload["client"])
    sendData(clientSocket, "groups:invite", {
        "groupName": payload["groupName"]
    })

def handle(clientSocket):
    request = receiveData(clientSocket)
    nickname = request["payload"].get("nickname")
    clientSockets[clientSocket] = {
        "nickname": nickname,
    }
    clientData[nickname] = {
        "joinTimestamp": int(time.time())
    }
    print(f"Added new client: {nickname}")
    broadcastDashboardLists()

    while True:
        try:
            payload = receiveData(clientSocket)
            payloadType = payload["payloadType"]
            print(payload)
            payload = payload["payload"]

            if payloadType == "users:leave":
                removeClient(clientSocket)
                broadcastDashboardLists()
            elif payloadType == "1v1:request":
                send1v1RequestToClient(payload)
            elif payloadType == "1v1:accept" or payloadType == "1v1:decline":
                sendToClient(payload.get("initiator"), payloadType, payload)
            elif payloadType == "1v1:message":
                sendToClient(payload.get("to"), payloadType, payload)
            elif payloadType == "groups:new":
                payload["clients"] = []
                groups[payload["groupName"]] = payload
                broadcastDashboardLists()
            elif payloadType == "groups:join":
                addClientToGroup(payload["groupName"], nickname)
                broadcastMessageToGroup("groups:info", groups[payload["groupName"]])
                print(groups)
            elif payloadType == "groups:leave":
                groups[payload["groupName"]]["clients"].remove(nickname)
                broadcastMessageToGroup("groups:info", groups[payload["groupName"]])
                print(groups)
            elif payloadType == "groups:message":
                broadcastMessageToGroup("groups:message", payload)
            elif payloadType == "groups:inviteList":
                sendGroupInviteList(clientSocket, payload)
            elif payloadType == "groups:invite":
                sendGroupInvite(payload)
        except:
            return

def receive():
    while True:
        client, address = server.accept()
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
receive()
