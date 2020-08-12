from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from bs4 import BeautifulSoup as soup
import requests
import json
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Firefox(options=options)
driver.get('https://codepen.io/freeCodeCamp/full/zNqgVx')
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
sleep(5)
# html = driver.execute_script("return document.body.innerHTML")
# print(html)
html = driver.page_source
driver.quit()
sleep(2)
root = soup(html,'html.parser')
bint = [str(i) for i in root.findAll('li')]
with open("parsed_data.json",'w') as file:
    json.dump(bint,file)