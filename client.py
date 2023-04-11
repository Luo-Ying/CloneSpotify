import sys, Ice
import SpotifyDuPauvre
import os
import vlc

class Client:

    def __init__(self) -> None:
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()
        self.player.set_mrl("rtsp://127.0.0.1:8554/")

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

    def stop(self):
        self.player.stop()

 
with Ice.initialize(sys.argv) as communicator:
    base = communicator.stringToProxy("SpotifyDuPauvre:default -p 10000")
    app = SpotifyDuPauvre.ServerPrx.checkedCast(base)
    if not app:
        raise RuntimeError("Invalid proxy")

    app.helloWorld("Hello World!")

    client = Client()

    # client.uploadMusic(app, "E:\Yingqi\etudes\M1S2\middleware-Spotify_du_pauvre\musicToUpload\房东的猫 - 云烟成雨.mp3")

    while True:

        command = input("\033[92mWaiting a command :\n")

        if command == "play":
            name = input("\033[92mEnter the name of a music\n")
            result = app.playMusic(name)
            if result == True:
                client.play()
            else:
                print("\033[91mFichier introuvable")

        elif command == "stop":
            client.stop()
            app.stopMusic()

    # result = app.playMusic("房东的猫 - 云烟成雨")
    # if result == True : client.play()
    # else : print("\033[91mFichier introuvable")
        

