# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 21:02:39 2020

@author: Z77X-I5
"""

import numpy
import datetime
import os

def fib(n):
    if n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    else:
        lst = fib(n-1)
        lst.append(lst[-1] + lst[-2])
        return lst

# Practice on day [1, 2, 3, 5, 8, 13, 21, 34, 55]
practice_day_lst = fib(10)[2:]
start_card = 10
max_card = 250
card_list = list(range(max_card+1))
starting_date = datetime.date(2022, 12, 19)

# Start with start_card on first day
card_group_lst = [[x+1 for x in list(range(start_card))]]

# Three cards at a time for card 11-100
if max_card > 100:
    for i in range(start_card+1,100,3):
        str1 = card_list[i:i+3]
        card_group_lst.append(str1)
else:
    for i in range(11,max_card+1,3):
        str1 = card_list[i:i+3]
        card_group_lst.append(str1)

# Two cards at a time for card 101-200
if max_card > 200:
    for i in range(101,200,2):
        str1 = card_list[i:i+2]
        card_group_lst.append(str1)
elif max_card > 100:
    for i in range(101,max_card+1,2):
        str1 = card_list[i:i+2]
        card_group_lst.append(str1)

# One card at a time for 201-250
if max_card > 200:
    for i in range(201, max_card+1):
        str1 = card_list[i:i+1]
        card_group_lst.append(str1)

end_date = practice_day_lst[len(practice_day_lst)-1] + len(card_group_lst)

lst = [[] for _ in range(end_date*2)]

for i in range(len(card_group_lst)):
    i_practice_day_lst = [x+ i-1 for x in practice_day_lst]
    for i_day in i_practice_day_lst:
        lst[i_day] = lst[i_day] + card_group_lst[i]

with open("Schedules" + str(starting_date) + ".txt", "w") as f:
    count = 0
    for i in range(end_date*2):
        if lst[count] == []:
            break;
        i_date = starting_date + datetime.timedelta(days=i)
        f.write(str(i_date) + ":Day-" + str(i+1) + ":")

        if (i != 0 and ((i-3)%7 == 0 or (i+1)%7 == 0)):
            f.write("break" + "\n" )
        else:
            today_card = ','.join(str(p) for p in lst[count])
            today_number = len(list(today_card.split(",")))
            f.write(today_card  + ":" + str(today_number) + "\n")
            count += 1