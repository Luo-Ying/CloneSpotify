import sys, Ice
import os
import vlc
from termcolor import colored
import string
import IceStorm

Ice.loadSlice('server.ice')
import SpotifyDuPauvre

class Client:

    def __init__(self) -> None:
        self.ipv4 = "192.168.1.128"
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()
        self.player.set_mrl("rtsp://" + self.ipv4 + "/")
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

        
    def play(self, app):
        # self.player.play()
        if(self.player.get_state() == vlc.State.Paused):
            # print("music playing....")
            self.player.play()
            return True
        else:
            value = input("\033[34mEnter the name/num of a music: ")
            try:
                num = int(value)
                # print(num)
                if(num < len(self.listMusics)): 
                    result = app.playMusic(self.listMusics[num])
                    if result == True:
                        self.player.play()
                    else:
                        print("\033[31mNo such music in the database")
                else:
                    print("\033[31mNo such music in the list")
            except ValueError:
                # print("无法将字符串转换为整数")
                isMusic = False
                for item in self.listMusics:
                    if(''.join(item.split()) ==  ''.join(value.split())): 
                        result = app.playMusic(item)
                        if result == True:
                            isMusic = True
                            self.player.play()
                            break
                if(isMusic == False):print("\033[31mNo such music")

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def deleteMusic(self, app, name):
        # par title, par filename
        app.deleteMusicByTitle(name)

    def getAllMusics(self, app):
        self.listMusics = app.getAllMusics()
        self.showListMusics()

    def showListMusics(self):
        print("\n\033[37m" + colored("List of musics", attrs=['bold']) + ": \033[0m\n")
        for i in range(0, len(self.listMusics)):
            print(str(i) + " - " + self.listMusics[i] + "\n")

    def modifMusicTitle(self, app, titleCurrent:str, newTitle:str):
        app.updateMusicChangeTitle(titleCurrent, newTitle)

    def searchMusic(self, app, strMusic):
        musicResults = app.searchMusic(strMusic)
        for result in musicResults:
            print("\n")
            print(colored(result.title, attrs=['bold']))
            print("artiste : " + result.artist)
            print("album : " + result.album)
            print("\n")

 
with Ice.initialize(sys.argv, "config.pub") as communicator:
    base = communicator.stringToProxy("SpotifyDuPauvre:default -p 10010")
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
            # value = input("\033[34mEnter the name/num of a music: ")
            # try:
            #     num = int(value)
            #     # print(num)
            #     if(num < len(client.listMusics)): 
            #         result = app.playMusic(client.listMusics[num])
            #         if result == True:
            #             client.play()
            #         else:
            #             print("\033[31mNo such music in the database")
            #     else:
            #         print("\033[31mNo such music in the list")
            # except ValueError:
            #     # print("无法将字符串转换为整数")
            #     isMusic = False
            #     for item in client.listMusics:
            #         if(''.join(item.split()) ==  ''.join(value.split())): 
            #             result = app.playMusic(item)
            #             if result == True:
            #                 isMusic = True
            #                 client.play()
            #                 break
            #     if(isMusic == False):print("\033[31mNo such music")
            client.play(app)

        elif command == "pause":
            client.pause()
            if(app.pauseMusic() == False): print("\033[31mSomething wrong")

        elif command == "stop":
            client.stop()
            if(app.stopMusic() == False): print("\033[31mSomething wrong")

        elif command == "delete":
            title = input("\033[34mEnter the " + colored("title", attrs=['bold']) + " of a music: ")
            client.deleteMusic(app, title)

        elif command == "upload":
            path = input("\033[34mEnter the path of a music: ")
            filename = os.path.basename(path)
            client.uploadMusic(app, path)
            client.getAllMusics(app)

        elif command == "show":
            # client.showListMusics()
            client.getAllMusics(app)

        elif command == "modify":
            print("\n\033[37m " + colored("Choose one music for the operation (num of music)", attrs=['bold']) + " : \033[0m\n")
            for i in range(0, len(client.listMusics)):
                print(str(i) + " - " + client.listMusics[i] + "\n")
            num = input("\033[34m\033[0m\n")
            newtitle = input("\033[34mEnter a new title: \033[0m")
            print(newtitle)
            if (int(num) < len(client.listMusics)): client.modifMusicTitle(app, client.listMusics[int(num)], newtitle)

        elif command == "search":
            strMusic = input("\033[34mEnter your string to search: \033[0m")
            client.searchMusic(app, strMusic)


        else:
            print("\033[31mNo such command")
        

