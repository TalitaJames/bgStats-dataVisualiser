import pprint
import json
import api_bgg
import time
import datetime
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np


pp = pprint.PrettyPrinter(depth=3) # Formats the json print mesages to be easy read


class BGStatsData:
    def __init__(self, filename,yyyy=1970, mm=1, dd=1):
        #loads the json file
        raw_data = json.load(open(filename,encoding="utf8"))
        
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
        
        gameMechanics_count=Counter(gameMechanics_flat)
        gameCategories_count=Counter(gameCategories_flat)
        
        print(gameMechanics_count)
        print(gameCategories_count)
        
        plt.bar(range(len(gameMechanics_count)), list(gameMechanics_count.values()), align='center')
        plt.xticks(range(len(gameMechanics_count)), list(gameMechanics_count.keys()))
        plt.show()
        
        
        plt.bar(range(len(gameCategories_count)), list(gameCategories_count.values()), align='center')
        plt.xticks(range(len(gameCategories_count)), list(gameCategories_count.keys()))
        plt.show()
            
    
    def playerWinCount(self):
        playerList=[]
        
        for k in range(len(self.players)):
            player={}
            
            playerRefId= self.players[k]['id']
            player.update({'name':self.players[k]['name']})
            player.update({'plays':0})
            player.update({'wins':0})
            
            for i in range(len(self.plays_timeLim)): #for each game
                # pp.pprint(self.plays_timeLim[i])
                
                for j in range(len(self.plays_timeLim[i]['playerScores'])): #for the players in that game
                    # print("\t\tplayer %i of %i" %(j,len(self.plays_timeLim[i]['playerScores']))) #Debug
                    
                    playerInfo=self.plays_timeLim[i]['playerScores'][j]
                    
                    
                    if playerInfo['playerRefId'] == playerRefId:
                        player.update({'plays':player['plays']+1})
                    
                        if playerInfo['winner'] == True:
                            player.update({'wins':player['wins']+1})
                
                # print("\t"+str(player))
            playerList.append(player)
                    
        pp.pprint(playerList)
                    
                    

        
        
        # pp.pprint(playerRefId)
        # for i in range(len(self.players)):
            
            
            # playerWinCount=self.statIDtoBggID(playerRefId)
            # playerWinCount.append(bggGameID)
        pass

def runData():
    data=BGStatsData('BGStatsExport.json')

    

if __name__=='__main__':
    print("hello world")
    
    data=BGStatsData('BGStatsExport.json')

    bggID_List=data.playerWinCount()
    
 
            
    
    