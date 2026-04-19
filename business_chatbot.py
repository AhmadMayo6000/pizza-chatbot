import streamlit as st
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ============================================
# HANAN MAYO PIZZA - CUSTOMER SUPPORT CHATBOT
# ============================================
BUSINESS_NAME = "Hanan Mayo Pizza"
BUSINESS_TAGLINE = "Fresh & Delicious Pizza!"
BUSINESS_EMOJI = "🍕"
THEME_COLOR = "#FF6B35"  # Warm orange-red, perfect for pizza
BUSINESS_INFO = """
You are a helpful customer support assistant for Hanan Mayo Pizza.

About us:
- We are Hanan Mayo Pizza, serving delicious fresh pizza
- Open: Every day 11am to 11pm
- Phone: [YOUR-PHONE-NUMBER]
- Address: [YOUR-ADDRESS]

Our Menu:
- Mayo Special Pizza: Rs. 850 (small), Rs. 1500 (large)
- Chicken Fajita Pizza: Rs. 950 (small), Rs. 1600 (large)
- Pepperoni Pizza: Rs. 900 (small), Rs. 1500 (large)
- Veggie Delight Pizza: Rs. 800 (small), Rs. 1400 (large)
- Garlic Bread with Cheese: Rs. 350
- Soft Drinks: Rs. 150

Delivery:
- Free delivery on orders above Rs. 1500
- Delivery time: 30-45 minutes
- We deliver within 5km radius

Rules:
- Always be polite and friendly
- Keep answers short and clear
- If you don't know something, say "Please call us at [YOUR-PHONE-NUMBER]"
- Never make up information not listed above
- Answer in the same language the customer uses (Urdu or English)
- Always end with a helpful follow-up question
"""
# ============================================

# Page config
st.set_page_config(
    page_title=f"{BUSINESS_NAME} — AI Assistant",
    page_icon=BUSINESS_EMOJI,
    layout="centered"
)

# Custom CSS
st.markdown(f"""
<style>
    /* Hide streamlit default elements */
    #MainMenu, footer, header {{visibility: hidden;}}
    .block-container {{padding-top: 0rem;}}

    /* Header */
    .header {{
        background: linear-gradient(135deg, {THEME_COLOR}, #ff4757);
        padding: 28px 24px;
        border-radius: 0 0 24px 24px;
        margin-bottom: 24px;
        text-align: center;
        color: white;
    }}
    .header h1 {{
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }}
    .header p {{
        font-size: 14px;
        margin: 6px 0 0;
        opacity: 0.9;
    }}
    .online-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255,255,255,0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin-top: 10px;
    }}
    .dot {{
        width: 8px; height: 8px;
        background: #00ff88;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0%, 100% {{opacity: 1;}}
        50% {{opacity: 0.4;}}
    }}

    /* Quick buttons */
    .quick-btn {{
        display: inline-block;
        background: white;
        border: 1.5px solid {THEME_COLOR};
        color: {THEME_COLOR};
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        margin: 3px;
        cursor: pointer;
        font-weight: 500;
    }}

    /* Info cards */
    .info-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 10px;
        margin: 16px 0;
    }}
    .info-card {{
        background: white;
        border: 0.5px solid #eee;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
    }}
    .info-card .icon {{font-size: 20px; margin-bottom: 4px;}}
    .info-card .label {{font-size: 11px; color: #888; margin-bottom: 2px;}}
    .info-card .value {{font-size: 13px; font-weight: 600; color: #222;}}
</style>

<div class="header">
    <div style="font-size:40px; margin-bottom:8px;">{BUSINESS_EMOJI}</div>
    <h1>{BUSINESS_NAME}</h1>
    <p>{BUSINESS_TAGLINE}</p>
    <div class="online-badge">
        <div class="dot"></div>
        AI Assistant Online 24/7
    </div>
</div>

<div class="info-grid">
    <div class="info-card">
        <div class="icon">🕐</div>
        <div class="label">Open Today</div>
        <div class="value">11am – 11pm</div>
    </div>
    <div class="info-card">
        <div class="icon">🛵</div>
        <div class="label">Delivery</div>
        <div class="value">30–45 mins</div>
    </div>
    <div class="info-card">
        <div class="icon">📞</div>
        <div class="label">Call Us</div>
        <div class="value">[YOUR-PHONE-NUMBER]</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick question buttons
st.markdown("**Quick questions:**")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🍕 Menu"):
        st.session_state.quick = "What pizzas do you have?"
with col2:
    if st.button("🛵 Delivery"):
        st.session_state.quick = "How does delivery work?"
with col3:
    if st.button("💰 Prices"):
        st.session_state.quick = "What are your prices?"
with col4:
    if st.button("🕐 Hours"):
        st.session_state.quick = "What are your opening hours?"

st.divider()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"👋 Welcome to {BUSINESS_NAME}! I'm your AI assistant. Ask me about our menu, delivery, prices, or hours. How can I help you today?"}
    ]

# Handle quick buttons
if "quick" in st.session_state:
    st.session_state.messages.append({"role": "user", "content": st.session_state.quick})
    del st.session_state.quick

# Show messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Get AI response for last user message if needed
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner(""):
            api_messages = [{"role": "system", "content": BUSINESS_INFO}]
            api_messages += st.session_state.messages

            response = client.chat.completions.create(
               model="llama-3.3-70b-versatile",
                messages=api_messages
            )
            ai_reply = response.choices[0].message.content
            st.write(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# Chat input
user_input = st.chat_input(f"Ask {BUSINESS_NAME} anything...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# Footer
st.markdown("""
<div style='text-align:center; color:#aaa; font-size:12px; margin-top:30px; padding:16px;'>
    Powered by AI • Available 24/7 • Response time under 3 seconds
</div>
""", unsafe_allow_html=True)
