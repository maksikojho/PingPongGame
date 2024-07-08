from tkinter import *

root = Tk()
c = Canvas(root, width=800, height=500, background="#003300")
c.pack()

c.create_line(50, 0, 50, 500, fill="white")
c.create_line(400, 0, 400, 500, fill="white")
c.create_line(750, 0, 750, 500, fill="white")

ball = c.create_oval(390, 240, 410, 260, fill="white")
raket1 = c.create_rectangle(0, 10, 50, 60, fill="red")
raket2 = c.create_rectangle(750, 390, 800, 450, fill="blue")

pad_speed = 5
speedl = 0
speedr = 0


def move_pads():
    pads = {raket1: speedl, raket2: speedr}
    for pad in pads:
        c.move(pad, 0,pads[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > 500:
            c.move(pad,0, 500 - c.coords(pad)[3],)


c.focus_set()


def move_raket(event):
    global speedl, speedr
    if event.keysym == "w":
        speedl = -pad_speed
    elif event.keysym == "s":
        speedl = pad_speed
    elif event.keysym == "Up":
        speedr = -pad_speed
    elif event.keysym == "Down":
        speedr = pad_speed


c.bind("<KeyPress>", move_raket)


def stop_pad(event):
    global speedl, speedr
    if event.keysym in "ws":
        speedl = 0
    elif event.keysym in ("Up", "Down"):
        speedr = 0


c.bind("<KeyRelease>", stop_pad)

import random

ball_x_speed = 5
ball_y_speed = 0


def bounce(action):
    global ball_x_speed, ball_y_speed
    if action == "strike":
        if ball_y_speed ==0:
            ball_y_speed = random.random()
        ball_x_speed = -ball_x_speed
    else:
        ball_y_speed = -ball_y_speed
        pass


def move_ball():
    ball_left, ball_top, ball_right, ball_bot = c.coords(ball)

    if ball_right + ball_x_speed <= 750 and ball_left + ball_x_speed >= 50:
        c.move(ball, ball_x_speed, ball_y_speed)
    elif ball_left <= 50 or ball_right >= 750:
        ball_c = (ball_top + ball_bot) / 2
        if ball_right > 400:
            if c.coords(raket2)[1] < ball_c < c.coords(raket2)[3]:
                bounce("strike")
                print('strike1')

            else:
                update_score("left")
                c.itemconfigure(ball, state='hidden')
                c.update()
                c.after(1000, spawn_ball())
        else:
            print('ball left')
            if c.coords(raket1)[1] < ball_c < c.coords(raket1)[3]:
                bounce("strike")

            else:
                update_score("right")
                c.itemconfigure(ball, state='hidden')
                c.update()
                c.after(1000, spawn_ball())
    else:
        pass
    if ball_top + ball_y_speed < 0 or ball_bot + ball_y_speed > 500:
        bounce("ricochet")


player1 = 0
player2 = 0

p_1 = c.create_text(300, 20, text=player1, font=('Arial', 15), fill="white")
p_2 = c.create_text(500, 20, text=player2, font=('Arial', 15), fill="white")

zero_speed = 1


def update_score(player):
    global player1, player2
    if player == "left":
        player1 += 1
        c.itemconfigure(p_1, text=player1)
    else:
        player2 += 1
        c.itemconfigure(p_2, text=player2)


def spawn_ball():
    global ball_x_speed, ball_y_speed
    ball_x_speed = -ball_x_speed
    ball_y_speed = 0
    c.itemconfigure(ball, state='normal')
    c.coords(ball, 390, 240, 410, 260)


def main():
    move_ball()
    move_pads()
    root.after(20, main)

if __name__ == '__main__':
    main()
root.mainloop()