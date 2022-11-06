from scraper.models.equipment import EquipmentLink, Equipment
from typing import List, Optional
import math
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    __item_per_page__: int = 0


    @abstractmethod
    def _retrieve_item_list(self, pages_count: int, keyword: str) -> List [EquipmentLink]:
        pass

    def _get_page_content(self, query: str) -> Optional[BeautifulSoup]:
        resp = requests.get(f"{self.__domain__}/query")
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
        scraped_equipments =  [self._retrieve_equipment_info(equipment_link) for equipment_link in equipments_links]
        return [scraped_equipment for scraped_equipment in scraped_equipments if scraped_equipment is not None]