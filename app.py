import streamlit as st

# ==========================================
# 1. 頁面基礎設定
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
# 這裡我把 React 那邊的 Tailwind 風格轉換成 CSS
st.markdown("""
    <style>
    /* 全域字體與背景 */
    .stApp {
        background-color: #f8fafc; /* Slate-50 */
        font-family: "Noto Sans TC", sans-serif;
    }
    
    /* 隱藏預設選單，模擬 App 質感 */
    #MainMenu, footer {visibility: hidden;}
    
    /* 頂部 WanderFlow 標題列 */
    .app-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        z-index: 999;
        padding: 10px 20px;
        border-bottom: 1px solid #e2e8f0;
        text-align: center;
        font-weight: bold;
        color: #334155;
        letter-spacing: 2px;
        font-size: 14px;
    }
    
    /* 讓內容往下推，不要被標題擋住 */
    .block-container {
        padding-top: 60px !important;
        padding-bottom: 100px !important;
    }

    /* Hero 卡片 (當天重點資訊) */
    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%); /* Slate-900 to Slate-700 */
        color: white;
        padding: 24px;
        border-radius: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    }
    .hero-date {
        font-size: 14px;
        opacity: 0.8;
        margin-bottom: 4px;
    }
    .hero-city {
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .hero-temp {
        background: rgba(255,255,255,0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        display: inline-block;
    }

    /* 時間軸卡片 */
    .timeline-row {
        display: flex;
        margin-bottom: 20px;
    }
    .timeline-time {
        width: 60px;
        font-size: 12px;
        color: #64748b; /* Slate-500 */
        padding-top: 15px;
        text-align: right;
        margin-right: 15px;
        font-weight: 600;
        border-right: 2px solid #e2e8f0;
        padding-right: 15px;
    }
    .timeline-content {
        flex: 1;
        background: white;
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
    }
    .timeline-title {
        font-weight: 700;
        color: #1e293b; /* Slate-800 */
        font-size: 16px;
        margin-bottom: 4px;
    }
    .timeline-desc {
        font-size: 14px;
        color: #475569; /* Slate-600 */
        line-height: 1.5;
        margin-bottom: 8px;
    }
    
    /* 標籤 Tag */
    .tag {
        display: inline-block;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 5px;
        font-weight: 600;
    }
    .tag-transport { background: #e0f2fe; color: #0284c7; } /* Sky Blue */
    .tag-food { background: #dcfce7; color: #16a34a; } /* Green */
    .tag-stay { background: #f3e8ff; color: #9333ea; } /* Purple */
    .tag-sight { background: #ffedd5; color: #ea580c; } /* Orange */

    </style>
    
    <div class="app-header">WANDERFLOW</div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. 行程資料庫 (整合你的 Notion 資料)
# ==========================================
# 這裡模擬 React 中的 data/tripData.ts
itinerary = [
    {
        "day": "Day 1",
        "date": "1/28 (三)",
        "city": "札幌 Sapporo",
        "weather": "❄️ -3°C | 降雪機率 60%",
        "events": [
            {"time": "12:30", "title": "桃園起飛", "type": "transport", "desc": "酷航 TR892 (T1)", "link": "", "tags": ["飛行"]},
            {"time": "17:20", "title": "抵達新千歲", "type": "transport", "desc": "入境、領行李、國內線買伴手禮", "link": "https://maps.app.goo.gl/9QZ8Z8Z8Z8Z8Z8Z8", "tags": ["必買:Kinotoya"]},
            {"time": "19:30", "title": "Check-in 里士滿", "type": "stay", "desc": "札幌站前 Richmond Hotel", "link": "https://maps.app.goo.gl/hotel1", "tags": ["訂單:12345"]},
            {"time": "20:30", "title": "湯咖哩 GARAKU", "type": "food", "desc": "狸小路排隊名店，記得加起司飯", "link": "https://maps.app.goo.gl/curry", "tags": ["必吃"]},
        ]
    },
    {
        "day": "Day 2",
        "date": "1/29 (四)",
        "city": "札幌 Sapporo",
        "weather": "☁️ -5°C | 多雲",
        "events": [
            {"time": "08:00", "title": "二條市場", "type": "food", "desc": "早餐吃海鮮丼 (大磯/丼兵衛)", "link": "", "tags": ["海膽"]},
            {"time": "10:30", "title": "北海道神宮", "type": "sight", "desc": "雪中神社參拜，吃判官餅", "link": "", "tags": ["六花亭"]},
            {"time": "14:00", "title": "森彥咖啡", "type": "food", "desc": "木造老屋喝下午茶", "link": "", "tags": ["氣氛"]},
            {"time": "18:00", "title": "狸小路逛街", "type": "sight", "desc": "藥妝補貨、唐吉訶德", "link": "", "tags": ["免稅"]},
        ]
    },
    {
        "day": "Day 3",
        "date": "1/30 (五)",
        "city": "小樽 Otaru",
        "weather": "🌨️ -6°C | 大雪",
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
        "weather": "🌫️ -4°C | 陰",
        "events": [
            {"time": "11:00", "title": "退房", "type": "stay", "desc": "寄放行李或直接去車站", "link": "", "tags": []},
            {"time": "13:15", "title": "飯店接駁車", "type": "transport", "desc": "札幌北口發車 (別遲到！)", "link": "", "tags": ["預約制"]},
            {"time": "20:45", "title": "冬季花火", "type": "sight", "desc": "湖畔煙火大會", "link": "", "tags": ["溫泉"]},
        ]
    },
    {
        "day": "Day 6",
        "date": "2/2 (一)",
        "city": "函館 Hakodate",
        "weather": "🌃 -2°C | 晴",
        "events": [
            {"time": "10:00", "title": "前往函館", "type": "transport", "desc": "JR 特急北斗號 (約2小時)", "link": "", "tags": ["鐵路便當"]},
            {"time": "16:00", "title": "函館山夜景", "type": "sight", "desc": "搭纜車上山，世界三大夜景", "link": "", "tags": ["必看"]},
            {"time": "18:00", "title": "小丑漢堡", "type": "food", "desc": "函館限定平民美食", "link": "", "tags": ["必吃"]},
        ]
    }
]

# 打包清單 (原本是 Modal，這裡改成 Sidebar 或 Expander)
packing_tips = [
    "護照 (檢查效期)", "日幣現鈔 & 信用卡 (吉鶴/FlyGo)", "Esim 網卡設定", 
    "演唱會門票 (最重要！)", "止痛藥/感冒藥/腸胃藥", 
    "行動電源 (兩顆)", "有線電棒 (無線不能上機)", 
    "發熱衣 (洋蔥式穿法)", "防滑靴/鞋底釘 (雪地必備)"
]

# ==========================================
# 4. App 邏輯
# ==========================================

# --- 頂部日期選擇器 (模擬 BottomNav 的功能) ---
# 使用 Tabs 讓使用者在天數間切換，這在手機上操作很直覺
day_labels = [day["date"] for day in itinerary]
selected_tab = st.selectbox("選擇行程日期", range(len(day_labels)), format_func=lambda x: day_labels[x])

current_plan = itinerary[selected_tab]

# --- 顯示 Hero 區塊 ---
st.markdown(f"""
<div class="hero-card">
    <div class="hero-date">{current_plan['day']} • {current_plan['date']}</div>
    <div class="hero-city">{current_plan['city']}</div>
    <div class="hero-temp">{current_plan['weather']}</div>
</div>
""", unsafe_allow_html=True)

# --- 顯示打包小貼士 (Expander) ---
with st.expander("🎒 打包與行前檢查 (點擊展開)"):
    for tip in packing_tips:
        st.markdown(f"- {tip}")

# --- 顯示 Timeline (核心功能) ---
st.markdown("### 📅 行程安排")

for event in current_plan['events']:
    # 決定 Tag 顏色
    tag_class = "tag-sight"
    if event['type'] == 'transport': tag_class = "tag-transport"
    elif event['type'] == 'food': tag_class = "tag-food"
    elif event['type'] == 'stay': tag_class = "tag-stay"
    
    # 產生 Tag HTML
    tags_html = "".join([f'<span class="tag {tag_class}">{t}</span>' for t in event['tags']])
    
    # 產生按鈕 HTML (如果有連結)
    link_html = ""
    if event['link']:
        # 這裡用一個小 trick 讓它看起來像文字連結
        pass # Streamlit 的 link_button 比較好用，我們放在下面

    # 渲染卡片 HTML 結構
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
    
    # 如果有導航連結，在卡片下方顯示一個小按鈕
    if event['link']:
        # 利用 columns 讓按鈕靠右或置中
        c1, c2 = st.columns([1, 4])
        with c2:
            st.link_button("📍 導航", event['link'])

# 底部留白
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
