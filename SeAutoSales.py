'''
Copyright (c) 2024, Steedform All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are not permitted provided that the code retains the
above copyright notice.
'''

from tkinter import simpledialog
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
    time.sleep(0.4)

# Function to click on a specific element
def double_click_element(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.doubleClick()
    time.sleep(0.4)

# Function to click on a specific element
def right_click_element(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click(button='right')
    time.sleep(0.4)

# Function to switch to the next tab in Edge
def switch_app_tab():
    keyboard.press_and_release('alt+tab')
    time.sleep(1)  # Wait for the tab to switch

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

time.sleep(1)

# switch_app_tab()

# Move to Sales Tab
click_element(*get_coordinates('moveToSales', coordinates))

# Click on create View
click_element(*get_coordinates('createView', coordinates))

time.sleep(0.5)

move_to(*get_coordinates('Random_Sales', coordinates))


# Click on really create yes
perform_shortcut('Enter')

perform_shortcut('Enter')

# Click on print tab
click_element(*get_coordinates('printTab', coordinates))

# click on printer drpdwn
click_element(*get_coordinates('prtDrpDwn', coordinates))

gp(r"..\prt_sales_con.txt", "Sales", "prtDrpDwn", "salesPrt")


# Checking whether is an undermount
um_file = open(r"..\um.txt", 'r')
um = um_file.read().strip()

if um == "True":
    no_of_copies = "3"
else:
    no_of_copies = "2"

# click on noof copies field
click_element(*get_coordinates("noCopies", coordinates))

time.sleep(0.5)

# Wite no of copies
# pyautogui.write(no_of_copies)
pyperclip.copy(no_of_copies)

time.sleep(0.5)

perform_shortcut("ctrl+V")

time.sleep(0.3)

# Print
click_element(*get_coordinates('prt', coordinates))
time.sleep(1)


# Create a simple Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Display a message box with OK and Cancel buttons
response_print_pdf = messagebox.askokcancel(
    "Confirmation", "Do you wish to print it as a pdf?")

# Use an if condition to perform actions based on the response
if response_print_pdf:
    print("User clicked OK. Proceeding...")
    no_diags = simpledialog.askstring(
        "Input", "Please Enter the number of Diagrams")
    no_diags = int(no_diags)
    gp(r"..\prt_sales_pdf_con.txt", "SalesPDF", "prtDrpDwn", "pdfPrt")
    click_element(*get_coordinates("noCopies", coordinates))
    pyperclip.copy(1)
    perform_shortcut("ctrl+V")
    click_element(*get_coordinates('prt', coordinates))
    for i in range(no_diags):
        print("No diags", no_diags, "type", type(no_diags))
        print(i)
        time.sleep(1.5)
        click_element(*get_coordinates('savePdfMenu', coordinates))
        jobs_path_pdf = get_jobs_path(r"..\jobs_path.txt")
        job_id_pdf = get_job_id(r"..\job_id.txt")
        pyautogui.write(fr"{jobs_path_pdf}\{job_id_pdf}")
        time.sleep(0.2)
        perform_shortcut("Enter")
        time.sleep(0.2)
        click_element(*get_coordinates('svPdfFd', coordinates))
        time.sleep(0.2)
        pyautogui.write(f"{job_id_pdf}_{i}")
        time.sleep(0.2)
        perform_shortcut("Enter")
        time.sleep(1.5)
        print("Done {}".format(i))
    
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False, channel="msedge", args=["--start-maximized", "--disable-infobars"])
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the login page
        page.goto('https://steedform.moraware.net/sys/')  # Replace with your actual login URL
        page.set_viewport_size({"width": 1920, "height": 1080})

        # Get credentials from a file or another source
        username, password = get_credentials(path_to_credentials=r"../credentials.txt")

        # Fill in the login form using the updated selectors
        page.fill('input[name="user"]', username)  # Username field
        page.fill('input[name="pwd"]', password)    # Password field

        # Click the login button
        page.click('#LOGIN')

        # Wait for the page to load
        page.wait_for_load_state('networkidle')

        # Navigate to the page with the table
        page.wait_for_load_state('networkidle')  # Wait for all network requests to finish

        # Now go to the page with the table
        click_element(*get_coordinates('search_fd', coordinates))
        
        time.sleep(0.5)
        
        pyautogui.write(job_id_pdf)
        
        time.sleep (0.1)
        
        click_element(*get_coordinates('search_btn', coordinates))
        
        time.sleep(0.5)
        page.wait_for_load_state('networkidle')
        time.sleep(3)
        click_element(*get_coordinates('search_result', coordinates))
        page.wait_for_load_state('networkidle')

        # Example: Extract table data
        rows = page.locator('#FilesScroll1Body tr')
        for i in range(rows.count()):
            # Get all the cell texts for the row
            cells = rows.nth(i).locator('td')
            cell_data = [cells.nth(j).inner_text() for j in range(cells.count())]
            print(f"Row {i+1}: {cell_data}")
            
        # Example: Click the button to attach a file
        attach_button_selector = '#btnCreateFile'
        page.click(attach_button_selector)

        for i in range(no_diags):
            time.sleep(2)
            # Wait for the label element to be visible
            page.wait_for_selector('label.fileUploadButton')

            # Click on the label to activate the file input
            page.click('label.fileUploadButton')
            
            time.sleep(2)
            
            pyautogui.write(f"{jobs_path_pdf}\{job_id_pdf}\{job_id_pdf}_{i}")
            time.sleep(0.5)
            perform_shortcut('Enter')
            
            time.sleep(1)
        
            page.wait_for_selector('select[name="attrVal3"]')

        # Select the "CAD file" option by its value
        page.select_option('select[name="attrVal3"]', '10')
        time.sleep(1)
        
        # Wait for the "Save" button and click it
        page.wait_for_selector('button.dialogSubmitButton[name="ok"]')
        page.click('button.dialogSubmitButton[name="ok"]')
        time.sleep(1)
        browser.close()
    # Add your code for the OK condition here
else:
    print("User clicked Cancel. Aborting print pdf process........")

# Moving to Production at once
# Click on Production tab
click_element(*get_coordinates("proTab", coordinates))
time.sleep(1)

# click on create view
click_element(*get_coordinates("createViewPro", coordinates))

time.sleep(2)

move_to(*get_coordinates('Random_Sales', coordinates))

perform_shortcut("Enter")

perform_shortcut("Enter")
