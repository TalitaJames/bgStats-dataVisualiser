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
    width = 1280
    height = 1920

    wrapped=Image.open('pictureAssets/Spotify_Wrapped_Blank.jpg')
    wrappedDraw = ImageDraw.Draw(wrapped)  
    
    font = ImageFont.truetype('pictureAssets/fonts/Courier Prime.ttf', 50)
    font_heading = ImageFont.truetype('pictureAssets/fonts/Courier Prime.ttf', 40)
    font_big = ImageFont.truetype('pictureAssets/fonts/Courier Prime Bold.ttf', 60)
    font_year = ImageFont.truetype('pictureAssets/fonts/Courier Prime Bold.ttf', 112)

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


def topGames(list):
    games=['Spot It', 'Ticket to Ride', 'Catan', 'Codenames', 'Pandemic']
    mechanics=['Pattern Recognition', 'Strategy', 'Communication Limits', 'Strategy', 'Strategy']

    #region Fonts
    font_heading = ImageFont.truetype('pictureAssets/fonts/CircularStd-Black.ttf', 320)
    font_game = ImageFont.truetype('pictureAssets/fonts/CircularStd-Medium.ttf', 175)
    font_subtext = ImageFont.truetype('pictureAssets/fonts/CircularStd-Book.ttf', 150)
    
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
    
    #the five games
    for i in range(5):
        #region game images
        #start x,y
        x_im=940
        y_im=1600+974*i
        
        gameImageURL=list[i].image
        response = requests.get(gameImageURL)
        gameImage = Image.open(BytesIO(response.content))
        gameImage.save('pictureAssets/gameimage.png')
                
        gameImage=gameImage.resize((875,875))
        wrapped.paste(gameImage, (x_im,y_im))
        
        #endregion
        
        x_txt=1980
        y_txt=1820
        # Game name
        wrappedDraw.text((x_txt, y_txt+980*i), list[i].name, 'black', font=font_game)
       
       
        #subtext  
        wrappedDraw.text((x_txt, y_txt+980*i+310), str(list[i].mechanics), 'black', font=font_subtext)



    wrapped.save('pictureExports/topGames.png')
    


if __name__=='__main__':    
    print("***** Start *****")
    playerData, gameData = dataGathering.parseData()
    
    #region for player and game, sorts into lists
    
    #games sorted by play count
    gameList = [game for game in gameData.values()]
    gameList.sort(key=lambda x: x.plays, reverse=True)
    
    #players sorted by play count then win count
    playerCountList = [player for player in playerData.values()]
    playerWinList=playerCountList
    
    playerCountList.sort(key=lambda x: x.plays, reverse=True)
    playerWinList.sort(key=lambda x: x.wins, reverse=True)
    
    #endregion
    
    topGames(gameList)
    print("***** DONE *****\n\n")