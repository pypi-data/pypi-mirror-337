import os
import time
from colorama import Fore, Back, Style, init
init()

def new_cartel_text():
    print ("Внимание: Данная библиотека не хочет как либо оскорбить картель")
    time.sleep (3)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("кортель")
    time.sleep (2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + "кортель")
    time.sleep (0.04)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Style.RESET_ALL + "кортель")
    time.sleep(2)
    exit()
