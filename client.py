import sys, Ice
import SpotifyDuPauvre
import os
import vlc

class Client:

    def __init__(self) -> None:
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()
        self.player.set_mrl("rtsp://192.168.1.128:5000/music")

    def uploadMusic(self, app, pathMusicFile):
        print("Path of file received: " + pathMusicFile)

        filename = os.path.basename(pathMusicFile)
        print("filename: " + filename)
        
        with open(pathMusicFile, 'rb') as file:
            file_size = os.fstat(file.fileno()).st_size
            print(f"Size of file : {file_size} bytes")
            quotient, remainder = divmod(file_size, 102400)
            print(f"quotion: {quotient}, remainder: {remainder}")

            for i in range(quotient):
                part = file.read(102400)
                app.uploadPart(part)

            part = file.read(remainder)
            app.uploadPart(part)

            file.close()

            app.uploadFileAndInsertMusic(filename)

        
    def play(self):
        self.player.play()

 
with Ice.initialize(sys.argv) as communicator:
    base = communicator.stringToProxy("SpotifyDuPauvre:default -p 10000")
    app = SpotifyDuPauvre.ServerPrx.checkedCast(base)
    if not app:
        raise RuntimeError("Invalid proxy")

    app.helloWorld("Hello World!")

    client = Client()

    client.uploadMusic(app, "/mnt/e/Yingqi/etudes/M1S2/middleware-Spotify_du_pauvre/musicToUpload/房东的猫 - 云烟成雨.mp3")

    result = app.playMusic("房东的猫 - 云烟成雨")
    if result == True : client.play()
    else : print("\033[91mFichier introuvable")
        

