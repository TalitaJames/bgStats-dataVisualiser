import pprint
import time
import argparse
import os, shutil
import pickle

import requests
import xmltodict, json

import datetime
import collections

import matplotlib.pyplot as plt
import numpy as np

pp = pprint.PrettyPrinter(depth=2) # Formats the json print mesages to be easy read
verbose=False #How much information to print to the user
directory='dataExport/'

class Game:
    def __init__(self, bgg_id, name=None):
        self.bgg_id = bgg_id
        
        self.plays = 0
       
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
        self.categories = [link['@value'] for link in game_dict['link']
                          if link['@type'] == 'boardgamecategory']

        #most games have many names, some have one name
        try: self.name = game_dict['name'][0]['@value']
        except KeyError: self.name = game_dict['name']['@value']

class Play:
    def __init__(self, location, date, bgg_id, name, ignore, players):
        self.location = location
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') # eg "2022-12-14 10:00:00",
        self.bgg_id=bgg_id
        self.name=name
        self.ignore=ignore
        self.players=players # {ID: {name, playerOBJ, winnerBool}}
        
  
    def __str__(self):
        return f"{self.name} with ID: {self.bgg_id} played at {self.location} on {self.date} with {self.players}"

class Player:
    def __init__(self, id, name, tags):
        self.id = id
        self.name = name
        self.plays = 0
        self.wins = 0
        self.tags=tags
        self.gamesList=[]
        
    def __str__(self):
        return f"{self.name} (ID {self.id}) has P: {self.plays} W: {self.wins} and Tags: {self.tags}\n\t They have UUIDs of{self.gamesList}"

def padZeros(num, list):
    return f"{str(num).zfill(len(str(len(list))))}/{len(list)}"

def loadPlayers(data):
    global directory
    if os.path.exists(directory+'players.pickle'):
        with open(directory+'players.pickle', 'rb') as f:
            if verbose: print("\tLoaded player data from pickle")
            print("Loading Players Done!\n")
            return pickle.load(f)
    
    players = {}
    
    #go thru each human and create them as a person obj
    for count, human in enumerate(data['players']):
        human_id=human['id']
        tags=[]
                
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
        if verbose: print(f"\tLoaded {padZeros(count+1,data['players'])} {human['name']} \t tags {tags}") 
            
    # for each game update each players info (uuid, plays & wins)
    for gamePlay in data['plays']:
        UUID=gamePlay['uuid']
        if verbose: print(f"Game UUDI: {UUID}")
        for player in gamePlay['playerScores']:                     
            players[player['playerRefId']].plays += 1 
            players[player['playerRefId']].gamesList.append(UUID)
            if player['winner'] == True: players[player['playerRefId']].wins +=1
    
    
    #save all the data for later use
    with open(directory +'players.pickle', 'wb') as f:
        if verbose: print("Saved data")
        pickle.dump(players, f)
        
    print("Loading Players Done!\n")
    return players

def loadGames(data):
    global directory
    if os.path.exists(directory +'games.pickle'):
        with open(directory + 'games.pickle', 'rb') as f:
            if verbose: print(f"\tLoaded games from pickle")
            print("Loading Games Done!\n")
            return pickle.load(f)
    
    games={}
    gameMax=len(data['games'])
    
    for gameNum, game in enumerate(data['games']):
        
        games[game['id']] = Game(game['bggId'], game['name'])
        if verbose: print(f"\tLoaded {padZeros(gameNum+1,data['games'])}: {game['name']}")
        time.sleep(2) # so we don't overload the api w/ calls
    
    if verbose: print(f"\nCounting plays:")
    
    for i,gamePlay in enumerate(data['plays']):
        games[gamePlay['gameRefId']].plays += 1
        if verbose: print(f"\tGame {padZeros(i,data['plays'])}: {games[gamePlay['gameRefId']].name} has {games[gamePlay['gameRefId']].plays} plays")
    
    with open(directory + 'games.pickle', 'wb') as f:
        pickle.dump(games, f)
        if verbose: print(f"\tGames have been saved!")
    
    print("Loading Games Done!\n")
    return games

def loadLocations(data):
    global directory
    if os.path.exists(directory +'locations.pickle'):
        with open(directory + 'locations.pickle', 'rb') as f:
            if verbose: print(f"\tLoaded locations from pickle")
            print("Loading Locations Done!\n")
            return pickle.load(f)
    
    locations={}
    for num, location in enumerate(data['locations']):
        locations[location['id']]=location['name']
        if verbose: print(f"\tLoaded {padZeros(num+1, data['locations'])} {location['name']}")
      
    with open(directory + 'locations.pickle', 'wb') as f:
        pickle.dump(locations, f)
        if verbose: print(f"\tlocations have been saved!")  
        
    print("Loading Locations Done!\n")
    return locations
    
def loadPlays(data,locations,gameData):
    global directory
    if os.path.exists(directory +'plays.pickle'):
        with open(directory + 'plays.pickle', 'rb') as f:
            if verbose: print(f"\tLoaded plays from pickle")
            print("Loading Plays Done!\n")
            return pickle.load(f)
    
    plays={}
    
    for count, play in enumerate(data['plays']):
        try: location=locations[play['locationRefId']]
        except KeyError: location= None
        bgg_id=gameData[play['gameRefId']].bgg_id
        date=play['playDate']
        ignore=play['ignored']
        # name="NO WIFI"
        name=gameData[play['gameRefId']].name
        players={}
        for count2,person in enumerate(play['playerScores']):
            players[person['playerRefId']]={'score':person['score'],'winner':person['winner']}
            # if verbose: print(f"\t\tLoaded {padZeros(count2+1,play['playerScores'])}: ID:{person['playerRefId']} Score:{person['score']} Winner:{person['winner']}")

        plays[play['uuid']]=Play(location,date,bgg_id,name,ignore,players)

        
        if verbose: print(f"\tLoaded {padZeros(count+1,data['plays'])}: {name} bggID {bgg_id}\n")
    
    
    with open(directory + 'plays.pickle', 'wb') as f:
        pickle.dump(plays, f)
        if verbose: print(f"\tPlays have been saved!")
    
    print("Loading Plays Done!\n")
    return plays 


#limit the data to games played since the input argument date
def timeRange(data,timeRangeStart):
    timeLim_plays=[]
    originalLength=len(data['plays'])
    
    for play in (data['plays']):
        gameTime=datetime.datetime.fromisoformat(play['playDate'])
        
        
        if (gameTime>=timeRangeStart):
            timeLim_plays.append(play)
        
        if verbose: print(f"\tgame played at {gameTime.strftime('%c')} was {'ADDED' if gameTime>=timeRangeStart else 'REMOVED'}")
    
    data.update({'plays': timeLim_plays})
    
    print(f"Reduced to {len(data['plays'])} from {originalLength} plays\n")
        
    return data

def parseData():
    print("-------- Starting to parse data")
    global verbose, directory
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--new', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-in', '--input', type=str, help="the directory to the .json")
    parser.add_argument('-d', '--date', type=str, help="the date to limit the data by (DD/MM/YYYY)")
    args = parser.parse_args()
    
    verbose=args.verbose
    if verbose: print("Verbose print statments on! \n")
    
    if (args.new or args.date) and os.path.exists(directory):
        if verbose: print("Removing old data")
        shutil.rmtree(directory)
    
    # create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    
    # find the .json file (defults to a file named after todays date)
    if not args.input:
        if verbose: print("No input file specified, looking for todays file")
        today = datetime.datetime.now()
        dateString = today.strftime("%Y_%m_%d")
        if verbose: print(f" Looking for file named 'BGStatsExport/{dateString}.json'")
        
        assert os.path.exists(f'BGStatsExport/{dateString}.json'), f"\n\tNo file named 'BGStatsExport/{dateString}.json' found\n"
        args.input = os.path.join(os.path.dirname(__file__), f'BGStatsExport/{dateString}.json')
        
    
    
    # date to start counting data from
    if not args.date:
        dateLim=datetime.datetime(1970, 1, 1) #well before games were recorded
    else:
        dateList=args.date.split("/")
        dd=int(dateList[0])
        mm=int(dateList[1])
        yy=int(dateList[2])
        dateLim=datetime.datetime(yy, mm, dd) 
        
        if verbose: print(f"starting from {dd}/{mm}/{yy} \t{dateLim.date}")
        
    
    with open(args.input, 'r', encoding='UTF-8') as f:
        raw_data = json.load(f)

    if not os.path.exists(os.path.join(os.path.dirname(__file__), directory)):
        os.mkdir(os.path.join(os.path.dirname(__file__), directory))


    data=timeRange(raw_data, dateLim)
    
    playerData=loadPlayers(data)
    locationData=loadLocations(data)
    gameData=loadGames(data)
    playData=loadPlays(data,locationData,gameData)
    
    print("-------- Data has been parsed")
    return playerData, gameData, playData


if __name__=='__main__':    
    data=parseData()
    
    
    
 
            
    
    