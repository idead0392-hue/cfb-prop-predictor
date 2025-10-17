import streamlit as st
import asyncio
from cfb_prop_predictor.workflow import run_cfb_prop_workflow

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="CFB Prop Predictor", layout="wide")
st.title("🏈 CFB Prop Predictor Agent (Python Version)")
st.markdown("Enter prop details and the AI agent will run a full data and analysis workflow.")

# --- Helper to run async code in Streamlit ---
def run_async(coro):
    return asyncio.run(coro)

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
        
        with st.spinner("🔍 Agent is gathering live data and running analysis..."):
            response = run_async(run_cfb_prop_workflow(request))

        if response:
            st.success("Prediction Complete!")
            
            pred = response.get("prediction", {})
            conf = pred.get("confidence", 0)
            reason = response.get("reasoning", "No reasoning provided.")
            rec = pred.get('recommendedBet', 'N/A').upper()
            color = "green" if rec == "OVER" else "red" if rec == "UNDER" else "orange"

            st.subheader(f"Recommendation: :{color}[{rec}]")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Confidence", f"{conf} / 100")
            c2.metric("Projected Value", pred.get('projectedValue', 0))
            c3.metric("Edge vs. Line", pred.get('edge', 0))
            
            with st.expander("Show Detailed Reasoning"):
                st.markdown(reason)
            with st.expander("Show Full JSON Response"):
                st.json(response)
