import streamlit as st
from openai import OpenAI
import re

# --- Page Configuration ---
st.set_page_config(
    page_title="The Vibe Perfecter",
    page_icon="✨",
    layout="centered"
)

# --- UI Elements ---
st.title("✨ The Vibe Perfecter ✨")
st.markdown("Never send the wrong message again. Write your draft, pick your vibe, and send with confidence.")
st.divider()

# --- Main Form ---
with st.form("vibe_form"):
    original_text = st.text_area("1. Paste your draft message here:", height=150, placeholder="e.g., Why isn't this done yet? I need it.")
    
    selected_vibe = st.selectbox(
        "2. Choose the vibe you want to create:",
        (
            "Friendly & Casual",
            "Professional & Formal",
            "Firm but Polite",
            "Playful & Flirty",
            "Gently Disagreeing",
            "Enthusiastic & Excited",
            "Empathetic & Supportive"
        )
    )
    
    submitted = st.form_submit_button("✨ Perfect My Vibe ✨")

# --- Logic and API Call ---
if submitted:
    # Use the API key from Streamlit's secrets
    api_key = st.secrets.get("DEEPSEEK_API_KEY")

    if not api_key:
        st.error("API Key not found. This app has not been configured correctly by the owner.")
    elif not original_text:
        st.error("Please enter a draft message to perfect.")
    else:
        try:
            with st.spinner("Perfecting your vibe... Please wait."):
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

                prompt = f"""
                You are a "Vibe Perfecter". Rewrite the original text to match the desired vibe.
                Keep the core meaning but change the tone and phrasing.
                Provide three distinct, high-quality options.
                START EACH OPTION EXACTLY with the heading "### Option X:", where X is the option number.

                ---
                Original Text: "{original_text}"
                Desired Vibe: "{selected_vibe}"
                ---
                """

                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.7,
                )
                
                result = response.choices[0].message.content

            st.divider()
            st.success("Here are your perfected vibes!")
            
            options = re.split(r'### Option \d+:', result)
            for i, option in enumerate(options):
                if option.strip():
                    st.text_area(label=f"Option {i}", value=option.strip(), height=150)

        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- Footer ---
st.divider()
