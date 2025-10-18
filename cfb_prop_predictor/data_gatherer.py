from playwright.async_api import async_playwright
from cfb_prop_predictor.types import GatheredData
from cfb_prop_predictor.utils.play_scraper import scrape_player_props, scrape_matchup_odds
from typing import Dict
import asyncio

async def gather_data(request: Dict) -> GatheredData:
    """
    Orchestrates data gathering from web scraping and APIs.
    """
    game = request.get('game')
    player = request.get('player')
    prop_type = request.get('propType')

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Run scraping tasks concurrently for efficiency
        tasks = {
            'odds_data': scrape_player_props(page, player, prop_type) if player else None,
            'matchup_odds': scrape_matchup_odds(page, game) if game else None,
        }
        
        results = await asyncio.gather(*tasks.values())
        data_dict = dict(zip(tasks.keys(), results))

        await browser.close()
        
    return GatheredData(**data_dict)

