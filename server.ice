module SpotifyDuPauvre
{

	sequence<byte> byteList;
    // string uploadingFile;
    sequence<string> musicList;

    interface Server
    {
        void helloWorld(string helloWorld);
        bool playMusic(string filename);
        bool stopMusic();
		bool uploadPart(byteList part);
		bool uploadFileAndInsertMusic(string filename);
        void addMusic(string musicData);
        void deleteMusicByTitle(string titleMusic);
        void searchMusic(string titleMusic);
        void updateMusicChangeTitle(string titleCurrent, string newTitle);
        musicList getAllMusics();
        // bool updateMusic(string musicName);
    }
}