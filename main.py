import socket as s
import json
import time
import sys
import Abalone_V2 as av
import math


class NotAJSONObject(Exception):
	pass

class Timeout(Exception):
	pass


def sendJSON(socket, obj):
	"""
		Vérifie que l'objet est bien un JSON\n
		Le convertit en objet JSON et l'envoie vers l'adresse liée au socket
	"""

	message = json.dumps(obj)
	if message[0] != '{':
		raise NotAJSONObject('sendJSON support only JSON Object Type')
	message = message.encode('utf8')
	total = 0
	while total < len(message):
		sent = socket.send(message[total:])
		total += sent

def receiveJSON(socket, timeout = 1):
	"""
		Reçoit un socket et un timer, attend que le message soit reçu.\n
		Vérifie que le message est bien un JSON et le convertit.\n
		Retourne l'objet JSON.
	"""

	finished = False
	message = ''
	data = ''
	start = time.time()
	while not finished:
		message += socket.recv(4096).decode('utf8')
		if len(message) > 0 and message[0] != '{':
			raise NotAJSONObject('Received message is not a JSON Object')
		try:
			data = json.loads(message)
			finished = True
		except json.JSONDecodeError:
			if time.time() - start > timeout:
				raise Timeout()
	
	return data

def fetch(address, data, timeout=1):
	"""
	Utilise receiveJSON et sendJSON.\n
	Envoie un message vers l'adresse encodée.\n
	Attend un retour et renvoie la réponse.
	"""

	socket = s.socket()
	socket.connect(address)

	sendJSON(socket, data)
	response = receiveJSON(socket, timeout)
	return response


if __name__ == '__main__':
	port = int(sys.argv[1])

	print("Start...")

	response = fetch(('127.0.0.1', 3000), {
		"request": "subscribe",
		"port": port,
		"name": "zozo le donzo",
		"matricules": ["18332", "20324"]
	})

	socket = s.socket(s.AF_INET, s.SOCK_STREAM)
	
	try:
		socket.bind(('127.0.0.1', port))
	except s.error as e:
		print(e)
	
	print("Waiting for ping...")

	socket = s.socket(s.AF_INET, s.SOCK_STREAM)
	
	try:
		socket.bind(('127.0.0.1', port))
	except s.error as e:
		print(e)
	
	socket.listen()

	while True:
		client, addr = socket.accept()
		data = receiveJSON(client)

		if data["request"] == "ping":
			sendJSON(client, {"response":"pong"})
		elif data["request"] == "play":
			board = data["state"]["board"]
			currentPlayer = data["state"]["current"]

			if currentPlayer == 0:
				player = False
			else:
				player = True

			state = av.Board(board)
			score, move = av.minimax(state, 2, True, player, - math.inf, math.inf)

			print(move)

			sendJSON(client, {
				"response":"move",
				"move" : {
					"marbles": move[0],
					"direction": move[1]
				},
				"message":"il est tard"
			})

		client.close()