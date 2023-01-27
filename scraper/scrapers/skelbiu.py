from scraper.scrapers.base import BaseScraper
from scraper.models.equipment import Equipment, EquipmentLink
from typing import List, Optional, Dict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
from selenium.common.exceptions import (NoSuchElementException,ElementClickInterceptedException,ElementNotInteractableException)
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

class Skelbiu (BaseScraper):
    __items_per_page__: int = 24
    __domain__: str = "https://www.skelbiu.lt"
   
    def _retrieve_item_list(self, pages_count: int, keyword: str) -> List[EquipmentLink]:
        results: List[EquipmentLink] = []
        
        driver = webdriver.Chrome()
        driver.get("https://www.skelbiu.lt/")
        search = driver.find_element(By.ID, "searchKeyword")
        search.clear()
        search.send_keys(f"{keyword}")
        click_search = driver.find_element(By.ID, "searchButton")
        click_search.send_keys(Keys.ENTER)
        driver.implicitly_wait(0.5)
        click_cat = driver.find_element(By.CLASS_NAME, "popular_categories_link")
        click_cat.send_keys(Keys.ENTER)
        print(pages_count)
        for page_num in range (1, pages_count + 1):
            elements = driver.find_elements(By.CLASS_NAME, 'itemReview')
#links = [elem.find_element(By.CLASS_NAME, 'js-cfuser-link').get_attribute('href') for elem in elems]


            for element in elements:
                link_to_equipment=element.find_element(By.CLASS_NAME, 'js-cfuser-link').get_attribute('href')
                results.append(EquipmentLink(url=link_to_equipment))
                
            
            click_next = driver.find_element(By.CSS_SELECTOR ,"a[rel='next']")
            click_next.send_keys(Keys.ENTER)
            _sleep = random.randint(1,10)
            time.sleep(_sleep)
                
            
        return results

    def _retrieve_equipment_info(self, link: EquipmentLink) -> Optional[Equipment]:
        driver= webdriver.Chrome()
        driver.get(link.url)
        try:
            title = driver.find_element(By.CLASS_NAME, "left-block").find_element(By.TAG_NAME, 'h1').text
        except (NoSuchElementException, UnboundLocalError):
            title = "None"
        try:
            image = driver.find_element(By.ID, 'main-photo' )
            image_link = image.get_attribute('src')
        except (NoSuchElementException, UnboundLocalError):
            image_link = "None"
        try:
            price = driver.find_element(By.CLASS_NAME, "price").text
        except (NoSuchElementException, UnboundLocalError):
            price = "None"
        try:
            specs = driver.find_element(By.CSS_SELECTOR, "div[itemprop='description']").text
        except (NoSuchElementException, UnboundLocalError):
            specs = "None"
        try:
            condition = driver.find_element(By.CLASS_NAME, "value").text
        except (NoSuchElementException, UnboundLocalError):
            condition = "None"
        _sleep = random.randint(1,10)
        time.sleep(_sleep)
        
        return{
            "title": title.strip(),
            "price": price.replace("\n"," ").strip(),
            "link" : link.url,
            
            "image": image_link,
           
            "condition": condition,
                 #"about": about_equipment.strip(),
            "specs": specs
                    
            }

        