
import struct

#####################################################################################


def encodeHeader(isFromServer, isResponse, sequence):
    header = sequence & 0x3fffffff
    if isFromServer:
        header += 0x80000000
    if isResponse:
        header += 0x40000000
    return struct.pack('<I', header)


def decodeHeader(data):
    [header] = struct.unpack('<I', data[0 : 4])
    return [header & 0x80000000, header & 0x40000000, header & 0x3fffffff]


def encodeInt32(size):
    return struct.pack('<I', size)


def decodeInt32(data):
    return struct.unpack('<I', data[0 : 4])[0]


def encodeWords(words):
    size = 0
    encodedWords = b''
    for word in words:
        strWord = str(word)
        encodedWords += encodeInt32(len(strWord))
        encodedWords += str.encode(strWord)
        encodedWords += b'\x00'
        size += len(strWord) + 5

    return size, encodedWords


def decodeWords(size, data):
    numWords = decodeInt32(data[0:])
    words = []
    offset = 0
    while offset < size:
        wordLen = decodeInt32(data[offset : offset + 4])
        word = data[offset + 4 : offset + 4 + wordLen]
        words.append(word.decode('ascii'))
        offset += wordLen + 5

    return words

###################################################################################

class RConPacket:

    # Check whether a byte array contains at least a complete packet
    def containsCompletePacket(byteArray):
        if len(byteArray) < 8:
            return False
        if len(byteArray) < decodeInt32(byteArray[4:8]):
            return False
        return True

    containsCompletePacket = staticmethod(containsCompletePacket)

    def createClientRequest(sequence, words):
        packet = RConPacket()
        packet.isFromServer = False
        packet.isResponse = False
        packet.sequence = sequence
        packet.words = words
        return packet

    createClientRequest = staticmethod(createClientRequest)

    def createClientResponse(sequence, words):
        packet = RConPacket()
        packet.isFromServer = True
        packet.isResponse = True
        packet.sequence = sequence
        packet.words = words
        return packet

    createClientResponse = staticmethod(createClientResponse)

    # Decode packet from a byte array
    def decode(byteArray):
        packet = RConPacket()
        [packet.isFromServer, packet.isResponse, packet.sequence] = decodeHeader(byteArray)
        packetSize = decodeInt32(byteArray[4:8])
        wordsSize = packetSize - 12
        packet.words = decodeWords(wordsSize, byteArray[12:])
        return packet, packetSize

    decode = staticmethod(decode)

    # Encode packet as a byte array
    def encode(self):
        encodedHeader = encodeHeader(self.isFromServer, self.isResponse, self.sequence)
        encodedNumWords = encodeInt32(len(self.words))
        [wordsSize, encodedWords] = encodeWords(self.words)
        encodedSize = encodeInt32(wordsSize + 12)
        return encodedHeader + encodedSize + encodedNumWords + encodedWords

    # Convert packet to human-readable string
    def __str__(self):

        result = ""

        if (self.isFromServer):
            result += "IsFromServer, "
        else:
            result += "IsFromClient, "

        if (self.isResponse):
            result += "Response, "
        else:
            result += "Request, "

        result += "Sequence: " + str(self.sequence)

        if self.words:
            result += " Words:"
            for word in self.words:
                result += "\"" + word + "\""

        return result
