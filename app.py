import streamlit as st
from openai import OpenAI
import time

# --- 1. НАСТРОЙКИ (Лимиты) ---
# Обязательно должно быть первой командой
st.set_page_config(page_title="Mystic Oracle AI", page_icon="🔮", layout="centered")

MAX_FREE_READINGS = 3  # Сколько раз можно гадать бесплатно за один заход

# --- 2. CSS СТИЛИ (PREMIUM LOOK) ---
st.markdown("""
    <style>
    /* Подключаем красивый шрифт */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato&display=swap');
    
    /* Основной фон (Мистический градиент) */
    .stApp {
        background: radial-gradient(circle at center, #1a0b2e 0%, #000000 100%);
        color: #e0d2b4; /* Цвет шампанского */
        font-family: 'Lato', sans-serif;
    }
    
    /* Заголовки */
    h1, h2 {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        text-align: center;
    }
    
    /* Поля ввода (Инпуты) - делаем их заметными */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.1);
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

    /* Блок результата */
    .result-box {
        background: rgba(0,0,0,0.6);
        border: 1px solid #9370DB;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    
    /* Скрываем лишнее от Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. ИНИЦИАЛИЗАЦИЯ API ---
try:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url="https://api.vsegpt.ru/v1"
    )
except:
    st.error("⚠️ Ошибка: Нет API ключа. Проверь Secrets.")
    st.stop()

# Инициализация счетчика гаданий
if 'readings_count' not in st.session_state:
    st.session_state['readings_count'] = 0

# --- 4. ИНТЕРФЕЙС (ЦЕНТР ЭКРАНА) ---

st.title("🌌 Mystic Oracle")
st.markdown("<p style='text-align: center; opacity: 0.8;'>Ask the cards, and the truth shall be revealed...</p>", unsafe_allow_html=True)

# Проверка лимита
if st.session_state['readings_count'] >= MAX_FREE_READINGS:
    st.error("🌙 Your spiritual energy is drained for now.")
    st.markdown("""
        <div style="text-align: center; padding: 20px; border: 1px solid #FFD700; border-radius: 10px; background: rgba(0,0,0,0.5);">
            <h3>Want Unlimited Answers?</h3>
            <p>The AI sees shadows, but a Master Psychic sees faces.</p>
            <br>
            <a href="https://google.com" target="_blank" style="text-decoration: none;">
                <button style="background: #FFD700; color: black; border: none; padding: 12px 24px; font-weight: bold; font-size: 16px; border-radius: 5px; cursor: pointer;">
                    Talk to a Real Psychic (Live) ➤
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

else:
    # Поля ввода (БЕЗ сайдбара, сразу на экране)
    # Добавил Знак Зодиака — людям это нравится
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("Your Name", placeholder="e.g. Sarah")
    with col2:
        zodiac = st.selectbox("Zodiac Sign", ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])

    question = st.text_area("Your Question", height=100, placeholder="Will he come back? What is my destiny?")
    
    spread_type = st.selectbox("Select Ritual", 
            ["One Card (Daily Advice)", "❤️ Love & Relationships", "💰 Career & Future", "🔮 Celtic Cross (Deep Reading)"])

    # --- 5. ЛОГИКА ГАДАНИЯ ---
    if st.button("👁️ REVEAL MY FATE"):
        if not question or not user_name:
            st.warning("⚠️ The spirits need your Name and Question.")
        else:
            # Увеличиваем счетчик
            st.session_state['readings_count'] += 1
            
            # Анимация
            progress_text = "Shuffling the ancient deck..."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text="Connecting to Astral Plane...")
            my_bar.empty()

            try:
                # Промпт для ИИ
                system_msg = "You are a mystical Tarot Reader. Use tarot emojis. Tone: Mysterious, slightly dark but empowering. Structure: 1. The Cards Drawn. 2. Deep Interpretation. 3. Direct Advice. Keep it concise."
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
                
                # Вывод результата в красивой рамке
                st.markdown(f"<div class='result-box'>{prediction.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
                
                st.markdown("---")
                
                # МОНЕТИЗАЦИЯ (Кнопка внизу)
                st.info("💡 The cards reveal a hidden path...")
                st.markdown("""
                <div style="text-align: center;">
                    <a href="https://google.com" target="_blank">
                        <button style="background: #228B22; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 5px; cursor: pointer;">
                            👁️ Chat with a Real Psychic Now
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True) # Сюда потом вставишь партнерку

            except Exception as e:
                st.error("The cosmic connection was interrupted. Try again.")
