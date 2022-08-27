import tkinter as tk
import time
import random
import bot

def win_search():
    global board, board_array
    moves_played = len(board)
    red_or_yellow = 4*((moves_played + 1) % 2) + 1
    row = 5
    while board_array[row][int(board[-1])] != 0:
        row -= 1
    board_array[row][int(board[-1])] = red_or_yellow
    game_state = "continue"
    for i in range(0, 6):
        for j in range(0, 4):
            total = 0
            for k in range(0, 4):
                total += board_array[i][j + k]
            if total / red_or_yellow == 4:
                game_state = red_or_yellow
    for i in range(0, 3):
        for j in range(0, 7):
            total = 0
            for k in range(0, 4):
                total += board_array[i + k][j]
            if total / red_or_yellow == 4:
                game_state = red_or_yellow
        for j in range(0, 4):
            total = 0
            for k in range(0, 4):
                total += board_array[i + k][j + k]
            if total / red_or_yellow == 4:
                game_state = red_or_yellow
        for j in range(3, 7):
            total = 0
            for k in range(0, 4):
                total += board_array[i + k][j - k]
            if total / red_or_yellow == 4:
                game_state = red_or_yellow
    if game_state == 1:
        game_state = "Red"
    elif game_state == 5:
        game_state = "Yellow"
    return game_state


def bot_makes_move():
    global what_pressed_where, board, board_array
    move = random.randrange(0, 7)
    while what_pressed_where[move] >= 6:
        move = random.randrange(0, 7)
    return move


def set_difficulty(difficulty):
    interaction.configure(text=difficulty+" Difficulty")


def back_to_menu():
    interaction.configure(text="Choose your difficulty!")
    easy_button.grid(row=1, column=0), medium_button.grid(row=1, column=1)
    hard_button.grid(row=1, column=2), empty_label.grid(row=2, column=1)
    settings_button.grid(row=4, column=2), exit_button.grid(row=4, column=0)
    game_frame.configure(bg="White")
    title.configure(font=("Consolas", "40", "bold"))
    menu_button.grid_forget()
    restart_button.grid_forget()
    for j in range(1, 8):
        btns[j-1].grid_forget()
    sqr_number = -1
    for i in range(1, 7):
        for j in range(1, 8):
            sqr_number += 1
            sqrs[sqr_number].grid_forget()


def restart():
    global what_pressed_where, board, board_array
    set_difficulty("Medium")
    what_pressed_where = [0, 0, 0, 0, 0, 0, 0]
    board_array = [[0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0]]
    board = ''
    sqr_number = -1
    for i in range(1, 7):
        for j in range(1, 8):
            sqr_number += 1
            sqrs[sqr_number].configure(bg="#2AB0F2")
    for i in range(0, 7):
        btns[i]["state"] = "active"


def main_action(which_button_was_pressed):
    global what_pressed_where, board
    what_pressed_where[which_button_was_pressed] += 1
    board = board + str(which_button_was_pressed)
    sqr_target = which_button_was_pressed + 7*(6 - what_pressed_where[which_button_was_pressed])
    sqrs[sqr_target].configure(bg="Red")
    state = win_search()
    if state == "continue":
        bot_move = int(bot.tree(board, 7).best_move)
        board = board + str(bot_move)
        what_pressed_where[bot_move] += 1
        time.sleep(1)
        sqrs[bot_move + 7*(6 - what_pressed_where[bot_move])].configure(bg="Yellow")
        state = win_search()
        if state != "continue":
            interaction.configure(text=state+" wins!")
            for i in range(0, 7):
                btns[i]["state"] = "disabled"
##        print(int(bot.tree(board, 7).best_move))
    else:
        interaction.configure(text=state+" wins!")
        for i in range(0, 7):
            btns[i]["state"] = "disabled"
    for i in range(0, 7):
        if what_pressed_where[i] >= 6:
            btns[i]["state"] = "disabled"


def play_game():
    global what_pressed_where, board, board_array
    easy_button.grid_forget(), medium_button.grid_forget(), hard_button.grid_forget()
    settings_button.grid_forget(), exit_button.grid_forget(), empty_label.grid_forget()
    menu_button.grid(row=1, column=0)
    restart_button.grid(row=1, column=2)
    game_frame.configure(bg="Blue")
    title.configure(font=("Consolas", "15", "bold"))
    what_pressed_where = [0, 0, 0, 0, 0, 0, 0]
    board_array = [[0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0]]
    board = ''
    for j in range(0, 7):
        btns[j].grid(row=0, column=j+1, padx=5, pady=5)
        btns[j]["state"] = "active"
    sqr_number = -1
    for i in range(1, 7):
        for j in range(1, 8):
            sqr_number += 1
            sqrs[sqr_number].grid(row=i, column=j, padx=7, pady=7)
            sqrs[sqr_number].configure(bg="#2AB0F2")


window = tk.Tk()
window.configure(bg="White")
window.geometry("400x320")
info_frame = tk.Frame(master=window,
                      bg="White")
title = tk.Label(master=info_frame,
                 text='Connect Four',
                 font=("Consolas", "40", "bold"),
                 bg="White")
interaction = tk.Label(master=info_frame,
                       text='Choose your difficulty:',
                       bg="White")
outer_game_frame = tk.Frame(master=window,
                            bg="White")
game_frame = tk.Frame(master=outer_game_frame,
                      bg="White")
easy_button = tk.Button(master=game_frame,
                        text="   Easy   ",
                        bg="white",
                        command=lambda x='Easy': [set_difficulty(x), play_game()])
medium_button = tk.Button(master=game_frame,
                          text="Medium",
                          bg="white",
                          command=lambda x ='Medium': [set_difficulty(x), play_game()])
hard_button = tk.Button(master=game_frame,
                        text="Hard",
                        bg="white",
                        command=lambda x='Hard': [set_difficulty(x), play_game()])
settings_button = tk.Button(master=game_frame,
                            text="Settings",
                            bg="White")
restart_button = tk.Button(master=outer_game_frame,
                           text='      Restart      ',
                           command=lambda: restart(),
                           bg="White")
menu_button = tk.Button(master=outer_game_frame,
                        text='Back to Menu',
                        command=lambda: back_to_menu(),
                        bg="White")
empty_label = tk.Label(master=game_frame,
                       text='      ',
                       bg="White")
empty_label1 = tk.Label(master=game_frame,
                        text='      ',
                        bg="White")
exit_button = tk.Button(master=game_frame,
                        text='Exit Game',
                        command=window.destroy,
                        bg="White")
btns = []
for btn_activation in range(0, 7):
    btns.append(tk.Button(master=game_frame,
                          text=chr(0x25BC),
                          height=1,
                          width=2,
                          command=lambda x=btn_activation: main_action(x)))
sqrs = []
for sqr_activation in range(0, 42):
    sqrs.append(tk.Label(master=game_frame,
                         text=' ',
                         height=1,
                         width=2,
                         bg="White"))

info_frame.pack()
title.pack()
interaction.pack()
outer_game_frame.pack()
game_frame.grid(row=0, column=1)
empty_label1.grid(row=0, column=1)
easy_button.grid(row=1, column=0)
medium_button.grid(row=1, column=1)
hard_button.grid(row=1, column=2)
empty_label.grid(row=3, column=1)
settings_button.grid(row=4, column=2)
exit_button.grid(row=4, column=0)

window.mainloop()

