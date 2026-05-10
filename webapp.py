import streamlit as st
import cv2
import time
import os
import base64
from engine import CatoEngine
import streamlit.components.v1 as components
   
# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Meme Factory", layout="wide")

def get_img_64(path):
    """ฟังก์ชันสำหรับแปลงไฟล์รูปภาพเป็น Base64 เพื่อแสดงผลใน HTML"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def play_bg_music(file_path):
    try:
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        # components.html รัน <script> ได้จริง ต่างจาก st.markdown
        html_code = f"""
            <script>
            (function() {{
                if (window.parent._bgAudio) return;
                
                var audio = new Audio("data:audio/mp3;base64,{b64}");
                audio.loop = true;
                audio.volume = 0.4;
                window.parent._bgAudio = audio;
                
                var playPromise = audio.play();
                if (playPromise !== undefined) {{
                    playPromise.catch(function() {{
                        var unlockAudio = function() {{
                            audio.play();
                            window.parent.document.removeEventListener('click', unlockAudio);
                            window.parent.document.removeEventListener('keydown', unlockAudio);
                        }};
                        // ผูกกับ parent document เพราะ components.html อยู่ใน iframe
                        window.parent.document.addEventListener('click', unlockAudio);
                        window.parent.document.addEventListener('keydown', unlockAudio);
                    }});
                }}
            }})();
            </script>
        """
        # height=0 เพื่อไม่ให้กินพื้นที่หน้าจอ
        components.html(html_code, height=0)
        
    except FileNotFoundError:
        st.error(f"❌ ไม่พบไฟล์เพลงที่: {file_path}")

play_bg_music(r"song\music_Kiko.mp3")
        
# CSS ส่วนกลาง 
st.markdown("""     
    <style>

    /* -----------------------------
    🌸 COLOR PALETTE
    ------------------------------*/
    :root {
        --growing-pink: #CB748E;
        --sleeping-pink: #D698AB;
        --shy-pink: #EED4DB;

        --tulip-green: #73986F;
        --ground-green: #426E55;
        --sleeping-green: #2D4839;

        --white-soft: #fffafc;
    }

    /* -----------------------------
    🌸 MAIN BACKGROUND
    ------------------------------*/
    .stApp {
        background: linear-gradient(
            180deg,
            #fdf3f6 0%,
            #f8e7ec 35%,
            #eef4ee 100%
        ) !important;

        overflow-x: hidden;
    }

    /* -----------------------------
    🌸 HIDE STREAMLIT DEFAULT UI
    ------------------------------*/
    #MainMenu,
    footer,
    header,
    .stAppDeployButton,
    [data-testid="collapsedControl"],
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* -----------------------------
    🌸 MAIN CONTAINER
    ------------------------------*/
    .main .block-container {
        max-width: 1000px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    /* -----------------------------
    🌸 TITLES
    ------------------------------*/
    h1, h2, h3, .stTitle {
        color: var(--ground-green) !important;
        font-weight: 900 !important;
        letter-spacing: 1px;
        text-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }

    /* -----------------------------
    🌸 FORM CARD
    ------------------------------*/
    div[data-testid="stForm"] {

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.95),
                rgba(255,248,250,0.92)
            ) !important;

        border: 3px solid rgba(203,116,142,0.25) !important;

        border-radius: 35px !important;

        padding:
            130px 40px 40px 40px !important;

        margin-top: 90px !important;

        position: relative !important;

        box-shadow:
            0 15px 40px rgba(203,116,142,0.18),
            0 4px 10px rgba(0,0,0,0.05);

        backdrop-filter: blur(10px);

        overflow: visible !important;

        transition: all 0.3s ease;
    }

    /* Hover form */
    div[data-testid="stForm"]:hover {
        transform: translateY(-2px);
        box-shadow:
            0 18px 45px rgba(203,116,142,0.25),
            0 6px 14px rgba(0,0,0,0.08);
    }

    /* -----------------------------
    🌸 CAT IMAGE
    ------------------------------*/
    .cat-staff-position {
        text-align: center;
        position: relative;
        z-index: 10;
        margin-bottom: -105px;
    }

    .cat-staff-position img {

        width: 390px !important;

        border-radius: 28px !important;

        border: 6px solid rgba(255,255,255,0.95);

        box-shadow:
            0 12px 35px rgba(0,0,0,0.15),
            0 4px 12px rgba(203,116,142,0.2);

        transition: all 0.35s ease-in-out;

        background: white;
    }

    .cat-staff-position img:hover {
        transform:
            scale(1.04)
            rotate(-1.5deg);

        box-shadow:
            0 18px 45px rgba(203,116,142,0.35);

        cursor: pointer;
    }

    /* -----------------------------
    🌸 BUTTONS
    ------------------------------*/
    div.stButton > button {

        background: linear-gradient(
            135deg,
            var(--growing-pink),
            var(--sleeping-pink)
        ) !important;

        color: white !important;

        border: none !important;

        border-radius: 18px !important;

        padding: 0.8rem 1.4rem !important;

        font-size: 18px !important;

        font-weight: 700 !important;

        box-shadow:
            0 8px 20px rgba(203,116,142,0.25);

        transition: all 0.25s ease-in-out;
    }

    div.stButton > button:hover {

        transform:
            translateY(-3px)
            scale(1.03);

        background: linear-gradient(
            135deg,
            #d97e9a,
            #e3a8b7
        ) !important;

        box-shadow:
            0 12px 24px rgba(203,116,142,0.35);
    }

    /* -----------------------------
    🌸 INPUT BOX
    ------------------------------*/
    .stTextInput input {

        background: rgba(255,255,255,0.85) !important;

        border: 2px solid rgba(203,116,142,0.2) !important;

        border-radius: 18px !important;

        padding: 14px !important;

        color: var(--ground-green) !important;

        font-size: 16px !important;

        transition: all 0.25s ease;
    }

    .stTextInput input:focus {

        border: 2px solid var(--growing-pink) !important;

        box-shadow:
            0 0 0 5px rgba(203,116,142,0.12) !important;
    }

    /* -----------------------------
    🌸 ALERT / NOTIFICATION
    ------------------------------*/
    div[data-testid="stNotification"] {

        background: rgba(255,255,255,0.85) !important;

        border: 2px solid rgba(115,152,111,0.3) !important;

        border-radius: 18px !important;

        color: var(--ground-green) !important;

        backdrop-filter: blur(8px);
    }

    /* -----------------------------
    🌸 CAMERA / IMAGE BLOCK
    ------------------------------*/
    [data-testid="stVerticalBlock"] > div:has(div.stImage) {

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.7),
                rgba(255,245,248,0.85)
            ) !important;

        border-radius: 25px !important;

        border: 2px solid rgba(203,116,142,0.15) !important;

        padding: 18px !important;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.05);
    }

    /* -----------------------------
    🌸 FLOATING DECORATIONS
    ------------------------------*/

    /* ซ้ายล่าง */
    .stApp::before {
        content: "🐾 🐾";
        position: fixed;
        bottom: 22px;
        left: 20px;
        font-size: 55px;
        opacity: 0.18;
        transform: rotate(-15deg);
        z-index: 0;

        animation: pawFloat 4s ease-in-out infinite;
    }

    /* ขวาบน */
    .stApp::after {
        content: "🌷";
        position: fixed;
        top: 20px;
        right: 25px;
        font-size: 58px;
        opacity: 0.22;
        z-index: 0;

        animation: tulipFloat 5s ease-in-out infinite;
    }

    /* ขวาล่าง */
    html::after {
        content: "🧶";
        position: fixed;
        bottom: 25px;
        right: 30px;
        font-size: 50px;
        opacity: 0.25;
        z-index: 0;

        animation: yarnBounce 3.5s infinite ease-in-out;
    }

    /* -----------------------------
    🌸 ANIMATIONS
    ------------------------------*/

    @keyframes pawFloat {
        0% { transform: translateY(0px) rotate(-15deg); }
        50% { transform: translateY(-8px) rotate(-12deg); }
        100% { transform: translateY(0px) rotate(-15deg); }
    }

    @keyframes tulipFloat {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    @keyframes yarnBounce {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
        100% { transform: translateY(0px); }
    }

    /* -----------------------------
    🌸 REMOVE TEXT SELECTION
    ------------------------------*/
    * {
        user-select: none !important;
        -webkit-user-drag: none !important;
    }

    /* -----------------------------
    🌸 SCROLLBAR
    ------------------------------*/
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f5dce3;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(
            180deg,
            var(--growing-pink),
            var(--tulip-green)
        );
        border-radius: 20px;
    }

    /* -----------------------------
    🌸 FLOATING CAT ICON
    ------------------------------*/
    .floating-cat {
        display: inline-block;
        animation: floatingCat 3s ease-in-out infinite;
    }

    @keyframes floatingCat {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }

    </style>
    """, unsafe_allow_html=True)

# 2. เตรียม Session State
if 'page' not in st.session_state:
    st.session_state.page = 'login'

if 'engine' not in st.session_state:
    # เริ่มต้น Engine (Backend) แทนการเรียก main() ตรงๆ [cite: 100]
    st.session_state.engine = CatoEngine()

# หน้าที่ รับ Webhook

if st.session_state.page == 'login':
    empty_left, center_col, empty_right = st.columns([1, 2, 1])
    with center_col:
        st.markdown('<div style="text-align: center;"><h1>🛰️ CatoCord | DiscordMeow AI</h1></div>', unsafe_allow_html=True )
        
        # แสดงรูปแมวหน้า Login
        def get_img_64(path):
            with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
        
        try:
            img_b64 = get_img_64("assets/cat-watching.jpg")
            st.markdown(f'<div class="cat-staff-position"><img src="data:image/jpeg;base64,{img_b64}" /></div>', unsafe_allow_html=True)
        except: st.warning("ไม่พบรูปแมวใน assets/cat-watching.jpg")

        with st.form("login_form"):
            st.markdown("### 🐱 ใส่ Webhook เพื่อเริ่มจารกรรม")
            webhook_url = st.text_input("Discord Webhook URL:", placeholder="https://discord.com/api/webhooks/...")
            submit_login = st.form_submit_button("🚀 เริ่มความสนุกเลย!")

        if submit_login:
            if webhook_url.startswith("https://discord.com/api/webhooks/"):
                # ส่ง Webhook เข้าไปใน Engine
                st.session_state.engine.set_webhook(webhook_url)
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("❌ ลิงก์ Webhook ไม่ถูกต้อง")


#  Dashboard สแกนหน้า
elif st.session_state.page == 'dashboard':
    is_running = st.session_state.get('run_detection', False)
    
    # UI ส่วนปุ่มควบคุม Start/Stop/Back
    col_back, _, col_ctrl = st.columns([1, 2, 1])
    with col_back:
        if st.button("⬅️ BACK"):
            st.session_state.run_detection = False
            st.session_state.page = 'login'
            st.rerun()
    with col_ctrl:
        if not is_running:
            if st.button("🟢 START", use_container_width=True):
                st.session_state.run_detection = True
                st.rerun()
        else:
            if st.button("🔴 STOP", use_container_width=True):
                st.session_state.run_detection = False
                st.rerun()

    st.markdown("<div class='meow-title'><h1>หน่วยจารกรรมข้อมูลแมวเหมียว</h1></div>", unsafe_allow_html=True)

    if is_running:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### <span class='live-text'>📸 กล้องตรวจจับ</span>", unsafe_allow_html=True)
            live_placeholder = st.empty()
        with col2:
            st.markdown("### <span class='evidence-text'>📄 หลักฐาน (มีม)</span>", unsafe_allow_html=True)
            meme_placeholder = st.empty()
        
        # พื้นที่แสดงผล Jumpscare
        # พื้นที่แสดงผล Jumpscare
        jumpscare_placeholder = st.empty()

        cap = cv2.VideoCapture(0)
        while cap.isOpened() and st.session_state.run_detection:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.flip(frame, 1)

            if 'sound_played' not in st.session_state:
                st.session_state.sound_played = False

            processed_frame, display_path, caption, js_active = st.session_state.engine.process_frame(frame)
            live_placeholder.image(processed_frame, channels="RGB", use_container_width=True)

            if js_active:
                if not st.session_state.get('sound_played', False):
                    try:
                        with open("song/Cat meow sound effect.mp3", "rb") as f:
                            b64 = base64.b64encode(f.read()).decode()

                        unique_key = int(time.time() * 1000)

                        audio_html = f"""
                            <style>
                                /* ซ่อน iframe ที่ components.html สร้างขึ้น */
                                iframe {{ display: none !important; }}
                            </style>
                            <script>
                            (function() {{
                                var old = window.parent.document.getElementById('jumpscare-audio');
                                if (old) old.remove();

                                var audio = window.parent.document.createElement('audio');
                                audio.id = 'jumpscare-audio';
                                audio.src = 'data:audio/mp3;base64,{b64}';
                                audio.style.display = 'none';
                                window.parent.document.body.appendChild(audio);

                                audio.play().catch(function(e) {{
                                    console.warn('Jumpscare blocked key_{unique_key}:', e);
                                }});
                            }})();
                            </script>
                        """
                        with jumpscare_placeholder:
                            components.html(audio_html, height=0)

                        st.session_state.sound_played = True

                    except FileNotFoundError:
                        pass

            else:
                # ตอนไม่มี jumpscare → เคลียร์ทุกอย่างออก
                jumpscare_placeholder.empty()
                st.session_state.sound_played = False

            if display_path:
                meme_placeholder.image(display_path, caption=caption, use_container_width=True)

        cap.release()
    else:
        # แสดงแมวนอนหลับ
        st.markdown("<div style='text-align: center; padding: 60px;'><h2>😴 MeowCV กำลังฝันถึงปลา...</h2></div>", unsafe_allow_html=True)