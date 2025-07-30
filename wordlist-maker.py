#!/bin/python3

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-fn", "--first-name", help="First name of the target")
parser.add_argument("-ln", "--last-name", help="Last name of the target")
parser.add_argument("-b", "--birthday", help="Target's birthday (MM-DD-YYYY, with leading zeros)")
parser.add_argument("-e", "--extra", help="Words that might be a potential target's password like their pet's name, city, favorite movie/song, etc")
args = parser.parse_args()

args_dict = vars(args)
val_list = list(args_dict.values())
key_list = list(args_dict.keys())

first_name = args.first_name
last_name = args.last_name
birthday = args.birthday
extra = args.extra

special_characters = "\!@#$%^&*-+?_=,./'~|:"

wordlist = []

combinations_list = []
with open('combinations.txt', 'r') as combinations:
    for i in combinations:
        c = i.replace('\n', '')
        combinations_list.append(c)
        

def casesen(word):
        cword = word.capitalize()
        uword = word.upper()
        lword = word.lower()
        cases = [cword, uword, lword]
        return cases

def simplepasswords(word_cases):
    for i in combinations_list:
        for j in word_cases:
            password_1 = i + j
            password_2 = j + i
            wordlist.append(password_1)
            wordlist.append(password_2)
            if len(i) < 4:
                password_3 = i + j + i
                wordlist.append(password_3)
                if all(c == i[0] for c in i) and len(i) > 1:
                    password_4 = i[::-1] + j + i
                    password_5 = i + j + i[::-1]
                    wordlist.append(password_4)
                    wordlist.append(password_5)


if first_name is not None and last_name is not None:
    wordlist.append(first_name + last_name)
    wordlist.append(last_name + first_name)
    for i in combinations_list:
        if any(j in special_characters for j in i):
            wordlist.append(first_name + i + last_name)
            wordlist.append(last_name + i + first_name)
    
if first_name is not None:
    fn_cases = casesen(first_name)
    wordlist.extend(fn_cases)
    simplepasswords(fn_cases)
    for i in fn_cases:
        wordlist.append(i[::-1])
if last_name is not None:
    ln_cases = casesen(last_name)
    wordlist.extend(ln_cases)
    simplepasswords(ln_cases)
    for i in ln_cases:
        wordlist.append(i[::-1])
if extra is not None:
    e_cases = []
    extra = extra.split(',')
    for i in extra:
        extra = casesen(i)
        e_cases.extend(extra)
    e_cases = list(set(e_cases))
    e_cases_c = []
    for i in e_cases:
        if i.isdigit() is False:
            e_cases_c.append(i)
    simplepasswords(e_cases_c)
    

if birthday is not None:
    date_list = birthday.split('-')
    DD = str(date_list[0])
    MM = str(date_list[1])
    YY = str(date_list[2])

    day = (DD,)
    mon = (MM,)
    year = (YY,)

    if DD.startswith('0'):
        D = DD[1]
        day = day + (D,)
    if MM.startswith('0'):
        M = MM[1]
        mon = mon + (M,)
    if len(YY) >= 4:
        Y = YY[2:]
        year = year + (Y,)


    def datecombinations(day, mon, year, word=('',)):
        date_combinations = []
        for d in day:
            for m in mon:
                for y in year:
                    for w in word:
                        date_combinations.append(w + d)
                        date_combinations.append(w + m)
                        date_combinations.append(w + y)

                        date_combinations.append(w + d + m)
                        date_combinations.append(w + m + d)
                        date_combinations.append(w + y + d)
                        date_combinations.append(w + y + m)
                        date_combinations.append(w + d + y)
                        date_combinations.append(w + m + y)
                                            
                        date_combinations.append(w + d + m + y)
                        date_combinations.append(w + m + d + y)
                        date_combinations.append(w + y + d + m)
                        date_combinations.append(w + y + m + d)
                        date_combinations.append(w + d + y + m)
                        date_combinations.append(w + m + y + d)

                        date_combinations.append(d + w)
                        date_combinations.append(m + w)
                        date_combinations.append(y + w)
                        
                        date_combinations.append(d + m + w)
                        date_combinations.append(m + d + w)
                        date_combinations.append(y + d + w)
                        date_combinations.append(y + m + w)
                        date_combinations.append(d + y + w)
                        date_combinations.append(m + y + w)
                        

                        date_combinations.append(d + m + y + w)
                        date_combinations.append(m + d + y + w)
                        date_combinations.append(y + d + m + w)
                        date_combinations.append(y + m + d + w)
                        date_combinations.append(d + y + m + w)
                        date_combinations.append(m + y + d + w)

        return(date_combinations)

    for i in datecombinations(day, mon, year):
        wordlist.append(i)
    
    
    if first_name is not None:
        for i in fn_cases:
            for j in datecombinations(day, mon, year, word=(i,)):
                wordlist.append(j)
    if last_name is not None:
        for i in ln_cases:
            for j in datecombinations(day, mon, year, word=(i,)):
                wordlist.append(j)

    if first_name is not None and last_name is not None:
        for i in fn_cases:
            for j in ln_cases:
                for k in datecombinations(day, mon, year, word=(i+j,)):
                    wordlist.append(k)



for i in wordlist:
    print(i)
print(len(wordlist))

