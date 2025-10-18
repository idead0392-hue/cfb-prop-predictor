from cfb_prop_predictor.types import GatheredData, AnalysisOutput, PredictionOutput

def predict(data: GatheredData, analysis: AnalysisOutput) -> dict:
    """
    Generates a final prediction based on the analysis.
    """
    prop_line = data.odds_data.prop_line if data.odds_data else 0.0
    projected_value = analysis.key_metrics.get("seasonAverage", 0.0) # Using placeholder
    edge = projected_value - prop_line
    
    confidence = 50.0 # Base confidence
    
    # Adjust confidence based on edge
    if prop_line > 0:
        edge_percent = abs(edge / prop_line)
        confidence += edge_percent * 50 

    # Adjust based on game context
    if analysis.game_context and "Fast-paced" in str(analysis.game_context.get("paceOfPlay")):
        confidence += 5

    confidence = max(10, min(95, round(confidence)))
    
    recommended_bet = "avoid"
    if confidence > 55 and prop_line > 0:
        recommended_bet = "over" if edge > 0 else "under"
        
    prediction = PredictionOutput(
        recommendedBet=recommended_bet,
        projectedValue=round(projected_value, 1),
        edge=round(edge, 1),
        confidence=confidence
    )
    
    reasoning = f"Projection of {prediction.projected_value} (placeholder) vs. line of {prop_line} creates an edge of {prediction.edge}. " \
                f"Confidence is rated at {confidence}/100 based on game context."

    return {
        "prediction": prediction.dict(by_alias=True),
        "reasoning": reasoning
    }
