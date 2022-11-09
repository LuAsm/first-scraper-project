from scraper.models.equipment import EquipmentLink, Equipment
from typing import List, Optional
import math
from abc import ABC, abstractmethod
from decimal import DivisionByZero
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    __item_per_page__: int = 0
    __domain__: str = ""


    @abstractmethod
    def _retrieve_item_list(self, pages_count: int, keyword: str) -> List [EquipmentLink]:
        pass

    def _get_page_content(self, query: str) -> Optional[BeautifulSoup]:


        resp = requests.get(f"{self.__domain__}/{query}")
        if resp.status_code == 200:
            return BeautifulSoup (resp.content)
        raise Exception("Cannot reach content")

  


    @abstractmethod
    def _retrieve_equipment_info(self, link: EquipmentLink) -> Optional [Equipment]:
        pass

    def scrape(self, equipments_count: int, keyword: str ) -> List[Equipment]:
        try:
            pages_count = math.ceil(equipments_count / self.__item_per_page__)
            
        except ZeroDivisionError:
            raise AttributeError("Equipments per page is zero")

        equipments_links = self._retrieve_item_list(pages_count, keyword)
        scraped_equipments: List[Optional[Equipment]] = []
        for equipment_link in tqdm(equipments_links):
            scraped_equipment = self._retrieve_equipment_info(equipment_link)
            if scraped_equipment:
                scraped_equipments.append(scraped_equipment)
        return scraped_equipments