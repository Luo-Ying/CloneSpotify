import sys, Ice
import SpotifyDuPauvre
import pymongo
import json
import os
import vlc
 
class Server(SpotifyDuPauvre.Server):

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["mydb"]
    collection = db["test"]
    
    def __init__(self):
        self.uploadingFile = b""
        self.player = vlc.Instance()
        self.media_player = self.player.media_player_new()

    def helloWorld(self, helloWorld, current=None):
        print(helloWorld)
        
    # def getNewIndex(self, current=None):
    #     index = self.index
    #     self.index += 1
    #     return index

    def playMusic(self, musicName, current=None):
        file = "musics/" + musicName + ".mp3"
        if os.path.exists(file) != True : return False
        media = self.player.media_new(file)

        media.add_option(":sout=#transcode{vcodec=h264,acodec=mpga,ab=128,channels=2,samplerate=44100,scodec=none}:rtp{sdp=rtsp://127.0.0.1:8554/}")
        # media.add_option("rtp{sdp=rtsp://127.0.0.1:8554/}")
        media.add_option("--no-sout-all")
        media.add_option("--sout-keep")
        media.get_mrl()

        self.media_player = self.player.media_player_new()
        self.media_player.set_media(media)
        self.media_player.play()
        return True

    def stopMusic(self, current=None):
        self.media_player.stop()
       
    def uploadPart(self, part, current=None):
        # if id not in self.uploadingFile : self.uploadingFile[id] = b""
        self.uploadingFile += part
        return 0
        
    def uploadFileAndInsertMusic(self, filename, current=None):
        file = open("musics/" + filename, "wb")
        file.write(self.uploadingFile)
        file.close()
        print(file)
        return 0

    def addMusic(self, dataMusic:str, current=None):
        # data = {"title": "test", "url": "www.goggle.com"}
        print("coucou")
        dataToInsert = json.loads(dataMusic)
        result = self.collection.insert_one(dataToInsert)

    def deleteMusic(self, titleMusic:str, current=None):
        result = self.collection.delete_one({"title": titleMusic})

    def searchMusic(self, titleMusic:str, current:None):
        result = self.collection.find_one({"title": titleMusic})
        print(result)

    def updateMusicChangeTitle(self, titleCurrent:str, newTitle:str, current=None):
        result = self.collection.update_one({"title": titleCurrent}, {"$set": {"title": newTitle}})
 
with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("SpotifyDuPauvre", "default -p 10000")
    object = Server()
    adapter.add(object, communicator.stringToIdentity("SpotifyDuPauvre"))
    adapter.activate()
    communicator.waitForShutdown()