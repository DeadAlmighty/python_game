import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import pygame

pygame.mixer.init()

dice_sound = pygame.mixer.Sound("sounds/dice.wav")
snake_sound = pygame.mixer.Sound("sounds/snake.wav")
ladder_sound = pygame.mixer.Sound("sounds/ladder.wav")
win_sound = pygame.mixer.Sound("sounds/win.wav")

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

dice_box = tk.Frame(frame,width=160,height=200,
                    bg="#2c2f33")
dice_box.pack(pady=10)

dice_box.pack_propagate(False)

cell=60

snakes={16:6,47:26,49:11,85:56,62:19,
        64:60,87:24,93:73,95:75,98:78}

ladders={1:38,4:14,9:31,21:42,28:84,
         36:44,51:67,71:91,80:100}

positions=[]
tokens=[]
turn=0
num_players=0
colors=["red","blue","green","purple"]

dice_img=[]
for i in range(1,7):
    img=Image.open(f"images/dice{i}.png")
    img=img.resize((100,100))
    dice_img.append(ImageTk.PhotoImage(img))

dice_label=tk.Label(dice_box,image=dice_img[0],
                    bg="#2c2f33")
dice_label.place(relx=0.5,y=20,anchor="n")

turn_label=tk.Label(frame,text="Select Players",
                    font=("Arial",18,"bold"),
                    fg="cyan",
                    bg="#2c2f33")
turn_label.pack()

def draw_board():
    num=100
    for row in range(10):
        cols=range(10) if row%2==0 else range(9,-1,-1)
        for col in cols:
            x1=col*cell
            y1=row*cell
            x2=x1+cell
            y2=y1+cell
            color="#99aab5" if (row+col)%2==0 else "#7289da"
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
    return col*60+15,row*60+15

def draw_snakes():
    for h,t in snakes.items():
        x1,y1=get_coords(h)
        x2,y2=get_coords(t)
        canvas.create_line(x1+15,y1+15,x2+15,y2+15,
                           width=7,fill="red",smooth=True)
draw_snakes()

def draw_ladders():
    for s,e in ladders.items():
        x1,y1=get_coords(s)
        x2,y2=get_coords(e)
        canvas.create_line(x1,y1,x2,y2,width=3,fill="yellow")
        canvas.create_line(x1+10,y1,x2+10,y2,width=3,fill="yellow")
draw_ladders()

# ⭐ FIXED ANIMATION
def animate(token,start,end,callback=None):

    step = 1 if end > start else -1
    steps = list(range(start + step, end + step, step))

    def move():
        if not steps:
            if callback:
                callback()
            return

        pos = steps.pop(0)
        x,y=get_coords(pos)
        canvas.coords(token,x,y,x+30,y+30)
        root.after(140,move)

    move()

def roll_animation(final, callback=None):
    count=10
    def spin():
        nonlocal count
        if count==0:
            dice_label.config(image=dice_img[final-1])
            if callback:
                root.after(200,callback)
            return
        dice_label.config(image=random.choice(dice_img))
        count-=1
        root.after(80,spin)
    spin()

def finish_turn():
    global turn
    if positions[turn]==100:
        win_sound.play()
        messagebox.showinfo("Winner",f"Player {turn+1} Wins!")
        return
    turn=(turn+1)%num_players
    turn_label.config(text=f"Player {turn+1} Turn",
                      fg=colors[turn])

def roll_dice():
    global turn
    if num_players==0:
        return

    dice=random.randint(1,6)
    dice_sound.play()

    player_turn = turn
    current = positions[player_turn]

    def move_player():

        if current + dice > 100:
            finish_turn()
            return

        target = current + dice

        def after_walk():
            positions[player_turn] = target

            if target in snakes:
                snake_sound.play()
                snake_target = snakes[target]

                def after_snake():
                    positions[player_turn] = snake_target
                    finish_turn()

                animate(tokens[player_turn],target,snake_target,after_snake)

            elif target in ladders:
                ladder_sound.play()
                ladder_target = ladders[target]

                def after_ladder():
                    positions[player_turn] = ladder_target
                    finish_turn()

                animate(tokens[player_turn],target,ladder_target,after_ladder)

            else:
                finish_turn()

        animate(tokens[player_turn],current,target,after_walk)

    roll_animation(dice, move_player)

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

def player_popup():
    popup=tk.Toplevel(root)
    popup.title("Select Players")
    popup.geometry("300x200")
    popup.configure(bg="#2c2f33")
    tk.Label(popup,text="Select Number of Players",
             font=("Arial",14,"bold"),
             fg="white",bg="#2c2f33").pack(pady=20)
    tk.Button(popup,text="2 Players",
              command=lambda:(start_game(2),popup.destroy())
              ).pack(pady=5)
    tk.Button(popup,text="3 Players",
              command=lambda:(start_game(3),popup.destroy())
              ).pack(pady=5)
    tk.Button(popup,text="4 Players",
              command=lambda:(start_game(4),popup.destroy())
              ).pack(pady=5)

btn=tk.Button(frame,text="🎲 ROLL DICE",
              command=roll_dice,
              font=("Arial",16,"bold"),
              bg="#5865f2",
              fg="white",
              width=15)
btn.pack(pady=20)

restart_btn=tk.Button(frame,text="🔁 RESTART",
                      command=restart,
                      font=("Arial",16,"bold"),
                      bg="#ed4245",
                      fg="white",
                      width=15)
restart_btn.pack()

root.after(200,player_popup)
root.mainloop()