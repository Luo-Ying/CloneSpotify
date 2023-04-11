module SpotifyDuPauvre
{

	sequence<byte> byteList;
    // string uploadingFile;

    interface Server
    {
        void helloWorld(string helloWorld);
		// int getNewIndex();
        bool playMusic(string filename);
        void stopMusic();
		bool uploadPart(byteList part);
		bool uploadFileAndInsertMusic(string filename);
        void addMusic(string musicData);
        void deleteMusic(string titleMusic);
        void searchMusic(string titleMusic);
        void updateMusicChangeTitle(string titleCurrent, string newTitle);
    }
}