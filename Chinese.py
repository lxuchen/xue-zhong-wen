from tkinter import *
from datetime import date
import os
import sqlite3

'''
Init the root widget with title
'''
root = Tk()
root.title("Robert学中文")

'''
Main function of dispalying a word in proper grid:
    - 'the_word_list contains the word and its pinyin, looks like this:
      ['鱼', 'yú']
    - 'the_word_audio is the string of the audio file path of the word:
      ./audio/鱼.m4a
    - the layout of a word GUI:
      ┌─frame title (number)────────┐
      │      ┌───────────────┐      │
      │      │  word label   │      │
      │      │ (word/pinyin) │      │
      │      └───────────────┘      │
      │ ┌───────────┐ ┌───────────┐ │
      │ │  toggle   │ │   play    │ │
      │ │show/unshow│ │   audio   │ │
      │ │  button   │ │   button  │ │
      │ └───────────┘ └───────────┘ │
      └─────────────────────────────┘
'''
toggle = 1
def show_word(card_index_list, card_index, word_index, frame_row, frame_col):

    conn = sqlite3.connect("Chinese.db")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM words1000 WHERE oid=" + str(card_index_list[card_index]*4 + word_index + 1))
    the_word_list = list(res.fetchone())
    conn.commit()
    conn.close()

    the_word_audio = "./audio/" + the_word_list[0] + ".m4a"

    word_frame = LabelFrame(root, text="[" + str(card_index_list[card_index]+1) + "-" + str(word_index+1) + "]", width=400, height=150, fg="blue")
    word_frame.grid(row=frame_row, column=frame_col)
    word_frame.grid_propagate(False)

    # print(the_word_list)

    if(the_word_list[2] == 1):
        word_label = Label(word_frame, text=the_word_list[toggle], padx=160, pady=20, font=("Kaiti SC", 40, 'bold'), fg="red")
        word_label.grid(sticky=W, row=0, column=0, columnspan=5)
    else:
        word_label = Label(word_frame, text=the_word_list[toggle] + '✅', padx=140, pady=20, font=("Kaiti SC", 40, 'bold'), fg="red")
        word_label.grid(sticky=W, row=0, column=0, columnspan=5)

    word_play_button = Button(word_frame, text="Play", command=lambda: play_audio(the_word_audio), fg="red")
    word_play_button.grid(row=1, column=0)

    word_toggle_button = Button(word_frame, text="Show", command=lambda: toggle_word(word_frame, word_label, word_toggle_button, card_index_list, card_index, word_index))
    word_toggle_button.grid(row=1, column=1)

    if(the_word_list[2] == 1):
        word_check_button = Button(word_frame, text="Check", command=lambda: check_word(word_frame, word_check_button, card_index_list, card_index, word_index, toggle))
        word_check_button.grid(row=1, column=2)
    else:
        word_check_button = Button(word_frame, text="Uncheck", command=lambda: uncheck_word(word_frame, word_check_button, card_index_list, card_index, word_index, toggle))
        word_check_button.grid(row=1, column=2)

    word_mark_button = Button(word_frame, text="Mark: " + str(the_word_list[3]), command=lambda: mark_word(word_frame, word_mark_button, card_index_list, card_index, word_index))
    word_mark_button.grid(row=1, column=3)

    word_reset_button = Button(word_frame, text="Reset", command=lambda: reset_mark(word_frame, word_mark_button, card_index_list, card_index, word_index))
    word_reset_button.grid(row=1, column=4)

'''
Function to toggle word/pinyin by showing different item in current_word_list
'''
def toggle_word(current_word_frame, current_word_label, current_word_toggle_button, current_card_index_list, current_card_index, current_word_index):
    global toggle
    conn = sqlite3.connect("Chinese.db")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM words1000 WHERE oid=" + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    the_word_list = list(res.fetchone())
    conn.commit()
    conn.close()

    if(toggle == 1):
        toggle = 0
    else:
        toggle = 1

    # print(the_word_list)

    if(the_word_list[2] == 1):
        current_word_label = Label(current_word_frame, text=the_word_list[toggle], padx=160, pady=20, font=("Kaiti SC", 40, 'bold'), fg="red")
        current_word_label.grid(sticky=W, row=0, column=0, columnspan=5)
    else:
        current_word_label = Label(current_word_frame, text=the_word_list[toggle] + '✅', padx=140, pady=20, font=("Kaiti SC", 40, 'bold'), fg="red")
        current_word_label.grid(sticky=W, row=0, column=0, columnspan=5)

    if(toggle == 0):
        current_word_toggle_button = Button(current_word_frame, text="Unshow", command=lambda: toggle_word(current_word_frame, current_word_label, current_word_toggle_button, current_card_index_list, current_card_index, current_word_index))
    else:
        current_word_toggle_button.destroy()
        current_word_toggle_button = Button(current_word_frame, text="Show", command=lambda: toggle_word(current_word_frame, current_word_label, current_word_toggle_button, current_card_index_list, current_card_index, current_word_index))
    current_word_toggle_button.grid(row=1, column=1)



'''
Function to play sound by calling afplay, slow but works
'''
def play_audio(audio_file_name):
    os.system("afplay " +  audio_file_name)

'''
Function to check word as fnished
'''
def check_word(current_word_frame, current_word_check_button, current_card_index_list, current_card_index, current_word_index, current_toggle):
    conn = sqlite3.connect("Chinese.db")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM words1000 WHERE oid=" + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    the_word_list = list(res.fetchone())
    cur.execute("UPDATE words1000 SET display = 0 WHERE oid = " + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    res = cur.execute("SELECT * FROM words1000 WHERE oid=" + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    the_word_list = list(res.fetchone())
    conn.commit()
    conn.close()

    # print(the_word_list)

    word_label = Label(current_word_frame, text=the_word_list[current_toggle] + '✅', padx=140, pady=20, font=("Kaiti SC", 40, 'bold'), fg="red")
    word_label.grid(sticky=W, row=0, column=0, columnspan=5)

    current_word_check_button = Button(current_word_frame, text="Uncheck", command=lambda: uncheck_word(current_word_frame, current_word_check_button, current_card_index_list, current_card_index, current_word_index, current_toggle))
    current_word_check_button.grid(row=1, column=2)

'''
Function to uncheck word
'''
def uncheck_word(current_word_frame, current_word_check_button, current_card_index_list, current_card_index, current_word_index, current_toggle):
    conn = sqlite3.connect("Chinese.db")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM words1000 WHERE oid=" + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    the_word_list = list(res.fetchone())
    cur.execute("UPDATE words1000 SET display = 1 WHERE oid = " + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    res = cur.execute("SELECT * FROM words1000 WHERE oid=" + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    the_word_list = list(res.fetchone())
    conn.commit()
    conn.close()

    # print(the_word_list)

    word_label = Label(current_word_frame, text=the_word_list[current_toggle], padx=160, pady=20, font=("Kaiti SC", 40, 'bold'), fg="red")
    word_label.grid(sticky=W, row=0, column=0, columnspan=5)

    current_word_check_button.destroy()
    current_word_check_button = Button(current_word_frame, text="Check", command=lambda: check_word(current_word_frame, current_word_check_button, current_card_index_list, current_card_index, current_word_index, current_toggle))
    current_word_check_button.grid(row=1, column=2)
'''
Function to tally mark word
'''
def mark_word(current_word_frame, current_word_mark_button, current_card_index_list, current_card_index, current_word_index):
    conn = sqlite3.connect("Chinese.db")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM words1000 WHERE oid=" + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    the_word_list = list(res.fetchone())
    cur.execute("UPDATE words1000 SET mark = " + str(the_word_list[3]+1) + " WHERE oid = " + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    res = cur.execute("SELECT * FROM words1000 WHERE oid=" + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    the_word_list = list(res.fetchone())
    conn.commit()
    conn.close()

    # print(the_word_list)

    current_word_mark_button = Button(current_word_frame, text="Mark: " + str(the_word_list[3]), command=lambda: mark_word(current_word_frame, current_word_mark_button, current_card_index_list, current_card_index, current_word_index))
    current_word_mark_button.grid(row=1, column=3)

'''
Function to reset tally mark to zero
'''
def reset_mark(current_word_frame, current_word_mark_button, current_card_index_list, current_card_index, current_word_index):
    conn = sqlite3.connect("Chinese.db")
    cur = conn.cursor()
    cur.execute("UPDATE words1000 SET mark = 0 WHERE oid = " + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    res = cur.execute("SELECT * FROM words1000 WHERE oid=" + str(current_card_index_list[current_card_index] * 4 + current_word_index + 1))
    the_word_list = list(res.fetchone())
    conn.commit()
    conn.close()

    # print(the_word_list)

    current_word_mark_button = Button(current_word_frame, text="Mark: " + str(the_word_list[3]), command=lambda: mark_word(current_word_frame, current_word_mark_button, current_card_index_list, current_card_index, current_word_index))
    current_word_mark_button.grid(row=1, column=3)

'''
Function to display next card, either forward or backward
'''
def next_card(card_index_list, card_index, direction):

    show_word(card_index_list, card_index, 0, 3, 0)
    show_word(card_index_list, card_index, 1, 3, 1)
    show_word(card_index_list, card_index, 2, 4, 0)
    show_word(card_index_list, card_index, 3, 4, 1)

    back_button = Button(root, text="<<", command=lambda: next_card(card_index_list, card_index-1, "backward"), fg='blue')
    next_button = Button(root, text=">>", command=lambda: next_card(card_index_list, card_index+1, "forward"), fg='blue')

    '''
    Disable the NEXT button when at the end of the card
    '''
    if(direction == 'forward'):
        if card_index == len(card_index_list)-1:
            next_button = Button(root, text=">>", state=DISABLED)
    elif(direction == 'backward'):
        if card_index == 0 or card_index == -len(card_index_list):
            back_button = Button(root, text="<<", state=DISABLED)

    back_button.grid(row=5, column=0)
    next_button.grid(row=5, column=1)

'''
Main function to show a card:
    - 'todays_line' is a list converted from the schedule line of today and looks like this:
      ['2022-11-29', 'Day-8', '11,12,13,17,18,19,20,21,22,23,24,25', '12']
    - 'today_card_index_list' is the list of indexes of the cards that need to be displayed.
      It is derived from todays_line[2] and looks like this:
      [10, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    - The layout of a card, where the 'card_date_entry' will bind with <Return> key to get a specific date
      ┌───────────────┐  ┌───────────────┐
      │card_date_label│  │card_date_entry│
      └───────────────┘  └───────────────┘
      ┌──────────────────────────────────┐
      │        schedule_info_label       │
      └──────────────────────────────────┘
      ┌───────────────┐  ┌───────────────┐
      │   word_frame  │  │  word_frame   │
      └───────────────┘  └───────────────┘
      ┌───────────────┐  ┌───────────────┐
      │   word_frame  │  │  word_frame   │
      └───────────────┘  └───────────────┘
'''
def show_card(the_date):

    '''
    Fetch the schedule for today
    '''
    conn = sqlite3.connect("Chinese.db")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM schedule WHERE date='" + str(the_date) + "'")
    todays_line = list(res.fetchone())
    conn.commit()
    conn.close()

    if(todays_line[2] != 'break'):
        '''
        If today is not a break, then create widgets to display the cards for today
        '''
        today_card_index_list = [int(i)-1 for i in todays_line[2].split(",")]
        card_list_str = str([int(i) for i in todays_line[2].split(",")])
        # print(card_list_str)
        # print(today_card_index_list)

        card_date_label = Label(root, text="Welcome! Today is: ", justify=LEFT, anchor=W)
        card_date_label.grid(sticky=W, row=0, column=0, columnspan=2)

        card_date_entry = Entry(root, width=10, borderwidth=5, justify=LEFT)
        card_date_entry.grid(row=0, column=1, sticky=E)
        card_date_entry.insert(0, todays_line[0])
        card_date_entry.bind('<Return>', (lambda event: show_card(card_date_entry.get())))


        # if(schedule_info_label.winfo_exists()):
        #     schedule_info_label.destroy()
        schedule_info_label = Label(root, text=todays_line[1] + " has " +todays_line[3] + " cards: " + card_list_str, justify=LEFT, anchor=W)
        schedule_info_label.grid(sticky=W, row=1, column=0, columnspan=2)

        current_card_index = 0

        '''
        Display each of 4 words in different grid
        '''
        show_word(today_card_index_list, current_card_index, 0, 3, 0)
        show_word(today_card_index_list, current_card_index, 1, 3, 1)
        show_word(today_card_index_list, current_card_index, 2, 4, 0)
        show_word(today_card_index_list, current_card_index, 3, 4, 1)

        back_button = Button(root, text="<<", command=lambda: next_card(today_card_index_list, current_card_index-1, "backward"), fg='blue')
        next_button = Button(root, text=">>", command=lambda: next_card(today_card_index_list, current_card_index+1, "forward"), fg='blue')
        back_button.grid(row=5, column=0)
        next_button.grid(row=5, column=1)

    else:
        '''
        Otherwise, display today is a break and encourage input a date to review
        '''
        card_date_label = Label(root, text="Welcome! Today is: ", justify=LEFT, anchor=W)
        card_date_label.grid(sticky=W, row=0, column=0, columnspan=2)

        card_date_entry = Entry(root, width=10, borderwidth=5, justify=LEFT)
        card_date_entry.grid(row=0, column=1, sticky=E)
        card_date_entry.insert(0, todays_line[0])
        card_date_entry.bind('<Return>', (lambda event: show_card(card_date_entry.get())))

        break_info_label = Label(root, text="Today is a break! Enter any date to review...", justify=LEFT, anchor=W, fg="red")
        break_info_label.grid(sticky=W, row=1, column=0, columnspan=2)

'''
Get today's date
    - Note that 'today' is not a string.
    - The type of 'today' is <class 'datetime.date'>
      so you need to convert by doing str(today)
    - specify a date here is also a good way for troubleshooting
'''
today = date.today()

'''
Show a card for 'today'
'''
show_card(today)

'''
Loop the root widget
'''
root.mainloop()