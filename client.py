import sys, Ice
import SpotifyDuPauvre
import os
import vlc
from termcolor import colored
import string

class Client:

    def __init__(self) -> None:
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()
        self.player.set_mrl("rtsp://127.0.0.1:8554/")
        self.listMusics = []

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

    def deleteMusic(self, app, name):
        # par title, par filename
        app.deleteMusicByTitle(name)

    def getAllMusics(self, app):
        self.listMusics = app.getAllMusics()
        # print(listMusics)
        print("\n" + colored("List of musics", attrs=['bold']) + ": \n")
        for i in range(0, len(self.listMusics)):
            print(str(i) + " - " + self.listMusics[i] + "\n")

 
with Ice.initialize(sys.argv) as communicator:
    base = communicator.stringToProxy("SpotifyDuPauvre:default -p 10000")
    app = SpotifyDuPauvre.ServerPrx.checkedCast(base)
    if not app:
        raise RuntimeError("Invalid proxy")

    app.helloWorld("Hello World!")

    client = Client()

    client.getAllMusics(app)

    # client.uploadMusic(app, "E:\Yingqi\etudes\M1S2\middleware-Spotify_du_pauvre\musicToUpload\房东的猫 - 云烟成雨.mp3")
    # client.uploadMusic(app, "E:\Yingqi\etudes\M1S2\middleware-Spotify_du_pauvre\musicToUpload\PianoPanda - Flower Dance（钢琴版I）.mp3")

    while True:

        command = input("\033[92mWaiting a command : ")

        if command == "play":
            value = input("\033[34mEnter the name/num of a music: ")
            try:
                num = int(value)
                # print(num)
                if(num < len(client.listMusics)): 
                    result = app.playMusic(client.listMusics[num])
                    if result == True:
                        client.play()
                    else:
                        print("\033[31mNo such music in the database")
                else:
                    print("\033[31mNo such music in the list")
            except ValueError:
                # print("无法将字符串转换为整数")
                isMusic = False
                for item in client.listMusics:
                    if(''.join(item.split()) ==  ''.join(value.split())): 
                        result = app.playMusic(item)
                        if result == True:
                            isMusic = True
                            client.play()
                            break
                if(isMusic == False):print("\033[31mNo such music")

        elif command == "stop":
            client.stop()
            if(app.stopMusic() == False): print("\033[31mSomething wrong")

        elif command == "delete":
            title = input("\033[34mEnter the " + colored("title", attrs=['bold']) + " of a music: ")
            client.deleteMusic(app, title)

        elif command == "upload":
            path = input("\033[34mEnter the path of a music: ")
            client.uploadMusic(app, path)

        elif command == "show":
            client.getAllMusics(app)

        else:
            print("\033[31mNo such command")
    # result = app.playMusic("房东的猫 - 云烟成雨")
    # if result == True : client.play()
    # else : print("\033[91mFichier introuvable")
        

