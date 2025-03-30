from . import keydetection as kd
import colorama
import time
import os
import math

clear = lambda: os.system('cls || clear')

def menu(choices: list[str], max_display = math.inf, scroll: bool | None = None):
    global clear
    if scroll is None:
        scroll = max_display != math.inf
    c = 0
    lenght = len(choices)
    if c == -1: c = lenght - 1
    if c >= lenght: c = 0
    for i in range(lenght):
        n = i + c
        if not scroll:
            n = i
        if i >= max_display:
            break
        if n >= lenght:
            break
        option = choices[n]
        if choices[c] == option:
            print(f"{colorama.Style.BRIGHT}{option} <{colorama.Style.RESET_ALL}")
        else:
            print(option)
    while kd.current_key != 'enter':
        time.sleep(0.08)
        if kd.current_key != '':
            clear()
            if kd.current_key == 'up':
                c -= 1
            if kd.current_key == 'down':
                c += 1
            if c == -1: c = lenght - 1
            if c >= lenght: c = 0
            for i in range(lenght):
                n = i + c
                if not scroll:
                    n = i
                if i >= max_display:
                    break
                if n >= lenght:
                    break
                option = choices[n]
                if choices[c] == option:
                    print(f"{colorama.Style.BRIGHT}{option} <{colorama.Style.RESET_ALL}")
                else:
                    print(option)

    return c