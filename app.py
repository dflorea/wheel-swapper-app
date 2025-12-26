import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import os

# 1. UI Configuration
st.set_page_config(page_title="Gemini Wheel Swapper", page_icon="🛞")
st.title("🛞 Gemini AI Wheel Swapper")
st.subheader("Upload a car and your dream wheels to see the magic.")

# 2. Get API Key (From Render Environment Variables or local)
#api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
import os
# ... other imports ...

# Get the key directly from the system environment
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please set the GEMINI_API_KEY in your secrets/environment.")
    st.stop()

client = genai.Client(api_key=api_key)

# 3. Frontend: File Uploaders
col1, col2 = st.columns(2)

with col1:
    car_file = st.file_uploader("Step 1: Upload Car Photo", type=['jpg', 'jpeg', 'png'])
    if car_file:
        st.image(car_file, caption="The Base Car", use_container_width=True)

with col2:
    wheel_file = st.file_uploader("Step 2: Upload Wheels Photo", type=['jpg', 'jpeg', 'png'])
    if wheel_file:
        st.image(wheel_file, caption="The New Wheels", use_container_width=True)

# 4. Action Button
if car_file and wheel_file:
    if st.button("🪄 Swap Wheels Now"):
        with st.spinner("Gemini is working its magic..."):
            try:
                # Convert uploaded files to PIL Images
                car_img = Image.open(car_file)
                wheel_img = Image.open(wheel_file)

                # Send to Gemini 3 (Nano Banana Pro)
                #response = client.models.generate_content(
                #    model="gemini-3-pro-image-preview", # Nano Banana Pro
                #    contents=[
                #        "Image A: The base car.",
                #        car_img,
                #        "Image B: The new wheels.",
                #        wheel_img,
                #        "Task: Seamlessly replace the wheels on the car in Image A with the wheels from Image B. Match lighting and perspective."
                #    ],
                #    config=types.GenerateContentConfig(response_modalities=["IMAGE"])
                #)
                response = client.models.generate_content(
                        model="gemini-3-pro-image-preview",
                        contents=[
                                "Image A (Source):", car_img,
                                "Image B (Wheels):", wheel_img,
                                """Task: Perform a localized edit on Image A. 
                                1. Keep the car's body, color, lighting, and entire background EXACTLY as they appear in Image A.
                                2. Replace ONLY the wheels and tires in Image A with the style shown in Image B.
                                3. Match the angle and perspective of the original wheels.
                                4. Do not generate a new car; edit the existing car from Image A."""
                        ],
                        config=types.GenerateContentConfig(response_modalities=["IMAGE"])
                )

                # Display Result
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        st.success("Transformation Complete!")
                        st.image(part.inline_data.data, caption="Your New Ride", use_container_width=True)
            
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Upload both images to enable the magic button.")
