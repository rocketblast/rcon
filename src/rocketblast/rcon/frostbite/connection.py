import logging
#
# This class can be used to talk to a MOH/BFBC2 game server. It can send commands to the server, and receive responses.
# When a receive is performed, the code will wait until a full packet is available.
# It is not suitable for sending commands and receiving events at the same time.
#

import socket
from packet import RConPacket

###################################################################################

class SynchronousCommandConnection:

	def __init__(self):
		self.socket = None
		
	def connect(self, host, port):

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((host, port))
		self.socket.setblocking(1)

		self.clientSequence = 0
		self.receiveBuffer = b''
		self.sentSequence = None

	def isconnected(self):
                if self.socket != None:
                        return True
                return False

	def disconnect(self):
		if self.socket != None:
			self.socket.close()
			self.socket = None

	# Wait until the local receive buffer contains a full packet (appending data from the network socket),
	# then split receive buffer into first packet and remaining buffer data

	def receive(self, what="response"):
		while True:
			while not RConPacket.containsCompletePacket(self.receiveBuffer):
                                self.receiveBuffer += self.socket.recv(4096)

                        [packet, packetSize] = RConPacket.decode(self.receiveBuffer)

			self.receiveBuffer = self.receiveBuffer[packetSize:len(self.receiveBuffer)]

                        if what == "response" and packet.isResponse and packet.sequence == self.sentSequence:
				return packet.words
                        elif what == "any":
                        #if not packet.isResponse:
                                response = RConPacket.createClientResponse(packet.sequence, packet.words)
                                self.socket.send(response.encode())

                                self.sentSequence = self.clientSequence
                                self.clientSequence = (self.clientSequence + 1) & 0x3fffffff

                                return packet.words
                        # Nytt slut
			#elif packet.isResponse and packet.sequence == self.sentSequence:
			#	return packet.words

	def send(self, words):

		request = RConPacket.createClientRequest(self.clientSequence, words)
		self.socket.send(request.encode())

		self.sentSequence = self.clientSequence
		self.clientSequence = (self.clientSequence + 1) & 0x3fffffff
