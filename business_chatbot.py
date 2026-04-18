import streamlit as st
from groq import Groq
import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ============================================
# EDIT THIS SECTION FOR EACH CLIENT
# ============================================
BUSINESS_NAME = "Pizza Palace"
BUSINESS_INFO = """
You are a helpful customer support assistant for Pizza Palace.

About us:
- We are a pizza restaurant in Lahore, Pakistan
- Open: Every day 11am to 11pm
- Phone: 0300-1234567
- Address: 23 Main Boulevard, Gulberg, Lahore

Our Menu:
- Margherita Pizza: Rs. 800 (small), Rs. 1400 (large)
- BBQ Chicken Pizza: Rs. 950 (small), Rs. 1600 (large)
- Pepperoni Pizza: Rs. 900 (small), Rs. 1500 (large)
- Garlic Bread: Rs. 300
- Soft Drinks: Rs. 150

Delivery:
- Free delivery on orders above Rs. 1500
- Delivery time: 30-45 minutes
- We deliver within 5km radius

Rules:
- Always be polite and friendly
- If you don't know something, say "Please call us at 0300-1234567"
- Never make up information not listed above
- Answer in the same language the customer uses (Urdu or English)
"""
# ============================================

st.set_page_config(page_title=f"{BUSINESS_NAME} Support", page_icon="🍕")
st.title(f"🍕 {BUSINESS_NAME}")
st.caption("Chat with us — we reply instantly!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hello! Welcome to {BUSINESS_NAME}. How can I help you today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask about our menu, delivery, or hours...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Build messages with system prompt
    api_messages = [{"role": "system", "content": BUSINESS_INFO}]
    api_messages += st.session_state.messages

    # Use Groq model (NOT gpt-3.5-turbo)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Groq's free model
        messages=api_messages
    )

    ai_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.write(ai_reply)
