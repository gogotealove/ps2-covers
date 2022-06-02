"""
⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝
⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇
⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀
⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁⠀⠀
⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂⠀⠀⠀⠀
⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋⠀⠀⠀
    
     NO COVERS?
"""


import re
from time import sleep
from urllib.error import HTTPError
from termcolor import colored
from colorama import init
import urllib.request
import yaml
import os, sys


COVERS_URL = 'https://github.com/LouiseSulyvahn/PCSX2_Cover_Downloader/raw/main/covers/'
VERSION_URL = 'https://raw.githubusercontent.com/LouiseSulyvahn/PCSX2_Cover_Downloader/main/version'
VERSION = 1.3


def path():
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(os.path.realpath(sys.executable))
    elif __file__:
        path = os.path.dirname(__file__)
    return path


def check_version():
    try:
        version = urllib.request.urlopen(VERSION_URL)
        if float(version.read().decode('utf-8').replace('\n','')) != VERSION:
            print('[LOG]:', colored(f'New update available!\n', 'green'))
    except:
        pass     


def serial_list():  # Get game serial
    with open(f'{path()}\cache\gamelist.cache', errors='ignore') as file:
        regex = re.compile('(\w{4}-\d{5})').findall(file.read())
        serial_list = list(dict.fromkeys(regex))
        print('[LOG]:', colored(f'Found {len(serial_list)} games', 'green'))
        if len(serial_list) == 0:
            print('[ERROR]:', colored(f'You have 0 games installed', 'red'))
            input()
            quit()  
        return serial_list
    

def existing_covers():
    covers = [w.replace('.jpg', '') for w in os.listdir(f'{path()}\covers')]
    return covers
  
  
"""" #GameIndex JSON
def serial_to_name(serial:str):  # Get game name using serial
    with open(f'{path()}\GameIndex.json', encoding='utf-8-sig') as file:
        try:
            json_data = json.loads(file.read())
            name = json_data[serial]['name']
            return name
        except KeyError:
            print('[WARNING]:', colored(f'{serial} Not found. Skipping...', 'yellow'))
            return None
"""


def serial_to_name(serial:str):  # Get game name using serial
    with open(f'{path()}\/resources\GameIndex.yaml', encoding='utf-8-sig') as file:
        try:
            yaml_file = yaml.load(file.read(), Loader=yaml.CBaseLoader)
            return yaml_file[serial]["name"]
        except KeyError:
            print('[WARNING]:', colored(f'{serial} Not found. Skipping...', 'yellow'))
            return None


def download_covers(serial_list:list):  # Download Covers
    existing_cover = existing_covers()
    for i in range(len(serial_list)):
        game_serial = serial_list[i]
        game_name = serial_to_name(serial_list[i])
        if game_name != None:
            if game_serial not in existing_cover:
                print('[LOG]:',colored(f'Downloading {game_serial} | {game_name} cover...', 'green'))
                try:
                    urllib.request.urlretrieve(f'{COVERS_URL}{game_serial}.jpg', f'covers/{game_serial}.jpg')
                    sleep(1)
                except HTTPError:
                    print('[WARNING]',colored(f'{game_serial} | {game_name} Not found. Report it in GitHub please...','yellow'))
            else:
                print('[WARNING]:',colored(f'{game_serial} | {game_name} already exist in \covers. Skipping...','yellow'))                


def run():
    check_version()
    download_covers(serial_list())
    print('[LOG]:', colored(f'Done!', 'green'))
    input()


init()
run()