import streamlit as st
from openai import OpenAI
import time

# --- 1. НАСТРОЙКИ СТРАНИЦЫ ---
# Эта команда должна быть самой первой!
st.set_page_config(page_title="Mystic Oracle AI", page_icon="🔮", layout="centered")

# ЗАЩИТА БЮДЖЕТА: 3 бесплатных гадания на сессию
MAX_FREE_READINGS = 3

# --- 2. ДИЗАЙН (LUXURY DARK THEME) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato&display=swap');
    
    /* Фон: Глубокий космос */
    .stApp {
        background: radial-gradient(circle at center, #1a0b2e 0%, #000000 100%);
        color: #e0d2b4;
        font-family: 'Lato', sans-serif;
    }
    
    /* Заголовки: Золото */
    h1, h2, h3 {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        text-align: center;
    }
    
    /* Поля ввода: Полупрозрачные */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea, 
    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        border: 1px solid #FFD700;
        border-radius: 8px;
    }
    
    /* Главная кнопка */
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #DAA520, #B8860B);
        border: none;
        color: black;
        padding: 15px;
        font-family: 'Cinzel', serif;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(218, 165, 32, 0.5);
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.8);
    }

    /* Блок с предсказанием */
    .result-box {
        background: rgba(0,0,0,0.7);
        border: 1px solid #9370DB;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 0 20px rgba(147, 112, 219, 0.2);
    }
    
    /* Скрываем футер Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. ПОДКЛЮЧЕНИЕ VSEGPT API ---
try:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url="https://api.vsegpt.ru/v1"
    )
except Exception:
    st.error("⚠️ API Key Error. Check Streamlit Secrets.")
    st.stop()

# Счетчик попыток
if 'readings_count' not in st.session_state:
    st.session_state['readings_count'] = 0

# --- 4. ИНТЕРФЕЙС ---

st.title("🌌 Mystic Oracle")
st.markdown("<p style='text-align: center; opacity: 0.8; margin-bottom: 30px;'>The cards reveal what is hidden...</p>", unsafe_allow_html=True)

# Если лимит исчерпан -> Отправляем на гороскоп (Moon Reading)
if st.session_state['readings_count'] >= MAX_FREE_READINGS:
    st.error("🌙 Your energy is drained.")
    st.markdown("""
        <div style="text-align: center; padding: 20px; border: 1px solid #FFD700; border-radius: 10px; background: rgba(0,0,0,0.5);">
            <h3 style="color: #FFD700;">Unlock Your Full Destiny</h3>
            <p>Don't stop now. The stars have a personal message for you.</p>
            <br>
            <a href="https://a.moonmystical.com/optin1724860719225#aff=fadapulb1f6" target="_blank">
                <button style="background: #FFD700; color: black; border: none; padding: 12px 24px; font-weight: bold; font-size: 16px; border-radius: 5px; cursor: pointer;">
                    Watch Your Personal Reading (Video) ➤
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

else:
    # Поля ввода
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("Your Name", placeholder="e.g. Sarah")
    with col2:
        zodiac = st.selectbox("Zodiac Sign", ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])

    question = st.text_area("Your Question", height=100, placeholder="Will he come back? Who is my soulmate?")
    
    spread_type = st.selectbox("Select Ritual", 
            ["One Card (Daily Advice)", "❤️ Love & Relationships", "💰 Career & Future", "🔮 Celtic Cross (Deep Reading)"])

    # --- 5. ЛОГИКА ГАДАНИЯ ---
    if st.button("👁️ REVEAL MY FATE"):
        if not question or not user_name:
            st.warning("⚠️ The spirits need your Name and Question to connect.")
        else:
            st.session_state['readings_count'] += 1
            
            # Анимация
            progress_text = "Connecting to the Astral Plane..."
            my_bar = st.progress(0, text=progress_text)
            
            steps = [
                (20, "Shuffling the ancient deck..."),
                (45, "Channeling your energy..."),
                (70, "Revealing hidden truths..."),
                (100, "The cards have spoken.")
            ]
            
            for percent, label in steps:
                time.sleep(0.4)
                my_bar.progress(percent, text=label)
            my_bar.empty()

            try:
                # Промпт (БЕЗ слова Cliffhanger)
                system_msg = (
                    "You are a mystical Tarot Reader. Use tarot emojis. "
                    "Structure your response strictly as a continuous narrative:\n"
                    "1. Reveal the cards drawn.\n"
                    "2. Interpret their deep meaning specifically for the user's situation.\n"
                    "3. End with a mysterious warning about a specific hidden influence or person coming soon, "
                    "but mention that the vision is 'clouded' and needs a special medium to fully reveal.\n"
                    "CRITICAL: Do NOT use labels like 'Cliffhanger', 'Intrigue', or 'Conclusion'. "
                    "Write naturally."
                )
                user_msg = f"Querent: {user_name}, Zodiac: {zodiac}. Question: {question}. Spread: {spread_type}."

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    temperature=0.7
                )
                
                prediction = response.choices[0].message.content
                
                # Вывод текста
                st.markdown(f"<div class='result-box'>{prediction.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
                st.markdown("---")
                
                # --- 💰 УМНАЯ МОНЕТИЗАЦИЯ (ТВОИ ЛИЧНЫЕ ССЫЛКИ) ---
                
                # 1. Ссылка на Рисунок (Soulmate)
                LINK_SOULMATE = "https://www.soulmatesketch.com/2-01721767000544#aff=fadapulb1f6"
                
                # 2. Ссылка на Гороскоп (Moon Reading)
                LINK_MOON = "https://a.moonmystical.com/optin1724860719225#aff=fadapulb1f6"
                
                # Определяем тему вопроса
                text_to_check = (spread_type + " " + question).lower()
                is_love = any(word in text_to_check for word in ['love', 'relationship', 'heart', 'marriage', 'ex', 'crush', 'husband', 'wife', 'him', 'boyfriend', 'girlfriend', 'soulmate'])

                if is_love:
                    # Показываем Рисунок
                    offer_link = LINK_SOULMATE
                    btn_text = "😍 Reveal Your Future Soulmate's Face (View Sketch)"
                    offer_desc = "The cards show a specific person coming towards you... Want to see their face?"
                    btn_style = "background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%); color: #333;"
                else:
                    # Показываем Гороскоп
                    offer_link = LINK_MOON
                    btn_text = "🌙 Watch Your Personal Moon Reading (Video)"
                    offer_desc = "Your date of birth holds a secret code. Unlock your destiny video now."
                    btn_style = "background: linear-gradient(90deg, #2b5876 0%, #4e4376 100%); color: white;"

                # Отрисовка кнопки
                st.info(f"💡 {offer_desc}")
                st.markdown(f"""
                <div style="text-align: center; margin-top: 15px;">
                    <a href="{offer_link}" target="_blank">
                        <button style="{btn_style} border: none; padding: 16px 32px; font-weight: bold; border-radius: 50px; cursor: pointer; font-size: 18px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); transition: transform 0.2s; width: 100%;">
                            {btn_text} ➤
                        </button>
                    </a>
                    <p style="font-size: 12px; margin-top: 10px; opacity: 0.6;">*Limited time offer for Mystic Oracle users</p>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Cosmic Connection Error: {e}")
