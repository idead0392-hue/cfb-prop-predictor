from cfb_prop_predictor.agents.data_gatherer import gather_data
from cfb_prop_predictor.agents.analyzer import analyze
from cfb_prop_predictor.agents.predictor import predict
from typing import Dict
import asyncio

async def run_cfb_prop_workflow(request: Dict) -> Dict:
    """
    Asynchronously runs the full data gathering, analysis, and prediction workflow.
    """
    # Step 1: Gather data
    gathered = await gather_data(request)

    # Step 2: Analyze data
    analysis = analyze(gathered)

    # Step 3: Generate prediction
    prediction_result = predict(gathered, analysis)

    return {
        "prediction": prediction_result["prediction"],
        "reasoning": prediction_result["reasoning"],
        "supportingData": {
            "gathered": gathered.dict(by_alias=True),
            "analysis": analysis.dict(by_alias=True),
        }
    }
