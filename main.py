import socket as s
import json
import time

class NotAJSONObject(Exception):
	pass


def sendJSON(socket, obj):
    message = json.dumps(obj)
    
    if message[0] != "{":
        raise NotAJSONObject('sendJSON support only JSON Object Type')
    
    message = message.encode('utf8')
    total = 0

    while total < len(message):
        sent = socket.send(message[total:])
        total += sent

def receiveJSON(socket, timeout=1):
    finished = False
    message = ""
    data = ""
    start = time.time()

    while not finished:
        message += socket.recv(4096).decode("utf8")

        if len(message) > 0 and message[0] != '{':
            raise NotAJSONObject("Received message is not a JSON Object")

        try:
            data = json.loads(message)
            finished = True
        except:
            if time.time() - start > timeout:
                raise TimeoutError()
    
    return data


subscribeData = '{ "request": "subscribe", "port": 7000, "name": "fun_name_for_the_client", "matricules": ["12345", "67890"] }'
pongData = '{ "response": "pong" }'

if __name__ == '__main__':
    SERVER_ADDRESS = ('127.0.0.1', 3000)
    CLIENT_ADDRESS = ('127.0.0.1', 7000)
    SUBSCRIPTION = json.loads(subscribeData)
    PONG = json.loads(pongData)

    socket = s.socket()
    socket.bind(CLIENT_ADDRESS)
    socket.connect(SERVER_ADDRESS)
    sendJSON(socket, SUBSCRIPTION)
    print(receiveJSON(socket))


    # message = ""
    # finished = False
    # while not finished:
    #     message += socket.recv(4096).decode("utf8")

    #     if len(message) > 0 and message[0] != '{':
    #         raise NotAJSONObject("Received message is not a JSON Object")
    
    # print(message)