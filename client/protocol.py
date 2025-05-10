
import pickle

MESSAGE_SIZE = 4096

def sendData(socket, payloadType, payload):

    dictionary = {
        "payloadType": payloadType,
        "payload": payload
    }

    socket.send(pickle.dumps(dictionary))

def receiveData(socket):
    message = pickle.loads(socket.recv(MESSAGE_SIZE))
    return message