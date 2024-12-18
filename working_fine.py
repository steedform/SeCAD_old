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
import sys, os, psutil
import time
from tkinter import simpledialog
import threading

sys.stdout = open("output_file.txt", 'w')  # Redirect standard output
sys.stderr = open("error_file.txt", 'w')    # Redirect standard error (optional)

# Function to listen for a key press and terminate the application
def listen_for_exit_key():
    keyboard.wait('esc')  # Wait for the 'Esc' key
    messagebox.showinfo("ByeBye!","Exiting Program.......")
    print("Program Terminated")# Optional: Print a message to the output file
    sys.stdout.flush()
    os._exit(0)  # Forcefully exit the program

# Start the key listener in a separate thread
exit_thread = threading.Thread(target=listen_for_exit_key)
exit_thread.daemon = True  # This allows the thread to exit when the main program exits
exit_thread.start()

start_time = time.time()
print(f"******************************************************** {start_time} *********************************************************")

def read_csv(file_path):
    """Reads the CSV file and returns the data as a list of rows."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = [row for row in reader if row]  # Filter out empty rows
    return data

def categorize_fields(data):
    """Categorizes fields as 'common_<field_name>' or 'various' based on their values across rows."""
    field_names = data[0][1:]  # Field names excluding area
    num_fields = len(field_names)
    
    # Initialize common variables
    common_values = {}
    
    for i in range(num_fields):
        current_field_values = [row[i + 1] for row in data[1:]]  # Gather values for the current field
        unique_values = set(current_field_values)

        if len(unique_values) == 1:  # All values are the same
            common_values[field_names[i]] = current_field_values[0]
        else:
            common_values[field_names[i]] = 'various'  # Different values

    # Create variables for each common value
    for field, value in common_values.items():
        if value != 'various':
            globals()[f'common_{field}'] = value
        else:
            globals()[f'common_{field}'] = 'various'

    # Print results
    print("Categorized Results:")
    for key, value in common_values.items():
        print(f"{key}: {value}")

# Example usage
#data = read_csv('your_file.csv')
#categorize_fields(data)

#Function Move ontop of a specific element
def move_to(x,y):
    pyautogui.moveTo(x,y)
    time.sleep(0.5)

# Function to click on a specific element
def click_element(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(0.5)
    
# Function to click on a specific element
def double_click_element(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.doubleClick()
    time.sleep(0.6)
    
# Function to click on a specific element
def right_click_element(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click(button='right')
    time.sleep(1)
    
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
    time.sleep(3)
    
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

# Replace these with your actual credentials
username = 'greg'  # e.g., 'greg'
password = 'greg01'  # e.g., 'greg01'

def get_jobs_path():
    file_jobs_path = open("jobs_path.txt", "r")
    jobs_path = file_jobs_path.read()
    jobs_path = jobs_path.strip()
    
    return jobs_path


#print(get_jobs_path())

user_input = simpledialog.askstring("Input", "Please Enter the Job Number ;)")
pyperclip.copy(user_input)

print(f"\n****************************** {user_input} ****************************************")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel="msedge", args=["--start-maximized", "--disable-infobars"])  # Set headless=True if you want to run without UI
    context = browser.new_context()
    page = context.new_page()

    # Navigate to the login page
    page.goto('https://steedform.moraware.net/sys/')  # Change to your actual login URL
    page.set_viewport_size({"width": 1920, "height": 1080})
    
    # Fill in the login form using the updated selectors
    page.fill('input[name="user"]', username)  # Username field
    page.fill('input[name="pwd"]', password)    # Password field

    # Click the login button using the ID of the submit button
    page.click('#LOGIN')  # Using the ID selector for the submit button

    # Wait for the page to load after login
    page.wait_for_load_state('networkidle')  # Wait for all network requests to finish

    # Now go to the page with the table
    click_element(*get_coordinates('search_fd', coordinates))
    
    time.sleep(0.5)
    
    perform_shortcut("ctrl+V")
    
    time.sleep (0.1)
    
    click_element(*get_coordinates('search_btn', coordinates))
    
    time.sleep(0.5)
    page.wait_for_load_state('networkidle')
    
    click_element(*get_coordinates('search_result', coordinates))
    
    time.sleep(1.5)
    page.wait_for_load_state('networkidle')
    
    elements = page.query_selector_all('td:has(div:has-text("Selections:")) div > table')

    csv_data = []
    capturing_data = True
    count = 0

    for row in elements:
        # Get all cells in the current row
        cells = row.query_selector_all('td')
                
        if cells and cells[0].evaluate("el => el.style.fontWeight === 'bold'"):
            if capturing_data == True:
                row_data = [cell.inner_text().strip() for cell in cells]
                #print(row_data, capturing_data)
                #print("appending1")
                csv_data.append(row_data)
                capturing_data = False
            else:
                row_data = [cell.inner_text().strip() for cell in cells]
                print(row_data, capturing_data)
                print("llllllalalalallalalalalal")
                with open("um.txt", "w") as um_file:
                    for i, um_data_lbl in enumerate(row_data):
                        if um_data_lbl.strip().lower() == "undermount":
                            um_file.write("True")
                            um_file.flush()
                            break
                        else:
                            if i == len(row_data) - 1:
                                um_file.write("False")
                                um_file.flush()                        
                #print("Im here!!")     
                break
        else:
            if count == 0:
                count = count + 1
                pass
            else:
                if len(cells) > 0:  # Ensure there are cells to capture
                    row_data = [cell.inner_text().strip() for cell in cells]
                    print(f"Row Data and Capturing Data\n{row_data}, {capturing_data} \n")
                    csv_data.append(row_data)
                    #print("appending2")
              
    csv_write = []   
    csv_line_by_line = []            
    for i, csv_data_line in enumerate(csv_data[0]):
        #print("I am looping")
        if i % 7 == 0 and i != 0:
            csv_write.append(csv_line_by_line)
            csv_line_by_line = []
            csv_line_by_line.append(csv_data_line)
        else:
            csv_line_by_line.append(csv_data_line)
            print(csv_line_by_line)
            if i == len(csv_data[0]) - 1:
                csv_write.append(csv_line_by_line)
                
    print("csv_data\n \n \n")
    print(csv_data)        
    print("\ncsv_write\n \n \n")        
    print(csv_write)        
    # Print the collected CSV data
    # Optionally, write to CSV
    with open('selections_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(csv_write)
      
    # Use query_selector_all to find the job name
    job_name_element = page.query_selector_all('.pageInfoLabel:has-text("Job Name:") + .pageInfoValue')
    
    if job_name_element:
        job_name_full = job_name_element[0].inner_text()
        print("Job Name:", job_name_full)
    else:
        print("Job Name not found.")
        job_name = ""
    
    with open("Job_name_full.txt", mode='w') as file_job_name:
    
        if "-" in job_name_full and "," in job_name_full:
            # Find the first occurrence of both characters
            first_dash = job_name_full.find("-")
            first_comma = job_name_full.find(",")

            # Split from the first occurring character
            if first_dash < first_comma and first_dash != -1:
                job_name = job_name_full[:first_dash].strip()
                job_name2 = job_name_full[first_dash + 1:].strip()
                file_job_name.write(f"1. {job_name_full}")
                
            else:
                job_name = job_name_full[:first_comma].strip()
                job_name2 = job_name_full[first_comma + 1:].strip()
                file_job_name.write(f"2. {job_name_full}")
        elif "-" in job_name_full:
            job_name = job_name_full.split("-")[0].strip()
            job_name2 = job_name_full.split("-")[1].strip()
            file_job_name.write(f"1. {job_name_full}")
        elif "," in job_name_full:
            job_name = job_name_full.split(",")[0].strip()
            job_name2 = job_name_full.split(",")[1].strip()
            file_job_name.write(f"2. {job_name_full}")
        else:
            job_name = job_name_full
            job_name2 = ""
            file_job_name.write(f"3. {job_name_full}")
                
            time.sleep(1)
        
        file_job_name.flush()
            
 
file_path = 'selections_data.csv'  # Replace with your actual file path
data = read_csv(file_path)
categorize_fields(data)

shortcut_path = "C:\\Sekon\\SekonPrograms\\SeCAD V12\\SeCAD12 - Shortcut.lnk"

# Start the application
os.startfile(shortcut_path)

messagebox.showinfo("Important", "Press Next on your StreamDeck when SeCAD opens. Thanks!")
time.sleep(2)

keyboard.wait('ctrl+0')
time.sleep(0.5)

#Save project
click_element(*get_coordinates('file', coordinates))
time.sleep(0.55)

click_element(*get_coordinates('save_project_as', coordinates))

click_element(*get_coordinates('file_name_fd', coordinates))

perform_shortcut("ctrl+v")
#pyautogui.write("test")

click_element(*get_coordinates('save', coordinates))

time.sleep(0.5)

#Click on oder data
click_element(*get_coordinates('order_data', coordinates))

time.sleep(1)

#Click on fields in pop-up
click_element(*get_coordinates('material_colour', coordinates))

pyautogui.write(globals()['common_Material Colour'])

click_element(*get_coordinates('material_brand', coordinates))

pyautogui.write(globals()['common_Material Brand'])

click_element(*get_coordinates('edge_profile', coordinates))

pyautogui.write(globals()['common_Edge Profile'])

click_element(*get_coordinates('thickness', coordinates))

pyautogui.write("20")

time.sleep(0.5)

click_element(*get_coordinates('job_name', coordinates))
time.sleep(0.5)
pyautogui.write(job_name)

time.sleep(1)

print(globals()['common_Material Brand'].strip())
if globals()['common_Material Brand'].strip() == 'SA Zenith Surfaces':
    click_element(*get_coordinates('clk_grp_drp_dwn', coordinates))
    time.sleep(1)
    click_element(*get_coordinates('clk_grp_stn',coordinates))
    time.sleep(1)
    click_element(*get_coordinates('clk_mtrl_drp_dwn', coordinates))
    time.sleep(1)
    click_element(*get_coordinates('clk_mtrl', coordinates))
    time.sleep(1)
else:
    messagebox.showinfo("Important", "Well, Click next on your streamDeck when you are done with the Inputs ;)")
    keyboard.wait("ctrl+0")
    

click_element(*get_coordinates('order_okay', coordinates))



click_element(*get_coordinates('file', coordinates))
time.sleep(0.4)
click_element(*get_coordinates('file_import', coordinates))

time.sleep(1.5)

click_element(*get_coordinates('import_dxf', coordinates))

time.sleep(0.5)

click_element(*get_coordinates('import_menu_bar', coordinates))

time.sleep(1)

pyautogui.write(get_jobs_path())

time.sleep(0.5)

perform_shortcut("enter")

time.sleep(0.5)

click_element(*get_coordinates('import_file_fd', coordinates))

perform_shortcut("ctrl+v")

time.sleep(0.5)

perform_shortcut("enter")

time.sleep(0.5)

perform_shortcut("ctrl+v")

pyautogui.write("T")

click_element(*get_coordinates('import_btn', coordinates))

time.sleep(0.2)

perform_shortcut('Enter')


time.sleep(0.5)

end_time = time.time()

elapsed_time = end_time - start_time

messagebox.showinfo("Completed!", f"Process Completed! Please check your logs\n {elapsed_time} seconds!!!")
print("Completed!", f"Process Completed for {user_input}! Please check your logs\n {elapsed_time} seconds!!!")