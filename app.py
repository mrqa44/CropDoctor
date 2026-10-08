import streamlit as st
from dotenv import load_dotenv
import os
import urllib.parse

from services.gemini_client import analyze_plant_image, ask_agronomist
from utils.image_utils import process_image
from utils.tts import generate_audio
from utils.weather import get_spraying_weather

# Load environment variables securely
load_dotenv()

st.set_page_config(page_title="AgriLens | ایگری لینس", page_icon="🌱", layout="centered")

# Initialize session state for history and chat
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_result" not in st.session_state:
    st.session_state.current_result = None

def main():
    st.title("🌱 AgriLens")
    st.markdown("**Your AI Plant Doctor | آپ کا اے آئی پلانٹ ڈاکٹر**")
    st.info("Upload or take a picture of a sick plant leaf to get a diagnosis, weather advice, and chat with the AI.")
    
    # --- Sidebar Settings & Weather ---
    st.sidebar.header("Settings | ترتیبات")
    language = st.sidebar.selectbox("Language | زبان", ["English", "Urdu"])
    
    crop_options = [
        "Not sure", "Wheat (گندم)", "Cotton (کپاس)", "Rice (چاول)", 
        "Sugarcane (گنا)", "Maize (مکئی)", "Mango (آم)", "Citrus (ترشاوہ)", "Tomato (ٹماٹر)"
    ]
    crop_type = st.sidebar.selectbox("Crop Type | فصل کی قسم", crop_options)
    
    # NEW FEATURE: Weather-based Spraying Advice
    st.sidebar.divider()
    st.sidebar.subheader("⛅ Spraying Conditions (Local)")
    weather = get_spraying_weather()
    if weather:
        st.sidebar.metric("Temperature", f"{weather['temp']}°C", f"Wind: {weather['wind']} km/h")
        for advice in weather["advice"]:
            if "✅" in advice:
                st.sidebar.success(advice)
            else:
                st.sidebar.warning(advice)
    
    st.sidebar.divider()
    st.sidebar.subheader("Recent Scans History")
    if not st.session_state.history:
        st.sidebar.write("No scans yet.")
    else:
        for idx, item in enumerate(st.session_state.history):
            st.sidebar.caption(f"Scan {idx+1}: {item['crop']}")

    # --- Input Section ---
    tab1, tab2 = st.tabs(["📸 Take Photo", "📂 Upload Image"])
    
    img_file_buffer = None
    with tab1:
        camera_input = st.camera_input("Take a clear picture of the leaf")
        if camera_input: 
            img_file_buffer = camera_input
    with tab2:
        upload_input = st.file_uploader("Upload a picture of the leaf", type=["jpg", "jpeg", "png"])
        if upload_input: 
            img_file_buffer = upload_input

    # --- Analysis Trigger ---
    if img_file_buffer is not None:
        st.image(img_file_buffer, caption="Selected Image", use_container_width=True)
        
        if st.button("🔍 Analyze Plant", type="primary", use_container_width=True):
            with st.spinner("Analyzing your plant... | آپ کے پودے کا تجزیہ ہو رہا ہے..."):
                
                image_bytes = img_file_buffer.getvalue()
                processed_bytes = process_image(image_bytes)
                clean_crop = crop_type.split(" (")[0]
                
                result = analyze_plant_image(processed_bytes, crop_type=clean_crop, language=language)
                
                if "error" in result:
                    st.error(f"⚠️ Error: {result['error']}")
                else:
                    # Clear chat history for a new image
                    st.session_state.chat_history = []
                    st.session_state.current_result = result
                    st.session_state.history.append({"crop": clean_crop, "result": result})

    # Show results if we have them
    if st.session_state.current_result:
        display_result(st.session_state.current_result, language)

def display_result(result, language):
    st.divider()
    
    if not result.get("is_plant", False):
        st.error("⚠️ We couldn't recognize a plant in this image. Please take a clearer photo.")
        st.write(f"**Message:** {result.get('problem', '')}")
        return

    st.success("✅ Analysis Complete!")
    
    # Key Info Card
    st.markdown(f"### 🌾 Crop: {result.get('plant_name', 'Unknown')}")
    st.markdown(f"### 🩺 Problem: {result.get('problem', 'Unknown')}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Confidence", result.get('confidence', 'N/A').title())
    with col2:
        st.metric("Severity", result.get('severity', 'N/A').title())

    # Text to Speech feature
    st.markdown("#### 🔊 Listen to Summary")
    summary_text = f"{result.get('plant_name')}. {result.get('problem')}. {', '.join(result.get('treatment_organic', []))}."
    audio_bytes = generate_audio(summary_text, language)
    if audio_bytes:
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.caption("Audio summary unavailable.")

    # Details
    st.markdown("#### 🔬 Symptoms Seen")
    for sym in result.get("symptoms", []):
        st.markdown(f"- {sym}")
        
    st.markdown("#### 🌱 Organic Treatments (Try First)")
    for tr in result.get("treatment_organic", []):
        st.markdown(f"✅ {tr}")
        
    st.markdown("#### 🧪 Chemical Treatments (Caution)")
    for ch in result.get("treatment_chemical", []):
        st.markdown(f"⚠️ {ch}")
        
    st.markdown("#### 🛡️ Prevention")
    for pr in result.get("prevention", []):
        st.markdown(f"- {pr}")

    st.info(f"👨‍🌾 **Expert Advice:** {result.get('expert_advice', '')}")
    
    # NEW FEATURE: WhatsApp Share Button
    st.markdown("#### 📲 Share with a Local Expert")
    wa_msg = f"Hello, I need help. My {result.get('plant_name')} crop has been diagnosed with {result.get('problem')}. Can you advise me?"
    wa_url = f"https://wa.me/?text={urllib.parse.quote(wa_msg)}"
    st.markdown(f"[**Click here to share via WhatsApp**]({wa_url})")

    if result.get("alternative_possibilities"):
        with st.expander("Other possibilities if confidence is low"):
            for alt in result.get("alternative_possibilities"):
                st.markdown(f"- {alt}")

    st.warning("Disclaimer: This is AI-generated guidance. Always verify with a local agricultural expert. Follow exact product label instructions for any chemicals.")

    # Download Report
    report_text = f"AgriLens Diagnosis Report\n-------------------------\n"
    report_text += f"Crop: {result.get('plant_name')}\nProblem: {result.get('problem')}\nSeverity: {result.get('severity', 'N/A').title()}\n\n"
    report_text += "Symptoms:\n" + "\n".join([f"- {s}" for s in result.get('symptoms', [])]) + "\n\n"
    report_text += "Organic Treatments:\n" + "\n".join([f"- {t}" for t in result.get('treatment_organic', [])]) + "\n\n"
    report_text += "Chemical Treatments:\n" + "\n".join([f"- {c}" for c in result.get('treatment_chemical', [])]) + "\n\n"
    report_text += f"Expert Advice:\n{result.get('expert_advice', '')}\n"
    
    st.download_button(
        label="📥 Download Report (.txt)",
        data=report_text,
        file_name="agrilens_report.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    # NEW FEATURE: Interactive Agronomist Chat
    st.divider()
    st.markdown("### 💬 Ask Follow-up Questions")
    st.caption("Ask the AI Agronomist for clarification on treatments, where to buy supplies, or disease details.")
    
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])
            
    if prompt := st.chat_input("E.g., How much water does this crop need now?"):
        # Display user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Call API
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_agronomist(prompt, result, language)
                st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
