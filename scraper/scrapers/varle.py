from scraper.scrapers.base import BaseScraper
from scraper.models.equipment import Equipment, EquipmentLink
from typing import List, Optional, Dict

from bs4 import BeautifulSoup
#from scraper.models.sql import mydb



class Varle(BaseScraper):
    __items_per_page__: int = 39
    __domain__: str = "https://www.varle.lt" 
    def _retrieve_item_list(self, pages_count: int, keyword: str) -> List[EquipmentLink]:
        results: List[EquipmentLink] = []
        for page_num in range (2, pages_count + 2):
            content = self._get_page_content(f"search/?p={page_num}&q={keyword}")
            if content:
                equipments_list_div = content.find("div", class_="ajax-content")
                

                base_url="https://www.varle.lt"
                if not equipments_list_div:
                    
                    break  
                
                all_equipments_div = equipments_list_div.find_all("div", class_="GRID_ITEM")
                for equipment_div in all_equipments_div:
                    link_to_equipment = base_url + equipment_div.find("a")["href"]
                    results.append(EquipmentLink(url=link_to_equipment[20:]))
                    
                    
            else:
                continue
        return results
    
    def _retrieve_equipment_info(self, link: EquipmentLink) -> Optional[Equipment]:
        
        base_url="https://www.varle.lt"
        content = self._get_page_content(link.url)
        
        
        if content:
            
            equipment_title = content.find("div", class_="title-block").find("h1").text
            print(equipment_title)
            try:

                main_equipment_image = content.find("img").get("src")
            except KeyError:
                main_equipment_image = None

            price = content.find("div",class_="price-tag").find("span",class_="price-value").text
            #try:
             #   about_equipment= content.find("div", class_="PRODUCT_DESCRIPTION").text
            #except AttributeError:
            #    pass
            try:    
                specs_div = content.find("div", class_="PRODUCT_SPEC")
            
                li_rows = specs_div.find_all("li")
                specs: List[Dict] = []
            except AttributeError:
                pass  
            try:
                for li_row in li_rows:
                    spans = li_row.find_all("span")
                    specs.append({"Spec": spans[0].text.strip(), "value": spans[1].text.strip()})
            except (IndexError , UnboundLocalError):
                specs="None"
              
                
            return{
                    "model": equipment_title.strip(),
                    "price": price.replace("\n"," ").strip(),
                    "link" : base_url+link.url,
                    "image": base_url+main_equipment_image,
                 #  "about": about_equipment.strip(),
                    "specs": specs,
                    
                    }

                

        else: 
            return print("Cannot reach content") 
            
                   
        
