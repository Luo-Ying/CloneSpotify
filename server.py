import sys, Ice
import SpotifyDuPauvre
import pymongo
import json
import os
import vlc
from mutagen.mp3 import MP3
 
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

    def playMusic(self, musicTitle, current=None):
        filter = {'title': musicTitle}  # 替换为你的查询条件，如字段名和字段值

        document = self.collection.find_one(filter)
        filename = document['filename']

        file = "musics/" + filename
        if os.path.exists(file) != True : return False
        media = self.player.media_new(file)

        media.add_option(":sout=#transcode{vcodec=h264,acodec=mpga,ab=128,channels=2,samplerate=44100,scodec=none}:rtp{sdp=rtsp://127.0.0.1:8554/}")
        media.add_option("--no-sout-all")
        media.add_option("--sout-keep")
        media.get_mrl()

        self.media_player = self.player.media_player_new()
        self.media_player.set_media(media)
        self.media_player.play()
        return True

    def stopMusic(self, current=None):
        if (self.media_player.is_playing()):
            self.media_player.stop()
            return True
        else: 
            return False
       
    def uploadPart(self, part, current=None):
        self.uploadingFile += part
        return 0
        
    def uploadFileAndInsertMusic(self, filename, current=None):
        file = open("musics/" + filename, "wb")
        file.write(self.uploadingFile)
        file.close()
        print(file)
        audio = MP3("musics/" + filename)
        artist = audio['TPE1'].text[0] if 'TPE1' in audio else None
        title = audio['TIT2'].text[0] if 'TIT2' in audio else None
        # title = filename
        album = audio['TALB'].text[0] if 'TALB' in audio else None
        print("file infos: " , title, album, artist)
        musicData = '{"title": "' + title + '", "artist": "' + artist + '", "album": "' + album + '", "filename": "' + filename + '", "url": ' + '"E://Yingqi/etudes/M1S2/middleware-Spotify_du_pauvre/musics/' + filename + '"}'
        dataToInsert = json.loads(musicData)
        result = self.collection.insert_one(dataToInsert)
        # print("result: " + result)
        print("upload file successfuly! ")
        self.uploadingFile = b""
        return 0

    def addMusic(self, dataMusic:str, current=None):
        data = {"title": "test", "url": "www.goggle.com"}
        print("coucou")
        dataToInsert = json.loads(dataMusic)
        result = self.collection.insert_one(dataToInsert)

    def deleteMusicByTitle(self, titleMusic:str, current=None):
        filter = {'title': titleMusic}  # 替换为你的查询条件，如字段名和字段值

        document = self.collection.find_one(filter)
        filename = document['filename']

        file = "musics/" + filename
        if os.path.exists(file) != True : return False
        if os.path.isfile(file):  # 判断文件是否存在
            os.remove(file)  # 删除文件

        # 使用delete_one()方法删除单个文档
        result = self.collection.delete_one(filter)

        # 检查删除操作的结果
        if result.deleted_count == 1:
            print("Delete music successfully! ")
        else:
            print("No item in the database! ")
        return True

    def getAllMusics(self, current:None):
        listMusic = []
        all_data = list(self.collection.find())
        for data in all_data:
            listMusic.append(data['title'])
        return listMusic

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