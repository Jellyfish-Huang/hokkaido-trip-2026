import streamlit as st
import pandas as pd

# ==========================================
# 1. 日式極簡風格設定 (CSS Magic)
# ==========================================
st.set_page_config(
    page_title="Hokkaido 2026",
    page_icon="🗻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 定義日式配色：白練 (背景)、墨色 (字)、藍鼠 (強調)、紅鳶 (警示)
st.markdown("""
    <style>
    /* 全域設定 */
    .stApp {
        background-color: #fcfaf2; /* 白練色：像和紙一樣的米白 */
        color: #2b2b2b; /* 墨色 */
        font-family: "Helvetica Neue", "PingFang TC", "Microsoft JhengHei", sans-serif;
    }
    
    /* 隱藏多餘元素 */
    #MainMenu, footer {visibility: hidden;}
    
    /* 卡片設計 - 極簡風 */
    .zen-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px; /* 較小的圓角 */
        box-shadow: 0 1px 3px rgba(0,0,0,0.05); /* 非常淡的陰影 */
        margin-bottom: 15px;
        border: 1px solid #efeecd;
    }
    
    /* 標籤 Tag 設計 */
    .tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        margin-right: 5px;
        font-weight: 500;
    }
    .tag-food {background-color: #e8f5e9; color: #2e7d32;} /* 必吃 */
    .tag-buy {background-color: #fff3e0; color: #ef6c00;} /* 必買 */
    .tag-tip {background-color: #e3f2fd; color: #1565c0;} /* 攻略 */
    
    /* 時間軸線條 */
    .timeline-time {
        font-family: 'Courier New', monospace;
        font-weight: bold;
        color: #9e9e9e;
        font-size: 14px;
    }
    
    /* 標題優化 */
    h1, h2, h3 {
        font-weight: 400 !important;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 智慧行程資料庫 (已幫你擴充 AI 建議)
# ==========================================
schedule_data = {
    "Day 1 (1/28 抵達)": {
        "city": "Sapporo", 
        "weather": "❄️ -3°C",
        "events": [
            {
                "time": "17:20", "icon": "🛬", "title": "抵達新千歲空港", "loc": "New Chitose Airport",
                "desc": "入境、領行李、買伴手禮",
                "tags": [("必買", "Kinotoya起司塔"), ("必買", "美瑛選果玉米麵包")],
                "ai_tip": "💡 國內線航廈比較好逛！如果有時間，建議先去國內線買伴手禮再搭車，不然進市區有時候買不到限定款。"
            },
            {
                "time": "19:30", "icon": "🏨", "title": "Check-in 里士滿", "loc": "Richmond Hotel Sapporo Ekimae",
                "desc": "JR 札幌站步行 5 分鐘",
                "tags": [("重要", "護照"), ("訂單", "123456")],
                "ai_tip": "💡 飯店對面就有便利商店，建議先買好隔天早餐或大瓶水。"
            },
            {
                "time": "20:30", "icon": "🍛", "title": "晚餐：湯咖哩", "loc": "Soup Curry GARAKU",
                "desc": "狸小路排隊名店",
                "tags": [("必吃", "雞腿湯咖哩"), ("必加", "起司飯")],
                "ai_tip": "💡 這家超級排！建議先去抽號碼牌，然後去逛旁邊的唐吉訶德。"
            }
        ]
    },
    "Day 2 (1/29 市區)": {
        "city": "Sapporo",
        "weather": "☁️ -5°C", 
        "events": [
            {
                "time": "08:00", "icon": "🦀", "title": "二條市場早餐", "loc": "Nijo Market",
                "desc": "體驗當地人的廚房",
                "tags": [("必吃", "海膽丼"), ("必吃", "哈密瓜")],
                "ai_tip": "💡 推薦「大磯」或「丼兵衛」。別忘了買乾干貝當零食！"
            },
            {
                "time": "10:30", "icon": "⛩️", "title": "北海道神宮", "loc": "Hokkaido Jingu",
                "desc": "雪中神社超美",
                "tags": [("必買", "拉拉熊繪馬"), ("必吃", "六花亭判官餅")],
                "ai_tip": "💡 判官餅是神宮限定，現場烤熱熱的超好吃，配免費熱茶剛剛好。"
            },
            {
                "time": "14:00", "icon": "☕", "title": "森彥咖啡", "loc": "Morihico Coffee",
                "desc": "木造老屋文青咖啡",
                "tags": [("氣氛", "安靜")],
                "ai_tip": "💡 本店座位不多，不能大聲聊天，適合享受下雪的寧靜午後。"
            }
        ]
    },
    "Day 3 (1/30 小樽)": {
        "city": "Otaru",
        "weather": "❄️ -6°C",
        "events": [
            {
                "time": "10:30", "icon": "🍰", "title": "堺町通商店街", "loc": "Sakaimachi Street",
                "desc": "甜點與玻璃藝品",
                "tags": [("必吃", "北菓樓夢不思議泡芙"), ("必吃", "LeTAO紅茶巧克力")],
                "ai_tip": "💡 六花亭二樓有位子可以坐著吃買來的點心，牛奶也很濃！"
            },
            {
                "time": "15:00", "icon": "🚠", "title": "天狗山夜景", "loc": "Otaru Tenguyama Ropeway",
                "desc": "情書拍攝地，北海道三大夜景",
                "tags": [("注意", "保暖"), ("攝影", "藍調時刻")],
                "ai_tip": "💡 冬天這裡風超級大！圍巾帽子手套一定要戴好。日落前30分鐘就要上去卡位。"
            }
        ]
    }
}

# ==========================================
# 3. 頁面邏輯
# ==========================================

# 側邊導航
with st.sidebar:
    st.title("🗻 2026 北海道")
    page = st.radio("MENU", ["行程規劃", "住宿與航班", "記帳小幫手"])
    st.divider()
    st.caption("J人的護身符 • 日本製")

# --- 頁面 1: 行程規劃 (結合 AI 導遊) ---
if page == "行程規劃":
    days = list(schedule_data.keys())
    selected_day = st.selectbox("", days) # 空白標題保持極簡
    
    day_info = schedule_data[selected_day]
    
    # Hero Section
    st.markdown(f"""
    <div style="padding: 20px 0; border-bottom: 1px solid #eee; margin-bottom: 20px;">
        <div style="font-size: 12px; color: #888; letter-spacing: 2px;">TODAY'S LOCATION</div>
        <div style="font-size: 28px; font-weight: 300;">{day_info['city']} <span style="font-size:18px; color:#888;">{day_info['weather']}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # 顯示行程
    for event in day_info['events']:
        # 使用 Markdown 生成極簡卡片
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"<div class='timeline-time'>{event['time']}<br><span style='font-size:24px'>{event['icon']}</span></div>", unsafe_allow_html=True)
            with col2:
                # 建立卡片內容
                card_content = f"""
                <div class="zen-card">
                    <div style="font-weight: bold; font-size: 16px;">{event['title']}</div>
                    <div style="font-size: 14px; color: #666; margin-bottom: 8px;">{event['desc']}</div>
                    <div style="margin-bottom: 10px;">
                """
                # 生成標籤
                for tag_type, tag_text in event.get('tags', []):
                    cls = "tag-tip"
                    if tag_type == "必吃": cls = "tag-food"
                    if tag_type == "必買": cls = "tag-buy"
                    card_content += f"<span class='tag {cls}'>{tag_text}</span>"
                
                card_content += "</div>"
                
                # AI 小提醒區域
                if 'ai_tip' in event:
                    card_content += f"""
                    <div style="font-size: 13px; color: #555; background: #f9f9f9; padding: 10px; border-radius: 4px; border-left: 3px solid #ccc;">
                        {event['ai_tip']}
                    </div>
                    """
                card_content += "</div>"
                
                st.markdown(card_content, unsafe_allow_html=True)
                
                # 導航按鈕 (Streamlit原生按鈕無法塞進 HTML 字串，所以放外面)
                map_url = f"https://www.google.com/maps/search/?api=1&query={event['loc']}"
                st.link_button("📍 導航去這裡", map_url)

# --- 頁面 2: 住宿與航班 ---
elif page == "住宿與航班":
    st.subheader("✈️ 航班資訊")
    st.info("**去程**：1/28 酷航 TR892 (12:30 TPE - 17:20 CTS)")
    st.info("**回程**：2/6 泰越捷 VZ571 (09:30 CTS - 13:30 TPE)")
    
    st.divider()
    
    st.subheader("🏨 住宿憑證")
    with st.expander("1/28-2/1 札幌里士滿"):
        st.markdown("**Booking ID:** 12345678\n\n**地址:** 札幌市中央區北3条...")
        st.image("https://via.placeholder.com/300x150?text=Booking+Confirmation", caption="訂房截圖")

# --- 頁面 3: 記帳小幫手 ---
elif page == "記帳小幫手":
    st.subheader("💰 旅費追蹤")
    
    # 簡單的記帳功能 (使用 Session State 暫存)
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
        
    with st.form("add_expense"):
        col1, col2 = st.columns(2)
        item = col1.text_input("項目 (如: 拉麵)")
        cost = col2.number_input("金額 (日幣)", min_value=0)
        submitted = st.form_submit_button("➕ 加入")
        
        if submitted and item:
            st.session_state.expenses.append({"item": item, "cost": cost})
            st.success("已記錄！")
            
    # 顯示清單
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.table(df)
        total = df['cost'].sum()
        st.metric("目前總花費 (JPY)", f"¥{total:,.0f}", delta=None)
        st.caption(f"約合台幣 TWD {total*0.22:,.0f}")
    else:
        st.info("目前還沒有花費喔！")
