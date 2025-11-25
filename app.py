import streamlit as st
import requests # 用來抓天氣的工具

# ==========================================
# 1. 介面基礎設定
# ==========================================
st.set_page_config(
    page_title="WanderFlow - 北海道",
    page_icon="❄️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. 注入 React 版的靈魂 (CSS 魔法)
# ==========================================
st.markdown("""
    <style>
    /* 全域字體與背景 */
    .stApp {
        background-color: #f8fafc; /* Slate-50 */
        font-family: "Noto Sans TC", sans-serif;
    }
    
    /* 隱藏預設選單 */
    #MainMenu, footer {visibility: hidden;}
    
    /* 頂部 WanderFlow 標題列 */
    .app-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        z-index: 999;
        padding: 12px 20px;
        border-bottom: 1px solid #e2e8f0;
        text-align: center;
        font-weight: 800;
        color: #334155;
        letter-spacing: 3px;
        font-size: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .block-container {
        padding-top: 80px !important;
        padding-bottom: 100px !important;
    }

    /* Hero 卡片 (天氣顯示區) */
    .hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 24px;
        border-radius: 24px;
        margin-bottom: 24px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    /* 裝飾用的背景光暈 */
    .hero-card::before {
        content: "";
        position: absolute;
        top: -50px;
        right: -50px;
        width: 150px;
        height: 150px;
        background: rgba(56, 189, 248, 0.2);
        filter: blur(40px);
        border-radius: 50%;
    }

    .hero-date { font-size: 13px; opacity: 0.8; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px;}
    .hero-city { font-size: 36px; font-weight: 800; margin-bottom: 12px; letter-spacing: -1px;}
    
    .weather-badge {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(4px);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 15px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* 時間軸卡片 */
    .timeline-row { display: flex; margin-bottom: 20px; }
    .timeline-time {
        width: 55px;
        font-size: 13px;
        color: #64748b;
        padding-top: 16px;
        text-align: right;
        margin-right: 16px;
        font-weight: 700;
        position: relative;
    }
    /* 時間軸直線 */
    .timeline-time::after {
        content: "";
        position: absolute;
        top: 40px;
        right: -9px;
        width: 2px;
        height: calc(100% + 20px);
        background-color: #e2e8f0;
    }
    
    .timeline-content {
        flex: 1;
        background: white;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
        transition: transform 0.2s;
    }
    .timeline-content:active { transform: scale(0.98); } /* 手機點擊回饋 */

    .timeline-title { font-weight: 700; color: #1e293b; font-size: 16px; margin-bottom: 4px; }
    .timeline-desc { font-size: 14px; color: #475569; line-height: 1.5; margin-bottom: 10px; }
    
    /* 標籤 Tag */
    .tag { display: inline-block; font-size: 11px; padding: 3px 8px; border-radius: 6px; margin-right: 6px; font-weight: 600; }
    .tag-transport { background: #e0f2fe; color: #0369a1; }
    .tag-food { background: #dcfce7; color: #15803d; }
    .tag-stay { background: #f3e8ff; color: #7e22ce; }
    .tag-sight { background: #ffedd5; color: #c2410c; }

    </style>
    
    <div class="app-header">WANDERFLOW</div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. 真實天氣功能 (Open-Meteo API)
# ==========================================
def get_live_weather(lat, lon):
    try:
        # 使用 Open-Meteo 免費 API
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        
        # 解析資料
        temp = data['current_weather']['temperature']
        code = data['current_weather']['weathercode']
        
        # 將天氣代碼轉換成 Emoji 和文字
        # 參考: https://open-meteo.com/en/docs
        condition = "晴"
        icon = "☀️"
        
        if code in [1, 2, 3]: condition, icon = "多雲", "☁️"
        elif code in [45, 48]: condition, icon = "起霧", "🌫️"
        elif code in [51, 53, 55, 61, 63, 65]: condition, icon = "下雨", "🌧️"
        elif code in [71, 73, 75, 77, 85, 86]: condition, icon = "下雪", "🌨️"
        elif code >= 95: condition, icon = "雷雨", "⚡"
        
        return f"{icon} 目前 {temp}°C | {condition}"
    except:
        return "📡 天氣連線中..."

# 城市座標資料庫 (札幌, 小樽, 洞爺湖, 函館)
city_coords = {
    "札幌 Sapporo": (43.0618, 141.3545),
    "小樽 Otaru": (43.1907, 140.9947),
    "洞爺湖 Toya": (42.5645, 140.8587),
    "函館 Hakodate": (41.7687, 140.7288)
}

# ==========================================
# 4. 行程資料庫
# ==========================================
itinerary = [
    {
        "day": "Day 1",
        "date": "1/28 (三)",
        "city": "札幌 Sapporo",
        "events": [
            {"time": "12:30", "title": "桃園起飛", "type": "transport", "desc": "酷航 TR892 (T1) -> 新千歲", "link": "", "tags": ["飛行"]},
            {"time": "19:30", "title": "Check-in 里士滿", "type": "stay", "desc": "札幌站前 Richmond Hotel", "link": "https://maps.app.goo.gl/dummy", "tags": ["訂單:12345"]},
            {"time": "20:30", "title": "湯咖哩 GARAKU", "type": "food", "desc": "狸小路排隊名店，記得加起司飯", "link": "https://maps.app.goo.gl/dummy", "tags": ["必吃"]},
        ]
    },
    {
        "day": "Day 2",
        "date": "1/29 (四)",
        "city": "札幌 Sapporo",
        "events": [
            {"time": "08:00", "title": "二條市場", "type": "food", "desc": "早餐吃海鮮丼 (大磯/丼兵衛)", "link": "", "tags": ["海膽"]},
            {"time": "10:30", "title": "北海道神宮", "type": "sight", "desc": "雪中神社參拜，吃判官餅", "link": "", "tags": ["六花亭"]},
            {"time": "14:00", "title": "森彥咖啡", "type": "food", "desc": "木造老屋喝下午茶", "link": "", "tags": ["氣氛"]},
        ]
    },
    {
        "day": "Day 3",
        "date": "1/30 (五)",
        "city": "小樽 Otaru",
        "events": [
            {"time": "09:00", "title": "前往小樽", "type": "transport", "desc": "JR 快速 Airport (往右邊看海)", "link": "", "tags": ["JR"]},
            {"time": "10:30", "title": "堺町通散策", "type": "sight", "desc": "北菓樓泡芙、LeTAO、六花亭", "link": "", "tags": ["甜點"]},
            {"time": "15:00", "title": "天狗山夜景", "type": "sight", "desc": "情書拍攝地，提早上山卡位", "link": "", "tags": ["百萬夜景"]},
        ]
    },
    {
        "day": "Day 5",
        "date": "2/1 (日)",
        "city": "洞爺湖 Toya",
        "events": [
            {"time": "13:15", "title": "飯店接駁車", "type": "transport", "desc": "札幌北口發車 (別遲到！)", "link": "", "tags": ["預約制"]},
            {"time": "20:45", "title": "冬季花火", "type": "sight", "desc": "湖畔煙火大會", "link": "", "tags": ["溫泉"]},
        ]
    },
    {
        "day": "Day 6",
        "date": "2/2 (一)",
        "city": "函館 Hakodate",
        "events": [
            {"time": "10:00", "title": "前往函館", "type": "transport", "desc": "JR 特急北斗號 (約2小時)", "link": "", "tags": ["鐵路便當"]},
            {"time": "16:00", "title": "函館山夜景", "type": "sight", "desc": "搭纜車上山，世界三大夜景", "link": "", "tags": ["必看"]},
        ]
    }
]

# ==========================================
# 5. App 邏輯
# ==========================================

# --- 頂部日期選擇器 ---
day_labels = [day["date"] for day in itinerary]
selected_idx = st.selectbox("選擇行程日期", range(len(day_labels)), format_func=lambda x: day_labels[x])
current_plan = itinerary[selected_idx]

# --- 抓取即時天氣 ---
# 1. 取得該城市的座標
lat, lon = city_coords.get(current_plan['city'], (43.0618, 141.3545))
# 2. 呼叫 API
live_weather = get_live_weather(lat, lon)

# --- 顯示 Hero 區塊 ---
st.markdown(f"""
<div class="hero-card">
    <div class="hero-date">{current_plan['day']} • {current_plan['date']}</div>
    <div class="hero-city">{current_plan['city']}</div>
    <div class="weather-badge">{live_weather}</div>
</div>
""", unsafe_allow_html=True)

# --- 顯示打包小貼士 (Expander) ---
with st.expander("🎒 行前檢查與打包清單"):
    tips = ["護照效期檢查", "日幣與吉鶴卡", "Esim 設定", "演唱會門票！", "行動電源", "有線電棒", "止痛藥/腸胃藥"]
    for tip in tips:
        st.markdown(f"- {tip}")

# --- 顯示 Timeline ---
st.markdown("### 📅 行程安排")

for event in current_plan['events']:
    # 決定 Tag 顏色
    tag_class = "tag-sight"
    if event['type'] == 'transport': tag_class = "tag-transport"
    elif event['type'] == 'food': tag_class = "tag-food"
    elif event['type'] == 'stay': tag_class = "tag-stay"
    
    tags_html = "".join([f'<span class="tag {tag_class}">{t}</span>' for t in event['tags']])
    
    # 渲染卡片
    st.markdown(f"""
    <div class="timeline-row">
        <div class="timeline-time">{event['time']}</div>
        <div class="timeline-content">
            <div class="timeline-title">{event['title']}</div>
            <div class="timeline-desc">{event['desc']}</div>
            <div style="margin-top:8px;">{tags_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 按鈕
    if event['link']:
        c1, c2 = st.columns([1, 4])
        with c2:
            st.link_button("📍 導航", event['link'])

# 底部留白
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
