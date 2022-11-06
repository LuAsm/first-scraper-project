from scraper.models.equipment import Equipment
from typing import List, Dict
from scraper.scrapers.base import BaseScraper
from scraper.scrapers import SCRAPERS

class Scraper:
    def _parse_scrapers(self, scrapers: list[str]) -> List[BaseScraper]:
        return [SCRAPERS[scraper] for scraper in scrapers]

    def scrape(self, keyword: str, recipes_per_scraper_count: int, scrapers: List[str]) -> List[Equipment]:
        parsed_scrapers: List[BaseScraper] = self._parse_scrapers(scrapers)
        results: List[Dict] = []

        for scraper in parsed_scrapers:
            results.append({"scraper": scraper.__class__.__name__, "items": scraper.scrape(recipes_per_scraper_count, keyword)})
        
        return results