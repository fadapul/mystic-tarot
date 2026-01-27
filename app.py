import streamlit as st
from openai import OpenAI

# 1. Настройка страницы (Должна быть самой первой строчкой)
st.set_page_config(page_title="Mystic AI Tarot", page_icon="🔮", layout="centered")

# 2. Подключение к VseGPT (через Secrets)
try:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url="https://api.vsegpt.ru/v1"
    )
except Exception:
    st.error("⚠️ API Key missing. Please check Streamlit Secrets.")
    st.stop()

# 3. Дизайн (Темная тема CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #262730; 
        color: white;
    }
    /* Стиль главной кнопки */
    .stButton > button {
        width: 100%;
        background-color: #4B0082;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: 1px solid #8A2BE2;
    }
    .stButton > button:hover {
        background-color: #6A0DAD;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Боковая панель (Настройки)
# Интерфейс на АНГЛИЙСКОМ, так как рынок США
with st.sidebar:
    st.title("🔮 Tarot Settings")
    user_name = st.text_input("Your Name", "Stranger")
    question = st.text_area("Your Question", height=100, placeholder="Will he come back? What is my destiny?")
    spread_type = st.selectbox("Select Spread", 
        ["One Card (Daily Advice)", "Love & Relationships", "Past / Present / Future", "Celtic Cross"])
    
    st.markdown("---")
    st.caption("Mystic AI Tarot v1.0")

# 5. Основной экран
st.title("🌌 Mystic AI Tarot Reader")
st.write("Focus on your question and ask the spirits...")

# Логика гадания
if st.button("✨ Reveal My Fate ✨"):
    if not question:
        st.warning("The spirits are silent... Please enter your question in the sidebar.")
    else:
        with st.spinner("Shuffling the deck... Connecting to the Astral Plane..."):
            try:
                # Промпт для ИИ (на английском)
                system_msg = "You are a mystical, empathetic Tarot Reader. Use tarot emojis. Be mysterious but helpful. Structure: 1. The Cards. 2. Interpretation. 3. Advice."
                user_msg = f"Querent: {user_name}. Question: {question}. Spread: {spread_type}. Do a reading."

                # ПРАВИЛЬНЫЙ запрос для модели gpt-4o-mini
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    temperature=0.7
                )
                
                prediction = response.choices[0].message.content
                
                # Вывод результата
                st.success("The cards have been drawn!")
                st.markdown("### 🔮 Your Reading:")
                st.write(prediction)
                st.markdown("---")
                
                # 6. МОНЕТИЗАЦИЯ (Кнопка)
                st.info("Need a deeper reading from a real master?")
                # Ссылку https://google.com заменишь на свою партнерскую позже
                st.link_button("👁️ Talk to a Real Psychic Now (Live Chat)", "https://google.com") 

            except Exception as e:
                st.error(f"Magical Error: {e}")
