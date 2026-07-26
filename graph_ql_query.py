import argparse
from halo import Halo
from queries import getEventId, getSets, getSetScore
import csv

parser = argparse.ArgumentParser(
    prog='Start.gg Bracket Win Gatherer',
    description='Gets number of wins per registered player in a start.gg bracket'
)

parser.add_argument('url')
parser.add_argument('-o')
args = parser.parse_args()
print("Bracket URL: {}".format(args.url))
#bracketUrl = 'https://www.start.gg/tournament/mtl-underground-fridays-30/event/street-fighter-6-pc'
bracketUrl = args.url

#get the slug from the bracket URL
slug = bracketUrl.replace('https://www.start.gg/', '')

event = getEventId(slug)
eventID = event['event']['id']
print(event['event']['id'])

#get all sets for an event ID
allSets = getSets(eventID)

players = {}
setDict = {}

for fSet in allSets['event']['sets']['nodes']:
    #print(fSet)
    #populate the dictionary of all sets in the event, where the set ID is the key and the set data is the value
    setDict[fSet['id']] = fSet['slots']
    #print(setDict[fSet['id']])
    for entrant in fSet['slots']:
        if entrant['entrant']['id'] not in players:
            #add entry to players dictionary, where player ID is the key and name is the value
            players[str(entrant['entrant']['id'])] = entrant['entrant']['name'].encode("ascii", errors="ignore").decode()
            
#Create and populate a dictionary of player scores, where the key is their start.gg id
dictPlayerScores = {}

for player in players:
    #print(players[player])
    dictPlayerScores[player] = 0
    
spinner = Halo(text='Summing set scores...', spinner='dots')
spinner.start()

for _set in setDict:
    #id is the id for the player within the set, entrant id is the id for the player in start.gg (idk why this shit is different)
    #setPlayers = {
    #    setDict[_set][0]['id'] : setDict[_set][0]['entrant']['id'],
    #    setDict[_set][1]['id'] : setDict[_set][1]['entrant']['id']
    #}
    setPlayers = {}
    for set in setDict[_set]:
        setPlayers.update({set['id']:set['entrant']['id']})
    
    results = getSetScore(_set)
    _players = []
    #player1 = ( result['set']['slots'][0]['id'], result['set']['slots'][0]['standing']['stats']['score']['value'] )
    #player2 = ( result['set']['slots'][1]['id'], result['set']['slots'][1]['standing']['stats']['score']['value'] )
    for result in results['set']['slots']:
        if result['standing']['stats']['score']['value'] is None or result['standing']['stats']['score']['value'] == -1:
            _players.append((result['id'], 0))
        else:
            _players.append((result['id'], result['standing']['stats']['score']['value']))
    
    #Check if win count is null or -1 (-1 is DQ, null means their opponent DQed)
        
        
    #if player1[1] is None or player1[1] == -1:
    #    playerList = list(player1)
    #    playerList[1] = 0
    #    player1 = tuple(playerList)
    #Same check for player 2
    #if player2[1] is None or player2[1] == -1:
    #    playerList = list(player2)
    #    playerList[1] = 0
    #    player2 = tuple(playerList)
        
    #dictPlayerScores[str(setPlayers[player1[0]])] += player1[1]
    #dictPlayerScores[str(setPlayers[player2[0]])] += player2[1]
    for player in _players:
        dictPlayerScores[str(setPlayers[player[0]])] += player[1]

spinner.stop()

print('Total games won')
totalData = []
for playerID in dictPlayerScores:
    print('{} : {}'.format(players[playerID], dictPlayerScores[playerID]))
    totalData.append({'tag':players[playerID], 'points': dictPlayerScores[playerID]})
    if args.o:
        with open(args.o, 'w', newline='') as csvfile:
            fieldnames = ['tag', 'points']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(totalData)
        