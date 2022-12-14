from PIL import Image, ImageDraw, ImageFont 
import requests
import re
from io import BytesIO
import operator

import dataGathering
import plotting

fileFolder="pictureExports/"


# takes a list and returns a string 
# "1. data\n2. data" of the top x items in the list
def topX(list, x):
    string=""
    max=x
    if len(list)<x:
        max=len(list)
        
    for i in range(max):
        string += (f"{i+1}. {list[i]}\n")

    return string

def overview(playData):
    

    wingspan=Image.open('pictureAssets/blankDesigns_WingspanSquare.jpg')
    wingspanDraw = ImageDraw.Draw(wingspan)  
    
    #region Fonts
    font_heading=ImageFont.truetype('pictureAssets/fonts/BebasNeue-Regular.ttf', 850)
    font_subtext=ImageFont.truetype('pictureAssets/fonts/ThirstyRoughLtTwo.ttf', 320)
    font_text=ImageFont.truetype('pictureAssets/fonts/Shaky Hand Some Comic.ttf', 320)
    font_footer=ImageFont.truetype('pictureAssets/fonts/Shaky Hand Some Comic.ttf', 240)
                
    brown="#49423E"
    
    #endregion

    #region data
    playCount=len(playData)
        
    gamePlayList=[play.bgg_id for count, play in playData.items()]
        
    distinctGames = len(set(gamePlayList))
    #endregion

    wingspanDraw.text((wingspan.width//2,1100),'Games of 2022',fill='white',font=font_heading,anchor='ms')
    
    wingspanDraw.text((760,2900),f'{playCount} Games played',fill=brown,font=font_text)
    wingspanDraw.text((2700,4600),f'{distinctGames} Distinct Games',fill=brown,font=font_text)
    
    wingspanDraw.text((wingspan.width-100, wingspan.height-100), "TALITAJAMES.COM/BG", brown, font=font_footer, anchor='rs')


    wingspan.save('pictureExports/overview_wingspan.png')
    print("Saved overview_wingspan.png'\n")
    


def topGames(gameList):

    #region Fonts
    font_heading = ImageFont.truetype('pictureAssets/fonts/SlabSerHPLHS.ttf', 350)
    font_game = ImageFont.truetype('pictureAssets/fonts/SlabSerHPLHS.ttf', 300)
    font_subtext = ImageFont.truetype('pictureAssets/fonts/times-new-roman.ttf', 175)
    font_albedus = ImageFont.truetype('pictureAssets/fonts/times-new-roman-italic.ttf', 200)
    
    font_footer = ImageFont.truetype('pictureAssets/fonts/SlabSerHPLHS.ttf', 175)
    brown="#914233"
    #endregion
    
    intGames=4 #number of games to graph
    
    #create image
    potion=Image.open('pictureAssets/blankDesigns_PotionSquare.jpg')
    potionDraw = ImageDraw.Draw(potion)  
   
    #headint
    potionDraw.text((potion.width//2, 525), 'TOP GAMES PLAYED', brown, font=font_heading,anchor='ms')

    #footer
    potionDraw.text((potion.width-200,potion.height-150), "TALITAJAMES.COM/BG", brown, font=font_footer,anchor='rs')
    
    # coords for the 4 games (done by top right coner of game image)
    x1,y1,x2,y2=1200,1000,4300,2350
    titleOffset=300
    infoOffset=200
    position=[(x1,y1),(x2,y1),(x1,y2),(x2,y2)]
    colour=["#C9B037","#969696","#6A3805","#B3E5FC"] #gold, silver, bronze, hot pink
    
    #draw each four games
    for i in range(intGames):
        #paste the game image
            
        gameImageURL=gameList[i].image
        if gameList[i].bgg_id==0:
            gameImage = Image.open('pictureAssets/none_game.png')
        else:
            response = requests.get(gameImageURL)
            gameImage = Image.open(BytesIO(response.content))
            gameImage.save('pictureAssets/gameimage.png')
        
        imSize=950
        gameImage=gameImage.resize((imSize,imSize))
        potion.paste(gameImage, (position[i][0]-imSize,position[i][1]))
                
        #subtext  
        mechanics=gameList[i].mechanics
        mechanics=[(f'{x[:17]}...') if len(x)>20 else x for x in mechanics]
        mechanics_str="\n".join(mechanics[:4])
        # print(f" for {gameList[i].name} {mechanics_str}")
        
        potionDraw.multiline_text((position[i][0]+titleOffset//2-70,position[i][1]+infoOffset), mechanics_str, 'black', font=font_subtext,spacing=10,anchor='la')
        
        
        #draw meeple
        meeple=Image.open('pictureAssets/meeple.png')
        scale=0.27
        meeple=meeple.resize((int(scale*meeple.width),int(scale*meeple.height)))
        colourBG=Image.new('RGB', (meeple.width,meeple.height), colour[i])
        mx,my = -35,50
        potion.paste(colourBG, (position[i][0]-mx,position[i][1]-my), mask=meeple)
        
        #game name
        gameName=gameList[i].name
        gameNameClean = re.sub('^(the |a |an )', '', gameName, re.IGNORECASE)
        gameNameClean = gameNameClean if len(gameNameClean)<16 else f'{gameNameClean[:14]}...'
        potionDraw.text((position[i][0]+titleOffset, position[i][1] + meeple.height-my), 
                        gameNameClean, brown, font=font_game, anchor='ls')
    

    #region graph for albedus humblescore
    darkGreen="#265127"
    
    # x1,y1,x2,y2=945,3655,5800,4500
    # x1,y1,x2,y2=1700,3700,5741,5120
    # x3,y3= 959,3760 #top left corner of the speech bubble
    x1,y1,x2,y2=959,3700,5741,5120
    x3= 1700 #bottom left (far down) corner 
    
    
    # potionDraw.rectangle((x1,y1,x2,y2), fill='#E0FFE0') #to visualise the space
    playCountDataList=[gameList[i].plays for i in range(intGames)]
    playCountNameList=[gameList[i].name for i in range(intGames)]
    
    #text (game names on each bar)
    labelGameBar=[f"{playCountNameList[i]} ({playCountDataList[i]})" for i in range(intGames)]
    
    #load the picture
    graphDirectory=plotting.dataBarChart_png(playCountDataList, labelList=labelGameBar,
                                             barColour=darkGreen, countLabels=False,
                                             textLabels=True,flipAxis=True)
    graphPlayCount=Image.open(graphDirectory)
    
    #scale the image to fit in the box with corners of (x1,y1) and (x2,y2)
    width_final=x2-x1
    height_final=y2-y1
    wScale=width_final/graphPlayCount.width
    hScale=height_final/graphPlayCount.height
    scale=min(wScale,hScale)
    
    #keep aspect ratio
    graphPlayCount=graphPlayCount.resize((int(scale*graphPlayCount.width),int(scale*graphPlayCount.height)))
    
    #warp graph to best fill
    # graphPlayCount=graphPlayCount.resize((int(wScale*graphPlayCount.width),int(hScale*graphPlayCount.height)))
    
    #paste the graph in
    potion.paste(graphPlayCount, (x1+width_final-graphPlayCount.width,y1+height_final-graphPlayCount.height), mask=graphPlayCount)    
    potionDraw.text((x3,y2-450), 'Play\nCount\nGrap'.upper(), darkGreen, font=font_albedus, anchor='ls')
    
    #endregion
        
    fileName='topGames_potion.png'
    potion.save(f'{fileFolder}/{fileName}')
    print(f"Saved '{fileName}'")


def topComponents(playDict, gameDict, sorter='mechanics'):
    
    #region fonts
    font_heading = ImageFont.truetype('pictureAssets/fonts/Algerian-Regular.ttf', 400)
    font_text = ImageFont.truetype('pictureAssets/fonts/Cambria.ttf', 220)
    
    font_footer = ImageFont.truetype('pictureAssets/fonts/Algerian-Regular.ttf', 175)
    #endregion
    
    sortingChar=operator.attrgetter(sorter)
    
    #region component count
    componentCount={}
    
    for play in playDict.values():
        gameId=play.gameRefId
        
        game=gameDict[gameId]
        component=sortingChar(game)
        # print(f"\t{sorter} for {game.name}: {component}")
        
        for mech in component:
            componentCount.update({mech:1+int(componentCount.get(mech) or 0)})
    
    mechanicCountList = [mechanism for mechanism in componentCount.keys()]
    mechanicCountList.sort(key=lambda x: componentCount[x], reverse=True)
    
        
    #endregion
    
    #create and heading image
    azulSquare = Image.open('pictureAssets/blankDesigns_AzulSquare.jpg')
    azulSquareDraw = ImageDraw.Draw(azulSquare) 
    azulSquareDraw.text((2270,1050), f'TOP {sorter}','black', font=font_heading)  #link
         
    
    positions = [(1500,1740),(2300,2375),(3250,3300),(1500,3850),(3050,4750)]
    for i, pos in enumerate(positions):
        azulSquareDraw.text(pos, mechanicCountList[i],'black', font=font_text)  #link
        
    #footer   
    azulSquareDraw.text((azulSquare.width-100, azulSquare.height-100), "TALITAJAMES.COM/BG", 'black', font=font_footer, anchor='rs')  #link

    fileName=f"top{sorter.title()}_azul.png"
    azulSquare.save(f"{fileFolder}{fileName}")
    print(f"Saved '{fileName}'")
    

def topPlayers(playerDict, sorter='wins'):
    
    try: playerDict.pop(1) #get rid of anonymous player
    except KeyError: pass
    
    playerList = [player for player in playerDict.values()]
    sortingChar=operator.attrgetter(sorter)
    playerList=sorted(playerList, key= lambda x: sortingChar(x), reverse=True)
    
    
    # playerList.sort(key=lambda x: x.plays, reverse=True)
    
    #region fonts
    # font_heading = ImageFont.truetype('pictureAssets/fonts/Algerian-Regular.ttf', 400)
    font_text = ImageFont.truetype('pictureAssets/fonts/CMU-Roman.ttf', 300)
    font_subtext = ImageFont.truetype('pictureAssets/fonts/CMU-Roman.ttf', 150)
    
    font_footer = ImageFont.truetype('pictureAssets/fonts/CMU-Roman.ttf', 175)
    #endregion
    
    #create and heading image
    cryptidSquare = Image.open('pictureAssets/blankDesigns_CryptidSquare.jpg')
    cryptidSquareDraw = ImageDraw.Draw(cryptidSquare) 
    # cryptidSquareDraw.text((2270,1050), 'TOP MECHANICS','black', font=font_heading)  #link

    #create top players string
    numTop=5
    maxLines=numTop
    if len(playerList)<numTop:
        maxLines=len(playerList)


    xi,yi=2700,1875 #initial coordinates for the names
    barScale = max([playerList[0].wins, playerList[0].plays]) #largest value to scale the data by
    
    for i in range(maxLines):
        y=yi+730*i
        x=xi
        yo=y+320
        
        #make the text
        playerNameText=f"{i+1}. {playerList[i].name if len(playerList[i].name) < 17 else f'{playerList[i].name[:15]}...'}"
        cryptidSquareDraw.text((x,y), playerNameText,'black', font=font_text)
        
        #plot their plays/wins on a bar chart
        imageDirectory=plotting.singlePlayerBarChart_png(playerList[i], barScale, playColour='#3B173D',winColour='#257CBF')
        barChart=Image.open(imageDirectory)
        scale=1
        barChart=barChart.resize((int(scale*barChart.width),int(scale*barChart.height)))
        cryptidSquare.paste(barChart,(x,yo), mask=barChart)
    
    #subtext
    cryptidSquareDraw.multiline_text((xi-12,yi+475), "Plays\nWins",'black', font=font_subtext, anchor='rm')
    cryptidSquareDraw.text((2463,1725), f"By {sorter[:-1]} count",'black', font=font_subtext, anchor='lt')
   
        
    #footer   
    cryptidSquareDraw.text((cryptidSquare.width-100, cryptidSquare.height-100), "TALITAJAMES.COM/BG", 'black', font=font_footer, anchor='rs')  #link

    fileName=f"topPlayers_{sorter}_cryptid.png"
    cryptidSquare.save(f'{fileFolder}{fileName}')
    print(f"Saved '{fileName}'")



# gets data, sorts it, then creates images
def genPhotos():
    #region data import
    playerDict, gameDict, playDict = dataGathering.parseData()
        
    #games sorted by play count
    gameList = [game for game in gameDict.values()]
    gameList.sort(key=lambda x: x.plays, reverse=True)
    
    #players sorted by play count then win count
    playerCountList = [player for player in playerDict.values()]
    
    playerCountList.sort(key=lambda x: x.plays, reverse=True)
    
    #endregion
        
    print("***** Generating photos *****")
    overview(playDict)
    topPlayers(playerDict, sorter='plays')  
    topPlayers(playerDict, sorter='wins')  
    topComponents(playDict, gameDict, sorter="mechanics")
    topComponents(playDict, gameDict, sorter="categories")
    topGames(gameList)
    print("\n***** Photos are Done *****")
    


if __name__=='__main__':    
    print("***** Start *****")
    if True: #standard task, else run data for manipluation
        genPhotos()
    else:
        playerData, gameData, playData = dataGathering.parseData()
        print(playerData[4])
    
    
    
    print("***** DONE *****\n\n")
   