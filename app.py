import streamlit as st
from langchain_core.messages import HumanMessage

from graph import app

# ---------------------------------------------
# Page Configuration
# ---------------------------------------------

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------
# Header
# ---------------------------------------------

st.title("🌍 AI Travel Planner")
st.write("Plan personalized trips using AI.")

# ---------------------------------------------
# Sidebar
# ---------------------------------------------

with st.sidebar:

    st.header("About")

    st.write("""
### AI Travel Planner

This assistant uses **LangGraph + LLMs** to:

- 📍 Recommend destinations
- 💰 Estimate trip costs
- 🚌 Recommend transport
- 🗓️ Generate complete itineraries
""")

# ---------------------------------------------
# User Input
# ---------------------------------------------

query = st.text_area(
    "Describe your trip",
    placeholder="Example: Suggest a 4-day mountain trip under 100k."
)

# ---------------------------------------------
# Plan Trip
# ---------------------------------------------

def display_trip(final_state):

    st.success("Trip Generated!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Destination")
        st.success(final_state["chosen_destination"])

    with col2:
        st.subheader("💰 Estimated Cost")
        st.metric(
            "Budget",
            f"PKR {final_state['estimated_cost']}"
        )

    st.subheader("🚌 Recommended Transport")
    st.info(final_state["recommended_transport"])

    st.subheader("Why this destination?")
    st.write(final_state["reason"])

    st.divider()

    st.header("🗓️ Complete Itinerary")
    st.markdown(final_state["itinerary"])

if st.button("Plan Trip"):

    if not query.strip():
        st.warning("Please describe your trip.")
        st.stop()

    progress = st.status("Planning your trip...", expanded=True)

    final_state = None

    try:

        for event in app.stream(
            {
                "messages": [
                    HumanMessage(content=query)
                ]
            }
        ):
            node = list(event.keys())[0]

            progress.write(
                f"✅ {node.replace('_', ' ').title()} completed"
            )

            final_state = event[node]

        progress.update(
            label="Trip generated successfully!",
            state="complete"
        )

        display_trip(final_state)

    except Exception as e:
        progress.update(
            label="Trip generation failed",
            state="error"
        )
        st.error(f"Error: {e}")