import numpy as np
import matplotlib.pyplot as plt

import pprint
import operator
import re

import dataGathering

pp = pprint.PrettyPrinter(depth=2) # Formats the json print mesages to be easy read
verbose=False

# For each tag, counts the number of plays, then graphs the data as a barchart
def tagBarChart(playerData):
    tagCounts={}
    for player in playerData.values():
        if player.id==2: continue # skip me because i am in all the groups
        else:
            for tag in player.tags:
                try: tagCounts[tag] += player.plays
                except KeyError: tagCounts[tag] = player.plays
    if verbose: pp.pprint(tagCounts)
    
    #region remove doxing groups
    if False:
        tagCounts.pop('Revive')
        tagCounts.pop('HopeUC')
        tagCounts['Comunity Games'] = tagCounts.pop('Game On!')
        tagCounts.update({'Comunity Games': tagCounts['Comunity Games']+tagCounts['CCLC Games']})
        tagCounts.pop('CCLC Games')
        tagCounts['Housemates'] = tagCounts.pop('Arundel')
        tagCounts['Uni Games'] = tagCounts.pop('Sutekh')
        
        # tagCounts.update({'Extended Family': tagCounts['Extended Family']-tagCounts['Family']})
    #endregion
    
    
    
    # creating the bar plot
    tags = list(tagCounts.keys())
    tags.sort(key=lambda x: tagCounts[x], reverse=True)
    tags = [tag[:] for tag in tags]
    
    playCounts = list(tagCounts.values())
    playCounts.sort(key=lambda x: x, reverse=True)
    
  
    # creating the bar plot
    plt.bar(tags, playCounts, color ='maroon',
            width = 0.5)
    plt.rcParams['savefig.dpi']=200
    plt.ylabel("Play count")
    plt.title("# of plays per group")
    
    plt.savefig('pictureExports/plotting_tagsBarChart.jpeg', bbox_inches='tight')
    print("\tFile 'plotting_tagsBarChart.jpeg' has been saved")
    

def playerBarChart(playerData, playSort=True):
    # sorts either by play count (playSort=True) or win count (playSort=False)
    playerIDs=[player.id for player in playerData.values()]
    
    if playSort:
        playerNumbers=[player.plays for player in playerData.values()]
        playerIDs.sort(key=lambda x: playerData[x].plays, reverse=True)
    else:
        playerNumbers=[player.wins for player in playerData.values()]
        playerIDs.sort(key=lambda x: playerData[x].wins, reverse=True)
        pass 
        
    playerNumbers.sort(key=lambda x: x, reverse=True)
    playerNames= [playerData[ID].name for ID in playerIDs]
    
    # creating the bar plot
    plt.bar(playerNames, playerNumbers, color ='maroon',
            width = 0.5)
    
    plt.ylabel("Play count",fontweight ='bold', fontsize = 15)
    plt.title(f"# of {'plays' if playSort else 'wins'} per person")
    plt.show()
    
    
def multiPlayerBarChart_jpeg(playerData, sorter='plays'):
    playerData.pop(1) # remove anonomous players
    
    #sort the data
    
    sortedPlayer=[player for player in playerData.values()]
    sortingChar=operator.attrgetter(sorter)
    sortedPlayers=sorted(sortedPlayer, key= lambda x: sortingChar(x), reverse=True)
    
    # turn the data into lists
    playerNames=[player.name for player in sortedPlayers]
    playerPlayCount=[player.plays for player in sortedPlayers]
    playerWinCount=[player.wins for player in sortedPlayers]
    
    #make the data into a shorter list
    pRange=7 # end range
    sRange=0 # start range (0 for all, 1 to get of me)
    plays = playerPlayCount[sRange:pRange]
    wins = playerWinCount[sRange:pRange]
    names = playerNames[sRange:pRange]
    firstNames=[re.split(' ', name)[0] for name in names]
    
    
    barWidth=0.25
    
    # # Set posplaysion of bar on X axis
    bar1 = np.arange(len(plays))
    bar2 = [x + barWidth for x in bar1]

    
    fig, ax = plt.subplots()
    ax.barh(bar1, plays, color ='r', label ='plays', height=barWidth)
    ax.barh(bar2, wins, color ='g', label ='wins',  height=barWidth)
    
    
    # Removes the borders of the plot
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    
    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 0)
    ax.yaxis.set_tick_params(pad = 2)
    ax.set_yticks(bar1, firstNames)
    
    # Add x, y gridlines    
    ax.grid(visible = True, color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)
    
    # Put top values on top
    ax.invert_yaxis()
    
    
    # Add numbers lables annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+1, i.get_y()+i.get_height()/2,
                str(round((i.get_width()), 2)),
                fontsize = 10, fontweight ='bold',  
                color ='black', va='center')
    
    # Add Plot Title
    plt.title(f"Top {pRange-sRange} players sorted by {sorter}", loc ='left')
  
    plt.legend()
    plt.savefig('pictureExports/plotting_playerData.jpeg')
    print("\tFile 'plotting_playerData.jpeg' has been saved")
 
    
def multiPlayerBarChart_png(playerData, sorter='plays', playColour='r', winColour='b', textColour='black'):
    try: playerData.pop(1) # remove anonomous players
    except: pass
    
    #sort the data
    sortedPlayer=[player for player in playerData.values()]
    sortingChar=operator.attrgetter(sorter)
    sortedPlayers=sorted(sortedPlayer, key= lambda x: sortingChar(x), reverse=True)
    
    
    # turn the data into lists
    playerPlayCount=[player.plays for player in sortedPlayers]
    playerWinCount=[player.wins for player in sortedPlayers]
    
    #make the data into a shorter list
    pRange=7 # end range
    sRange=0 # start range (0 for all, 1 to get of me)
    plays = playerPlayCount[sRange:pRange]
    wins = playerWinCount[sRange:pRange]
    
    barWidth=0.25
    
    # # Set posplaysion of bar on X axis
    bar1 = np.arange(len(plays))
    bar2 = [x + barWidth for x in bar1]
    
    fig, ax = plt.subplots()
    ax.barh(bar1, plays, color = playColour, label ='plays', height=barWidth)
    ax.barh(bar2, wins, color = winColour, label ='wins',  height=barWidth)
    
    
    # Removes the borders of the plot
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    
    plt.axis('off')
    
    ax.grid(visible = False) # hides x,y gridlines
    ax.invert_yaxis() # Put top values on top
    
    
    # Add numbers lables annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+1, i.get_y()+i.get_height()/2,
                str(round((i.get_width()), 2)),
                fontsize = 10, 
                color = textColour, va='center')
    
  
    plt.savefig('pictureExports/plotting_playerData.png', bbox_inches='tight',transparent=True)
    print("\tFile 'plotting_playerData.png' has been saved")
        
        
def singlePlayerBarChart_png(playerOBJ, scale, playColour='r', winColour='b', textColour='black'):
    
    plays = playerOBJ.plays
    wins = playerOBJ.wins
    
    
    barWidth=0.5
    
    # Set posion of bar on Y axis
    bar1 = 1
    bar2 = bar1 + barWidth
    
    fig, ax = plt.subplots(figsize=(20, 2))
    
    ax.barh(bar1, plays, color = playColour, label ='plays', height=barWidth)
    ax.barh(bar2, wins, color = winColour, label ='wins',  height=barWidth)
    
    
    #region make the grid background all blank
    visible = False # True for testing
    # Removes the borders of the plot
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(visible)    
   
    ax.grid(visible = visible) # hides x,y gridlines
    ax.invert_yaxis() # Put player values on top
    plt.axis(f"{'on' if visible else 'off'}")
    #endregion

    # Add number of win/plays to bars
    for i in ax.patches:
        plt.text(i.get_width()+1, i.get_y()+i.get_height()/2+0.05,
                str(round((i.get_width()), 2)),
                fontsize = 50, 
                color = textColour, va='center')

    
    plt.xlim(0, scale)
    plt.rcParams['savefig.dpi']=200 # higher number = higher quality
  
    plt.savefig('pictureExports/plotting_singlePlayerBarChart.png', bbox_inches='tight',transparent = not visible)
    print(f"\tFile 'plotting_singlePlayerBarChart.png' has been saved for {playerOBJ.name}")


# TODO work out what time i play the most games
def playTime():
    pass

# FIXME
def estWinCount(playerData, playData):
    allPlayers={}
    for player in playerData.values():
        gamesList=player.gamesList
        expectedWinMulti=0
        expectedWinPlus=0
        for UUID in gamesList:
            playerCount=len(playData[UUID].players)
            expectedWinMulti*=1/playerCount
            expectedWinPlus+=1/playerCount
        allPlayers.update({player.name: (expectedWinMulti, expectedWinPlus)})
    
    return allPlayers


if __name__=='__main__':
    print("***** Startint plotiong *****")
    playerData, gameData, playData = dataGathering.parseData()
    
    tagBarChart(playerData)
    multiPlayerBarChart_jpeg(playerData, sorter='wins')
    multiPlayerBarChart_png(playerData, sorter='plays')
    
    
    fakePerson=dataGathering.Player(22, 'Annie Easly',[])
    fakePerson.plays=67
    fakePerson.wins=36
    
    singlePlayerBarChart_png(fakePerson,100) 
   