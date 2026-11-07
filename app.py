import os
import streamlit as st
from google import genai
from PIL import Image

# Initialize the official Gemini Client
client = genai.Client()

# Set up page styling
st.set_page_config(page_title="PantryPal AI", page_icon="🥗", layout="centered")

st.title("🥗 PantryPal AI")
st.caption("Multimodal Food Waste Reduction & Recipe Optimizer")
st.write(
    "Upload a photo of your fridge, pantry, or ingredients to analyze item freshness "
    "and generate smart recipes prioritized by expiration window."
)

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Configuration")
    dietary_pref = st.selectbox(
        "Dietary Preference", 
        ["No Preference", "Vegetarian", "Vegan", "Gluten-Free", "High Protein"]
    )
    max_prep = st.slider("Max Preparation Time (mins)", 10, 60, 30)

# Main Image Input Component
uploaded_file = st.file_uploader("Upload a photo of your ingredients:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Pantry Photo", use_container_width=True)
    
    if st.button("🔍 Analyze & Generate Recipes", type="primary"):
        with st.spinner("Analyzing ingredients with Gemini..."):
            try:
                prompt = f"""
                You are an expert culinary analyst focused on reducing household food waste.
                Analyze the provided image and generate output formatted strictly in Markdown with these exact sections:

                ### 🧺 Identified Ingredients & Expiry Analysis
                List every detected food item and assign a freshness indicator:
                - 🔴 **Use Immediately** (within 1-2 days)
                - 🟡 **Use Soon** (within 3-5 days)
                - 🟢 **Stable** (1+ week)

                ### 📊 Insights & Waste Metrics
                Provide 2-3 quick quantitative insights (e.g., estimated percentage of perishable items needing immediate consumption).

                ### 🍳 3 Custom Waste-Reduction Recipes
                Provide 3 recipes based on user parameters (Dietary: {dietary_pref}, Max Time: {max_prep} mins):
                Prioritize ingredients marked 🔴 **Use Immediately**.
                For each recipe, include:
                - **Recipe Name** | ⏱️ Prep Time | 🏷️ Diet Tag
                - *Ingredients Used:* (highlight which 🔴 items are used)
                - *Quick Steps:* 3-4 bullet points
                - *Estimated Calories:* Approx value
                """

                # Send image and prompt to Gemini
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[img, prompt]
                )

                st.success("Analysis & Recipe Generation Complete!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error executing Gemini API: {e}")