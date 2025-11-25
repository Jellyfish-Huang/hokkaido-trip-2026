import streamlit as st
import requests
import google.generativeai as genai

# ==========================================
# 1. 介面基礎設定
# ==========================================
st.set_page_config(
    page_title="WanderFlow - 北海道 2026",
    page_icon="❄️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS 魔法：日式極簡風格
# ==========================================
st.markdown("""
    <style>
    /* 全域配色：日式白練色 */
    .stApp {
        background-color: #fcfaf2; 
        font-family: "Noto Sans TC", "Helvetica Neue", sans-serif;
    }
    
    #MainMenu, footer {visibility: hidden;}
    
    /* 側邊欄按鈕化 */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {
        padding: 15px 20px;
        margin-bottom: 10px;
        border-radius: 6px;
        background-color: #ffffff;
        color: #64748b;
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        cursor: pointer;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: #f8fafc;
        color: #0f172a;
        border-left: 4px solid #6c5ce7;
        transform: translateX(6px);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    
    /* 標題列 */
    .app-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(252, 250, 242, 0.9);
        backdrop-filter: blur(8px);
        z-index: 999;
        padding: 15px;
        border-bottom: 1px solid #efeecd;
        text-align: center;
        font-weight: 800;
        color: #2c3e50;
        letter-spacing: 3px;
        font-size: 14px;
    }
    .block-container { padding-top: 80px !important; }

    /* 卡片樣式 */
    .info-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #f0f0f0;
        margin-bottom: 16px;
    }
    .card-title { font-weight: 700; color: #2c3e50; font-size: 16px; margin-bottom: 8px;}
    .card-content { color: #596275; font-size: 14px; line-height: 1.7; }
    
    /* Checkbox 優化 */
    .stCheckbox { margin-bottom: 8px; }
    
    /* AI 建議區塊 */
    .ai-box {
        background-color: #fdfbf7;
        border-left: 3px solid #b2bec3;
        padding: 15px;
        border-radius: 4px;
        font-size: 14px;
        color: #636e72;
        margin-top: 10px;
    }
    
    /* Tags */
    .tag { display: inline-block; font-size: 11px; padding: 4px 10px; border-radius: 20px; margin-right: 6px; font-weight: 500; letter-spacing: 0.5px; }
    .tag-transport { background: #ecf0f1; color: #2980b9; }
    .tag-food { background: #eafef1; color: #27ae60; }
    .tag-stay { background: #f3e5f5; color: #8e44ad; }
    .tag-sight { background: #fdf2e9; color: #d35400; }
    </style>
    
    <div class="app-header">WANDERFLOW | HOKKAIDO</div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. 功能函式
# ==========================================
def get_live_weather(city_name):
    coords = {
        "札幌 Sapporo": (43.0618, 141.3545),
        "小樽 Otaru": (43.1907, 140.9947),
        "洞爺湖 Toya": (42.5645, 140.8587),
        "函館 Hakodate": (41.7687, 140.7288)
    }
    lat, lon = coords.get(city_name, (43.0618, 141.3545))
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        r = requests.get(url).json()
        temp = r['current_weather']['temperature']
        return f"{temp}°C"
    except:
        return "--"

def get_ai_souvenirs():
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "推薦 5 個北海道在地人私藏的伴手禮（排除白色戀人），格式：**商品**：特色簡介。"
        try:
            return model.generate_content(prompt).text
        except:
            return "AI 連線中..."
    return "請設定 API Key。"

# ==========================================
# 4. 資料庫 (行程 & 清單)
# ==========================================
itinerary = [
    {"day": "Day 1", "date": "1/28 (三)", "city": "札幌 Sapporo", "events": [
        {"time": "17:20", "title": "抵達新千歲空港", "type": "transport", "desc": "入境、領行李、國內線逛街", "link": "", "tags": ["飛行"]},
        {"time": "19:30", "title": "Check-in 里士滿", "type": "stay", "desc": "札幌站前 Richmond Hotel", "link": "https://goo.gl/maps/placeholder", "tags": ["住宿"]},
        {"time": "20:30", "title": "湯咖哩 GARAKU", "type": "food", "desc": "狸小路排隊名店，記得加起司飯", "link": "", "tags": ["晚餐"]}
    ]},
    {"day": "Day 2", "date": "1/29 (四)", "city": "札幌 Sapporo", "events": [
        {"time": "08:00", "title": "二條市場", "type": "food", "desc": "大磯海鮮丼", "link": "", "tags": ["早餐"]},
        {"time": "10:30", "title": "北海道神宮", "type": "sight", "desc": "雪中神社、六花亭判官餅", "link": "", "tags": ["景點"]},
        {"time": "14:00", "title": "森彥咖啡", "type": "food", "desc": "木造老屋文青下午茶", "link": "", "tags": ["咖啡"]},
    ]},
    {"day": "Day 3", "date": "1/30 (五)", "city": "小樽 Otaru", "events": [
        {"time": "10:30", "title": "堺町通散策", "type": "sight", "desc": "北菓樓泡芙、LeTAO、音樂盒堂", "link": "", "tags": ["逛街"]},
        {"time": "15:00", "title": "天狗山夜景", "type": "sight", "desc": "搭纜車，情書拍攝地", "link": "", "tags": ["必看"]},
    ]},
    {"day": "Day 5", "date": "2/1 (日)", "city": "洞爺湖 Toya", "events": [
        {"time": "13:15", "title": "搭乘接駁車", "type": "transport", "desc": "札幌北口 -> 萬世閣", "link": "", "tags": ["預約制"]},
        {"time": "20:45", "title": "冬季花火", "type": "sight", "desc": "邊泡溫泉邊看煙火", "link": "", "tags": ["祭典"]},
    ]},
    {"day": "Day 6", "date": "2/2 (一)", "city": "函館 Hakodate", "events": [
        {"time": "10:00", "title": "JR 北斗號", "type": "transport", "desc": "往函館 (約2hr)", "link": "", "tags": ["鐵路"]},
        {"time": "16:00", "title": "函館山夜景", "type": "sight", "desc": "百萬夜景，提早卡位", "link": "", "tags": ["世界三大夜景"]},
    ]}
]

# --- 根據你的需求更新的分類清單 ---
checklist_data = {
    "🪪 重要證件與錢財": [
        "護照", "身分證", "國際駕照", 
        "日幣現鈔", "信用卡", "Esim 或漫遊設定", "演唱會門票 (重要!)"
    ],
    "🔌 3C 與工具": [
        "充電器", "行動電源 (需隨身攜帶)", "行李秤", "有線電棒 (無線不可上機)"
    ],
    "💄 臉部保養與美妝": [
        "洗面乳/卸妝棉", "化妝水/乳液", "防曬 (雪地反射強)",
        "彩妝品/化妝鏡", "香水", "隱形眼鏡/眼鏡/眼鏡盒"
    ],
    "🚿 沐浴與髮品": [
        "牙刷牙膏/毛巾", "護髮乳", "造型品/髮油", "刮鬍刀"
    ],
    "🧣 衣物與禦寒": [
        "發熱衣褲", "內衣褲/襪子/睡衣", "手套/圍巾/帽子", "雪靴", "雨傘", "常備藥品"
    ]
}

# ==========================================
# 5. 側邊欄 (日式選單)
# ==========================================
with st.sidebar:
    st.title("MENU")
    options = ["行程規劃", "航班住宿", "行李清單", "伴手禮推薦"]
    page = st.radio("", options, label_visibility="collapsed")
    st.markdown("---")
    st.caption("Designed by Gemini")

# ==========================================
# 6. 主頁面內容
# ==========================================

# --- 頁面 1: 行程規劃 ---
if page == "行程規劃":
    day_labels = [d["date"] for d in itinerary]
    idx = st.selectbox("📅 選擇日期", range(len(day_labels)), format_func=lambda x: day_labels[x])
    plan = itinerary[idx]
    
    temp = get_live_weather(plan['city'])
    st.markdown(f"""
    <div style="background-color:#2c3e50; color:white; padding:24px; border-radius:12px; margin-bottom:24px; text-align:center;">
        <div style="font-size:12px; opacity:0.7; letter-spacing:2px; margin-bottom:5px;">CURRENT LOCATION</div>
        <div style="font-size:32px; font-weight:300; margin-bottom:10px;">{plan['city']}</div>
        <span style="background:rgba(255,255,255,0.15); padding:5px 15px; border-radius:20px; font-size:14px;">
            ❄️ 現在氣溫 {temp}
        </span>
    </div>
    """, unsafe_allow_html=True)

    for evt in plan['events']:
        bg_col = "tag-sight"
        if evt['type']=='transport': bg_col = "tag-transport"
        elif evt['type']=='food': bg_col = "tag-food"
        elif evt['type']=='stay': bg_col = "tag-stay"
        
        tags_html = "".join([f'<span class="tag {bg_col}">{t}</span>' for t in evt['tags']])
        
        st.markdown(f"""
        <div class="info-card" style="display:flex; align-items:flex-start;">
            <div style="min-width:60px; font-weight:bold; color:#b2bec3; font-size:13px; padding-top:2px;">{evt['time']}</div>
            <div style="flex:1;">
                <div class="card-title">{evt['title']}</div>
                <div class="card-content" style="margin-bottom:8px;">{evt['desc']}</div>
                <div>{tags_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if evt['link']:
            c1, c2 = st.columns([1, 5])
            with c2: st.link_button("📍 導航", evt['link'])

# --- 頁面 2: 航班住宿 ---
elif page == "航班住宿":
    st.subheader("✈️ 航班資訊")
    st.info("去程：1/28 酷航 TR892 (12:30-17:20)")
    st.info("回程：2/6 泰越捷 VZ571 (09:30-13:30)")
    
    st.divider()
    st.subheader("🏨 住宿")
    hotels = [
        ("1/28-2/1", "札幌里士滿", "¥57,678", "含早餐"),
        ("2/1-2/2", "洞爺湖萬世閣", "¥32,949", "含早晚餐 + 接駁"),
        ("2/2-2/4", "函館 MYSTAYS", "¥12,096", "函館站旁"),
        ("2/4-2/6", "Rembrandt Style", "TWD 8,540", "薄野區")
    ]
    for date, name, price, note in hotels:
        st.markdown(f"""
        <div class="info-card">
            <div class="card-title">{name}</div>
            <div class="card-content">
                📅 {date}<br>
                💰 {price}<br>
                📝 {note}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 頁面 3: 行李清單 (已更新) ---
elif page == "行李清單":
    st.subheader("🎒 必備清單")
    st.caption("出發前請再次確認：")
    
    if "checklist" not in st.session_state: st.session_state.checklist = {}
    
    # 這裡會讀取上面更新過的 checklist_data
    for category, items in checklist_data.items():
        st.markdown(f"**{category}**")
        for item in items:
            key = f"{category}_{item}"
            if key not in st.session_state.checklist: st.session_state.checklist[key] = False
            st.checkbox(item, key=key)
        st.divider()

# --- 頁面 4: 伴手禮 ---
elif page == "伴手禮推薦":
    st.subheader("🎁 伴手禮")
    st.markdown("""
    <div class="info-card">
        <div class="card-title">📝 你的清單</div>
        <div class="card-content">
        1. 六花亭 (葡萄奶油)<br>
        2. 札幌農學餅乾<br>
        3. LeTAO 起司蛋糕<br>
        4. 北菓樓 夢不思議泡芙
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✨ 讓 AI 推薦隱藏版"):
        with st.spinner("AI 正在搜尋在地好物..."):
            res = get_ai_souvenirs()
            st.markdown(f"<div class='ai-box'>{res}</div>", unsafe_allow_html=True)
