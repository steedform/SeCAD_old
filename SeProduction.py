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
    time.sleep(4)  # Wait for the tab to switch
    
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

coordinates = read_coordinates_from_csv('coordinates_SE.csv')

time.sleep(0.4)

#switch_app_tab()

#Click on Production tab
click_element(*get_coordinates("proTab", coordinates))

#click on create view
click_element(*get_coordinates("createViewPro", coordinates))

time.sleep(2)

perform_shortcut("Enter")

perform_shortcut("Enter")

