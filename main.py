import socket as s
import json
import time


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
	
	socket.close()
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
	port = 7001

	print("Start...")

	response = fetch(('192.168.1.60', 3000), {
		"request": "subscribe",
		"port": port,
		"name": "fun_name_for_the_client",
		"matricules": ["12345", "67890"]
	})

	socket = s.socket(s.AF_INET, s.SOCK_STREAM)
	
	try:
		socket.bind(('192.168.1.60', port))
	except s.error as e:
		print(e)
	
	print("Waiting for ping...")

	socket.listen(5)

	c, addr = socket.accept()
	print("got connection from", addr)
	sendJSON(c, {"response":"pong"})
	c.close()

	print("End...")