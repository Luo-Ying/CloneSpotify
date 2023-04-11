module SpotifyDuPauvre
{

    struct Music {
        string title;
        string artist;
        string album;
    };

    sequence<Music> musicResults;
	sequence<byte> byteList;
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
        musicResults searchMusic(string str);
        void updateMusicChangeTitle(string titleCurrent, string newTitle);
        musicList getAllMusics();
        // bool updateMusic(string musicName);
    }
}