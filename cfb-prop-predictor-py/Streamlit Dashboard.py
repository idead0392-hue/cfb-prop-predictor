import streamlit as st
import asyncio
from cfb_prop_predictor.workflow import run_cfb_prop_workflow
import sys

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="CFB Prop Predictor", layout="wide")
st.title("🏈 CFB Prop Predictor Agent (Python Version)")
st.markdown("Enter prop details and the AI agent will run a full data and analysis workflow.")

# --- Helper to run async code in Streamlit ---
def run_async(coro):
    # This is necessary to run asyncio code within Streamlit's execution model
    if sys.version_info >= (3, 7):
        return asyncio.run(coro)
    else: # For older python versions
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

# --- Input Form ---
with st.form("prop_request_form"):
    st.subheader("Prediction Request")
    col1, col2, col3 = st.columns(3)
    with col1:
        game = st.text_input("Game", "Alabama vs. Georgia", help="Format: 'Away Team vs. Home Team'")
    with col2:
        player = st.text_input("Player Name", "Jalen Milroe")
    with col3:
        prop_type = st.selectbox("Prop Type", ["player_passing_yards", "player_rushing_yards"])
    
    submitted = st.form_submit_button("▶️ Run Prediction")

# --- Workflow Execution ---
if submitted:
    if not all([game, player, prop_type]):
        st.warning("Please fill out all fields.")
    else:
        request = {"game": game, "player": player, "propType": prop_type}
        
        with st.spinner("🔍 Agent is gathering live data and running analysis... (This can take up to 30 seconds)"):
            try:
                response = run_async(run_cfb_prop_workflow(request))
            except Exception as e:
                st.error(f"An error occurred during the workflow: {e}")
                st.error("This might be due to the scraper being unable to find the player/game or a network issue. Please check your inputs.")
                response = None

        if response:
            st.success("Prediction Complete!")
            
            pred = response.get("prediction", {})
            conf = pred.get("confidence", 0)
            reason = response.get("reasoning", "No reasoning provided.")
            rec = pred.get('recommendedBet', 'N/A').upper()
            color = "green" if rec == "OVER" else "red" if rec == "UNDER" else "orange"

            st.subheader(f"Recommendation: :{color}[{rec}]")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Confidence", f"{conf:.0f} / 100")
            c2.metric("Projected Value", pred.get('projectedValue', 0))
            c3.metric("Edge vs. Line", pred.get('edge', 0))
            
            with st.expander("Show Detailed Reasoning"):
                st.markdown(reason)
            with st.expander("Show Full JSON Response"):
                st.json(response)
