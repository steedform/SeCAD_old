from defs import *
from playwright.sync_api import sync_playwright
import csv
import pyautogui
import keyboard
import time

def main():
    start_time = get_time_in_human()
    
    user_input = simpledialog.askstring("Input", "Please Enter the Job Number ;)", initialvalue="ST")
    pyperclip.copy(user_input)
    
    idFile = open(r"..\job_id.txt", "w")
    idFile.write(user_input)
    
    time.sleep(0.5)
    # Turn off Caps Lock if it's on
    if is_capslock_on():
        pyautogui.press('capslock')
    print(f"******************************************************** {start_time} *********************************************************")
    print(f"******************************************************** {user_input} *********************************************************")
    sys.stdout.flush()
    
    terminate_program()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="msedge", args=["--start-maximized", "--disable-infobars"])  # Set headless=True if you want to run without UI
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the login page
        page.goto('https://steedform.moraware.net/sys/')  # Change to your actual login URL
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        username, password = get_credentials(path_to_credentials=r"..\credentilas.txt")
        
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
        time.sleep(3)
        click_element(*get_coordinates('search_result', coordinates))
        
        
        page.wait_for_load_state('networkidle')
        time.sleep(3)
        
        elements = page.query_selector_all('td:has(div:has-text("Selections:")) div > table')
        
        write_job_det_to_csv(elements=elements)
        
        # Use query_selector_all to find the job name
        job_name_element = page.query_selector_all('.pageInfoLabel:has-text("Job Name:") + .pageInfoValue')
        
        job_name, job_name2, job_name_full = get_job_name(job_name_element=job_name_element, path_job_name=r"..\Job_name_full.txt")
        
        file_path = r"..\selections_data.csv"
        data = read_csv(file_path)
        categorize_fields(data)
        
        time.sleep(0.5)
        browser.close()

        shortcut_path = "C:\\Sekon\\SekonPrograms\\SeCAD V12\\SeCAD12 - Shortcut.lnk"
        
        # Start the application
        os.startfile(shortcut_path)

        keyboard.wait('ctrl+0')
        time.sleep(0.1)

        #Save project
        click_element(*get_coordinates('file', coordinates))
        time.sleep(0.1)

        click_element(*get_coordinates('save_project_as', coordinates))
        time.sleep(0.1)
        click_element(*get_coordinates('file_name_fd', coordinates))
        
        time.sleep(0.1)
        perform_shortcut("ctrl+v")
        time.sleep(0.2)
        #pyautogui.write("test")

        click_element(*get_coordinates('save', coordinates))

        time.sleep(0.5)

        #Click on oder data
        click_element(*get_coordinates('order_data', coordinates))

        time.sleep(0.2)
        
        categorized_results = categorize_fields(data)
        common_material_colour = categorized_results.get('Material Colour', 'various')

        #Click on fields in pop-up
        click_element(*get_coordinates('material_colour', coordinates))

        pyautogui.write(categorized_results.get('Material Colour', 'various'))

        click_element(*get_coordinates('material_brand', coordinates))

        pyautogui.write(categorized_results.get('Material Brand', 'various'))

        click_element(*get_coordinates('edge_profile', coordinates))

        pyautogui.write(categorized_results.get('Edge Profile', 'various'))

        click_element(*get_coordinates('thickness', coordinates))
        
        try:
            pyautogui.write(categorized_results.get('Material Thickness', 'various').split("mm")[0])
        except Exception as e:
            pyautogui.write(categorized_results.get('Material Thickness', 'various'))
        time.sleep(0.5)

        click_element(*get_coordinates('job_name', coordinates))
        time.sleep(0.5)
        pyautogui.write(job_name_full)

        time.sleep(1)
        #sys.exit(0)
        
        print("******************CAT*****************", categorized_results.get('Material Brand', 'various').strip())
        
        if categorized_results.get('Material Brand', 'various').strip() == 'SA Zenith Surfaces':
            click_element(*get_coordinates('clk_grp_drp_dwn', coordinates))
            time.sleep(0.5)
            click_element(*get_coordinates('clk_grp_stn',coordinates))
            time.sleep(0.5)
            click_element(*get_coordinates('clk_mtrl_drp_dwn', coordinates))
            time.sleep(0.5)
            click_element(*get_coordinates('clk_mtrl', coordinates))
            time.sleep(0.5)
        
        messagebox.showinfo("Important", "Well, Click next on your streamDeck when you are done with the Inputs ;)")
        keyboard.wait("ctrl+0")
            

        click_element(*get_coordinates('order_okay', coordinates))



        click_element(*get_coordinates('file', coordinates))
        time.sleep(0.2)
        click_element(*get_coordinates('file_import', coordinates))

        time.sleep(0.6)

        click_element(*get_coordinates('import_dxf', coordinates))

        time.sleep(0.2)

        click_element(*get_coordinates('import_menu_bar', coordinates))

        time.sleep(0.2)

        pyautogui.write(get_jobs_path(r"..\jobs_path.txt"))

        time.sleep(0.2)

        perform_shortcut("enter")

        time.sleep(0.1)

        click_element(*get_coordinates('import_file_fd', coordinates))

        perform_shortcut("ctrl+v")

        time.sleep(0.1)

        perform_shortcut("enter")

        time.sleep(0.1)

        perform_shortcut("ctrl+v")

        pyautogui.write("T")
        time.sleep(0.1)

        click_element(*get_coordinates('import_btn', coordinates))

        time.sleep(0.1)

        perform_shortcut('Enter')


        time.sleep(0.3)

        end_time = get_time_in_human()

        elapsed_time = elapsed_time_cal(start_time=start_time, end_time=end_time)

        messagebox.showinfo("Completed!", f"Process Completed! Please check your logs\n {elapsed_time} seconds!!!")
        print("Completed!", f"Process Completed for {user_input}! Please check your logs\n {elapsed_time} seconds!!!")
        
        time.sleep(0.5)
        perform_shortcut("Enter")
        time.sleep(0.5)
        perform_shortcut("Enter")
        


if __name__ == '__main__': 
    print("Executing Program!!!!")
    sys.stdout.flush()
    main()