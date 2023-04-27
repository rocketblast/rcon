import logging

from .connection import SynchronousCommandConnection as ClientBase
import socket

import hashlib

class Client(ClientBase):
    class ClientException(Exception):
        pass

    def __init__(self, host=None, port=None, password=None, lock=None):
        ClientBase.__init__(self)

        self.__lock = lock

        if host and port:
            try:
                ClientBase.connect(self, host, port)
            except socket.error as x:
                logging.error(x)
                if x.errno == 10060:
                    raise Client.ClientException('Timeout')
                elif x.errno == 10061:
                    raise Client.ClientException('Refused')
                else:
                    raise Client.ClientException('Socket error {}'.format(x.errno))
            else:
                data = self.send(['version'])
                
                if password:
                    data = self.send(['login.hashed'])
                    #data = self.receive()

                    if data[0] == 'OK' and len(data) == 2:
                        data = self.send(['login.hashed', hashlib.md5(data[1].decode('hex') + password).hexdigest().upper()])
                        #data = self.receive()

                        if data[0] != 'OK':
                            raise Client.ClientException('Login failed')
                    else:
                        raise Client.ClientException('No valid response for command login.hashed')


    def send(self, words):
        try:
            if self.__lock:
                self.__lock.acquire()

            ClientBase.send(self, words)
        except socket.error as x:
            logging.error(x)
            if x.errno == 10057:
                raise Client.ClientException('Lost connection')
            if x.errno == 10060:
                raise Client.ClientException('Timeout')
            else:
                raise Client.ClientException('Socket error {}'.format(x.errno))
        else:
            try:
                return ClientBase.receive(self, 'response')
            except socket.error as x:
                logging.error(x)
                if x.errno == 10054:
                    raise Client.ClientException('Lost connection')
                if x.errno == 10060:
                    raise Client.ClientException('Timeout')
                else:
                    raise Client.ClientException('Socket error {}'.format(x.errno))
        finally:
            if self.__lock:
                self.__lock.release()

    def connected(self):
        return bool(self.socket)

    def listen(self):
        try:
            return ClientBase.receive(self, 'any')
        except socket.error as x:
            logging.error(x)
            if x.errno == 10054:
                raise Client.ClientException('Lost connection')
            if x.errno == 10060:
                raise Client.ClientException('Timeout')
            else:
                raise Client.ClientException('Socket error {}'.format(x.errno))

    def disconnect(self):
        ClientBase.disconnect(self)
        self = None






mapFromMOHBuildIdToRelease = {
    "576759" : "Open Beta R1",
    "582779" : "Open Beta R3",
    "586148" : "R4",
    "586627" : "R5",
    "586981" : "R6",
    "587960" : "R7",
    "592364" : "R8",
    "615937" : "R9",
    }

mapFromBFBC2BuildIdToRelease = {
    "581637": "R22",
    "584642": "R23",
    "593485": "R24",
    "602833": "R25",
    "609063": "R26",
    "617877": "R27",
    "621775": "R28",
    "638140": "R30",
}

mapFromBF3BuildIdToRelease = {
    "836535": "Open Beta RB",
    "868283": "Open Beta RC",
    "870420": "Open Beta RD",
    "872601": "Open Beta RE",
    "873274": "Open Beta RF",
    "877154": "Final R1",
    "879067": "Final R2",
    "879322": "Final R3",
    "879793": "Final R4",
    "881071": "Final R5",
    "882210": "Final R6",
    "883137": "Final R7",
    "883971": "Final R8",
    "886605": "Final R9",
    "888890": "Final R10",
    "892188": "Final R11",
    "893642": "Final R12",
    "893407": "Final R13",
    "894565": "Final R14",
    "895012": "Final R15",
    "895921": "Final R16",
    "896646": "Final R17",
    "902705": "Final R18",
    "903227": "Final R19",
    "926998": "Final R20",
    "933688": "Final R21",
    "940924": "Final R22",
    "948577": "Final R23",
    "951336": "Final R24",
    "951364": "Final R25",
    "964189": "Final R26",
    "972386": "Final R27",
    "981883": "Final R28",
    "1000930": "Final R29",
    "1009356": "Final R30",
    "1014305": "Final R31",
    "1028652": "Final R32",
    "1055290": "Final R33",
    "1066226": "Final R34",
    "1097264": "Final R35",
    "1125745": "Final R36",
    "1149977": "Final R38",
}


class FormatClient(Client):
    def __init__(self, host=None, port=None, password=None, lock=None):
        Client.__init__(self, host, port, password, lock)

        if self.connected():
            self.versioninfo(self.send(['version']))
            
    def versioninfo(self, data):
        if len(data) != 3 or data[0] != "OK":
            self.version = False, "Unknown", 0, "Unknown"
        else:
            # Hack
            if data[1] == 'BF3' and int(data[2]) == 0:
                self.version = True, 'BF4', 68690, 'Open Beta R1'
            elif data[1] == 'BF3' and int(data[2]) == 70517:
                self.version = True, 'BF4', int(data[2]), 'Open Beta R2'
            elif data[1] == 'BF4':
                self.version = True, 'BF4', int(data[2]), data[2]
            elif data[1] == 'BFHL':
                self.version = True, 'BFH', int(data[2]), data[2]
            elif data[1] == "MOH":
                if not data[2] in mapFromMOHBuildIdToRelease:
                    self.version = False, data[1], int(data[2]), "Unknown - " + data[2]
                else:
                    self.version = True, data[1], int(data[2]), mapFromMOHBuildIdToRelease[data[2]]
            elif data[1] == "BFBC2":
                if not data[2] in mapFromBFBC2BuildIdToRelease:
                    self.version = False, data[1], int(data[2]), "Unknown - " + data[2]
                else:
                    self.version = True, data[1], int(data[2]), mapFromBFBC2BuildIdToRelease[data[2]]
            elif data[1] == "BF" or data[1] == "BF3":
                if not data[2] in mapFromBF3BuildIdToRelease:
                    self.version = False, "BF3", int(data[2]), "Unknown - " + data[2]
                else:
                    self.version = True, "BF3", int(data[2]), mapFromBF3BuildIdToRelease[data[2]]
            else:
                self.version = False, "Unknown", 0, "Unknown - " + data[2]

        return self.version

    def serverinfo(self, data, version=None):
        [knownVersion, game, build, version] = version if version else (self.version if self.version else self.versioninfo([]))

        if knownVersion:
            if game in ['BF3', 'BF4', 'BFH']:
                if game == 'BF3' and build <= 868283:
                    indices = dict({
                        'serverName': 1,
                        'numPlayers': 2,
                        'currentLevel': 3,
                        'hasGamePassword': 4,
                        'serverUpTime': 5})
                elif game == 'BF3' and build == 870420:
                    indices = dict({
                        'serverName': 1,
                        'numPlayers': 2,
                        'maxPlayers': 3,
                        'currentLevel': 4,
                        'playList': 5,
                        'numTeamScores': 6})
                    
                    numTeamScores = data[6]
 
                    if numTeamScores > 0:
                        for teamScoreId in range(0, int(numTeamScores)):
                            indices['teamScore{0}'.format(teamScoreId)] = 7 + teamScoreId

                    offset = 7 + int(numTeamScores)

                    indices.update(dict({
                        'targetScore': offset + 0,
                        'ranked': offset + 1,
                        'punkBuster': offset + 2,
                        'hasGamePassword': offset + 3,
                        'serverUpTime': offset + 4,
                        'roundTime': offset + 5}))
                else:
                    offset = 0
                    indices = dict({
                        'serverName': 1,
                        'numPlayers': 2,
                        'maxPlayers': 3,
                        'playList': 4,
                        'currentLevel': 5,
                        'currentRound': 6,
                        'roundsTotal': 7,
                        'numTeamScores': 8})

                    # Trapping a known bug where the response does not contain
                    # team information due to the state changing map.
                    try:
                        numTeamScores = int(data[8])

                        if numTeamScores > 0:
                            for teamScoreId in range(0, int(numTeamScores)):
                                indices['teamScore{0}'.format(teamScoreId)] = 9 + teamScoreId

                            offset = 9 + int(numTeamScores)

                            indices.update(dict({
                                'targetScore': offset + 0,
                                'onlineState': offset + 1,
                                'ranked': offset + 2,
                                'punkBuster': offset + 3,
                                'hasGamePassword': offset + 4,
                                'serverUpTime': offset + 5,
                                'roundTime': offset + 6}))

                            offset = offset + 7

                    except ValueError:
                        offset = 9

                        indices.update(dict({
                            'ranked': offset + 0,
                            'punkBuster': offset + 1,
                            'hasGamePassword': offset + 2,
                            'serverUpTime': offset + 3,
                            'roundTime': offset + 4}))

                        offset = 14
                    
                    if game == 'BF3' and build <= 886605:
                        pass
                    else:
                        indices.update(dict({
                            'gameIpAndPort': offset + 0,
                            'punkBusterVersion': offset + 1,
                            'joinQueueEnabled': offset + 2,
                            'region': offset + 3,
                            'closestPingSite': offset + 4,
                            'country': offset + 5}))

                        offset = 20
                        if game == 'BF4':
                            indices.update(dict({'matchMakingEnabled': offset + 0}))
                            offset = 21
                        indices.update(dict({
                            'blazePlayerCount': offset + 0,
                            'blazeGameState': offset + 1}))

            else:
                indices = dict({
                    'serverName': 1,
                    'numPlayers': 2,
                    'maxPlayers': 3,
                    'playList': 4,
                    'currentLevel': 5,
                    'currentRound': 6,
                    'roundsTotal': 7,
                    'numTeamScores': 8})

                if data is not None:

                    numTeamScores = data[8]
                    for teamScoreId in range(0, int(numTeamScores)):
                        indices['teamScore{0}'.format(teamScoreId)] = 9 + teamScoreId

                    offset = 9 + int(numTeamScores)
                        
                    indices.update(dict({
                        'targetScore': offset + 0,
                        'onlineState': offset + 1}))

                    if (game == "MOH" and build >= 592364) or (game == "BFBC2" and build >= 617877):
                        indices.update(dict({
                            'ranked': offset + 2,
                            'punkBuster': offset + 3,
                            'hasGamePassword': offset + 4,
                            'serverUpTime': offset + 5,
                            'roundTime': offset + 6}))
                    if game == "BFBC2" and build >= 617877:
                        indices.update(dict({
                            'gameMod': offset + 7,
                            'mapPack': offset + 8}))
                    if game == "BFBC2" and build >= 621775:
                        indices['externalGameIpAndPort'] = offset + 9

            if data is not None:
                values = indices.fromkeys(indices)
                for key, index in indices.items():
                    values[key] = data[index]

                return {'type': 'keys with values',
                        'values': values,
                        'indices': indices}
            else:
                return {'type': 'keys with indices',
                        'indices': indices}

    def formatplayers(self, data, version=None):
        [knownVersion, game, build, version] = version if version else (self.version if self.version else self.versioninfo([]))

        if knownVersion:
            if game in ['BF3', 'BF4', 'BFH']:
                if game == 'BF3' and build < 883971:
                    pass
                else:
                    if data is not None:
                        numValues = int(data[1])
                        numPlayers = int(data[2 + numValues])
                        if numPlayers > 0:
                            players = dict()

                            offset = 3 + numValues
                            for offset in range(offset, len(data), numValues):
                                players[data[offset]] = dict()
                                for valueOffset in range(0, numValues):
                                    try:
                                        # Always force names to be strings.
                                        if data[valueOffset + 2] == 'name':
                                            raise ValueError

                                        players[data[offset]][data[valueOffset + 2]] = int(data[offset + valueOffset])
                                    except ValueError:
                                        players[data[offset]][data[valueOffset + 2]] = data[offset + valueOffset]
                        else:
                            players = dict()

                            #offset = 3 + numValues
                            #for valueOffset in range(0, numValues):
                            #    try:
                            #        players[serverInfo[offset]][serverInfo[valueOffset + 2]] = None
                            #    except Exception as x:
                            #        print('ERROR {0}\n{1}'.format(x, serverInfo))

                        return dict({
                            "numValues": numValues,
                            "numPlayers": numPlayers,
                            "players": players})
