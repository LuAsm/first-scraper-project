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

class Ebay (BaseScraper):
    __items_per_page__: int = 60
    __domain__: str = "https://www.ebay.co.uk/"
   
    def _retrieve_item_list(self, pages_count: int, keyword: str) -> List[EquipmentLink]:
        results: List[EquipmentLink] = []
        
        driver = webdriver.Chrome()
        driver.get("https://www.ebay.co.uk/")
        search = driver.find_element(By.ID, "gh-ac")
        search.clear()
        search.send_keys(f"{keyword}")
        click_search = driver.find_element(By.ID, "gh-btn")
        click_search.send_keys(Keys.ENTER)
        driver.implicitly_wait(0.5)
        click_used = driver.find_element(By.PARTIAL_LINK_TEXT ,"Used")
        click_used.send_keys(Keys.ENTER)
        click_new = driver.find_element(By.PARTIAL_LINK_TEXT ,"New")
        click_new.send_keys(Keys.ENTER)
        click_brand_1 = driver.find_element(By.PARTIAL_LINK_TEXT ,"AMD")
        click_brand_1.send_keys(Keys.ENTER)
        click_brand_2 = driver.find_element(By.PARTIAL_LINK_TEXT ,"ASUS")
        click_brand_2.send_keys(Keys.ENTER)
        click_brand_3 = driver.find_element(By.PARTIAL_LINK_TEXT ,"Dell")
        click_brand_3.send_keys(Keys.ENTER)
        click_brand_4 = driver.find_element(By.PARTIAL_LINK_TEXT ,"EVGA")
        click_brand_4.send_keys(Keys.ENTER)
        click_brand_5 = driver.find_element(By.PARTIAL_LINK_TEXT ,"GIGABYTE")
        click_brand_5.send_keys(Keys.ENTER)
        click_brand_6 = driver.find_element(By.PARTIAL_LINK_TEXT ,"MSI")
        click_brand_6.send_keys(Keys.ENTER)
        click_brand_7 = driver.find_element(By.PARTIAL_LINK_TEXT ,"NVIDIA")
        click_brand_7.send_keys(Keys.ENTER)
        print(pages_count)
        for page_num in range (1, pages_count + 1):
            elements = driver.find_elements(By.CSS_SELECTOR ,"li[class='s-item s-item__pl-on-bottom']")
#links = [elem.find_element(By.CLASS_NAME, 'js-cfuser-link').get_attribute('href') for elem in elems]


            for element in elements:
                link_to_equipment=element.find_element(By.CLASS_NAME, 's-item__link').get_attribute('href')
                results.append(EquipmentLink(url=link_to_equipment))
                
            
            click_next = driver.find_element(By.CSS_SELECTOR ,"a[aria-label='Go to next search page']")
            click_next.send_keys(Keys.ENTER)
            _sleep = random.randint(1,5)
            time.sleep(_sleep)
        
                
        driver.quit()    
        return results

    def _retrieve_equipment_info(self, link: EquipmentLink) -> Optional[Equipment]:
        driver= webdriver.Chrome()
        driver.get(link.url)
        try:
            title = driver.find_element(By.CLASS_NAME, "x-item-title__mainTitle").text
        except (NoSuchElementException, UnboundLocalError):
            title = "None"
        try:
            price = driver.find_element(By.CSS_SELECTOR ,"span[itemprop='price']").text
        except (NoSuchElementException, UnboundLocalError):
            price = "None"
        try:
            specs_label= driver.find_element(By.ID, "viTabs_0_is").find_elements(By.CLASS_NAME, "ux-labels-values__labels")
            text_label = [spec_label.find_element(By.CLASS_NAME, 'ux-textspans').text for spec_label in specs_label]
        except (NoSuchElementException, UnboundLocalError):
            specs_label = "None"
            text_label = ["None"]
        try:
            specs = driver.find_element(By.ID, "viTabs_0_is").find_elements(By.CLASS_NAME, "ux-labels-values__values")
            text = [spec.find_element(By.CLASS_NAME, 'ux-textspans').text for spec in specs]
        except (NoSuchElementException, UnboundLocalError):
            specs = "None"
            text = ["None"]

        try:
            condition = driver.find_element(By.CLASS_NAME, "x-item-condition-text").find_element(By.CLASS_NAME, "ux-textspans").text
        except (NoSuchElementException, UnboundLocalError):
            condition = "None"
        _sleep = random.randint(1,5)
        time.sleep(_sleep)
        item_specs = {text_label[i]: text[i] for i in range(len(text_label))}
        item_specs ["Condition:"] = condition
        return{
            "title": title.strip(),
            "price": price.replace("\n"," ").strip(),
            "link" : link.url,
            "condition": condition,
                 #"about": about_equipment.strip(),
            "item_specs": item_specs
                    
            }
