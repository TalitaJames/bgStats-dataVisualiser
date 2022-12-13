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

pp = pprint.PrettyPrinter(depth=2) # Formats the json print mesages to be easy read
verbose=False #How much information to print to the user


class Game:
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
    if os.path.exists('dataExports/players.pickle'):
        with open('dataExports/players.pickle', 'rb') as f:
            if verbose: print("loaded data from pickle\n")
            print("Loading Players Done!\n")
            return pickle.load(f)
    
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
            
    # for each game update each players plays and wins 
    for gamePlay in data['plays']:
        for player in gamePlay['playerScores']:                     
            players[player['playerRefId']].plays += 1 
            if player['winner'] == True: players[player['playerRefId']].wins +=1
    
    #save all the data for later use
    with open('dataExports/players.pickle', 'wb') as f:
        if verbose: print("saved data")
        pickle.dump(players, f)
        
    print("Loading Players Done!\n")
    return players

def loadGames(data):
    if os.path.exists('dataExports/games.pickle'):
        with open('dataExports/games.pickle', 'rb') as f:
            if verbose: print(f"\tGames have loaded from save")
            return pickle.load(f)
    
    games={}
    gameMax=len(data['games'])
    
    for gameNum, game in enumerate(data['games']):
        # pp.pprint(game)
        
        newGame=Game(game['bggId'],game['name'])
        games[game['id']] = Game(game['bggId'], game['name'])
        if verbose: print(f"\tLoaded {str((gameNum+1)).zfill(len(str(gameMax)))}/{gameMax}: {game['name']}")
        time.sleep(2) # so we don't overload the api w/ calls
    
    
    with open('dataExports/games.pickle', 'wb') as f:
        pickle.dump(games, f)
        if verbose: print(f"\tGames have been saved!")
    
    print("Loading Games Done!")
    return games

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
    global verbose
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--new', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-in', '--input', type=str)
    parser.add_argument('-d', '--date', type=str)
    args = parser.parse_args()
    
    if args.new and os.path.exists('dataExports/'):
        os.removedirs('dataExports/')
    if not args.input:
        args.input = os.path.join(os.path.dirname(__file__), 'BGStatsExport/BGStatsExport-2022_12_12.json')
    verbose=args.verbose
    if verbose: print("Verbose print statments on! \n")
    if not args.date:
        date=datetime.datetime(1970, 1, 1) #well before games were recorded
    else:
        dateList=args.date.split("/")
        dd=int(dateList[0])
        mm=int(dateList[1])
        yy=int(dateList[2])
        date=datetime.datetime(yy, mm, dd) 
        
        if verbose: print(f"starting from {dd}/{mm}/{yy} \t{date.date}")
        
    
    with open(args.input, 'r', encoding='UTF-8') as f:
        raw_data = json.load(f)

    data=timeRange(raw_data, date)
    
    loadPlayers(data)
    loadGames(data) #TODO have this do things
    
    return data


if __name__=='__main__':    
    print("------- Start")
    
    data=parseData()
    # pp.pprint(raw_data['tags'])
    print("------- Done")
    
    
    
 
            
    
    