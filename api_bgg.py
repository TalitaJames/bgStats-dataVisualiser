# Coppied from games database 
import requests
import xmltodict, json
import pprint

pp = pprint.PrettyPrinter(depth=4) # Formats the print mesages to be easy read


class BGG_gameinfo:
    def __init__(self, gameid):
        self.gameid=gameid
        xmlObj = requests.get('https://boardgamegeek.com/xmlapi2/thing?id=' + str(gameid))
        self.jsonObj = xmltodict.parse(xmlObj.text)
   
    def gameName(self):
        #some games only have one name, and will error when you treat it as a list
        try:
            name=self.jsonObj["items"]["item"]["name"][0]["@value"]
        except:
            name=self.jsonObj["items"]["item"]["name"]["@value"]
        return name

    # Returns the language dependance
    def languageDependency(self):
        for num in range(len(self.jsonObj["items"]["item"]["poll"])):
            if self.jsonObj["items"]["item"]["poll"][num]["@name"] == "language_dependence":
                langDepAdress = num

        langDepMaxVotes=0

        for j in range(len(self.jsonObj["items"]["item"]["poll"][langDepAdress]["results"]["result"])):
            if int(langDepMaxVotes) < int(self.jsonObj["items"]["item"]["poll"][langDepAdress]["results"]["result"][j]["@numvotes"]):
                langDepMaxVotes=self.jsonObj["items"]["item"]["poll"][langDepAdress]["results"]["result"][j]["@numvotes"]
                langDepLevelAddress=j
                langDepName = self.jsonObj["items"]["item"]["poll"][langDepAdress]["results"]["result"][j]["@value"]

        if langDepMaxVotes ==0:
            return "Unknown Data"
        else:
            return langDepName

    def thumbnail(self):
        return self.jsonObj["items"]["item"]["thumbnail"]

    def image(self):
        return self.jsonObj["items"]["item"]["image"]

    def yearPublished(self):
        return self.jsonObj["items"]["item"]["yearpublished"]["@value"]
    
    def description(self):
        return self.jsonObj["items"]["item"]["description"]
    
    #Times and numbers
    def minPlayers(self):
        return self.jsonObj["items"]["item"]["minplayers"]["@value"]
    
    def maxPlayers(self):
        return self.jsonObj["items"]["item"]["maxplayers"]["@value"]
    
    def playTime(self):
        return self.jsonObj["items"]["item"]["playingtime"]["@value"]


    # Arrays and info
    def __clasifications(self):
        boardgamecategory=[]
        boardgamemechanic=[]
        boardgamefamily=[]

        # makes an array of the categories, mechanics, families ect 
        for number in range(len(self.jsonObj["items"]["item"]["link"])):
            if self.jsonObj["items"]["item"]["link"][number]["@type"] == "boardgamecategory":
                boardgamecategory.append(self.jsonObj["items"]["item"]["link"][number]["@value"])
            
            elif self.jsonObj["items"]["item"]["link"][number]["@type"] == "boardgamemechanic":
                boardgamemechanic.append(self.jsonObj["items"]["item"]["link"][number]["@value"])
            
            elif self.jsonObj["items"]["item"]["link"][number]["@type"] == "boardgamefamily":
                boardgamefamily.append(self.jsonObj["items"]["item"]["link"][number]["@value"])
        
        listData = {'boardgamecategory': boardgamecategory, 'boardgamemechanic': boardgamemechanic, 'boardgamefamily': boardgamefamily}

        return listData

    def categories(self):
        return self.__clasifications()["boardgamecategory"]
    
    def mechanics(self):
        return self.__clasifications()["boardgamemechanic"]
    
    
    def family(self):
        return self.__clasifications()["boardgamefamily"]
    
    
    def dictionary(self):
        dictGameInfo={
                    "Name": self.gameName(),
                    "BGG Game ID": self.gameid,
                    "thumbnail": [ { "url": self.image() }],
                    "boardgamecategory": self.categories(),
                    "boardgamemechanic": self.mechanics(),
                    "year published": self.yearPublished(),
                    "min players": self.minPlayers(),
                    "max players": self.maxPlayers(),
                    "play time": self.playTime()
                }
        return dictGameInfo


if __name__ == "__main__":
    print("-------------------------------------")
    gameObj = BGG_gameinfo(253170)
    # pp.pprint(gameObj.jsonObj)
    # print((gameObj.gameName()))
    print(gameObj.mechanics())
    # print(gameObj.arrayToAirtable(gameObj.mechanics()))
    pp.pprint(gameObj.dictionary())
