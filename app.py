import streamlit as st
import requests
import google.generativeai as genai

# ==========================================
# 1. 介面基礎設定 & CSS
# ==========================================
st.set_page_config(
    page_title="WanderFlow - 北海道 2026",
    page_icon="❄️",
    layout="centered",
    initial_sidebar_state="expanded" # 展開側邊欄以便導航
)

st.markdown("""
    <style>
    /* 全域字體與背景 */
    .stApp {
        background-color: #f8fafc;
        font-family: "Noto Sans TC", sans-serif;
    }
    
    /* 隱藏預設選單 */
    #MainMenu, footer {visibility: hidden;}
    
    /* 標題列 */
    .app-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        z-index: 999;
        padding: 15px;
        border-bottom: 1px solid #e2e8f0;
        text-align: center;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: 2px;
        font-size: 16px;
    }
    .block-container {
        padding-top: 80px !important;
        padding-bottom: 100px !important;
    }

    /* 通用卡片樣式 */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #f1f5f9;
        margin-bottom: 15px;
    }
    .card-title { font-weight: 700; color: #334155; font-size: 16px; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;}
    .card-content { color: #64748b; font-size: 14px; line-height: 1.6; }
    
    /* 航班卡片 */
    .flight-card { border-left: 4px solid #0ea5e9; }
    
    /* 住宿卡片 */
    .hotel-card { border-left: 4px solid #8b5cf6; }

    /* 伴手禮 AI 區塊 */
    .ai-suggestion {
        background-color: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 15px;
        color: #0369a1;
        font-size: 14px;
        margin-top: 15px;
    }

    /* Checkbox 優化 */
    .stCheckbox { margin-bottom: 5px; }

    /* Tags */
    .tag { display: inline-block; font-size: 11px; padding: 3px 8px; border-radius: 6px; margin-right: 6px; font-weight: 600; }
    .tag-transport { background: #e0f2fe; color: #0369a1; }
    .tag-food { background: #dcfce7; color: #15803d; }
    .tag-stay { background: #f3e8ff; color: #7e22ce; }
    .tag-sight { background: #ffedd5; color: #c2410c; }
    </style>
    <div class="app-header">WANDERFLOW ❄️ HOKKAIDO</div>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 功能函式 (天氣 & AI)
# ==========================================
def get_live_weather(city_name):
    # 簡單對照表
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
        return "--°C"

def get_ai_souvenirs():
    """使用 Gemini 生成伴手禮建議"""
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = """
        請擔任北海道購物專家。
        根據以下地點：札幌、小樽、函館、洞爺湖。
        推薦 5 個「除了白色戀人、六花亭以外」的在地必買伴手禮。
        請用條列式，格式為：
        **[地點] 商品名稱**：簡單介紹為什麼值得買。
        """
        try:
            response = model.generate_content(prompt)
            return response.text
        except:
            return "⚠️ AI 連線忙碌中，請稍後再試。"
    else:
        return "⚠️ 請先在 Streamlit Secrets 設定 API Key 才能呼叫 AI 喔！"

# ==========================================
# 3. 資料庫
# ==========================================
# 行程資料
itinerary = [
    {"day": "Day 1", "date": "1/28 (三)", "city": "札幌 Sapporo", "events": [
        {"time": "17:20", "title": "抵達新千歲", "type": "transport", "desc": "入境、領行李、買伴手禮", "link": "", "tags": ["飛行"]},
        {"time": "19:30", "title": "Check-in 里士滿", "type": "stay", "desc": "札幌站前", "link": "https://goo.gl/maps/placeholder", "tags": ["住宿"]},
        {"time": "20:30", "title": "湯咖哩 GARAKU", "type": "food", "desc": "狸小路排隊名店", "link": "", "tags": ["晚餐"]}
    ]},
    {"day": "Day 2", "date": "1/29 (四)", "city": "札幌 Sapporo", "events": [
        {"time": "08:00", "title": "二條市場", "type": "food", "desc": "海鮮丼早餐", "link": "", "tags": ["早餐"]},
        {"time": "10:30", "title": "北海道神宮", "type": "sight", "desc": "參拜吃判官餅", "link": "", "tags": ["景點"]},
    ]},
    {"day": "Day 3", "date": "1/30 (五)", "city": "小樽 Otaru", "events": [
        {"time": "10:30", "title": "堺町通", "type": "sight", "desc": "甜點巡禮", "link": "", "tags": ["逛街"]},
        {"time": "15:00", "title": "天狗山", "type": "sight", "desc": "百萬夜景", "link": "", "tags": ["夜景"]},
    ]},
    {"day": "Day 5", "date": "2/1 (日)", "city": "洞爺湖 Toya", "events": [
        {"time": "13:15", "title": "接駁車出發", "type": "transport", "desc": "札幌北口 -> 萬世閣", "link": "", "tags": ["交通"]},
        {"time": "20:45", "title": "冬季花火", "type": "sight", "desc": "湖畔煙火", "link": "", "tags": ["活動"]},
    ]},
    {"day": "Day 6", "date": "2/2 (一)", "city": "函館 Hakodate", "events": [
        {"time": "10:00", "title": "JR 北斗號", "type": "transport", "desc": "往函館 (約2hr)", "link": "", "tags": ["交通"]},
        {"time": "16:00", "title": "函館山夜景", "type": "sight", "desc": "搭纜車上山", "link": "", "tags": ["必看"]},
    ]}
]

# 行李清單 (分類)
checklist_data = {
    "必備證件": ["護照 (檢查效期)", "日幣現鈔", "信用卡 (吉鶴/FlyGo)", "Esim 網卡設定", "演唱會門票 (最重要！)"],
    "電器": ["行動電源 (兩顆)", "有線電棒 (無線不可)", "充電器/轉接頭", "Wifi機 (備用)"],
    "衣物": ["發熱衣 (3套)", "防滑靴", "毛帽/手套/圍巾", "睡衣"],
    "盥洗": ["牙刷牙膏", "洗面乳", "隱形眼鏡", "常備藥品 (腸胃/感冒)"]
}

# ==========================================
# 4. 側邊欄導航
# ==========================================
with st.sidebar:
    st.title("❄️ 選單")
    # 使用 radio button 做頁面切換
    page = st.radio(
        "前往頁面",
        ["📅 每日行程", "✈️ 航班與住宿", "✅ 行李 Check List", "🎁 AI 伴手禮推薦"]
    )
    st.divider()
    st.caption("2026 Hokkaido Trip")

# ==========================================
# 5. 頁面內容邏輯
# ==========================================

# --- 頁面 1: 每日行程 (原本的功能) ---
if page == "📅 每日行程":
    # 日期選擇
    day_labels = [d["date"] for d in itinerary]
    idx = st.selectbox("選擇日期", range(len(day_labels)), format_func=lambda x: day_labels[x])
    plan = itinerary[idx]
    
    # Hero Card
    temp = get_live_weather(plan['city'])
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e293b,#0f172a);color:white;padding:20px;border-radius:20px;margin-bottom:20px;box-shadow:0 10px 20px rgba(0,0,0,0.1);">
        <div style="font-size:14px;opacity:0.8;">{plan['day']} • {plan['date']}</div>
        <div style="font-size:32px;font-weight:bold;">{plan['city']}</div>
        <div style="background:rgba(255,255,255,0.2);padding:5px 15px;border-radius:15px;display:inline-block;margin-top:10px;">
            🌡️ 即時氣溫：{temp}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Timeline
    for evt in plan['events']:
        # Tag Color Logic
        bg_col = "#e0f2fe" if evt['type']=='transport' else "#dcfce7" if evt['type']=='food' else "#ffedd5"
        tags_html = "".join([f"<span style='background:{bg_col};padding:2px 8px;border-radius:4px;font-size:12px;margin-right:5px;color:#333'>{t}</span>" for t in evt['tags']])
        
        st.markdown(f"""
        <div style="display:flex;margin-bottom:15px;">
            <div style="width:60px;text-align:right;padding-right:15px;color:#64748b;font-weight:bold;padding-top:10px;">{evt['time']}</div>
            <div style="flex:1;background:white;padding:15px;border-radius:12px;box-shadow:0 2px 5px rgba(0,0,0,0.05);border:1px solid #f1f5f9;">
                <div style="font-weight:bold;color:#334155;">{evt['title']}</div>
                <div style="font-size:14px;color:#64748b;margin:5px 0;">{evt['desc']}</div>
                <div>{tags_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if evt['link']:
            c1, c2 = st.columns([1,4])
            with c2: st.link_button("📍 導航", evt['link'])

# --- 頁面 2: 航班與住宿 ---
elif page == "✈️ 航班與住宿":
    st.subheader("✈️ 航班資訊")
    
    # 去程
    st.markdown("""
    <div class="info-card flight-card">
        <div class="card-title">🛫 去程：酷航 Scoot TR892</div>
        <div class="card-content">
            <b>日期：</b> 2026/1/28 (三)<br>
            <b>時間：</b> 12:30 TPE 桃園 T1 ➝ 17:20 CTS 新千歲<br>
            <b>行李：</b> 手提 10kg / 托運 30kg
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 回程
    st.markdown("""
    <div class="info-card flight-card">
        <div class="card-title">🛬 回程：泰越捷 Thai Vietjet VZ571</div>
        <div class="card-content">
            <b>日期：</b> 2026/2/6 (五)<br>
            <b>時間：</b> 09:30 CTS 新千歲 ➝ 13:30 TPE 桃園<br>
            <b>行李：</b> 手提 7kg / 托運 40kg
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🏨 住宿總表")
    
    hotels = [
        {"name": "札幌站前里士滿飯店", "date": "1/28 - 2/1 (4晚)", "note": "含早餐，近札幌站南口", "price": "¥57,678"},
        {"name": "洞爺湖萬世閣", "date": "2/1 - 2/2 (1晚)", "note": "含早晚餐，有免費接駁車(需預約)", "price": "¥32,949"},
        {"name": "HOTEL MYSTAYS Hakodate", "date": "2/2 - 2/4 (2晚)", "note": "函館站旁，交通方便", "price": "¥12,096"},
        {"name": "Rembrandt Style Sapporo", "date": "2/4 - 2/6 (2晚)", "note": "近薄野，方便逛雪祭", "price": "TWD 8,540"}
    ]
    
    for h in hotels:
        st.markdown(f"""
        <div class="info-card hotel-card">
            <div class="card-title">🏨 {h['name']}</div>
            <div class="card-content">
                <b>日期：</b> {h['date']}<br>
                <b>費用：</b> {h['price']}<br>
                <span style="background:#f3e8ff;padding:2px 6px;border-radius:4px;font-size:12px;color:#7e22ce;">{h['note']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 頁面 3: 行李 Check List ---
elif page == "✅ 行李 Check List":
    st.subheader("🎒 打包清單")
    st.caption("勾選後會自動儲存狀態 (重新整理網頁會重置)")

    # 初始化 session_state 用來存勾選狀態
    if "checklist" not in st.session_state:
        st.session_state.checklist = {}

    # 計算進度
    total_items = sum(len(items) for items in checklist_data.values())
    checked_items = 0

    # 顯示清單
    for category, items in checklist_data.items():
        st.markdown(f"**{category}**")
        for item in items:
            # 建立唯一的 key
            key = f"{category}_{item}"
            # 檢查並初始化狀態
            if key not in st.session_state.checklist:
                st.session_state.checklist[key] = False
            
            # 顯示 Checkbox
            is_checked = st.checkbox(item, key=key)
            if is_checked:
                checked_items += 1
        st.divider()

    # 顯示進度條 (放在最上面會更好，這裡示範簡單排版)
    progress = checked_items / total_items if total_items > 0 else 0
    st.sidebar.markdown(f"### 打包進度: {int(progress*100)}%")
    st.sidebar.progress(progress)

# --- 頁面 4: AI 伴手禮推薦 ---
elif page == "🎁 AI 伴手禮推薦":
    st.subheader("🛍️ 伴手禮購物清單")
    
    # 你的固定清單
    st.markdown("#### 📝 你的必買清單")
    st.info("六花亭 (葡萄奶油、核桃)、札幌農學餅乾、LeTAO (機場買)、北菓樓泡芙")
    
    st.divider()
    
    st.markdown("#### 🤖 AI 隱藏版推薦")
    st.caption("覺得買不夠嗎？讓 AI 幫你找找在地人推薦的好物！")
    
    if st.button("✨ 生成 AI 推薦清單"):
        with st.spinner("AI 正在搜尋北海道好吃的..."):
            result = get_ai_souvenirs()
            st.markdown(f"""
            <div class="ai-suggestion">
                {result}
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("---")
    st.caption("💡 小提醒：液體類 (布丁、果醬) 記得要托運喔！")
