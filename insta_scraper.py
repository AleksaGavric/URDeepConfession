import os
from selenium.common.exceptions import NoSuchElementException
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

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.instagram.com/")

def get_login_credentials():
    f = open("login_cred.txt", "r")
    tokens = [next(f) for x in range(2)] 
    f.close()
    
    return tokens

def login(tokens):
    username = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    username.clear()
    username.send_keys(tokens[0])
    password.clear()
    password.send_keys(tokens[1])
    time.sleep(2)
    
def open_insta_handle(handle):
    link = "https://www.instagram.com/{handle}".format(handle = handle)
    
    driver.get(link)
    
def scrape_post_urls():
    links = []
    end_scroll = []
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        
        elements = driver.find_elements(by = By.XPATH, value = '//a[@href]')
        
        for elem in elements:
            url = elem.get_attribute('href')
            
            if url not in links and 'p' in url.split('/'):
                    links.append(url)
                    
        time.sleep(1.5)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        end_scroll.append(new_height)
        
        if end_scroll.count(end_scroll[-1]) > 4:
            break
    
    with open("url_safe.txt", "w") as outfile:
        outfile.write("\n".join(links))
        
    return links

def save_images_from_urls(urls):
    images = []

    for a in urls:
        driver.get(a)
        time.sleep(1)
        img = driver.find_elements(By.TAG_NAME, value='img') 
        img = [i.get_attribute('src') for i in img] 
        images.append(img[1])
        
        while (True):
            try:
                driver.find_element(By.XPATH, '//button[contains(@aria-label, "Next")]').click()
                time.sleep(0.5)
                img = driver.find_elements(By.TAG_NAME, value='img')
                img = [i.get_attribute('src') for i in img]
                images.append(img[1])
            except NoSuchElementException:
                break
        
    counter = 0

    main_dir = os.getcwd()
    picture_dir = os.path.join(main_dir,
        'pictures/')

    for image in images:
        save_as = os.path.join(picture_dir, str(counter) +
        '.jpg')
        wget.download(image, save_as)
        counter += 1
        
def main():
    login_credentials = get_login_credentials()
    login(login_credentials)
    
    insta_handle = "ursecret_safe"
    open_insta_handle(insta_handle)
    
    urls = scrape_post_urls()
    save_images_from_urls(urls)
    
    driver.close()
    
main()
    

