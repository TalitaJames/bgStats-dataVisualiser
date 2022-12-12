import pprint
import time
import argparse
import os
import pickle

import requests
import xmltodict, json

import datetime
import collections

import matplotlib.pyplot as plt
import numpy as np

import api_bgg

pp = pprint.PrettyPrinter(depth=3) # Formats the json print mesages to be easy read
raw_data = json.load(open("BGStatsExport/2022-12-12.json",encoding="utf8"))
verbose=False #How much information to print to the user


#TODO GET RID OF THIS
class BGStatsData:
    def __init__(self,yyyy=1970, mm=1, dd=1):
        
        #seperates the data into main categories
        self.challenges = raw_data['challenges']
        self.games = raw_data['games']
        self.groups = raw_data['groups']
        self.locations = raw_data['locations']
        self.players = raw_data['players']
        self.plays = raw_data['plays']
        self.timeLimitPlays(yyyy,mm,dd) # Sets the self.plays_timeLim list
        self.tags = raw_data['tags']
        self.userInfo = raw_data['userInfo'] 

    # time limits the plays to a range
    def timeLimitPlays(self, yyyy,mm,dd):
        
        self.plays_timeLim=[]
        timeRangeStart=datetime.datetime(yyyy, mm, dd) # This is the date to change the start date
        
        for i in range(len(self.plays)):
            gameTime=datetime.datetime.fromisoformat(self.plays[i]['playDate'])
            if (gameTime>timeRangeStart):
                self.plays_timeLim.append(self.plays[i])

    # finds the BGG ID from the stat ID
    def statIDtoBggID(self, statID):
        for i in range(len(self.games)):
            if self.games[i]['id'] == statID:
                BggID = self.games[i]['bggId']
                return BggID

    # gets a list of each game ID from the plays
    def plays_BggGameIDs(self):
        bggGameIDs=[]

        for i in range(len(self.plays_timeLim)):
            gameRefId= self.plays[i]['gameRefId']
            bggGameID=self.statIDtoBggID(gameRefId)
            bggGameIDs.append(bggGameID)
        return bggGameIDs
    
    def countOfMechanics(self):
        bggID_List=data.plays_BggGameIDs()
        gameMechanics_nested=[]
        gameCategories_nested=[]
        
        print("Getting the Games info! " + str(len(bggID_List)) + " Games to go!")
        
        for i in range(len(bggID_List)):
            try:
                time.sleep(0.75)
                if bggID_List[i] !=0:
                    specificGame=api_bgg.BGG_gameinfo(bggID_List[i])
                    gameMechanics_nested.append(specificGame.mechanics())
                    gameCategories_nested.append(specificGame.categories())
                print("done with game: ",i)
            except:
                print("Error for game number %i, BggID: %i" %(i, bggID_List[i]))
        
        
        print("\n\nAnd the data")
        
        # print(gameMechanics_nested)
        # print(gameCategories_nested) 
        
        gameMechanics_flat = [item for sublist in gameMechanics_nested for item in sublist]
        gameCategories_flat = [item for sublist in gameCategories_nested for item in sublist]
        
        # print(gameMechanics_flat)
        # print(gameCategories_flat)
        
        gameMechanics_count=collections.Counter(gameMechanics_flat)
        gameCategories_count=collections.Counter(gameCategories_flat)
        
        print(gameMechanics_count)
        print(gameCategories_count)
        
        plt.bar(range(len(gameMechanics_count)), list(gameMechanics_count.values()), align='center')
        plt.xticks(range(len(gameMechanics_count)), list(gameMechanics_count.keys()))
        plt.show()
        
        
        plt.bar(range(len(gameCategories_count)), list(gameCategories_count.values()), align='center')
        plt.xticks(range(len(gameCategories_count)), list(gameCategories_count.keys()))
        plt.show()
            
    
    def playerWinCount(self):       
        for k in range(len(self.players)): #for each player
            player={}
            
            playerRefId= self.players[k]['id']
            player.update({'name':self.players[k]['name']})
            player.update({'plays':0})
            player.update({'wins':0})
            player.update({'ID':playerRefId})
            player.update({'expected wins':0})
            
            playerList=[]
            
            for i in range(len(self.plays_timeLim)): #for each game
               
                for j in range(len(self.plays_timeLim[i]['playerScores'])): #for the players in that game
                    # print(f"\t\tplayer {j} of {len(self.plays_timeLim[i]['playerScores'])}") #Debug
                    
                    playerInfo=self.plays_timeLim[i]['playerScores'][j]
                    
                    if playerInfo['playerRefId'] == playerRefId: #if person K is in game i
                        player.update({'plays':player['plays']+1})
                        
                        playerCount=len(self.plays_timeLim[i]['playerScores'])
                    
                        if playerInfo['winner'] == True:
                            player.update({'wins':player['wins']+1})
                        
      
            # print("\t"+str(player))
            playerList.append(player)
                    
        return playerList

class game:
    def __init__(self, bgg_id, name=None):
        self.bgg_id = bgg_id
        
        self.plays = collections.defaultdict(int)
       
        if bgg_id == 0: #game isn't on BGG, has been manually added
            self.image = 'pictureAssets/none_game.png'
            self.mechanics = []
            self.name = name
            return

        r = requests.get(
            f'https://boardgamegeek.com/xmlapi2/thing?id={bgg_id}')
        
        game_dict = xmltodict.parse(r.text)['items']['item']
        
        self.image = game_dict['image']
        self.mechanics = [link['@value'] for link in game_dict['link']
                          if link['@type'] == 'boardgamemechanic']

        #most games have many names, some have one name
        try: self.name = game_dict['name'][0]['@value']
        except KeyError: self.name = game_dict['name']['@value']

class Player:
    def __init__(self, id, name, tags):
        self.id = id
        self.name = name
        self.plays = 0
        self.wins = 0
        self.tags=tags
        
    def __str__(self):
        return f"{self.name} (ID {self.id}) has P: {self.plays} W: {self.wins} and Tags: {self.tags}"

def loadPlayers(data):
    players = {}
    
    #go thru each human and create them as a person obj
    for count, human in enumerate(data['players']):
        human_id=human['id']
        tags=[]

                
        #TODO update code such that it works with tags
        try:
            tagRawData=human['tags']
        except KeyError:
            if verbose:  print(f"ERROR! No tags for {human['name']}")
            tagRawData=[]
        
        for tag in tagRawData:
            tadID=tag['tagRefId']
            
            for tagMain in data['tags']:
                
                if tadID==tagMain['id']:
                    tags.append(tagMain['name'])
        
        
        players[human_id] = Player(human_id, human['name'], tags)
        if verbose: print(f"Loaded {count+1}/{len(data['players'])} {human['name']} \t tags {tags}") 
        
        

    for gamePlay in data['plays']: #for each game
        for player in gamePlay['playerScores']: #for the players in that game
        
            # print(f"\tplayerID {player['playerRefId']} of {len(gamePlay['playerScores'])} ppl") #Debug
            
            players[player['playerRefId']].plays += 1 
            if player['winner'] == True: players[player['playerRefId']].wins +=1
    
    #save all the data for later use
    with open('dataExports/players.pickle', 'wb') as f:
        pickle.dump(players, f)
        
    print("Loading Players Done!\n")

def loadGames(data):
    pass

def parseData():
    global verbose
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--new', action='store_true')
    parser.add_argument('-in', '--input', type=str)
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    
    if args.new and os.path.exists('dataExports/'):
        os.removedirs('dataExports/')
    if not args.input:
        args.input = os.path.join(os.path.dirname(
            __file__), 'BGStatsExport/2022-12-12.json')
    verbose=args.verbose
    if verbose:
        print("\n verbose print statments on! \n")
    
    with open(args.input, 'r', encoding='UTF-8') as f:
        raw_data = json.load(f)

    # data=timeRange(raw_data) #TODO: create a time limiting function
    data=raw_data
    
    loadPlayers(data)

    
    return data


if __name__=='__main__':    
    print("------- Start")
    data=parseData()
    # pp.pprint(raw_data['tags'])
    print("------- Done")
    
    
    
 
            
    
    