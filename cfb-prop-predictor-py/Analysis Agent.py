from cfb_prop_predictor.types import GatheredData, AnalysisOutput
import re

def analyze(data: GatheredData) -> AnalysisOutput:
    """
    Analyzes gathered data to produce key metrics and insights.
    """
    key_metrics = {"seasonAverage": 0.0} # Placeholder for now
    
    game_context = None
    if data.matchup_odds and data.matchup_odds.total and data.matchup_odds.spread:
        try:
            total_str = data.matchup_odds.total.get('over', '')
            spread_str = data.matchup_odds.spread.get('home', '')
            
            total_match = re.search(r'(\d+\.?\d*)', total_str)
            spread_match = re.search(r'([-\+]\d+\.?\d*)', spread_str)

            if total_match and spread_match:
                total = float(total_match.group(1))
                spread = float(spread_match.group(1))
                
                game_context = {
                    "paceOfPlay": "Fast-paced game expected" if total > 55 else "Average pace expected",
                    "impliedTeamTotal": (total / 2) - (spread / 2)
                }
        except (AttributeError, ValueError):
            game_context = {"error": "Could not parse odds."}

    return AnalysisOutput(
        trends={"recentForm": "Historical player data not yet implemented in this version."},
        keyMetrics=key_metrics,
        gameContext=game_context
    )
