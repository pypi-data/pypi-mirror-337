import os
import time
from colorama import Fore, Back, Style, init
init()

def new_cartel_text():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("кортель")
    time.sleep (2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + "кортель")
    time.sleep (0.04)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Style.RESET_ALL + "кортель")
    time.sleep(8)
    exit()