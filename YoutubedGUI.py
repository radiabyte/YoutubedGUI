import customtkinter as ctk
import pytube
from pytube import YouTube
from PIL import Image
import io
import requests
import urllib.request
from io import BytesIO
from pytube import extract
import re
import os
import time


#Global Variable
maindict={}
yt=None
debug=False


currentloc=str(os.getcwd())
req=currentloc+'\Downloaded'
if os.path.exists(req)==False:
    os.mkdir('Downloaded')

          
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme('blue')
appWidth, appHeight = 620, 700

class App(ctk.CTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        def get_image_data(url):
            response = requests.get(url)
            return response.content
        #Title
        self.title('Youtubed')
        self.geometry(f"{appWidth}x{appHeight}")
        #Link
        self.linkLabel=ctk.CTkLabel(self, text="Link")
        self.linkLabel.grid(row=0,column=0,padx=10,pady=10,sticky='w')
        self.linkEntry = ctk.CTkEntry(self, placeholder_text="https://youtu.be/dQw4w9WgXcQ?si=aVRq6QWsrAv8FNl9", width=400)
        self.linkEntry.grid(row=0, column=1,columnspan=5, padx=10, pady=10, sticky="ew")
        #Button
        self.submitButton=ctk.CTkButton(self,text='Submit',command=button_func)
        self.submitButton.configure(width=10)
        self.submitButton.grid(row=0, column=6, padx=10, pady=10, sticky='e')


        #Image
        image = Image.open(io.BytesIO(get_image_data("https://img.freepik.com/premium-vector/red-youtube-logo-social-media-logo_197792-1803.jpg")))
        ctk_image = ctk.CTkImage(image, size=(240,135))
        self.imageLabel = ctk.CTkLabel(self, image=ctk_image, text="",anchor='center')
        self.imageLabel.grid(row=1, column=2, columnspan=10, padx=10, pady=10,sticky='ew')
        self.imageLabel.grid_forget()

        #Title
        self.titleLabel=ctk.CTkLabel(self,text='Nothing lol',anchor='center')
        self.titleLabel.grid(row=2, column=2, columnspan=10, padx=10, pady=10, sticky='ew')
        self.titleLabel.grid_forget()
        #Option Menu
        self.resMenu=ctk.CTkOptionMenu(self,values=['Choose resolution'],width=500,anchor='center')
        self.resMenu.grid(row=3, column=2,columnspan=10,sticky='ew',padx=10,pady=10)
        self.resMenu.grid_forget()
        ##Download Button
        
        self.downloadButton=ctk.CTkButton(self,text='Download',command=down_button,width=500,anchor='center')
        self.downloadButton.grid(row=4,column=2,columnspan=10,sticky='ew',padx=10,pady=10)




def extract_variable_value(stream_metadata, variable_name):
    match=re.search(rf'{variable_name}="(.+?)" ',stream_metadata)
    if match:
        return match.group(1)
    else:
        return None

#Thumbnail

def video_id(url):
    id=extract.video_id(url)
    return str(id)

   
def button_func():
    url=str(app.linkEntry.get())
    global yt
    global debug
    yt=YouTube(url)
    videoid=video_id(url)
    imgurl = 'https://img.youtube.com/vi/'+videoid+'/maxresdefault.jpg'
    if debug:
        print(imgurl)
    u = urllib.request.urlopen(imgurl)
    raw_data = u.read()
    u.close()
    im = Image.open(BytesIO(raw_data))
    im = im.resize((240,135))
    list_audio=yt.streams.filter(only_audio=True)
    replace_image(im)
    title=yt.title
    replace_title(title)
    a=[]
    b=[]
    for items in list_audio:
        x=int((str(extract_variable_value(str(items),'abr'))).strip('kbps'))
        y=str(extract_variable_value(str(items),'itag'))
        a.append(x)
        b.append(y)
    global maindict
    mydic={}
    mystrdic={}
    for i in range(0,len(a)):
        mydic[a[i]]=b[i]
    mykeys=list(mydic.keys())
    mykeys.sort()
    sorteddic={i:mydic[i] for i in mykeys}
    if debug:
        print(sorteddic)
    sizes=[]
    strings=[]
    sorteddiclist=list(sorteddic.keys())
    for l in range(0,len(sorteddiclist)):
        gettagsize=sorteddiclist[l]
        ids=sorteddic[gettagsize]
        streamsize=yt.streams.get_by_itag(ids)
        sizeof=int(streamsize.filesize/(1048576))
        sizes.append(str(sizeof))
    for i in range(0,len(sizes)):
        mainstring=str(sorteddiclist[i])+' kbps'+' ('+str(sizes[i])+' MB'+')'
        strings.append(str(mainstring))
    for t in range(0,len(strings)):
        maindict[strings[t]]=(list(sorteddic.values()))[t]
    if debug:
        print(maindict)
    replace_options(strings)
    
    
        
def down_button():
    global maindict
    resreq=str(app.resMenu.get())
    if resreq!='Choose resolution':
        idno=maindict[resreq]
        downloader(idno)
    else:
        print('Please Choose Resolution')
        
def downloader(idno):
    global yt
    global req
    stream=yt.streams.get_by_itag(idno)
    name=yt.title+idno+'.mp3'
    stream.download(filename=name,output_path=req)
    print('Done')
    time.sleep(2)
    app.destroy()

def replace_image(im):
    new_img=ctk.CTkImage(im, size=(240,135))
    app.imageLabel.grid(row=1, column=2, columnspan=10, padx=10, pady=10,sticky='ew')
    app.imageLabel.configure(image=new_img)

#Title
def replace_title(title):
    new_title_label = ctk.CTkLabel(app, text=title,font=('Arial',15),anchor='center')
    new_title_label.grid(row=2, column=2, columnspan=10, padx=10, pady=10, sticky='ew')
    app.titleLabel = new_title_label
def replace_options(val):
    app.resMenu.configure(values=val)
    app.resMenu.grid(row=3, column=2,columnspan=10,sticky='ew',padx=10,pady=10)


if __name__=="__main__":
  app=App()
  app.mainloop()
