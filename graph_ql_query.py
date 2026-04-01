import argparse
from queries import getEventId, getSets, getSetScore

parser = argparse.ArgumentParser(
    prog='Start.gg Bracket Win Gatherer',
    description='Gets number of wins per registered player in a start.gg bracket'
)

parser.add_argument('-e')
args = parser.parse_args()
print("Bracket URL: {}".format(args.e))
#bracketUrl = 'https://www.start.gg/tournament/mtl-underground-fridays-30/event/street-fighter-6-pc'
bracketUrl = args.e

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
    print(setDict[fSet['id']])
    for entrant in fSet['slots']:
        if entrant['entrant']['id'] not in players:
            #add entry to players dictionary, where player ID is the key and name is the value
            players[str(entrant['entrant']['id'])] = entrant['entrant']['name']
            
#Create and populate a dictionary of player scores, where the key is their start.gg id
dictPlayerScores = {}

for player in players:
    #print(players[player])
    dictPlayerScores[player] = 0
    
for _set in setDict:
    #id is the id for the player within the set, entrant id is the id for the player in start.gg (idk why this shit is different)
    setPlayers = {
        setDict[_set][0]['id'] : setDict[_set][0]['entrant']['id'],
        setDict[_set][1]['id'] : setDict[_set][1]['entrant']['id']
    }
    
    result = getSetScore(_set)
    player1 = ( result['set']['slots'][0]['id'], result['set']['slots'][0]['standing']['stats']['score']['value'] )
    player2 = ( result['set']['slots'][1]['id'], result['set']['slots'][1]['standing']['stats']['score']['value'] )
    
    #Check if win count is null or -1 (-1 is DQ, null means their opponent DQed)
    if player1[1] is None or player1[1] == -1:
        playerList = list(player1)
        playerList[1] = 0
        player1 = tuple(playerList)
    #Same check for player 2
    if player2[1] is None or player2[1] == -1:
        playerList = list(player2)
        playerList[1] = 0
        player2 = tuple(playerList)
        
    dictPlayerScores[str(setPlayers[player1[0]])] += player1[1]
    dictPlayerScores[str(setPlayers[player2[0]])] += player2[1]
    
for playerID in dictPlayerScores:
    print('{} : {}'.format(players[playerID], dictPlayerScores[playerID]))