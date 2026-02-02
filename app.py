import streamlit as st
from openai import OpenAI
import time

# --- 1. НАСТРОЙКИ (ЭКОНОМИЯ ТОКЕНОВ) ---
st.set_page_config(page_title="Mystic Oracle AI", page_icon="🔮", layout="centered")

# Лимит слов в ответе (чтобы ИИ не писал мемуары за твой счет)
MAX_RESPONSE_TOKENS = 300 

# Лимит бесплатных гаданий на одного человека (защита от скликивания)
MAX_FREE_READINGS = 3

# --- 2. ДИЗАЙН (Dark Mode) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato&display=swap');
    .stApp { background: radial-gradient(circle at center, #1a0b2e 0%, #000000 100%); color: #e0d2b4; font-family: 'Lato', sans-serif; }
    h1, h2, h3 { font-family: 'Cinzel', serif; color: #FFD700; text-align: center; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5); }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div { background-color: rgba(255, 255, 255, 0.05); color: #ffffff; border: 1px solid #FFD700; border-radius: 8px; }
    .stButton > button { width: 100%; background: linear-gradient(45deg, #DAA520, #B8860B); border: none; color: black; padding: 15px; font-family: 'Cinzel', serif; font-size: 20px; font-weight: bold; border-radius: 10px; transition: all 0.3s; }
    .stButton > button:hover { transform: scale(1.02); box-shadow: 0 0 25px rgba(255, 215, 0, 0.8); }
    .result-box { background: rgba(0,0,0,0.7); border: 1px solid #9370DB; padding: 20px; border-radius: 10px; margin-top: 20px; font-size: 16px; line-height: 1.6; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. API VSEGPT ---
try:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url="https://api.vsegpt.ru/v1"
    )
except Exception:
    st.error("⚠️ API Key Error.")
    st.stop()

if 'readings_count' not in st.session_state:
    st.session_state['readings_count'] = 0

# --- 4. ИНТЕРФЕЙС ---
st.title("🌌 Mystic Oracle")

# Если лимит исчерпан -> Отправляем покупать
if st.session_state['readings_count'] >= MAX_FREE_READINGS:
    st.error("🌙 Your energy is drained.")
    st.markdown("""
        <div style="text-align: center; padding: 20px; border: 1px solid #FFD700; border-radius: 10px; background: rgba(0,0,0,0.5);">
            <h3 style="color: #FFD700;">Unlock Destiny</h3>
            <p>Don't stop now. The stars have a personal message for you.</p>
            <a href="https://a.moonmystical.com/optin1724860719225#aff=fadapulb1f6" target="_blank">
                <button style="background: #FFD700; color: black; border: none; padding: 12px 24px; font-weight: bold; border-radius: 5px; cursor: pointer;">Watch Personal Video ➤</button>
            </a>
        </div>
    """, unsafe_allow_html=True)
else:
    col1, col2 = st.columns(2)
    with col1: user_name = st.text_input("Name", placeholder="Name")
    with col2: zodiac = st.selectbox("Sign", ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])
    question = st.text_area("Question", height=100, placeholder="Will he come back?")
    spread = st.selectbox("Spread", ["Daily Advice", "❤️ Love", "💰 Future", "🔮 Celtic Cross"])

    if st.button("👁️ REVEAL FATE"):
        if not question or not user_name:
            st.warning("⚠️ Enter Name & Question")
        else:
            st.session_state['readings_count'] += 1
            
            # Анимация (Бесплатно, без запросов)
            my_bar = st.progress(0, text="Connecting...")
            for p, t in [(30, "Shuffling..."), (60, "Reading stars..."), (100, "Done.")]:
                time.sleep(0.3)
                my_bar.progress(p, text=t)
            my_bar.empty()

            try:
                # --- ЭКОНОМНЫЙ ПРОМПТ (Сжат до минимума) ---
                # Мы НЕ передаем историю сообщений. Только текущую инструкцию.
                system_prompt = (
                    "Role: Mystic Tarot Reader. "
                    "Task: Short, dark, mysterious reading with emojis. "
                    "Structure: 1.Cards. 2.Meaning. 3.Warning about a person/event. "
                    "Tone: Serious. No labels. Max 150 words."
                )
                user_prompt = f"User: {user_name}, {zodiac}. Q: {question}. Context: {spread}."

                # ЗАПРОС (Создаем "Новый чат" каждый раз)
                response = client.chat.completions.create(
                    model="gpt-4o-mini", # Самая дешевая модель
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=MAX_RESPONSE_TOKENS, # Обрезаем длину ответа для экономии
                    temperature=0.7
                )
                
                prediction = response.choices[0].message.content
                st.markdown(f"<div class='result-box'>{prediction.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
                st.markdown("---")
                
                # --- ОФФЕРЫ (DIGISTORE24) ---
                LINK_SOULMATE = "https://www.soulmatesketch.com/2-01721767000544#aff=fadapulb1f6"
                LINK_MOON = "https://a.moonmystical.com/optin1724860719225#aff=fadapulb1f6"
                
                is_love = any(w in (spread+question).lower() for w in ['love','ex','him','marry','heart'])
                
                if is_love:
                    link, txt, style = LINK_SOULMATE, "😍 See His Face (Sketch)", "background: linear-gradient(90deg, #ff9a9e, #fecfef); color: #333;"
                else:
                    link, txt, style = LINK_MOON, "🌙 Watch Personal Reading", "background: linear-gradient(90deg, #2b5876, #4e4376); color: white;"

                st.markdown(f"""
                <div style="text-align: center; margin-top: 15px;">
                    <a href="{link}" target="_blank"><button style="{style} border: none; padding: 16px 32px; font-weight: bold; border-radius: 50px; cursor: pointer; width: 100%; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">{txt} ➤</button></a>
                </div>""", unsafe_allow_html=True)

            except Exception as e:
                st.error("Connection Error. Try again.")
