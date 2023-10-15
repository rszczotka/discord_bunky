import subprocess
from pyautogui import *
import pyautogui
from tqdm import tqdm
from datetime import datetime
import time
import keyboard
import win32api, win32con
import mouse
import math
from dateutil.relativedelta import relativedelta
import asyncio
import discord
from discord import Webhook
import aiohttp
import colorama
from colorama import Fore, Back, Style


print(Fore.YELLOW +'''
  /$$$$$$  /$$$$$$$$ /$$$$$$        /$$    /$$       /$$                           /$$                
 /$$__  $$|__  $$__//$$__  $$      | $$   | $$      | $$                          | $$                
| $$  \__/   | $$  | $$  \ $$      | $$   | $$      | $$$$$$$  /$$   /$$ /$$$$$$$ | $$   /$$ /$$   /$$
| $$ /$$$$   | $$  | $$$$$$$$      |  $$ / $$/      | $$__  $$| $$  | $$| $$__  $$| $$  /$$/| $$  | $$
| $$|_  $$   | $$  | $$__  $$       \  $$ $$/       | $$  \ $$| $$  | $$| $$  \ $$| $$$$$$/ | $$  | $$
| $$  \ $$   | $$  | $$  | $$        \  $$$/        | $$  | $$| $$  | $$| $$  | $$| $$_  $$ | $$  | $$
|  $$$$$$/   | $$  | $$  | $$         \  $/         | $$$$$$$/|  $$$$$$/| $$  | $$| $$ \  $$|  $$$$$$$
 \______/    |__/  |__/  |__/          \_/          |_______/  \______/ |__/  |__/|__/  \__/ \____  $$
                                                                                             /$$  | $$
                                                                                            |  $$$$$$/
                                                                                             \______/  v3.0
                                                                                             
                                                                                                
                                                                                            GTAV Automatic Bunker Research bot arkis0
      
'''+ Style.RESET_ALL)

begin_position = False

inserted_webhook = input("Insert your webhook: ")

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    

def buy_resources():
    time.sleep(2)
    click(458, 494) #zakładka odnawiania
    time.sleep(2)
    click(967, 791) #przycisk kup zasoby
    time.sleep(2)
    click(1070, 620) #potwierdź zakup
    time.sleep(2)
    keyboard.press_and_release('esc') #powrót na home screen
    keyboard.press_and_release('esc') #swobodny widok
    print("Resources were ordered!")


def check_progress_of_research():
    x = 993
    y = 329
    matching_pixels_research = 0
    total_pixels = 597
    step_size = 4
    
    for i in tqdm(range(0, total_pixels, step_size)):
        if pyautogui.pixelMatchesColor(x + i, y, (46,135,46)):
            matching_pixels_research += 4
            
    research_level = math.ceil((matching_pixels_research / total_pixels) * 100)

    print("You have around", research_level, "% of completion on research")

    return research_level




def screenshot_of_current_project():
    print("Taking screenshot of current project...")
    click(468, 559)
    sleep(1)
    screenshot = pyautogui.screenshot(region=(1233, 468, 360, 360))
    screenshot.save("screenshot.png")
    keyboard.press_and_release('esc') #powrót na home screen



def check_amount_of_resources():
    print("Checking amount of resources...")
    x = 993
    y = 380
    matching_pixels_resources = 0
    total_pixels = 597

    step_size = 4
    for i in tqdm(range(0, total_pixels, step_size)):
        if pyautogui.pixelMatchesColor(x + i, y, (179, 57, 9)):
            matching_pixels_resources += 4

    resource_amount = math.ceil((matching_pixels_resources / total_pixels) * 100)

    print("You have around", resource_amount, "% of resources")
    if(resource_amount <= 30):
        print("You need to order more resources")
        buy_resources()
    else:
        print("You have sufficient amount of resources")
        keyboard.press_and_release('esc')
    return resource_amount


async def discordSend(research_level, resource_amount):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(inserted_webhook, session=session)
            with open('screenshot.png', 'rb') as f:
                image = discord.File(f)
            def generate_progress_bar(percent):
                filled_blocks = math.floor(percent / 10)
                empty_blocks = 10 - filled_blocks
                progress_bar = f"{percent}% [{'█' * filled_blocks}{'░' * empty_blocks}]"
                return progress_bar
            
            progress_bar_resources = generate_progress_bar(resource_amount)
            progress_bar_research = generate_progress_bar(research_level)
            if resource_amount <= 30:
                resource_color = 0xff0000
            elif resource_amount > 30 and resource_amount <= 60:
                resource_color = 0xffff00
            elif resource_amount > 60:
                resource_color = 0x00ff00
            
            embed = discord.Embed(title="Bunker Research status", color=resource_color, timestamp=datetime.now())
            embed.set_author(name="Bunky")
            embed.add_field(name="Amount of resources", value=progress_bar_resources, inline=False)
            embed.add_field(name="Progress of research", value=progress_bar_research, inline=False)
            embed.set_footer(text="↓ Ongoing research ↓")
            await webhook.send(embed=embed, username="Bunky", avatar_url="https://i.ibb.co/kmYhTCv/2023-09-29-17h22-26.png")
            await webhook.send(file=image)


time.sleep(2)

starting_setup = False
last_buy_time = 0
print("Bot won't start until you enter laptop home screen!")
while keyboard.is_pressed('q') == False:
    while starting_setup == False:
        if pyautogui.locateOnScreen('laptop_home_screen_logo.png', region=(0, 0, 1919, 1079), grayscale=True, confidence=0.8) != None:
            print("Laptop home screen detected! Bot is starting")
            starting_setup = True
            time.sleep(0.5)
            click(941, 645)
            
    research_level = check_progress_of_research()
    screenshot_of_current_project()
    resource_amount = check_amount_of_resources()
    asyncio.run(discordSend(research_level, resource_amount))
    
    
    time_of_check = time.time()
    print("Anti-kick started working! Next resource check in 15 minutes. Message from: ", time.ctime())
    while time.time() - time_of_check <= 900:
        if pyautogui.locateOnScreen('kick_time.png', region=(0, 0, 820, 1079), grayscale=True, confidence=0.8) != None:
            print("Kick message detected. Proceeding with activity")
            mouse.drag(0, 630, 1919, 630, absolute=True, duration=2)
            mouse.drag(1919, 630, 0, 630, absolute=True, duration=2)
            activity_detected = False
            while activity_detected == False:
                if pyautogui.locateOnScreen('kick_time.png', region=(0, 0, 820, 1079), grayscale=True, confidence=0.8) == None:
                    print("Activity was detected by game")
                    activity_detected = True
                else:
                    print("Activity was not detected by game! Retrying")
                    mouse.drag(0, 630, 1919, 630, absolute=True, duration=2)
                    mouse.drag(1919, 630, 0, 630, absolute=True, duration=2)
    keyboard.press_and_release('enter')
    time.sleep(3)
    if pyautogui.locateOnScreen('laptop_home_screen_logo.png', region=(0, 0, 1919, 1079), grayscale=True, confidence=0.8) != None:
            print("Laptop home screen detected!")
            time.sleep(0.5)
            click(941, 645)
