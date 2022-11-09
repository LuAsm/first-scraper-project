from scraper.models.equipment import Equipment
from typing import List, Dict
from scraper.scrapers.base import BaseScraper
from scraper.scrapers import SCRAPERS

class Scraper:
    def _parse_scrapers(self, scrapers: list[str]) -> List[Dict]:
        return [SCRAPERS[scraper]() for scraper in scrapers]

    def scrape(self, equipments_per_scraper_count: int, keyword: str, scrapers: List[str]) -> List[Dict]:
        parsed_scrapers: List[BaseScraper] = self._parse_scrapers(scrapers)
        results: List[Dict] = []

        for scraper in parsed_scrapers:
            print(equipments_per_scraper_count)
            print(keyword)
            results.append({
                "scraper": scraper.__class__.__name__, 
                "items": scraper.scrape(equipments_per_scraper_count, keyword)
                })
        
        return results