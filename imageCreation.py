from PIL import Image, ImageDraw, ImageFont 
import dataGathering


def topX(list, x):
    string=""
    max=x
    if len(list)<x:
        max=len(list)
        
    for i in range(max):
        string += (f"{i+1}. {list[i]}\n")

    return string


def gamesWrapped():
    width = 1080
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


def topGames():

    font_heading = ImageFont.truetype('pictureAssets/fonts/CircularStd-Black.ttf', 320)
    font_game = ImageFont.truetype('pictureAssets/fonts/CircularStd-Medium.ttf', 175)
    font_subtext = ImageFont.truetype('pictureAssets/fonts/CircularStd-Book.ttf', 150)
    
    
    wrapped=Image.open('pictureAssets/topGamesBlank.jpg')
    
    wrappedDraw = ImageDraw.Draw(wrapped)  
    wrappedDraw.text((500, 820), 'My Top Games', 'black', font=font_heading)
   
    
    wrappedDraw.rectangle([(1900,1800),(4500,6500)], fill ="#F774C4")

    for i in range(5):
        # game images
        x_im=940
        y_im=1600+974*i
        wrappedDraw.rectangle([(x_im,y_im),(x_im+875,y_im+875)], fill ="green")
        
        x_txt=1980
        y_txt=1820
        # Game name
        wrappedDraw.text((x_txt, y_txt+980*i), 'Hard to be the bard', 'black', font=font_game)
        
        #subtext  
        wrappedDraw.text((x_txt, y_txt+980*i+310), 'Christian Borle', 'black', font=font_subtext)



    wrapped.save('pictureExports/topGames.png')
    
    
    # Colour pink = #F774C4








if __name__=='__main__':    
    # data=dataGathering.parseData()
    # playerData=data['playerData']
    topGames()
    print("***** DONE gteen farts *****\n\n")