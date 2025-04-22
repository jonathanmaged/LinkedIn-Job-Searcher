from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pygetwindow as gw
import pyautogui
import time

def create_edge(edge_driver_path,url):

    # Setup Edge options
    options = Options()
    options.use_chromium = True
    options.add_argument("--start-maximized")  # Optional: start maximized
    options.add_argument('--log-level=3')  # Suppresses most logs (0 = ALL, 3 = ERROR)

    # Launch Edge with Selenium
    print("🚀 Launching Edge with Selenium...")
    service = Service(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service, options=options)
    driver.get(url)
    return driver

def check_signin_screen(driver):
    try:
        # Attempt to locate the sign-in screen
        signin_screen = driver.find_element(By.XPATH, "/html/body/div[5]/div/div")
    
        # Check if the element is displayed
        return signin_screen.is_displayed()
    
    except Exception as e:
        return False

# Function to close the sign in screen 
def close_signin_screen(driver):
    try:
        close_button = driver.find_element(
        By.XPATH,
        "/html/body/div[5]/div/div/section/button"
        )
        close_button.click()
    except Exception as e:
       print("exception from close signin screen function is",e) 

def signin_linkedin(email,password,driver):
    
    email_input = driver.find_element(By.XPATH,"/html/body/div[5]/div/div/section/div/div/form/div[1]/div[1]/div/div/input")
    password_input = driver.find_element(By.XPATH,"/html/body/div[5]/div/div/section/div/div/form/div[1]/div[2]/div/div/input")
    signin_button = driver.find_element(By.XPATH,"/html/body/div[5]/div/div/section/div/div/form/div[2]/button")

    email_input.send_keys(email)
    time.sleep(3)
    password_input.send_keys(password)
    signin_button.click()

def click_signin_button(driver):
    signin_button= driver.find_element(By.XPATH,"/html/body/div[5]/div/div/section/div/div/div/div[2]/button")
    signin_button.click()

def extract_jobs(driver):
    jobs_details = []

    # Find all job card elements using their unique attribute
    job_items = driver.find_elements(By.XPATH, "/html/body/div[1]/div/main/section[2]/ul/li")
    # y=len(job_items)
    # print("the len of the ul is ",y)

    # x=1
    for item in job_items:
        
        try:
            job_title_elem = item.find_element(By.CSS_SELECTOR, "h3.base-search-card__title")
            company_name_elem = item.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle")

            job_title = job_title_elem.text.strip()
            company_name = company_name_elem.text.strip()

            # company_name=job_title
            
            jobs_details.append({
                'job_title': job_title,
                'company_name': company_name
            })

        except Exception as e:
            print(f"Job title not found for item: {e}")
            job_title = "N/A"
        # x=x+1

      
    return jobs_details


def print_jobs_details(jobs_details):
    for job in jobs_details:
        print(f"Job Title: {job['job_title']}, Company: {job['company_name']}")
        # print(job['job_title'])

def check_jobs_list(jobs_list, current_jobs_list):
    """
    Compare two lists of job dicts and return jobs in current_jobs_list
    that are not in jobs_list.

    Each job is a dict with 'job_title' and 'company_name'.
    """
    new_jobs = []

    for job in current_jobs_list:
        exists = any(
            existing_job['job_title'] == job['job_title'] and
            existing_job['company_name'] == job['company_name']
            for existing_job in jobs_list
        )
        if not exists:
            return True

    return False

def show_screen(driver):
    print("show screen is open ")

    # Bring the window to the front
    for window in gw.getWindowsWithTitle(driver.title):
        if window.isMinimized:
            window.maximize()
        else:
            window.minimize()
            window.maximize()
        
def prevent_sleep():
    while True:
        # print("i am in the thread")
        pyautogui.moveRel(0, 50)  # Move mouse 1 pixel
        time.sleep(1)  # Every 60 seconds
        pyautogui.moveRel(0, -50) # Move back
        time.sleep(120)  # Every 60 seconds


    

