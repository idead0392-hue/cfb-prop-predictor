from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class OddsData(BaseModel):
    prop_line: float = Field(..., alias='propLine')
    over_odds: int = Field(..., alias='overOdds')
    under_odds: int = Field(..., alias='underOdds')


class MatchupOdds(BaseModel):
    away_team: str = Field(..., alias='awayTeam')
    home_team: str = Field(..., alias='homeTeam')
    spread: Dict[str, str]
    moneyline: Dict[str, str]
    total: Dict[str, str]


class PlayerStats(BaseModel):
    name: str
    season: Dict[str, float]
    last_five_games: List = Field(alias='lastFiveGames', default=[])


class GatheredData(BaseModel):
    odds_data: Optional[OddsData] = Field(alias='oddsData', default=None)
    matchup_odds: Optional[MatchupOdds] = Field(alias='matchupOdds', default=None)
    player_stats: Optional[PlayerStats] = Field(alias='playerStats', default=None)


class AnalysisOutput(BaseModel):
    trends: Dict[str, str]
    key_metrics: Dict[str, float] = Field(alias='keyMetrics')
    game_context: Optional[Dict[str, float | str]] = Field(alias='gameContext', default=None)


class PredictionOutput(BaseModel):
    recommended_bet: str = Field(..., alias='recommendedBet')
    projected_value: float = Field(..., alias='projectedValue')
    edge: float
    confidence: float


class WorkflowResult(BaseModel):
    prediction: PredictionOutput
    reasoning: str
    supporting_data: Dict = Field(alias='supportingData')
