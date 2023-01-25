import tkinter as tk
from tkinter import ttk
from tkinter import *
from pytube import Playlist
import os
from pytube import YouTube
import threading
import youtube_dl
import yt_dlp
from PIL import ImageTk
from urllib.request import urlopen
import multiprocessing.dummy as mp
root = tk.Tk()
root.geometry("550x380")
name_var = tk.StringVar()

ytdl_options={"format": "bestaudio", "quiet": False,'outtmpl': 'Downloads/%(title)s.%(ext)s',"no_warnings": True,'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],}

newpath = 'Downloads'
if not os.path.exists(newpath):
    os.makedirs(newpath) #creates directory for mp3 files if doesn't exist

def clicked():#used to create threads so tkinter doesn't crash while download in progress and user can make multiple downloads at the same time
    threading.Thread(target=download).start()

def write(*message, end="\n", sep=" "):#used to write informations to first text area
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    Console.see(tk.END)
    Console.insert(INSERT, text)

def write2(*message, end="\n", sep=" "):#used to write informations to second text area
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    Console2.see(tk.END)
    Console2.insert(INSERT, text)

def search_song(amount, song, get_url=False):
    info = youtube_dl.YoutubeDL(ytdl_options).extract_info(f"ytsearch{amount}:{song}", download=False,ie_key="YoutubeSearch")
    if len(info["entries"]) == 0: return None
    return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

def download():
    p = str(name_var.get())#gets link from user input area
    name_var.set("")
    if 'https://' in p:
        if "playlist" in p:#checks if input is playlist or song link
            l = Playlist(p)
            if var1.get()==1:
                p=mp.Pool(8)
                p.map(downloader,l.videos) # range(0,1000) if you want to replicate your example
                p.close()
                p.join()
            else:
                for video in l.videos:
                    downloader(video.watch_url)
        else:
            downloader(p)
    else:
        write(f"[SEARCHING] {p}")
        result = search_song(amount=5, song=p, get_url=True)
        threading.Thread(target=open_popup(search_str=p,result=result)).start()
        
def handler(url,window):
    downloader(url=url)
    window.destroy()
    

def downloader(url):
    if type(url)!=str:
        url=url.watch_url
    try:
        write(f"[DOWNLOADING] {YouTube(url).title}")
        with yt_dlp.YoutubeDL(ytdl_options) as ydl:
            ydl.download([url])
        write2(f"[SUCCESFUL] {YouTube(url).title}")
    except Exception as e:
        print(e)
        write2(f"[ERROR](video might be age restricted)")

def open_popup(search_str,result):
    top= Toplevel(root)
    top.geometry("800x250")
    top.title(f'Search Results for {search_str}')
    top.resizable(0,0)

    u = urlopen(YouTube(result[0]).thumbnail_url)
    raw_data = u.read()
    u.close()
    photo = ImageTk.PhotoImage(data=raw_data)
    label = tk.Label(top,image=photo,width=150,height=150)
    label.image = photo
    label.place(x=5,y=50)
    l=list(YouTube(result[0]).title)
    for i in range(len(YouTube(result[0]).title)//20):
        l.insert((i+1)*20,'\n')
    tk.Label(top,text=''.join(l)).place(x=5,y=5)
    Button(top,text='Download',command=lambda:handler(result[0],window=top)).place(x=45,y=210)

    u = urlopen(YouTube(result[1]).thumbnail_url)
    raw_data = u.read()
    u.close()
    photo = ImageTk.PhotoImage(data=raw_data)
    label = tk.Label(top,image=photo,width=150,height=150)
    label.image = photo
    label.place(x=165,y=50)
    l=list(YouTube(result[1]).title)
    for i in range(len(YouTube(result[1]).title)//20):
        l.insert((i+1)*20,'\n')
    tk.Label(top,text=''.join(l)).place(x=165,y=5)
    Button(top,text='Download',command=lambda:handler(result[1],window=top)).place(x=205,y=210)

    u = urlopen(YouTube(result[2]).thumbnail_url)
    raw_data = u.read()
    u.close()
    photo = ImageTk.PhotoImage(data=raw_data)
    label = tk.Label(top,image=photo,width=150,height=150)
    label.image = photo
    label.place(x=325,y=50)
    l=list(YouTube(result[2]).title)
    for i in range(len(YouTube(result[2]).title)//20):
        l.insert((i+1)*20,'\n')
    tk.Label(top,text=''.join(l)).place(x=325,y=5)
    Button(top,text='Download',command=lambda:handler(result[2],window=top)).place(x=365,y=210)

    u = urlopen(YouTube(result[3]).thumbnail_url)
    raw_data = u.read()
    u.close()
    photo = ImageTk.PhotoImage(data=raw_data)
    label = tk.Label(top,image=photo,width=150,height=150)
    label.image = photo
    label.place(x=485,y=50)
    l=list(YouTube(result[3]).title)
    for i in range(len(YouTube(result[3]).title)//20):
        l.insert((i+1)*20,'\n')
    tk.Label(top,text=''.join(l)).place(x=485,y=5)
    Button(top,text='Download',command=lambda:handler(result[3],window=top)).place(x=525,y=210)

    u = urlopen(YouTube(result[4]).thumbnail_url)
    raw_data = u.read()
    u.close()
    photo = ImageTk.PhotoImage(data=raw_data)
    label = tk.Label(top,image=photo,width=150,height=150)
    label.image = photo
    label.place(x=645,y=50)
    l=list(YouTube(result[4]).title)
    for i in range(len(YouTube(result[4]).title)//20):
        l.insert((i+1)*20,'\n')
    tk.Label(top,text=''.join(l)).place(x=645,y=5)
    Button(top,text='Download',command=lambda:handler(result[4],window=top)).place(x=685,y=210)


var1 = tk.IntVar()
c1 = tk.Checkbutton(root, text='Enable Multithreading ( ͡° ͜ʖ ͡°)',variable=var1, onvalue=1, offvalue=0).place(x=15,y=360)

#user entry and download button
name_label = tk.Label(root, text='Song name &\nURL or Playlist URL', font=('calibre', 8, 'bold'))
name_entry = tk.Entry(root,width=50, textvariable=name_var, font=('calibre', 10, 'normal'))
sub_btn = ttk.Button(root, text='DOWNLOAD', command=lambda:clicked())
name_label.grid(row=0, column=0)
name_entry.grid(row=0, column=1)
sub_btn.grid(row=0, column=2)

#first text output area
Console = Text()
Console.config(height=10, width=70,font=("Arial",9))
Console.grid(row=2, column=0,columnspan=3,pady=5)

#second text output area
Console2 = Text()
Console2.config(height=10, width=70,font=("Arial",9))
Console2.grid(row=3, column=0,columnspan=3,rowspan=2,pady=5)

root.title('Youtube mp3 Downloader - b b baka')
root.resizable(0,0)
root.mainloop()
