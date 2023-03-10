# pip3 install pytube;pip3 install soundcloud-lib;pip3 install python-vlc
from pytube import YouTube
import os
from sclib import SoundcloudAPI, Track, Playlist
from random import choice
from colorama import Fore
import vlc


colors = [Fore.RED, Fore.WHITE, Fore.YELLOW, Fore.GREEN, Fore.MAGENTA, Fore.CYAN]


music_folder = ""

def display_menu():
    files = os.listdir("ascii")
    ascii_art = choice(files)
    with open("ascii/" + ascii_art) as file:
        print(f"""
{file.read()}\n
1. Youtube 2 Mp3
2. Soundcloud 2 Mp3
3. Play music
4. Set new folder for Mp3's
5. stop playing music
6. exit
7. clear screen
    """)



def set_up_folder(destination):
    if destination[-1] == "/":
        print("[+] please do not include a / at the end [+]")
    else:
        return destination

def play_music(stop_music=False):
    counter = 0
    songs = {}
    if stop_music is False:
        for each_song in os.listdir(music_folder):
            print(f"{counter} | {choice(colors)}{each_song}{colors[1]}")
            counter += 1
            songs[counter]=each_song        
        
        which_song = input("enter song number :>")
        song = songs[int(which_song)]
        global p 
        p = vlc.MediaPlayer(music_folder + "/"+ song)
        p.play()
    else:
        p.stop()

def main():
    try:
        while True:
            user_input = input("MP3 Player :> ")
            if user_input == "6" or user_input == "exit":
                exit(0x00)
            elif user_input == "help" or user_input == "?" or user_input == "menu":
                display_menu()
            elif user_input == "4" or user_input == "folder":
                dest = input("enter folder :> ")
                music_folder = set_up_folder(dest)
            elif user_input == "2":
                soundcloud_to_mp3(music_folder)
            elif user_input == "1":
                youtube_to_mp3(music_folder)
            elif user_input == "3":
                play_music()
            elif user_input == "5" or user_input == "stop":
                play_music(stop_music=True)
            elif user_input == "7" or user_input == "clear":
                os.system("clear")
            else:
                print(f"{user_input} is not a command silly goose")

    except Exception as ex:
    	print(f"[+] {ex} has occerd [+]")
  
def youtube_to_mp3(folder):
    yt = YouTube(str(input("Enter YT URL :>")))
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=folder)
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)
    print(yt.title + " [<+>] Downloaded [<+>]")


def soundcloud_to_mp3(folder):
    playlist_or_mp3 = input("playlist or single song? (p or ss) :>")
    if playlist_or_mp3 == "p" or playlist_or_mp3 == "playlist" or playlist_or_mp3 == "1":
        playlist_to_download = input("enter playlist link :>")
        api = SoundcloudAPI()
        playlist = api.resolve(playlist_to_download)

        assert type(playlist) is Playlist

        for track in playlist.tracks:
            filename = f"{folder}/{track.title}.mp3"
            with open(filename, "wb+") as file:
                track.write_mp3_to(file)
        print(f"{track.title} downloaded and sent to: {filename}")

    
    elif playlist_or_mp3 == "ss" or playlist_or_mp3 == "2":
        mp3_to_download = input("enter Mp3 link :>")
        api = SoundcloudAPI()
        track = api.resolve(mp3_to_download)

        assert type(track) is Track

        filename = f"{folder}/{track.title}.mp3"

        with open(filename, "wb+") as file:
            track.write_mp3_to(file)
        print(f"[+] {track.title} downloaded and sent to: {filename} [+]")

        

if __name__ == "__main__":
    main()