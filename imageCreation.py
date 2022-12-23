from PIL import Image, ImageDraw, ImageFont 
import requests
from io import BytesIO
import operator

import dataGathering
import plotting

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
    font_game = ImageFont.truetype('pictureAssets/fonts/SlabSerHPLHS.ttf', 200)
    font_subtext = ImageFont.truetype('pictureAssets/fonts/times.ttf', 130)
    
    font_footer = ImageFont.truetype('pictureAssets/fonts/SlabSerHPLHS.ttf', 175)
    brown="#914233"
    #endregion
    
    potion=Image.open('pictureAssets/blankDesigns_PotionSquare.jpg')
    potionDraw = ImageDraw.Draw(potion)  
   
    potionDraw.text((potion.width//2, 525), 'TOP GAMES PLAYED', brown, font=font_heading,anchor='ms')

    #footer
    potionDraw.text((potion.width-200,potion.height-150), "TALITAJAMES.COM/BG", brown, font=font_footer,anchor='rs')
    
    x1,y1,x2,y2=1050,1000,4050,2250
    titleOffset=300
    infoOffset=190
    position=[(x1,y1),(x2,y1),(x1,y2),(x2,y2)]
    colour=["#C9B037","#969696","#6A3805","#FF00B3"] #gold, silver, bronze, hot pink
    
    for i in range(4):
        #region game images
            
        gameImageURL=gameList[i].image
        if gameList[i].bgg_id==0:
            gameImage = Image.open('pictureAssets/none_game.png')
        else:
            response = requests.get(gameImageURL)
            gameImage = Image.open(BytesIO(response.content))
            gameImage.save('pictureAssets/gameimage.png')
        
        imSize=750
        gameImage=gameImage.resize((imSize,imSize))
        potion.paste(gameImage, (position[i][0]-imSize,position[i][1]))
        
        #endregion
        
        #game name
        potionDraw.text((position[i][0]+titleOffset,position[i][1]), gameList[i].name, brown, font=font_game)
       
        #subtext  
        mechanics=gameList[i].mechanics
        mechanics_str="\n".join(mechanics[:4])
        # print(f" for {gameList[i].name} {mechanics_str}")
        
        potionDraw.multiline_text((position[i][0]+titleOffset//2,position[i][1]+infoOffset), mechanics_str, 'black', font=font_subtext,spacing=10,anchor='la')
        
        
        #draw meeple
        meeple=Image.open('pictureAssets/meeple.png')
        scale=0.27
        meeple=meeple.resize((int(scale*meeple.width),int(scale*meeple.height)))
        colourBG=Image.new('RGB', (meeple.width,meeple.height), colour[i])
        mx,my = -35,50
        potion.paste(colourBG, (position[i][0]-mx,position[i][1]-my), mask=meeple)
        
        

    potion.save('pictureExports/topGames_potion.png')
    print("Saved 'pictureExports/topGames_potion.png")


def topMechanics(gameList):
    
    #region fonts
    font_heading = ImageFont.truetype('pictureAssets/fonts/Algerian-Regular.ttf', 400)
    font_text = ImageFont.truetype('pictureAssets/fonts/Cambria.ttf', 220)
    
    font_footer = ImageFont.truetype('pictureAssets/fonts/Algerian-Regular.ttf', 175)
    #endregion
    
    
    #region mechanics count
    mechanicCount={}
    
    for game in gameList:
        mechanics=game.mechanics
        # print(f"mechanics for {game.name}: {mechanics}")
        for mech in mechanics:
            mechanicCount.update({mech:1+int(mechanicCount.get(mech) or 0)})
    
    mechanicCountList = [mechanism for mechanism in mechanicCount.keys()]
    mechanicCountList.sort(key=lambda x: mechanicCount[x], reverse=True)
    
        
    #endregion
    
    #create and heading image
    azulSquare = Image.open('pictureAssets/blankDesigns_AzulSquare.jpg')
    azulSquareDraw = ImageDraw.Draw(azulSquare) 
    azulSquareDraw.text((2270,1050), 'TOP MECHANICS','black', font=font_heading)  #link
         
    
    positions = [(1500,1740),(2300,2375),(3250,3300),(1500,3850),(3050,4750)]
    for i, pos in enumerate(positions):
        azulSquareDraw.text(pos, mechanicCountList[i],'black', font=font_text)  #link
        
    #footer   
    azulSquareDraw.text((azulSquare.width-100, azulSquare.height-100), "TALITAJAMES.COM/BG", 'black', font=font_footer, anchor='rs')  #link

        
    azulSquare.save('pictureExports/topMechanics_azul.png')
    print("Saved 'pictureExports/topMechanics_azul.png")
    
    
    


def topPlayers(playerDict, sorter='wins'):
    print(f"generating top players image")
    playerDict.pop(1) #get rid of anonymous player
    
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

    # #region create top players string
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
        plotting.singlePlayerBarChart_png(playerList[i], barScale, playColour='#3B173D',winColour='#257CBF')
        barChart=Image.open('pictureExports/plotting_singlePlayerBarChart.png')
        scale=1
        barChart=barChart.resize((int(scale*barChart.width),int(scale*barChart.height)))
        cryptidSquare.paste(barChart,(x,yo), mask=barChart)
    
    #subtext
    cryptidSquareDraw.multiline_text((xi-12,yi+475), "Plays\nWins",'black', font=font_subtext, anchor='rm')
    cryptidSquareDraw.text((2463,1725), f"By {sorter[:-1]} count",'black', font=font_subtext, anchor='lt')
   
        
    #footer   
    cryptidSquareDraw.text((cryptidSquare.width-100, cryptidSquare.height-100), "TALITAJAMES.COM/BG", 'black', font=font_footer, anchor='rs')  #link

        
    cryptidSquare.save('pictureExports/topPlayers_cryptid.png')
    print("Saved 'topPlayers_cryptid.png'\n")
    
    
    pass


# gets data, sorts it, then creates images
def genPhotos():
    #region data import
    playerData, gameData, playData = dataGathering.parseData()
        
    #games sorted by play count
    gameList = [game for game in gameData.values()]
    gameList.sort(key=lambda x: x.plays, reverse=True)
    
    #players sorted by play count then win count
    playerCountList = [player for player in playerData.values()]
    
    playerCountList.sort(key=lambda x: x.plays, reverse=True)
    
    #endregion
    
    #FIXME: player count and win count are the same
    
    print("***** Generating photos *****")
    # overview(playData)
    topPlayers(playerData)  
    # topMechanics(gameList)
    # topGames(gameList)
    print("***** Photos are Done *****")
    


if __name__=='__main__':    
    print("***** Start *****")
    if True: #standard task, else run data for manipluation
        genPhotos()
    else:
        playerData, gameData, playData = dataGathering.parseData()
        print(playerData[4])
    
    
    
    print("***** DONE *****\n\n")