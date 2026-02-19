import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import time

root = tk.Tk()
root.configure(bg="#2c2f33")
root.title("Snake & Ladders Deluxe")
root.geometry("900x650")

canvas = tk.Canvas(root,width=600,height=600,
                   bg="#23272a",highlightthickness=0)
canvas.pack(side=tk.LEFT)

frame = tk.Frame(root,bg="#2c2f33")
frame.pack(side=tk.RIGHT,padx=20)
title=tk.Label(frame,text="🐍 Snake & Ladder",
               font=("Arial",24,"bold"),
               fg="white",bg="#2c2f33")
title.pack(pady=10)


cell = 60

snakes = {16:6, 47:26, 49:11, 85:56, 62:19,
          64:60, 87:24, 93:73, 95:75, 98:78}

ladders = {1:38, 4:14, 9:31, 21:42, 28:84,
           36:44, 51:67, 71:91, 80:100}

# ⭐ MULTIPLAYER VARIABLES
positions=[]
tokens=[]
turn=0
num_players=0
colors=["red","blue","green","purple"]

# LOAD DICE
dice_img=[]
for i in range(1,7):
    img=Image.open(f"images/dice{i}.png")
    img=img.resize((100,100))
    dice_img.append(ImageTk.PhotoImage(img))

dice_label=tk.Label(frame,image=dice_img[0],
                    bg="#2c2f33")
dice_label.pack(pady=20)

turn_label=tk.Label(frame,
                    text="Select Players",
                    font=("Arial",18,"bold"),
                    fg="cyan",
                    bg="#2c2f33")
turn_label.pack()

# BOARD
def draw_board():
    num=100
    for row in range(10):
        if row%2==0:
            cols=range(10)
        else:
            cols=range(9,-1,-1)
        for col in cols:
            x1=col*cell
            y1=row*cell
            x2=x1+cell
            y2=y1+cell
            color = "#99aab5" if (row+col)%2==0 else "#7289da"
            canvas.create_rectangle(x1,y1,x2,y2,
                        fill=color,
                        outline="#2c2f33")
            canvas.create_text(x1+30,y1+30,text=str(num))
            num-=1

draw_board()

def get_coords(pos):
    if pos==0:
        return (10,550)
    pos-=1
    row=9-(pos//10)
    col=pos%10
    if (pos//10)%2==1:
        col=9-col
    x=col*60+15
    y=row*60+15
    return x,y

# DRAW SNAKES
def draw_snakes():
    for head,tail in snakes.items():
        x1,y1=get_coords(head)
        x2,y2=get_coords(tail)
        canvas.create_line(x1+15,y1+15,x2+15,y2+15,
                           width=7,fill="red",smooth=True)

# DRAW LADDERS
def draw_ladders():
    for start,end in ladders.items():
        x1,y1=get_coords(start)
        x2,y2=get_coords(end)
        canvas.create_line(x1,y1,x2,y2,width=3,fill="yellow")
        canvas.create_line(x1+10,y1,x2+10,y2,width=3,fill="yellow")

draw_snakes()
draw_ladders()

# ANIMATION
def animate(token,start,end):
    for i in range(start+1,end+1):
        x,y=get_coords(i)
        canvas.coords(token,x,y,x+30,y+30)
        root.update()
        time.sleep(0.15)

# DICE ROLL ANIMATION
def roll_animation(final):
    for _ in range(10):
        rand=random.randint(0,5)
        dice_label.config(image=dice_img[rand])
        root.update()
        time.sleep(0.08)
    dice_label.config(image=dice_img[final-1])

# ⭐ START GAME AFTER SELECTION
def start_game(players):
    global num_players,positions,tokens,turn

    num_players=players
    positions=[0]*num_players
    turn=0

    for i in range(num_players):
        token=canvas.create_oval(10+i*20,550,
                                 40+i*20,580,
                                 fill=colors[i])
        tokens.append(token)

    turn_label.config(text="Player 1 Turn")

# ⭐ PLAYER POPUP
def player_popup():
    popup=tk.Toplevel(root)
    popup.title("Select Players")
    popup.geometry("300x200")

    tk.Label(popup,text="Select Number of Players",
             font=("Arial",14)).pack(pady=20)

    def choose(n):
        start_game(n)
        popup.destroy()

    tk.Button(popup,text="2 Players",
              command=lambda:choose(2)).pack(pady=5)

    tk.Button(popup,text="3 Players",
              command=lambda:choose(3)).pack(pady=5)

    tk.Button(popup,text="4 Players",
              command=lambda:choose(4)).pack(pady=5)

# MULTIPLAYER DICE ROLL
def roll_dice():
    global turn

    if num_players==0:
        return

    dice=random.randint(1,6)
    roll_animation(dice)

    current_pos=positions[turn]

    if current_pos+dice<=100:
        animate(tokens[turn],current_pos,current_pos+dice)
        positions[turn]+=dice

        if positions[turn] in snakes:
            animate(tokens[turn],positions[turn],
                    snakes[positions[turn]])
            positions[turn]=snakes[positions[turn]]

        elif positions[turn] in ladders:
            animate(tokens[turn],positions[turn],
                    ladders[positions[turn]])
            positions[turn]=ladders[positions[turn]]

    if positions[turn]==100:
        messagebox.showinfo("Winner",
                            f"Player {turn+1} Wins!")
        return

    turn=(turn+1)%num_players
    turn_label.config(
    text=f"Player {turn+1} Turn",
    fg=colors[turn])


def restart():
    global positions,turn,tokens

    for t in tokens:
        canvas.delete(t)

    tokens.clear()

    positions=[0]*num_players
    turn=0

    for i in range(num_players):
        token=canvas.create_oval(10+i*20,550,
                                 40+i*20,580,
                                 fill=colors[i])
        tokens.append(token)

    turn_label.config(text="Player 1 Turn")

btn=tk.Button(frame,
              text="🎲 ROLL DICE",
              command=roll_dice,
              font=("Arial",16,"bold"),
              bg="#5865f2",
              fg="white",
              activebackground="#4752c4",
              width=15,
              relief="flat")

btn.pack(pady=20)

restart_btn=tk.Button(frame,
                      text="🔁 RESTART",
                      command=restart,
                      font=("Arial",16,"bold"),
                      bg="#ed4245",
                      fg="white",
                      activebackground="#c03537",
                      width=15,
                      relief="flat")

restart_btn.pack()

# ⭐ CALL POPUP AT START
player_popup()

root.mainloop()
