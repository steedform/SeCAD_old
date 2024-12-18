'''
Copyright (c) 2024, Steedform All rights reserved.
Redistribution and use in source and binary forms, with or without   
modification, are not permitted provided that the code retains the 
above copyright notice.
'''

from playwright.sync_api import sync_playwright
import csv
import pyautogui
import keyboard
import time
import pyperclip
import tkinter as tk
from tkinter import messagebox
import sys
import time
from defs import get_printer as gp
from defs import terminate_program as tp
from defs import *

tp()

'''
#Function Move ontop of a specific element
def move_to(x,y):
    pyautogui.moveTo(x,y)
    time.sleep(0.3)

# Function to click on a specific element
def click_element(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(0.5)
    
# Function to click on a specific element
def double_click_element(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.doubleClick()
    time.sleep(0.5)
    
# Function to click on a specific element
def right_click_element(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click(button='right')
    time.sleep(1)
    
# Function to switch to the next tab in Edge
def switch_app_tab():
    keyboard.press_and_release('alt+tab')
    time.sleep(2)  # Wait for the tab to switch
    
def open_new_site_url(url):
    keyboard.press_and_release("ctrl+T")
          # Focus the address bar
    pyautogui.write(url)
    pyautogui.press('enter')
    time.sleep(4)
    
def perform_shortcut(shortcut):
    keyboard.press_and_release(shortcut)
    time.sleep(1)
    
# Function to read coordinates from CSV
def read_coordinates_from_csv(file_path):
    coordinates = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:  # Ensure there are exactly 3 columns
                name = row[0]  # First column is the name
                x = int(row[1])  # Second column is x
                y = int(row[2])  # Third column is y
                coordinates[name] = (x, y)
    return coordinates

# Function to get coordinates by name
def get_coordinates(name, coordinates):
    return coordinates.get(name, None)
'''

coordinates = read_coordinates_from_csv(r"..\coordinates_SE.csv")

time.sleep(0.1)

#switch_app_tab()

#Move to print Tab
click_element(*get_coordinates("proPrtTab", coordinates))

#Select prtDrpDwn
click_element(*get_coordinates("proPrtDrpDwn", coordinates))

#Select Printer
gp(r"..\prt_prod_con.txt", "Production", "proPrtDrpDwn", "proPrt")
#messagebox.showinfo("Printer", "Please select your printer from the drop down and press next")
#keyboard.wait("ctrl+0")
time.sleep(0.2)

#Select no printouts
click_element(*get_coordinates("no_prt_outs", coordinates))

#Paste printouts
time.sleep(0.5)
pyautogui.write("1")
time.sleep(0.5)

#click on Printall
click_element(*get_coordinates("proPrtAll", coordinates))

#Moving to export
time.sleep(2)

#Click on expoer tab
click_element(*get_coordinates("exportTab", coordinates))

time.sleep(4)

#Click on xml
click_element(*get_coordinates("xmlTab", coordinates))

#Click on the xmlnamefield
click_element(*get_coordinates('name_xml', coordinates))

time.sleep(0.5)

#click_element save
click_element(*get_coordinates('xml_save', coordinates))

time.sleep(0.6)

perform_shortcut("alt+F4")

time.sleep(0.2)

perform_shortcut('Enter')
click_element(*get_coordinates("save_project_final", coordinates))