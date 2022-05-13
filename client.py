import socket
from threading import Thread
from tkinter import *
from xmlrpc.client import Server
from PIL import ImageTk,Image
import random

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None

canvas1 = None
player_name = None
name_entry = None
name_window = None

canvas2 = None
game_window = None
dice = None

left_boxes = []
right_boxes = []

finishing_box = None
player_type = None
roll_button = None
player_turn = None

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS
    IP_ADDRESS = '127.0.0.1'
    PORT = 5000
    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))
    ask_player_name()

def ask_player_name():
    global player_name
    global name_entry
    global name_window
    global canvas1
    global screen_height
    global screen_width

    name_window = Tk()
    name_window.title('Ludo Ladder')
    name_window.attributes('-fullscreen',True)
    screen_width = name_window.winfo_screenwidth()
    screen_height = name_window.winfo_screenheight()
    bg = ImageTk.PhotoImage(file = './assets/background.png')
    canvas1 = Canvas(name_window,width = 500,height = 500)
    canvas1.pack(fill = 'both',expand = True)
    canvas1.create_image(0,0,image = bg,anchor = 'nw')
    canvas1.create_text(screen_width/2,screen_height/5,text = 'Enter Your Name',font = ('Chalkboard SE',100),fill = 'white')

    name_entry = Entry(name_window,width = 15,justify='center',bd = 5,bg = 'white',font = ('Chalkboard SE',50))
    name_entry.place(x = screen_width/2-220,y = screen_height/4+100)

    button = Button(name_window,text= 'Save',font=('Chalkboard SE',30),width = 15,bd = 3,height = 2,bg = 'yellow',command = save_name)
    button.place(x = screen_width/2-130,y=screen_height/2-30)
    name_window.resizable(True,True)
    name_window.mainloop()

def save_name():
    global SERVER
    global player_name
    global name_window
    global name_entry

    player_name = name_entry.get()
    name_entry.delete(0,END)
    name_window.destroy()
    SERVER.send(player_name.encode())

    gameWindow()

def gameWindow():
    global game_window
    global canvas2
    global screen_height
    global screen_width
    global dice 

    game_window = Tk()
    game_window.title('Ludo Ladder')
    game_window.attributes('-fullscreen',True)
    screen_width = game_window.winfo_screenwidth()
    screen_height = game_window.winfo_screenheight()
    canvas2 = Canvas(game_window,width = 500,height = 500)
    canvas2.pack(fill = 'both',expand = True)
    bg = ImageTk.PhotoImage(file = './assets/background.png')
    canvas2.create_image(0,0,image = bg,anchor = 'nw')
    canvas2.create_text(screen_width/2,screen_height/5,text = 'Ludo Ladder',font = ('Helvetica bold',100),fill = 'white')

    left_board()
    right_board()
    finishingBox()

    global roll_button
    roll_button = Button(game_window,text = 'Roll Dice',fg = 'black',font = ('Chalkboard SE',15),bg = 'lightblue', command = roll_dice,width = 20,height = 5)

    global player_name
    global player_turn
    global player_type

    if (player_type=='player1' and player_turn):
        roll_button.place(x = screen_width/2-80,y = screen_height/2+250)
    else:
        roll_button.pack_forget() 

    dice = canvas2.create_text(screen_width/2+10,screen_height/2+250,text = '\u2680',font = ('Chalkboard SE',250),fill ='white' )
    game_window.resizable(True,True)
    game_window.mainloop()

def left_board():
    global game_window
    global left_boxes
    global screen_height

    x_position = 30

    for box in range(0,9):
        if box == 0:
            box_label = Label(game_window,font = ('Helvetica',30),width= 2,height=1,borderwidth=0,bg = 'red',relief = 'ridge')
            box_label.place(x = x_position,y = screen_height/2-88)
            left_boxes.append(box_label)
            x_position+=50
        else:
            box_label = Label(game_window,font = ('Helvetica',55),width = 2,height = 1,relief = 'ridge',borderwidth=1,bg = 'white')
            box_label.place(x = x_position,y = screen_height/2-100)
            left_boxes.append(box_label)
            x_position+=80

def right_board():
    global game_window
    global right_boxes
    global screen_height

    x_position = 750

    for box in range(0,9):
        if box == 8:
            box_label = Label(game_window,font = ('Helvetica',30),width= 2,height=1,borderwidth=1,bg = 'blue',relief = 'ridge')
            box_label.place(x = x_position,y = screen_height/2-88)
            right_boxes.append(box_label)
            x_position+=50
        else:
            box_label = Label(game_window,font = ('Helvetica',55),width = 2,height = 1,relief = 'ridge',borderwidth=1,bg = 'white')
            box_label.place(x = x_position,y = screen_height/2-100)
            right_boxes.append(box_label)
            x_position+=80

def finishingBox():
    global game_window
    global finishing_box
    global screen_height
    global screen_width

    finishing_box = Label(game_window,text = 'Home',font = ('Chalkboard SE',32),width = 8,height = 4,borderwidth=1,bg = 'yellow',fg = 'black')
    finishing_box.place(x = screen_width/2-100,y = screen_height/2-160)

def roll_dice():
    global SERVER
    global player_type
    global player_turn
    global roll_button

    dice_choices = ['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
    value = random.choice(dice_choices)

    roll_button.destroy()
    player_turn = False

    if (player_type == 'player1'):
        SERVER.send(f'{value}player2Turn'.encode())

    if(player_type == 'player2'):
        SERVER.send(f'{value}player1Turn'.encode())

setup()
