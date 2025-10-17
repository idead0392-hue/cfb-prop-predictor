import asyncio
from playwright.async_api import async_playwright, Page
from typing import Optional, List
from cfb_prop_predictor.types import OddsData, MatchupOdds


async def scrape_player_props(page: Page, player_name: str, prop_type: str) -> Optional[OddsData]:
    """Scrapes Rotowire for a specific player's prop line and odds."""
    await page.goto('https://www.rotowire.com/betting/college-football/player-props.php', wait_until='domcontentloaded')
    
    prop_identifier = prop_type.split('_')[1] # e.g., 'passing'
    
    locators = page.locator('.prop-lines-table tbody')
    for i in range(await locators.count()):
        section = locators.nth(i)
        header = await section.locator('tr.table-header td.font-bold').text_content()
        if header and prop_identifier in header.lower():
            player_rows = section.locator('tr:not(.table-header)')
            for j in range(await player_rows.count()):
                row = player_rows.nth(j)
                name = await row.locator('a.font-bold').text_content()
                if name and name.strip() == player_name:
                    line = await row.locator('.line-cell .line').text_content()
                    odds_list = await row.locator('.line-cell .odds').all_text_contents()
                    return OddsData(
                        propLine=float(line.strip()),
                        overOdds=int(odds_list[0].strip()),
                        underOdds=int(odds_list[1].strip())
                    )
    return None


async def scrape_matchup_odds(page: Page, game: str) -> Optional[MatchupOdds]:
    """Scrapes Rotowire for a specific game's matchup odds."""
    await page.goto('https://www.rotowire.com/betting/college-football/odds', wait_until='domcontentloaded')
    
    away_team_name, home_team_name = [team.strip() for team in game.split('vs.')]
    
    game_rows = page.locator('.odds-table-container .grid.grid-cols-12')
    for i in range(await game_rows.count()):
        row = game_rows.nth(i)
        teams = await row.locator('.w-full.flex.items-center a.text-sm').all_text_contents()
        if len(teams) >= 2 and away_team_name in teams[0] and home_team_name in teams[1]:
            odds_cells = await row.locator('.flex.w-full.justify-end .flex-col').all_text_contents()
            return MatchupOdds(
                awayTeam=teams[0].strip(),
                homeTeam=teams[1].strip(),
                spread={'away': odds_cells[0].strip(), 'home': odds_cells[1].strip()},
                moneyline={'away': odds_cells[2].strip(), 'home': odds_cells[3].strip()},
                total={'over': odds_cells[4].strip(), 'under': odds_cells[5].strip()}
            )
    return None
