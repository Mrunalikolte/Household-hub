import streamlit as st
import ollama

# 1. Page Configuration: Sets the browser tab title and icon
st.set_page_config(page_title="TrailReady AI", page_icon="🥾", layout="centered")

# 2. Header UI: Displays main title and subtitle on your web app
st.title("🥾 TrailReady: Offline Route & Trip Planner")
st.caption("Generate instant route itineraries and packing checklists locally.")

# 3. User Input Form: Collects location, distance, activity, and terrain preferences
with st.form("planner_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.text_input("Location / Trail Area", value="Forest Park")
        distance = st.selectbox("Distance / Duration", ["3 km / Quick Walk", "5 km / Moderate Run", "10 km+ / Day Hike"])
    
    with col2:
        activity = st.selectbox("Activity Type", ["Running", "Trail Walking", "Birdwatching", "Dog Walking"])
        terrain = st.multiselect("Terrain & Features", ["Shaded / Forest", "Paved", "Elevation / Hills", "Water Views"], default=["Shaded / Forest"])
    
    submit_button = st.form_submit_button("Generate Offline Plan")

# 4. Processing Logic: Runs when the user clicks the "Generate Offline Plan" button
if submit_button:
    if not location:
        st.warning("Please specify a location.")
    else:
        with st.spinner("Generating itinerary locally..."):
            
            # System Prompt: Tells the AI how to act and enforces strict length and formatting limits
            system_instruction = """
            You are an offline trail assistant. Your goal is to give hikers and runners quick, actionable details so they spend minimal time looking at screens.
            Format your output strictly into two sections:
            1. ROUTE ITINERARY (Brief step-by-step overview)
            2. PACKING CHECKLIST (Bullet points based on distance/terrain)
            Keep explanations under 150 words total.
            """
            
            # User Prompt: Combines user inputs into a structured message for the AI
            user_prompt = f"""
            Location: {location}
            Activity: {activity}
            Distance: {distance}
            Terrain/Features: {', '.join(terrain)}
            """
            
            try:
                # Calls Ollama to execute Llama 3.2 locally
                response = ollama.chat(
                    model="llama3.2:3b",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                
                # Displays the AI output on the Streamlit web screen
                st.markdown("---")
                st.subheader("📍 Your Trail Plan")
                st.markdown(response["message"]["content"])
                st.info("💡 Tip: Take a screenshot before heading out into areas with no signal!")
                
            except Exception as e:
                st.error(f"Error connecting to Ollama: {e}")