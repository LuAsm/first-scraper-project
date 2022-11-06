from scraper.scrapers.base import BaseScraper
from scraper.models.equipment import Equipment, EquipmentLink
from typing import List, Optional, Dict
import requests
from bs4 import BeautifulSoup


class Varle(BaseScraper):
    __items_per_page__: int = 38
    __domain__: str = "https://www.varle.lt" 
    def _retrieve_item_list(self, pages_count: int, keyword: str) -> List[EquipmentLink]:
        results: List[EquipmentLink] = []
        for page_num in range (2, pages_count + 2):
            content = self._get_page_content(f"/search/?p={page_num}&q={keyword}")
            if content:
                equipments_list_div = content.find("div", class_="ajax-container")


            base_url="https://www.varle.lt"
            if not equipments_list_div:
                break    
            all_equipments_div = equipments_list_div.find_all("div", class_="GRID_ITEM")
            for equipment_div in all_equipments_div:
                link_to_equipment = base_url + equipment_div.find("a")["href"]
                results.append(EquipmentLink(url=link_to_equipment))

            else:
                continue
        return results
    
    def _retrieve_equipment_info(self, link: EquipmentLink) -> Optional[Equipment]:

        content = self._get_page_content(link.url)
        if content:

            equipment_title = content.find("div", class_="title-block").find("h1").text
            try:

                main_equipment_image = content.find("img").get("src")
            except KeyError:
                main_equipment_image = None
            about_equipment= content.find("div", class_="PRODUCT_DESCRIPTION").text

            specs_div = content.find("div", class_="PRODUCT_SPEC")
            specs_table = specs_div.find("ul")
            li_rows = specs_table.find_all("li")
            specs: List[Dict] = []
            try:
                for li_row in li_rows:
                    spans = li_row.find_all("span")
                    specs.append({"Spec": spans[0].text.strip(), "result": spans[1].text.strip()})
            except IndexError:
                pass

            return {
                "title": equipment_title.strip(),
                "image": main_equipment_image,
                "about": about_equipment.strip(),
                "specs": specs
            }
        else: 
            return None
        
