from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from functions import close_signin_screen,create_edge,extract_jobs,print_jobs_details,check_jobs_list,show_screen,check_signin_screen,prevent_sleep
import time
import schedule
import datetime
import threading

# Your LinkedIn URL
url = "https://www.linkedin.com/jobs/search/?currentJobId=4208898737&f_E=1%2C2%2C3&f_F=it&f_I=96%2C4&f_T=9&f_TPR=r14400&geoId=102007122&keywords=Dotnet%20Developer%20OR%20.Net%20OR%20Backend%20OR%20FullStack%20OR%20Software%20Engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&spellCorrectionEnabled=true"
# Path to msedgedriver.exe
edge_driver_path = r"D:\edgedriver_win32\msedgedriver.exe"  # <-- Update this path

jobs_list = []

def initialize():
    driver = create_edge(edge_driver_path,url)
    return driver

def scheduled_task(driver):
    global jobs_list
    try:
        driver.refresh()
    except Exception as e:
        print(e)

    time.sleep(3)      
    signin_screen_exits = check_signin_screen(driver)

    if signin_screen_exits:
        close_signin_screen(driver)
        
    time.sleep(5)
    current_jobs_list = extract_jobs(driver)
    new_jobs_exist = check_jobs_list(jobs_list,current_jobs_list)
    if(new_jobs_exist):
        jobs_list=current_jobs_list
        show_screen(driver)
    
    
driver = initialize()
# time.sleep(6)

while True:
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔁 Running scheduled task...")
    scheduled_task(driver)
    print_jobs_details(jobs_list)
    print("jobs found count = ", len(jobs_list))
    time.sleep(60*10)
 

   


