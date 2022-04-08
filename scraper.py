'''
FLOW:

'''

import os
import wget
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time 

# setting up the driver using chrome 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.instagram.com/")

# get secure credentials
f = open("login_cred.txt", "r")
tokens = [next(f) for x in range(2)] 
f.close()

# login
username = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
username.clear()
username.send_keys(tokens[0])
password.clear()
password.send_keys(tokens[1])
Login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

# profile selection
driver.get("https://www.instagram.com/katelyn.freebern")

# scrape links in form of .img urls
elements = driver.find_elements(by=By.XPATH, value='//a[@href]')

links = []

# try: FOR STORING THE URLS
#     f = open("login_cred.txt", "r")
#     tokens = [next(f) for x in range(2)] 
#     f.close()
# except:

for elem in elements:
    url = elem.get_attribute('href')
    
    if url not in links and 'p' in url.split('/'):
            links.append(url)

# downloading images
images = []

for a in links:
    driver.get(a)
    time.sleep(5)
    img = driver.find_elements(By.TAG_NAME, value='img')
    img = [i.get_attribute('src') for i in img]

    images.append(img[1])

counter = 0

main_dir = os.getcwd()
picture_dir = os.path.join(main_dir,
    '/pictures')

for image in images:
    save_as = os.path.join(main_dir, str(counter) +
    '.jpg')
    wget.download(image, save_as)
    counter += 1
    
# TODO: enable button clicking within each pic page (must be with exception handling)
# make links file
# make it a class and modularize 