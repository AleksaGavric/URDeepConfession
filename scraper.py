'''
FLOW:

'''

import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor
import time 
import urllib.request
import requests

# setting up the driver using chrome 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.instagram.com/")

# login
username = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

# get secure credentials
f = open("login_cred.txt", "r")
tokens = [next(f) for x in range(2)] 
f.close()

username.clear()
username.send_keys(tokens[0])
password.clear()
password.send_keys(tokens[1])
Login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

driver.get("https://www.instagram.com/sidbendre")
# searchbox = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
# searchbox.clear()
# keyword = "ursecret_safe"
# searchbox.send_keys(keyword)
# time.sleep(5)
# searchbox.send_keys(Keys.ENTER)
# time.sleep(5)
# searchbox.send_keys(Keys.ENTER)
# time.sleep(5)

elements = driver.find_elements(by=By.XPATH, value='//a[@href]')

links = []
print("\n")

# try: FOR STORING THE URLS
#     f = open("login_cred.txt", "r")
#     tokens = [next(f) for x in range(2)] 
#     f.close()
# except:

for elem in elements:
    url = elem.get_attribute('href')
    
    if url not in links and 'p' in url.split('/'):
            links.append(url)
            print(url, "\n")
            


"""Saving the content of picture in the file"""
number = new_pictures[0]
link = new_pictures[1]

with open(os.path.join(folder, f"Image{number}.jpg"), "wb") as f:
    
    
    f.write(content_of_picture)
    

