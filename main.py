import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import time

root = tk.Tk()
root.title("Snake & Ladders Deluxe")
root.geometry("900x650")

canvas = tk.Canvas(root,width=600,height=600,bg="white")
canvas.pack(side=tk.LEFT)

frame = tk.Frame(root)
frame.pack(side=tk.RIGHT,padx=20)

cell = 60

snakes = {16:6, 47:26, 49:11, 56:53, 62:19,
          64:60, 87:24, 93:73, 95:75, 98:78}

ladders = {1:38, 4:14, 9:31, 21:42, 28:84,
           36:44, 51:67, 71:91, 80:100}

player1_pos = 0
player2_pos = 0
turn = 1

# LOAD DICE
dice_img=[]
for i in range(1,7):
    img=Image.open(f"dice{i}.png")
    img=img.resize((100,100))
    dice_img.append(ImageTk.PhotoImage(img))

# LOAD SNAKE IMAGE


dice_label=tk.Label(frame,image=dice_img[0])
dice_label.pack(pady=20)

turn_label=tk.Label(frame,text="Player 1 Turn",font=("Arial",18))
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
            canvas.create_rectangle(x1,y1,x2,y2,fill="#d1e7dd")
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
                           width=6,fill="red",smooth=True) 

# DRAW LADDERS
def draw_ladders():
    for start,end in ladders.items():
        x1,y1=get_coords(start)
        x2,y2=get_coords(end)
        canvas.create_line(x1,y1,x2,y2,width=5,fill="yellow")
        canvas.create_line(x1+10,y1,x2+10,y2,width=5,fill="yellow")

draw_snakes()
draw_ladders()


# TOKENS
p1=canvas.create_oval(10,550,40,580,fill="red")
p2=canvas.create_oval(50,550,80,580,fill="blue")

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

# DICE ROLL
def roll_dice():
    global player1_pos,player2_pos,turn

    dice=random.randint(1,6)
    roll_animation(dice)

    if turn==1:
        if player1_pos+dice<=100:
            animate(p1,player1_pos,player1_pos+dice)
            player1_pos+=dice

            if player1_pos in snakes:
                animate(p1,player1_pos,snakes[player1_pos])
                player1_pos=snakes[player1_pos]

            elif player1_pos in ladders:
                animate(p1,player1_pos,ladders[player1_pos])
                player1_pos=ladders[player1_pos]

        if player1_pos==100:
            messagebox.showinfo("Winner","Player 1 Wins!")
            return

        turn=2
        turn_label.config(text="Player 2 Turn")

    else:
        if player2_pos+dice<=100:
            animate(p2,player2_pos,player2_pos+dice)
            player2_pos+=dice

            if player2_pos in snakes:
                animate(p2,player2_pos,snakes[player2_pos])
                player2_pos=snakes[player2_pos]

            elif player2_pos in ladders:
                animate(p2,player2_pos,ladders[player2_pos])
                player2_pos=ladders[player2_pos]

        if player2_pos==100:
            messagebox.showinfo("Winner","Player 2 Wins!")
            return

        turn=1
        turn_label.config(text="Player 1 Turn")

def restart():
    global player1_pos,player2_pos,turn
    player1_pos=0
    player2_pos=0
    turn=1
    canvas.coords(p1,10,550,40,580)
    canvas.coords(p2,50,550,80,580)
    turn_label.config(text="Player 1 Turn")

btn=tk.Button(frame,text="ROLL DICE",
              command=roll_dice,font=("Arial",16),
              bg="green",fg="white")
btn.pack(pady=20)

restart_btn=tk.Button(frame,text="RESTART",
                      command=restart,font=("Arial",16),
                      bg="red",fg="white")
restart_btn.pack()

root.mainloop()
