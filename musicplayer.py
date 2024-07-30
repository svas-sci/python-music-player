from pygame import mixer
from tkinter import *
from tkinter import messagebox
import os
import tkinter as tk
import mysql.connector


from tkinter import Tk
from tkinter.filedialog import askdirectory


global mostpl


db_connection = mysql.connector.connect(
  host="localhost",
   
  # Change your username here
  user="root",  
   
  # Change your password here
  passwd="root",  
   
  # Need to point for the correct db
  database="songs"
)
mydb= db_connection.cursor()


def selectfolder():


    global path
    global songs
    songs = []
    path = askdirectory(title='Select Folder')
    for name in os.listdir(path):
        with open(os.path.join(path, name)) as f:
            songs.append(name)
    print(songs)
    songs.append('nothing playing')


global i
i = -1


global x
x = 0


def resetstate():
    global x
    x = 0
    print('this is x', x)


def setnextsong():
    global i, x


    if i != len(songs)-2:
        i +=1
        mixer.music.load(path + '/'+songs[i])
       
        resetstate()
        toggle()
        print('this is i', i)
        x = 1
        l.config(text = songs[i])
       
    else:
        mixer.music.load(path + '/'+songs[len(songs)-2])
       
        resetstate()
        toggle()
        print('this is i', i)
        x = 1
        l.config(text = songs[i])




def setprevsong():
    global i, x
    if i != 0:
        i -=1
        mixer.music.load(path + '/'+songs[i])
        resetstate()
        toggle()
        print('this is i', i)
        x = 1
        l.config(text = songs[i])


    else:
        mixer.music.load(path + '/'+songs[0])
        resetstate()
        toggle()
        print('this is i', i)
        x = 1
        l.config(text = songs[i])


def onselect(event):
    global i, x
    w = event.widget
    idx = int(w.curselection()[0])
    value = w.get(idx)
    btn.config(bg = 'green', relief="sunken", text  = ' || ')
    mixer.music.load(path + '/' + value)
    mixer.music.play()
    x = 1
    i = songs.index(value)
    commandtoadd = 'UPDATE songplaylist SET timesplayed = timesplayed + 1 WHERE songname ='+"'"+songs[i]+"'"
    mydb.execute(commandtoadd)
    db_connection.commit()
    l.config(text = songs[i])
    updatemostplayed()


def refreshlist():
    deletet ="DROP TABLE songplaylist"
    mydb.execute(deletet)
    db_connection.commit()
    print('deleted table')
    createt = "CREATE TABLE songplaylist(songname varchar(100), timesplayed int)"
    mydb.execute(createt)
    db_connection.commit()
    print('created table')
    for t in range (len(songs)-1):
        toinsert = 'INSERT INTO songplaylist values'+"('"+songs[t]+"'"+', 0'+")"
   
        mydb.execute(toinsert)
        db_connection.commit()


def mostplayed():
    mydb.execute("select songname from songplaylist order by timesplayed desc limit 1;")
    result = mydb.fetchall()
    mydb.execute("select timesplayed from songplaylist order by timesplayed desc limit 1;")
    checking1 = mydb.fetchall()
    print(result)
    print(checking1)
    if checking1 == [(0,)]:
        return ' '
    else:

        return result


# Starting the mixer
mixer.init()
 
# Loading the song


 
# Setting the volume
mixer.music.set_volume(0.7)


x = 0


def sets():
    global x
    x = 1
    print('this is x', x)




def toggle():
    if x == 1:


        if btn.config('relief')[-1] == 'sunken':
            btn.config(bg = 'red', relief="raised", text = ' ▶ ')
            mixer.music.pause()
        else:
            btn.config(bg = 'green', relief="sunken", text = ' || ')
            mixer.music.unpause()


    elif x == 0:
        btn.config(bg = 'green', relief="sunken", text  = ' || ')
        commandtoadd = 'UPDATE songplaylist SET timesplayed = timesplayed + 1 WHERE songname ='+"'"+songs[i]+"'"
        mydb.execute(commandtoadd)
        db_connection.commit()
        mixer.music.play()


def updatemostplayed():
    mostpl.config(text = mostplayed())


root = Tk()
root.title(" ")
root.geometry('350x200')
menubar = Menu(root)
root.configure(bg = 'black')
root.config(menu=menubar)
file_menu = Menu(menubar)
file_menu.add_command(
    label='Select Folder',
    command=selectfolder,
)
file_menu.add_command(
    label='Reset',
    command=refreshlist
)
menubar.add_cascade(
    label="File",
    menu=file_menu,
    underline=0
)


check = 0


selectfolder()




btn = Button(root, text = ' ',
                command = lambda:[toggle(), sets(), updatemostplayed()],
                bg = 'grey')


btn2 = Button(root, text=' > ',
                command = lambda:[setnextsong(), updatemostplayed()],
                bg = 'grey')


btn3 = Button(root, text=' < ',
                command = lambda:[setprevsong(), updatemostplayed()],
                bg = 'grey')




box = Listbox(root, height=2)
for z in range (len(songs)-1):
    box.insert(z, songs[z])


scrollbar = Scrollbar(root)




box.bind("<<ListboxSelect>>", onselect)
box.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = box.yview)
box.pack()


l = Label(root, text = songs[i])
mostplay = Label(root, text = 'Most Played')
mostpl = Label(root, text = mostplayed(), )


# Set the position of button on the top of window
btn.pack(side = 'top')  
btn2.pack(side = 'right')
btn3.pack(side= 'left')
l.pack(padx = 20, pady = 10)
mostpl.pack(side='bottom')
mostplay.pack()


root.mainloop()



