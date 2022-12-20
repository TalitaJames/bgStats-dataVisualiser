from PIL import Image, ImageDraw, ImageFont 
import requests
from io import BytesIO
import dataGathering

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

def gamesWrapped():

    wrapped=Image.open('pictureAssets/spotifyWrapped_blank.jpg')
    wrappedDraw = ImageDraw.Draw(wrapped)  
    
    #region Fonts
    font = ImageFont.truetype('pictureAssets/fonts/Courier Prime.ttf', 50)
    font_heading = ImageFont.truetype('pictureAssets/fonts/Courier Prime.ttf', 40)
    font_big = ImageFont.truetype('pictureAssets/fonts/Courier Prime Bold.ttf', 60)
    font_year = ImageFont.truetype('pictureAssets/fonts/Courier Prime Bold.ttf', 112)
    #endregion
    
    wrappedDraw.text((40, 200), 'Games', 'white', font=font_year)
    
    wrappedDraw.rectangle([(265,242),(813,790)], fill ="green")

    
    
    # 2*height/3=1280
    players=["Talita James", "Elisa James", "Xander James", "Esther Whitehead", "Joel Donnelly", "Nigel James", "Zack Alloggia", "Aarom Riley"]
    playerTop5List=topX(players,5)
    
    wrappedDraw.text((100,1100),'Most Played',fill='white',font=font_big)
    wrappedDraw.multiline_text((100, 1175), playerTop5List, 'white', font=font, spacing=20)
    
    wrappedDraw.text((570,1100),'Game Played',fill='white',font=font_big)
    # wrappedDraw.multiline_text(xy, text, fill=None, font=None, anchor=None, spacing=0, align=”left”)


    wrapped.save('pictureExports/wrapped.png')

def topGames(gameList):

    #region Fonts
    font_heading = ImageFont.truetype('pictureAssets/fonts/CircularStd-Black.ttf', 320)
    font_game = ImageFont.truetype('pictureAssets/fonts/CircularStd-Medium.ttf', 175)
    font_subtext = ImageFont.truetype('pictureAssets/fonts/CircularStd-Book.ttf', 130)
    
    font_BG = ImageFont.truetype('pictureAssets/fonts/CircularStd-Bold.ttf', 210)
    font_footer = ImageFont.truetype('pictureAssets/fonts/CircularStd-Bold.ttf', 175)
    #endregion
    
    wrapped=Image.open('pictureAssets/topGamesBlank.jpg')
    wrappedDraw = ImageDraw.Draw(wrapped)  
   
    
    #blanks out the original text used to time things up
    pink="#F774C4"
    wrappedDraw.rectangle([(1900,1800),(4500,6500)], fill =pink) # song names
    wrappedDraw.rectangle([(0,820),(4500,1500)], fill =pink) # heading
    wrappedDraw.rectangle([(0,7000),(4500,8000)], fill =pink) # watermark
   
    #region footer, logo, title 
    wrappedDraw.text((500, 820), 'My Top Games', 'black', font=font_heading) #heading
    
    #logo
    bgLogo=Image.open('pictureAssets/bgStatsLogo.png')
    
    bgResize=int(0.60*bgLogo.width)
    bgLogo=bgLogo.resize((bgResize,bgResize))
    bg_x=250
    bg_y=7440
    wrapped.paste(bgLogo, (bg_x, bg_y), mask=bgLogo)
    wrappedDraw.text((bg_x+bgResize+30, bg_y+0.3*bgResize), "BG Stats", 'black', font=font_BG)
    
   
    wrappedDraw.text((2250, bg_y+0.3*bgResize), "TALITAJAMES.COM/BG", 'black', font=font_footer)  #link
    #endregion
    
    # the five games
    for i in range(5):
        #region game images
        #start x,y
        x_im=940
        y_im=1600+974*i
        
        gameImageURL=gameList[i].image
        # print(f" {gameList[i].name} image url: {gameImageURL}")
        if gameList[i].bgg_id==0:
            gameImage = Image.open('pictureAssets/none_game.png')
        else:
            response = requests.get(gameImageURL)
            gameImage = Image.open(BytesIO(response.content))
            gameImage.save('pictureAssets/gameimage.png')
                
        gameImage=gameImage.resize((875,875))
        wrapped.paste(gameImage, (x_im,y_im))
        
        #endregion
        
        x_txt=1980
        y_txt=1745
        # Game name
        wrappedDraw.text((x_txt, y_txt+980*i), gameList[i].name, 'black', font=font_game)
       
        mechanics=gameList[i].mechanics
        mechanics_str="\n".join(mechanics[:3])
        # print(f" for {gameList[i].name} {mechanics_str}")
       
        #subtext  
        # wrappedDraw.text((x_txt, y_txt+980*i+310), mechanics_str, 'black', font=font_subtext)
        wrappedDraw.multiline_text((x_txt, y_txt+980*i+210), mechanics_str, 'black', font=font_subtext,spacing=40)

    wrapped.save('pictureExports/topGames.png')

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
    
    
    
    pass


def topPlayers(playerList):
    
    #region fonts
    # font_heading = ImageFont.truetype('pictureAssets/fonts/Algerian-Regular.ttf', 400)
    font_text = ImageFont.truetype('pictureAssets/fonts/CMU-Roman.ttf', 300)
    
    font_footer = ImageFont.truetype('pictureAssets/fonts/CMU-Roman.ttf', 175)
    #endregion
    
    #create and heading image
    cryptidSquare = Image.open('pictureAssets/blankDesigns_CryptidSquare.jpg')
    cryptidSquareDraw = ImageDraw.Draw(cryptidSquare) 
    # cryptidSquareDraw.text((2270,1050), 'TOP MECHANICS','black', font=font_heading)  #link

    #region create top players string
    topPlayerString=""
    numTop=5
    maxLines=numTop
    if len(playerList)<numTop:
        maxLines=len(playerList)
        
    for i in range(maxLines):
        topPlayerString += (f"{i+1}. {playerList[i].name if len(playerList[i].name) < 17 else f'{playerList[i].name[:15]}...'} ({playerList[i].plays})\n")

    #endregion
    
    
    cryptidSquareDraw.multiline_text((2700,1850), topPlayerString,'black', font=font_text,spacing=390)  #link
        
    #footer   
    cryptidSquareDraw.text((cryptidSquare.width-100, cryptidSquare.height-100), "TALITAJAMES.COM/BG", 'black', font=font_footer, anchor='rs')  #link

        
    cryptidSquare.save('pictureExports/topPlayers_cryptid.png')
    
    
    
    pass



def genPhotos():
    #region data import
    playerData, gameData, playsData = dataGathering.parseData()
        
    #games sorted by play count
    gameList = [game for game in gameData.values()]
    gameList.sort(key=lambda x: x.plays, reverse=True)
    
    #players sorted by play count then win count
    playerCountList = [player for player in playerData.values()]
    playerWinList=playerCountList
    
    playerCountList.sort(key=lambda x: x.plays, reverse=True)
    playerWinList.sort(key=lambda x: x.wins, reverse=True)
    #endregion
    
    
    
    topPlayers(playerCountList)
    topMechanics(gameList)
    pass


if __name__=='__main__':    
    print("***** Start *****")
   
    genPhotos()
    # topGames(gameList)
    # gamesWrapped()
    print("***** DONE *****\n\n")