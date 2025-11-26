# Newsy - Complete Meme Image Generator with Display
# Streamlit Frontend (NOW WITH ACTUAL IMAGE DISPLAY - NO EXTERNAL APPS NEEDED!)

import streamlit as st
import requests
import json
from datetime import datetime
from PIL import Image
from io import BytesIO
import base64

# Page Config
st.set_page_config(
    page_title="Newsy - Meme Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    :root {
        --color-primary: #208091;
        --color-background: #fcfcf9;
        --color-surface: #ffffff;
        --color-text: #134252;
    }
    
    .main {
        background-color: var(--color-background);
    }
    
    .stButton > button {
        background-color: var(--color-primary);
        color: white;
        width: 100%;
        padding: 12px;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        font-size: 16px;
    }
    
    .stButton > button:hover {
        background-color: #186b7d;
    }
    
    h1 {
        color: var(--color-text);
        font-size: 36px;
    }
    
    h2 {
        color: var(--color-text);
        font-size: 22px;
        margin-top: 30px;
    }
    
    .prompt-box {
        background: #f8f9fa;
        border-left: 4px solid #208091;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
        font-family: monospace;
        font-size: 12px;
        color: #333;
    }
    
    .success-badge {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🎨 Newsy - Meme Image Generator")
st.markdown("**Transform news articles into 2 viral meme images - Instantly!**")
st.markdown("✨ No external apps. No extra costs. Everything in one tool.")

# Sidebar Configuration
st.sidebar.title("⚙️ Configuration")
backend_url = st.sidebar.text_input(
    "Backend API URL",
    value="http://localhost:5000",
    help="Enter your Flask backend URL"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Supported Languages")
languages_info = {
    "🇬🇧 English": "en",
    "🇮🇳 Hindi": "hi",
    "🇮🇳 Tamil": "ta",
    "🇮🇳 Telugu": "te",
    "🇮🇳 Kannada": "ka",
    "🇮🇳 Malayalam": "ml",
    "🇮🇳 Marathi": "mr",
    "🇮🇳 Gujarati": "gu"
}
for lang_name in languages_info.keys():
    st.sidebar.markdown(f"• {lang_name}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Pro Tip")
st.sidebar.info("""
✅ **Everything happens here!**
- AI generates prompts
- Images generated locally (FREE)
- Text overlays added automatically
- Download & share instantly
""")

# Main Input Section
st.markdown("## 📥 Input Article")
col1, col2 = st.columns([3, 1])

with col1:
    article_url = st.text_input(
        "Article URL",
        placeholder="https://example.com/news-article",
        help="Enter the full URL of the news article"
    )

with col2:
    language = st.selectbox(
        "Output Language",
        options=list(languages_info.values()),
        format_func=lambda x: [k for k, v in languages_info.items() if v == x][0],
        help="Select the language for generated content"
    )

# Button Row
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    generate_btn = st.button("🎨 Generate 2 Meme Images", use_container_width=True, key="generate")
with col2:
    clear_btn = st.button("🔄 Clear", use_container_width=True, key="clear")
with col3:
    help_btn = st.button("❓ Guide", use_container_width=True, key="help")

# Initialize session state
if "content" not in st.session_state:
    st.session_state.content = None
if "loading" not in st.session_state:
    st.session_state.loading = False
if "error" not in st.session_state:
    st.session_state.error = None

# Handle Clear Button
if clear_btn:
    st.session_state.content = None
    st.session_state.error = None
    st.rerun()

# Handle Help Button
if help_btn:
    st.info("""
    ### 📖 How to Use Newsy:
    
    **What's New:**
    - ✅ Images are generated automatically in your tool
    - ✅ No need to open DALL-E or Midjourney
    - ✅ No API costs - everything is local
    - ✅ Download memes directly from this tool
    
    1. **Paste Article URL** - Any news article link
    2. **Select Language** - Choose your preferred language
    3. **Click Generate** - AI creates 2 complete meme images
    4. **Download & Share** - Save images directly to your device
    
    ### 🎨 What You Get:
    - ✅ Meme Image #1: Complete with text overlay
    - ✅ Meme Image #2: Different style with overlay
    
    ### 📊 Behind the Scenes:
    - Anthropic Claude: Summarizes article & creates concepts
    - PIL (Python): Generates images locally (FREE, NO API)
    - Pillow: Adds text overlays automatically
    
    **Result:** Professional meme images ready to post!
    """)

# Handle Generate Button
if generate_btn:
    if not article_url:
        st.error("❌ Please enter an article URL")
    else:
        st.session_state.loading = True
        try:
            with st.spinner("🔄 Analyzing article and generating complete meme images..."):
                # Prepare request
                payload = {
                    "url": article_url,
                    "language": language,
                    "timestamp": datetime.now().isoformat()
                }
                
                headers = {
                    "Content-Type": "application/json"
                }
                
                # Call Backend API
                response = requests.post(
                    f"{backend_url}/generate",
                    json=payload,
                    headers=headers,
                    timeout=60
                )
                
                if response.status_code == 200:
                    st.session_state.content = response.json()
                    st.session_state.error = None
                    st.session_state.loading = False
                    st.success("✅ Meme images generated successfully!")
                    st.rerun()
                else:
                    error_msg = response.json().get('error', 'Unknown error')
                    st.session_state.error = f"Error: {error_msg}"
                    st.session_state.loading = False
                    st.error(st.session_state.error)
                    
        except requests.exceptions.ConnectionError:
            st.session_state.error = "❌ Cannot connect to backend. Ensure Flask server is running at " + backend_url
            st.session_state.loading = False
            st.error(st.session_state.error)
        except Exception as e:
            st.session_state.error = f"❌ Error: {str(e)}"
            st.session_state.loading = False
            st.error(st.session_state.error)

# Display Generated Content
if st.session_state.content:
    content = st.session_state.content
    
    # Success message
    st.markdown('<div class="success-badge">✨ Meme images generated successfully and ready to download!</div>', unsafe_allow_html=True)
    
    # Article Summary
    st.markdown("## 📋 Article Analysis")
    summary = content.get("summary", {})
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📰 Headline", summary.get("headline", "N/A")[:50])
    with col2:
        st.metric("😊 Emotional Angle", summary.get("emotional_angle", "N/A"))
    
    st.write(f"**Description:** {summary.get('description', 'No description available')}")
    
    # Meme Images Section
    st.markdown("## 🖼️ Generated Meme Images (2)")
    
    meme_images = content.get("meme_images", [])
    
    if len(meme_images) >= 2:
        # Meme Image 1
        st.markdown("### Meme Image #1")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            img1 = meme_images[0]
            
            # Display image
            if img1.get('image_base64'):
                try:
                    img_data = base64.b64decode(img1.get('image_base64'))
                    image = Image.open(BytesIO(img_data))
                    st.image(image, use_column_width=True, caption=img1.get('style'))
                except Exception as e:
                    st.warning(f"Could not display image: {e}")
            
            # Download button
            if img1.get('image_base64'):
                st.download_button(
                    label="📥 Download Meme #1 (PNG)",
                    data=base64.b64decode(img1.get('image_base64')),
                    file_name=f"newsy_meme_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    use_container_width=True
                )
        
        with col2:
            st.markdown("**Details:**")
            st.markdown(f"**Style:** {img1.get('style')}")
            st.markdown(f"**Overlay:** `{img1.get('text_overlay')}`")
        
        st.markdown("**AI Concept Prompt:**")
        st.markdown(f'<div class="prompt-box">{img1.get("ai_prompt")}</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Meme Image 2
        st.markdown("### Meme Image #2")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            img2 = meme_images[1]
            
            # Display image
            if img2.get('image_base64'):
                try:
                    img_data = base64.b64decode(img2.get('image_base64'))
                    image = Image.open(BytesIO(img_data))
                    st.image(image, use_column_width=True, caption=img2.get('style'))
                except Exception as e:
                    st.warning(f"Could not display image: {e}")
            
            # Download button
            if img2.get('image_base64'):
                st.download_button(
                    label="📥 Download Meme #2 (PNG)",
                    data=base64.b64decode(img2.get('image_base64')),
                    file_name=f"newsy_meme_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    use_container_width=True
                )
        
        with col2:
            st.markdown("**Details:**")
            st.markdown(f"**Style:** {img2.get('style')}")
            st.markdown(f"**Overlay:** `{img2.get('text_overlay')}`")
        
        st.markdown("**AI Concept Prompt:**")
        st.markdown(f'<div class="prompt-box">{img2.get("ai_prompt")}</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Export Options
        st.markdown("## 📤 More Options")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 View Full Response (JSON)", use_container_width=True):
                st.json(content)
        
        with col2:
            if st.button("🔄 Generate Again with Same Article", use_container_width=True):
                st.info("👉 Click 'Generate 2 Meme Images' button above to create different variations!")
    
    else:
        st.warning("⚠️ Unable to generate complete meme images. Try again.")

else:
    if not st.session_state.loading:
        st.info("👈 Enter an article URL and select language to generate complete meme images instantly!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #626c7c; font-size: 12px;'>
    ✨ Newsy Complete Meme Image Generator v2.0<br/>
    <b>AI-Powered Meme Generation - 100% Local, 100% FREE</b><br/>
    No DALL-E costs. No Midjourney fees. No external apps needed.<br/>
    Built for news publishers & content creators
</div>
""", unsafe_allow_html=True)
