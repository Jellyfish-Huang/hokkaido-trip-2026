import streamlit as st
import webbrowser

# ==========================================
# 1. App 設定與 CSS 美化
# ==========================================
st.set_page_config(
    page_title="2026 北海道旅",
    page_icon="❄️",
    layout="centered",
    initial_sidebar_state="collapsed" # 預設收起側邊欄，讓畫面更像 App
)

# 自訂 CSS：讓畫面更有質感，去除多餘留白，製作卡片陰影
st.markdown("""
    <style>
    /* 全域字體優化 */
    .stApp {
        font-family: "Helvetica Neue", Arial, sans-serif;
    }
    
    /* 隱藏預設選單 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 卡片樣式 */
    .travel-card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border-left: 5px solid #6c5ce7; /* 卡片左邊的裝飾線 */
    }
    
    /* 時間軸樣式 */
    .time-label {
        font-size: 14px;
        font-weight: bold;
        color: #636e72;
        text-align: right;
        padding-right: 10px;
    }
    
    /* Hero Section 氣溫大字 */
    .weather-temp {
        font-size: 36px;
        font-weight: bold;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 資料庫 (這裡是你的行程核心，未來只要改這裡)
# ==========================================
# 結構：日期 -> [時間, 圖示, 標題, 地點, 描述, 詳細資訊(可選)]

schedule_data = {
    "Day 1 (1/28)": {
        "city": "Sapporo",
        "weather": "❄️ -3°C",
        "events": [
            {"time": "12:30", "icon": "🛫", "title": "桃園起飛", "loc": "桃園機場 T1", "desc": "酷航 TR892", "detail": "行李：手提10kg / 托運30kg\n訂位代號：XXXXXX"},
            {"time": "17:20", "icon": "🛬", "title": "抵達新千歲", "loc": "新千歲機場", "desc": "入境、領行李、買伴手禮", "detail": "必買：札幌農學、LeTAO"},
            {"time": "18:30", "icon": "🚆", "title": "JR 快速 Airport", "loc": "新千歲空港駅", "desc": "往札幌市區 (約 40 分鐘)", "detail": "不用劃位，刷西瓜卡即可"},
            {"time": "19:30", "icon": "🏨", "title": "Check-in", "loc": "札幌站前里士滿飯店", "desc": "放行李、休息", "detail": "訂單編號：123456\n含早餐\n23:59前可免費取消"},
            {"time": "20:00", "icon": "🍜", "title": "晚餐 & 採購", "loc": "Sapporo Stellar Place", "desc": "UQ 買發熱衣、湯咖哩", "detail": "Stellar Place 開到 21:00"}
        ]
    },
    "Day 2 (1/29)": {
        "city": "Sapporo",
        "weather": "☁️ -5°C",
        "events": [
            {"time": "08:00", "icon": "🦀", "title": "海鮮早餐", "loc": "二條市場", "desc": "豪華海鮮丼", "detail": "推薦：大磯、丼兵衛"},
            {"time": "10:00", "icon": "⛩️", "title": "參拜", "loc": "北海道神宮", "desc": "圓山公園散步", "detail": "記得買六花亭神宮限定判官餅"},
            {"time": "13:00", "icon": "☕", "title": "下午茶", "loc": "森彥咖啡", "desc": "木造老屋咖啡", "detail": "本店氛圍最好"},
            {"time": "18:00", "icon": "🛍️", "title": "逛街戰區", "loc": "狸小路商店街", "desc": "藥妝、唐吉訶德", "detail": "記得帶護照退稅"}
        ]
    },
    "Day 3 (1/30)": {
        "city": "Otaru",
        "weather": "❄️ -6°C",
        "events": [
            {"time": "09:00", "icon": "🚆", "title": "出發小樽", "loc": "札幌駅", "desc": "JR 函館本線", "detail": "往小樽方向，建議坐右邊看海"},
            {"time": "10:30", "icon": "📷", "title": "浪漫散策", "loc": "小樽運河", "desc": "堺町通、北一硝子館", "detail": "必吃：北菓樓泡芙、六花亭"},
            {"time": "15:00", "icon": "🚠", "title": "天狗山夜景", "loc": "小樽天狗山纜車", "desc": "情書拍攝地", "detail": "太晚去會排隊，建議 15:00 就上去卡位"}
        ]
    },
    "Day 4 (1/31)": {
        "city": "Sapporo",
        "weather": "☀️ -2°C",
        "events": [
            {"time": "10:00", "icon": "🏫", "title": "校園漫步", "loc": "北海道大學", "desc": "白楊林蔭道", "detail": "綜合博物館免費參觀"},
            {"time": "14:00", "icon": "🍺", "title": "啤酒巡禮", "loc": "札幌啤酒博物館", "desc": "成吉思汗烤肉", "detail": "最後入場 18:00"}
        ]
    },
    "Day 5 (2/1)": {
        "city": "Toyako",
        "weather": "🌫️ -4°C",
        "events": [
            {"time": "11:00", "icon": "👋", "title": "退房 Check-out", "loc": "札幌站前里士滿飯店", "desc": "前往搭車點", "detail": ""},
            {"time": "13:15", "icon": "🚌", "title": "飯店接駁車", "loc": "札幌駅北口", "desc": "往洞爺湖萬世閣", "detail": "預約確認信要存好"},
            {"time": "20:45", "icon": "🎆", "title": "冬季花火", "loc": "洞爺湖畔", "desc": "邊泡溫泉邊看煙火", "detail": "持續 20 分鐘"}
        ]
    }
}

# ==========================================
# 3. 介面邏輯 (UI Logic)
# ==========================================

# --- A. 頂部選單 (Day Selector) ---
# 使用 Tabs 來切換天數，這在手機上最直覺
days_list = list(schedule_data.keys())
selected_day = st.selectbox("📅 選擇行程日期", days_list)

# 取得當天資料
day_info = schedule_data[selected_day]

# --- B. Hero Section (動態首頁) ---
# 模擬 App 的頂部資訊卡
st.markdown(f"""
<div style="background: linear-gradient(135deg, #74b9ff, #0984e3); padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px;">
    <div style="font-size: 14px; opacity: 0.8;">CURRENT LOCATION</div>
    <div style="font-size: 24px; font-weight: bold;">📍 {day_info['city']}, Hokkaido</div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
        <div class="weather-temp">{day_info['weather']}</div>
        <div style="text-align: right; font-size: 14px;">
            <div>體感 -8°C</div>
            <div>降雪機率 40%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- C. Smart Timeline (時間軸卡片) ---
st.subheader("今日行程")

for event in day_info["events"]:
    # 使用 columns 來製作 左(時間) 右(卡片) 的佈局
    c1, c2 = st.columns([1.2, 4]) 
    
    with c1:
        st.markdown(f"<div class='time-label'>{event['time']}<br><span style='font-size:20px'>{event['icon']}</span></div>", unsafe_allow_html=True)
        
    with c2:
        # 卡片容器
        with st.container():
            # 這裡我們用一點 Markdown 技巧來模擬卡片外觀，但核心內容用 Streamlit 元件
            # 標題
            st.markdown(f"**{event['title']}**")
            # 描述
            st.caption(f"{event['desc']}")
            
            # 功能按鈕區
            col_map, col_info = st.columns([1, 1])
            
            with col_map:
                # 產生 Google Maps 連結
                map_url = f"https://www.google.com/maps/search/?api=1&query={event['loc']}"
                st.link_button("📍 導航", map_url, help=f"導航到 {event['loc']}")
            
            with col_info:
                # 如果有詳細資訊，顯示展開按鈕
                if event['detail']:
                    with st.expander("ℹ️ 詳細"):
                        st.write(event['detail'])
            
            st.divider() # 分隔線代替卡片下緣，因為 Streamlit 很難畫出完美的封閉 div

# --- D. 底部功能區 ---
st.info("💡 小撇步：點擊「導航」會直接打開 Google Maps App 喔！")
