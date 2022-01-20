from tkinter import *
import pygame,os,time,tkinter.ttk as ttk,tkinter.messagebox as tkm
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from mutagen.mp3 import MP3


app=Tk()

app.title("Tommy's Music Player")
app.geometry('700x650+450+100')
app.resizable(False,False)
app.iconbitmap('Images\Papirus-Team-Papirus-Apps-Multimedia-audio-player.ico')


# Initialize Pygame
pygame.mixer.init()

global stopped
stopped=False

def about():
    tkm.showinfo("Developer's Information","App was built in Python by\nThomas Burns Botchwey\n***Contacts***\n(233) 27 760 0637\n(233) 54 206 0234\n(233) 50 438 7074\nthomasburnsbotchwey@gmail.com\nCredit: codemy.com")


## Functions
# Add One Song
files_path=[]
song_names=[]
#song_index=[0,]
def add_song(event):
    if event:
        song=filedialog.askopenfilename(initialdir="C:\Music", title='Choose A Song',filetypes=(('mp3 Files','*.mp3'),('wav Files','*.wav')))
        directory=os.path.dirname(song)
        files_path.append(str(directory))
        os.chdir(directory)
        song_dir_split=os.path.split(song)
        song_only= song.split('/')[-1]#.split('.')[0]
        song_names.append(song_only)
        song_box.insert(END, song_only)


# Stop
def stop(event):
    if event:
        # Reset Slider and Status Bar
        status_bar.config(text='')
        music_slider.config(value=0)

        # Stop Song
        pygame.mixer.music.stop()
        song_box.selection_clear(ACTIVE)
        # Clear Status Bar
        status_bar.config(text='Select A Song and Hit Play   ')

        #Set Stop value to True
        global stopped
        stopped=True

# Global Pause Variable
global paused
paused=False


# Pause and UnPause
def pause(is_paused):
    
    global paused
    paused=is_paused
    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused=False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused=True        

# Add Many Songs

def add_many_songs(event):
    if event:
        songs=filedialog.askopenfilenames(initialdir="C:\Music", title='Choose A Song',filetypes=(('mp3 Files','*.mp3'),('wav Files','*.wav')))
        
        for b in songs:
            b=os.path.basename(b)
            song_names.append(b)
            song_box.insert(ANCHOR,b)

        for i in songs:
            i=os.path.dirname(i)  
            files_path.append(i)

# Next Song
def next_song(event):
    if event:
        # Reset Slider and Status Bar
        status_bar.config(text='')
        music_slider.config(value=0)
        #####################################################
        next_one=song_box.curselection()
        #print(next_one)
        song_index=(next_one[0])
        #print(next_one)
        #print(next_one[0])
        # Add 1 to current song index
        next_one=next_one[0]+1
        song=song_box.get(next_one)
        song_next=files_path[next_one]+chr(92)+song
        #song1=os.path.dirname(selected_song)
        pygame.mixer.music.load(song_next)
        pygame.mixer.music.play(loops=0)

        # Move active bar by clearing Current Selection
        song_box.selection_clear(0,END)

        # Highlight Next Song
        song_box.activate(next_one)

        # Set New Active Bar
        song_box.selection_set(next_one, last=None)
        #print(song)
        #print(next_one)

def previous_song(event):
    if event:
        # Reset Slider and Status Bar
        status_bar.config(text='')
        music_slider.config(value=0)
        #####################################################
        next_one=song_box.curselection()
        #print(next_one)
        song_index=(next_one[0])
        #print(next_one)
        #print(next_one[0])
        # Add 1 to current song index
        next_one=next_one[0]-1
        song=song_box.get(next_one)
        song_next=files_path[next_one]+chr(92)+song
        #song1=os.path.dirname(selected_song)
        pygame.mixer.music.load(song_next)
        pygame.mixer.music.play(loops=0)

        # Move active bar by clearing Current Selection
        song_box.selection_clear(0,END)

        # Highlight Next Song
        song_box.activate(next_one)

        # Set New Active Bar
        song_box.selection_set(next_one, last=None)


# Delete A Song
def remove_one_song():
    stop(True)
    # Delete Selected Song
    song_box.delete(ANCHOR)
    # Stop Music if it's playing
    pygame.mixer.music.stop()

    # Delete Song Index From Set
    next_one=song_box.curselection()
    song_index=(next_one[0])

    files_path.remove(song_index)
    song_names.remove(song_index)

# Delete All Songs
def remove_all_song():
    stop(True)
    # Delete All Songs
    song_box.delete(0,END)
    # Stop Music if it's playing
    pygame.mixer.music.stop()

    # Delete All Song Indecies From Set
    files_path.clear()
    song_names.clear()

# Getting Current Time
def play_time():
    # Check for double timing
    if stopped:
        return
    # Get current song time
    current_time=pygame.mixer.music.get_pos()/1000

    # throw up temporary label to get data
    #slider_label.config(text=f'Slider: {int(music_slider.get())} and Song Position: {int(current_time)}')

    # Convert to time format
    converted_current_time=time.strftime('%H:%M:%S',time.gmtime(current_time))
    
    # Get Song Duration with Mutagen
    selected_song=song_box.get(ACTIVE)
    selected_song_path=song_box.curselection()
    song_index=(selected_song_path[0])
    song_path=files_path[song_index]
    song_only=(selected_song)
    song=song_path+chr(92)+song_only

    # Get Length
    song_mutagen=MP3(song)
    song_length=song_mutagen.info.length

    converted_song_length=time.strftime('%H:%M:%S',time.gmtime(song_length))

    # Increase current time by one second
    current_time+=1

    if int(music_slider.get())==int(song_length):
        status_bar.configure(text='Time Elapsed: '+str(converted_song_length)+'  of   '+str(converted_song_length)+'    ')
        next_song(True)
    elif paused:
        pass

    elif int(music_slider.get())==int(current_time):
        # slider hasn't been moved
        # Update to Slider Position
        
        slider_position=int(song_length)
        music_slider.config(to=slider_position, value=int(current_time))
    else:

        # Convert to time format
        # Update to Slider Position
        converted_current_time=time.strftime('%H:%M:%S',time.gmtime(int(music_slider.get())))
        selected_song=song_box.get(ACTIVE)
        #############
        selected_song_path=song_box.curselection()
        song_index=(selected_song_path[0])
        song_path=files_path[song_index]
        song_only=(selected_song)
        song=song_path+chr(92)+song_only

        # Get Length
        song_mutagen=MP3(song)
        song_length=song_mutagen.info.length
        slider_position=int(song_length)
        #########
        music_slider.config(to=slider_position, value=int(music_slider.get()))
        status_bar.configure(text='Time Elapsed: '+str(converted_current_time)+'  of   '+str(converted_song_length)+'    ')
        
        # Move this thing along by one second
        next_time=int(music_slider.get())+1
        music_slider.config(value=next_time)


    # Output Time to Status Bar
    #status_bar.configure(text='Time Elapsed: '+str(converted_current_time)+'  of   '+str(converted_song_length)+'    ')
    
    # Update Current Slider Position In Sync With Current Time
    #music_slider.config( value=int(current_time))
    
    
    
    # Update Timer
    status_bar.after(1000, play_time)


# Play
def play(event):
    if event:
        music_slider.config(value=0)
        # Set Stop variable to False so song can play
        global stopped
        stopped=False
        #################################
        selected_song=song_box.get(ACTIVE)
        selected_song_path=song_box.curselection()
        song_index=(selected_song_path[0])
        
        song_path=files_path[song_index]
        song_only=(selected_song)
        song=song_path+chr(92)+song_only
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        # Activate Play Time
        play_time()
        # Get Current Volume
        #current_volume=pygame.mixer.music.get_volume()
        #slider_label.cofig(text=current_volume*100)

        # Update Slider to Position
        # Get Length
        '''
        song_mutagen=MP3(song)
        song_length=song_mutagen.info.length
        
        slider_position=int(song_length)
        music_slider.config(to=slider_position, value=0) 
        '''
        current_volume=pygame.mixer.music.get_volume()

        # Convert Floats to Multiples of 10
        current_volume=current_volume*100
        #slider_label.cofig(text=current_volume*100)

    

   

# Music Slider Function
def slide(x):
    '''
    selected_song=song_box.get(ACTIVE)
    selected_song_path=song_box.curselection()
    song_index=(selected_song_path[0])
    song_path=files_path[song_index]
    song_only=(selected_song)
    song=song_path+chr(92)+song_only

    # Get Length
    song_mutagen=MP3(song)
    song_length=song_mutagen.info.length
    '''
    selected_song=song_box.get(ACTIVE)
    selected_song_path=song_box.curselection()
    song_index=(selected_song_path[0])
    
    song_path=files_path[song_index]
    song_only=(selected_song)
    song=song_path+chr(92)+song_only
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(music_slider.get()))
    #slider_label.config(text=f'{int(music_slider.get())}  of  {int(song_length)}')



# Volume Slider Function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    # Get CUrrent Volume
    current_volume=pygame.mixer.music.get_volume()

    # Convert Floats to Multiples of 10
    current_volume=current_volume*100
    #slider_label.cofig(text=current_volume*100)

    # Change Volume Meter Bar
    if int(current_volume)<1:
        volume_meter_frame.config(image=vol0)
    elif int(current_volume)<1 and int(current_volume)<=5:
        volume_meter_frame.config(image=vol5)
    elif int(current_volume)<5 and int(current_volume)<=10:
        volume_meter_frame.config(image=vol10)
    elif int(current_volume)<10 and int(current_volume)<=15:
        volume_meter_frame.config(image=vol15)
    elif int(current_volume)<15 and int(current_volume)<=20:
        volume_meter_frame.config(image=vol20)
    elif int(current_volume)<20 and int(current_volume)<=25:
        volume_meter_frame.config(image=vol25)
    elif int(current_volume)<25 and int(current_volume)<=30:
        volume_meter_frame.config(image=vol30)
    elif int(current_volume)<30 and int(current_volume)<=35:
        volume_meter_frame.config(image=vol35)
    elif int(current_volume)<35 and int(current_volume)<=40:
        volume_meter_frame.config(image=vol40)
    elif int(current_volume)<40 and int(current_volume)<=45:
        volume_meter_frame.config(image=vol45)
    elif int(current_volume)<45 and int(current_volume)<=50:
        volume_meter_frame.config(image=vol50)
    elif int(current_volume)<50 and int(current_volume)<=55:
        volume_meter_frame.config(image=vol55)
    elif int(current_volume)<55 and int(current_volume)<=60:
        volume_meter_frame.config(image=vol60)
    elif int(current_volume)<60 and int(current_volume)<=65:
        volume_meter_frame.config(image=vol65)
    elif int(current_volume)<65 and int(current_volume)<=70:
        volume_meter_frame.config(image=vol70)
    elif int(current_volume)<70 and int(current_volume)<=75:
        volume_meter_frame.config(image=vol75)
    elif int(current_volume)<75 and int(current_volume)<=80:
        volume_meter_frame.config(image=vol80)
    elif int(current_volume)<80 and int(current_volume)<=85:
        volume_meter_frame.config(image=vol85)
    elif int(current_volume)<85 and int(current_volume)<=90:
        volume_meter_frame.config(image=vol90)
    elif int(current_volume)<90 and int(current_volume)<=95:
        volume_meter_frame.config(image=vol95)
    elif int(current_volume)<95 and int(current_volume)<=100:
        volume_meter_frame.config(image=vol100)


## Functions for Volume Up and Volume Down Keys

# Volume Up
def vol_up(event):
    if event:
        pygame.mixer.music.set_volume(volume_slider.get())
        # Get the CUrrent Volume
        current_volume=pygame.mixer.music.get_volume()

        # Convert Floats to Multiples of 10
        current_volume=current_volume*100
        current_volume=current_volume+5

def vol_down(event):
    if event:
        pygame.mixer.music.set_volume(volume_slider.get())
        # Get the CUrrent Volume
        current_volume=pygame.mixer.music.get_volume()

        # Convert Floats to Multiples of 10
        current_volume=current_volume*100
        current_volume=current_volume-5
#============================================================================================================================================
# Master Frame
master_frame=Frame(app)
master_frame.pack(pady=20)


# Playlist Box
song_box= Listbox(master_frame, bg='#2c2c2c', fg='white',width=63, selectbackground='#ffba00',selectforeground='#2c2c2c',font=('montserrat',9,'bold'))
song_box.grid(row=0,column=0)


# Button Images
forward_btn_img=PhotoImage(file="Images\_nextt.png")
back_btn_img=PhotoImage(file='Images\prev.png')
play_btn_img=PhotoImage(file='Images\playy.png')
pause_btn_img=PhotoImage(file='Images\pausee.png')
stop_btn_img=PhotoImage(file='Images\stopp.png')

# Volume Control Images
global vol
global vol0
global vol5
global vol10
global vol15
global vol20
global vol25
global vol30
global vol35
global vol40
global vol45
global vol50
global vol55
global vol60
global vol65
global vol70
global vol75
global vol80
global vol85
global vol90
global vol95
global vol100

vol=PhotoImage(file='Images\Vol\Vol.png')
vol0=PhotoImage(file='Images\Vol\Vol0.png')
vol5=PhotoImage(file='Images\Vol\Vol5.png')
vol10=PhotoImage(file='Images\Vol\Vol10.png')
vol15=PhotoImage(file='Images\Vol\Vol15.png')
vol20=PhotoImage(file='Images\Vol\Vol20.png')
vol25=PhotoImage(file='Images\Vol\Vol25.png')
vol30=PhotoImage(file='Images\Vol\Vol30.png')
vol35=PhotoImage(file='Images\Vol\Vol35.png')
vol40=PhotoImage(file='Images\Vol\Vol40.png')
vol45=PhotoImage(file='Images\Vol\Vol45.png')
vol50=PhotoImage(file='Images\Vol\Vol50.png')
vol55=PhotoImage(file='Images\Vol\Vol55.png')
vol60=PhotoImage(file='Images\Vol\Vol60.png')
vol65=PhotoImage(file='Images\Vol\Vol65.png')
vol70=PhotoImage(file='Images\Vol\Vol70.png')
vol75=PhotoImage(file='Images\Vol\Vol75.png')
vol80=PhotoImage(file='Images\Vol\Vol80.png')
vol85=PhotoImage(file='Images\Vol\Vol85.png')
vol90=PhotoImage(file='Images\Vol\Vol90.png')
vol95=PhotoImage(file='Images\Vol\Vol95.png')
vol100=PhotoImage(file='Images\Vol\Vol100.png')

# Controls Frame
controls_frame=Frame(master_frame)
controls_frame.grid(row=1,column=0,pady=20)

# Music Slider Frame
music_slider_frame=LabelFrame(master_frame)
music_slider_frame.grid(row=2,column=0,pady=10,padx=10)

# Volume Frame
volume_frame=LabelFrame(master_frame, text='Volume',bd=4,relief=GROOVE,font=('gilroy',10,'bold'))
volume_frame.grid(row=3,column=0,padx=10)

# Volume Bar and Meter Separator
sep=Label(volume_frame,image=vol)
sep.grid(row=0,column=1,padx=60)

# Volume Meter Frame
volume_meter_frame=Label(volume_frame,image=vol100)
volume_meter_frame.grid(row=0,column=2,padx=10,pady=20)


# Player Buttons
back_btn=Button(controls_frame, image=back_btn_img , borderwidth=0,command=lambda:previous_song(True))
forward_btn=Button(controls_frame, image=forward_btn_img , borderwidth=0, command=lambda:next_song(True))
play_btn=Button(controls_frame, image=play_btn_img , borderwidth=0,command=lambda:play(True))
pause_btn=Button(controls_frame, image=pause_btn_img , borderwidth=0,command=lambda:pause(paused))
stop_btn=Button(controls_frame, image=stop_btn_img , borderwidth=0,command=lambda:stop(True))

back_btn.grid(row=0,column=0,padx=10)
forward_btn.grid(row=0,column=1,padx=10)
play_btn.grid(row=0,column=2,padx=10)
pause_btn.grid(row=0,column=3,padx=10)
stop_btn.grid(row=0,column=4,padx=10)

# Menu Bar
menu = Menu(app) 
app.config(menu=menu) 

# Song Menu
songmenu = Menu(menu,tearoff=0) 
menu.add_cascade(label="Add Songs", menu=songmenu) 
songmenu.add_command(label="Add One Song to Playlist", command=lambda:add_song(True),accelerator='[Ctrl+O]' ) 
songmenu.add_command(label="Add Many Songs to Playlist", command=lambda:add_many_songs(True),accelerator='[Ctrl+A]' ) 
songmenu.add_separator()

# Remove Songs Menu
remove_songs_menu=Menu(menu,tearoff=0)
menu.add_cascade(label="Remove Songs", menu=remove_songs_menu) 
remove_songs_menu.add_command(label="Selected Song", command=remove_one_song)
remove_songs_menu.add_command(label="All Songs", command=remove_all_song)  

# Help Menu
helpmenu = Menu(menu,tearoff=0)
menu.add_cascade(label="About", menu=helpmenu) 
helpmenu.add_command(label="Developer's Info",command=about)

# Status Bar
status_bar=Label(app,text='Status Bar'+'   ',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=3)

# Music Slider
music_slider=ttk.Scale(music_slider_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=600)
music_slider.pack(pady=20,padx=20)

# Volume Slider
volume_slider=ttk.Scale(volume_frame, from_=0, to=1, orient=HORIZONTAL, value=1, command=volume, length=200)
volume_slider.grid(row=0,column=0,padx=15)

# Bidings
app.bind('<N>', next_song)
app.bind('<n>', next_song)
app.bind('<space>', play)
app.bind('<b>', pause)
app.bind('<P>', previous_song)
app.bind('<p>', previous_song)
app.bind('<S>', stop)
app.bind('<s>', stop)
app.bind('<Control-O>', add_song)
app.bind('<Control-o>', add_song)
app.bind('<Control-A>', add_many_songs)
app.bind('<Control-a>', add_many_songs)


# Temporary Slider Label
#slider_label=Label(app, text='0')
#slider_label.pack(pady=20)


app.mainloop()