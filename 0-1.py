from pytube import YouTube
import os
import tkinter as tk
from pytube.cli import on_progress
import requests
import re
import string
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from moviepy.editor import *
from tkinter.filedialog import askopenfilenames
from tkinter import filedialog
from tkinter import ttk



#清單下載
def list_download(inpur_url):
    set_patn=path.get()    
    inpur_url=url.get()    
    res = requests.get(inpur_url)
    links=[]
    plain_text = res.text
    
    if '&list=' and 'channel=' in inpur_url:
        cPL=inpur_url.split("list=")[1].split("&index")[0]      
        
    elif 'playlist?' in inpur_url:
        eq = inpur_url.rfind('=') + 1
        cPL = inpur_url[eq:]
    elif '&list=' and '&index=' in inpur_url:
        cPL=inpur_url.split("list=")[1].split("&index")[0]
        
    else:
        labelMsg.config(text='網址錯誤')
    
    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, plain_text)
    
    for m in mat:
        new_m = m.replace('&amp;', '&')
        work_m = 'https://youtube.com/' + new_m
        #print(work_m)
        if work_m not in links:
            links.append(work_m)
    for i in links:
        yt=YouTube(i,on_progress_callback=onProgress)
        vid = yt.streams.filter(subtype='mp4',resolution=cbb.get(),progressive=True).first()
        vid.download(set_patn)

#按鈕動作(清單下載)
def button_event():
    labelMsg.config(text='')
    if url.get()=='':
        labelMsg.config(text='網址欄必須輸入')
        return
    
    if path.get()=='':
        pathdir='download'
    else:
        pathdir=path.get()
    if not os.path.isdir(pathdir):
        os.mkdir(pathdir)
    
    try:
        inpur_url_F=url.get()
        if 'playlist?' or '&list=' in inpur_url_F:
            list_download(inpur_url_F)
            labelMsg.config(text='下載完成')
        
    except:
        labelMsg.config(text='影片無法下載')


#按鈕動作(單檔下載)
def button_event_2():
    set_patn=path.get()        
    labelMsg.config(text='')
    if url.get()=='':
        labelMsg.config(text='網址欄必須輸入')
        return    
    if path.get()=='':
        pathdir='download'
    else:
        pathdir=path.get()
    if not os.path.isdir(pathdir):
        os.mkdir(pathdir)
    
    try:
        inpur_url=url.get()
        if '&list' and 'channel=' in inpur_url:             
            n_url=inpur_url.split("watch?v=")[1].split("&list=")[0]
            i_url=inpur_url.split('channel=')[1]
            d_url='https://www.youtube.com/watch?v='+n_url+'&ab_channel='+i_url 
            yt=YouTube(d_url,on_progress_callback=onProgress)
            yt.streams.filter(subtype='mp4',resolution=cbb.get(),progressive=True).first().download(set_patn)
            labelMsg.config(text='下載完成')

        elif '&list' and 'index=' in inpur_url: 
            n_url=inpur_url.split("watch?v=")[1].split("&list=")[0]
            i_url=inpur_url.split('index=')[1]
            d_url='https://www.youtube.com/watch?v='+n_url
            yt=YouTube(d_url,on_progress_callback=onProgress)
            yt.streams.filter(subtype='mp4',resolution=cbb.get(),progressive=True).first().download(set_patn)
            labelMsg.config(text='下載完成')
        else:            
            yt=YouTube(url.get(),on_progress_callback=onProgress)
            yt.streams.filter(subtype='mp4',resolution=cbb.get(),progressive=True).first().download(set_patn)
            labelMsg.config(text='下載完成')        
    except:
        labelMsg.config(text='影片無法下載')
    
#選擇轉檔檔案
def select_file():
    #global file_
    file_ = filedialog.askopenfilename()
    file.set(file_)
#轉檔
def toMp3():
    filename=file.get()
    targetname=filename.split('\\')[-1].split('.')[0]
    n_m=targetname+'.mp3'
    video=VideoFileClip(filename)
    video.audio.write_audiofile(n_m)


#下載進度
def onProgress(stream, chunk, remains):
    global total,  percent
    total = stream.filesize
    percent = (total-remains) / total * 100
    print('下載中… {:05.2f}%'.format(percent), end='\r')

        

#圖形介面---------------------------
win=tk.Tk()
win.geometry('560x600')
win.title('Youtube download')
#輸入欄位---------------------------
videorb=tk.StringVar()
url=tk.StringVar()
path=tk.StringVar()
file = tk.StringVar()
#標題-------------------------------
img=Image.open("Youtube-Icon.png")
img=ImageTk.PhotoImage(img)
imLabel=tk.Label(win,image=img)
imLabel.place(x=226,y=10)
#-------網址
label1=tk.Label(win,text='網址:',font=('微軟正黑體',12,'bold'),fg='black')
label1.place(x=30,y=150)
entryUrl=tk.Entry(win,textvariable=url)
entryUrl.config(width=48)
entryUrl.place(x=200,y=156)



#------畫質選擇
#choice_frm = tk.Frame(win, width=560, height=50)
#choice_frm.place(x=50,y=220)
#設定提示文字
lb = tk.Label(text='選擇畫質 :',font=('微軟正黑體',12,'bold'),fg='black')
lb.place(x=30,y=230)
#解析度下拉選單
cbb = ttk.Combobox(values=['',"1080p","720p","480p","360p"],state="readonly",width=12)
cbb.place(x=200,y=230)



#-------路徑設置
from tkinter.filedialog import askdirectory
def select_path():
    labelMsg.config(text='')
    path_ = askdirectory()
    path.set(path_)




#-------路徑按鈕
label_path = tk.Label(text='下載路徑 :',font=('微軟正黑體',12,'bold'),fg='black')
label_path.place(x=30,y=190)
path = tk.StringVar()
entry_path = tk.Entry(fg='gray', bd=2, width=30, textvariable=path, cursor='xterm')
entry_path.place(x=200.2,y=190)
button_choice = tk.Button(text='選擇路徑 ', bd=1, width=7, command=select_path, cursor='hand2')
button_choice.place(x=420,y=187)





#-------下載按鈕
btnDown=tk.Button(win,text='清單下載',font=('微軟正黑體',10,'bold'),fg='black',command=button_event)
btnDown.place(x=200,y=260)
btnDown2=tk.Button(win,text='單檔下載',font=('微軟正黑體',10,'bold'),fg='black',command=button_event_2)
btnDown2.place(x=280,y=260)


#-------轉檔設置
label_file = tk.Label(text='轉檔檔案:',font=('微軟正黑體',12,'bold'),fg='black')
label_file.place(x=30,y=450)
entry_file = tk.Entry(fg='gray', bd=2, width=30, textvariable=file, cursor='xterm')
entry_file.place(x=200.2,y=450)
button_choice = tk.Button(text='選擇檔案', bd=1, width=7, command=select_file, cursor='hand2')
button_choice.place(x=420,y=450)
change = tk.Button(text='轉檔', bd=1, width=6, command=toMp3, cursor='hand2')
change.place(x=200,y=490)



#-------訊息欄位
labelMsg=tk.Label(win,text='',font=('微軟正黑體',16,'bold'),fg='black')
labelMsg.place(x=200,y=360)
labelMsg0=tk.Label(win,text='下載狀態 : ',font=('微軟正黑體',16,'bold'),fg='black')
labelMsg0.place(x=100,y=360)

win.mainloop()





















