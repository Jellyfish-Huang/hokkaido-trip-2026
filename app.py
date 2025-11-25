import streamlit as st
import pandas as pd

# ==========================================
# 1. 介面設定與 CSS 優化
# ==========================================
st.set_page_config(
    page_title="2026 北海道旅",
    page_icon="🗻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 重點：讓 Expander 看起來像一張卡片，並優化內部排版
st.markdown("""
    <style>
    /* 背景色：日式米白 */
    .stApp {
        background-color: #fcfaf2;
        font-family: "Helvetica Neue", "Microsoft JhengHei", sans-serif;
    }
    
    /* 隱藏預設選單 */
    #MainMenu, footer {visibility: hidden;}
    
    /* 標籤 Tag 樣式 */
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 13px;
        margin-right: 6px;
        font-weight: 500;
        margin-bottom: 5px;
    }
    .tag-food {background-color: #e8f5e9; color: #2e7d32; border: 1px solid #c8e6c9;}
    .tag-buy {background-color: #fff3e0; color: #ef6c00; border: 1px solid #ffe0b2;}
    .tag-tip {background-color: #e3f2fd; color: #1565c0; border: 1px solid #bbdefb;}
    
    /* AI 攻略區塊樣式 */
    .ai-box {
        background-color: #f5f5f5;
        border-left: 4px solid #6c5ce7;
        padding: 10px 15px;
        border-radius: 4px;
        margin-top: 10px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #444;
        line-height: 1.6;
    }
    
    /* 調整 Expander 的外觀 (Streamlit 原生限制較多，盡量優化) */
    .streamlit-expanderHeader {
        font-size: 18px;
        font-weight: 600;
        color: #333;
        background-color: white;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 行程資料庫 (可隨時擴充)
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
                "ai_tip": "💡 國內線航廈比較好逛！建議先去國內線 2F 買伴手禮（有些不能過海關，要先吃掉或放行李箱）。JR 車站在 B1。"
            },
            {
                "time": "19:30", "icon": "🏨", "title": "Check-in 里士滿", "loc": "Richmond Hotel Sapporo Ekimae",
                "desc": "JR 札幌站南口步行 5 分鐘",
                "tags": [("重要", "護照"), ("訂單", "123456")],
                "ai_tip": "💡 櫃台在 2 樓。飯店對面就有 Lawson，建議先買好隔天要去動物園的早餐與大瓶水。"
            },
            {
                "time": "20:30", "icon": "🍛", "title": "晚餐：湯咖哩 GARAKU", "loc": "Soup Curry GARAKU",
                "desc": "狸小路排隊名店",
                "tags": [("必吃", "雞腿湯咖哩"), ("必加", "起司飯")],
                "ai_tip": "💡 這裡不能預約，要現場抽號碼牌。如果等太久，轉角有一家「Suage+」也是名店，口味較清爽。"
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
                "ai_tip": "💡 推薦「大磯」或「丼兵衛」。別忘了買乾干貝當零食！早點去才不用排太久。"
            },
            {
                "time": "10:30", "icon": "⛩️", "title": "北海道神宮", "loc": "Hokkaido Jingu",
                "desc": "圓山公園散步",
                "tags": [("必買", "拉拉熊繪馬"), ("必吃", "六花亭判官餅")],
                "ai_tip": "💡 判官餅是神宮內的六花亭茶屋限定，現場烤熱熱的超好吃，配免費熱茶剛剛好。雪地路滑，慢慢走。"
            },
            {
                "time": "14:00", "icon": "☕", "title": "森彥咖啡", "loc": "Morihico Coffee",
                "desc": "木造老屋文青咖啡",
                "tags": [("氣氛", "安靜"), ("推薦", "手沖")],
                "ai_tip": "💡 這是本店（木造房），氣氛最好。座位不多，不能大聲喧嘩。如果客滿，附近的「円山動物園」也值得一逛。"
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
                "ai_tip": "💡 六花亭二樓有位子可以坐著吃買來的點心，牛奶也很濃！這條街很長，建議從南小樽站下車，往小樽站方向逛比較順路。"
            },
            {
                "time": "15:00", "icon": "🚠", "title": "天狗山夜景", "loc": "Otaru Tenguyama Ropeway",
                "desc": "情書拍攝地，北海道三大夜景",
                "tags": [("注意", "保暖"), ("攝影", "藍調時刻")],
                "ai_tip": "💡 冬天這裡風超級大！圍巾帽子手套一定要戴好。建議 15:30 左右上山，可以同時看到白天雪景和傍晚點燈後的夜景。"
            }
        ]
    }
}

# ==========================================
# 3. 頁面邏輯
# ==========================================

with st.sidebar:
    st.title("🗻 2026 北海道")
    page = st.radio("MENU", ["行程規劃", "住宿憑證", "記帳小幫手"])
    st.divider()
    st.caption("Designed for 2026 Trip")

# --- 頁面 1: 行程規劃 (點擊展開式) ---
if page == "行程規劃":
    # 日期選擇器
    days = list(schedule_data.keys())
    selected_day = st.selectbox("📅 選擇日期", days)
    
    day_info = schedule_data[selected_day]
    
    # 頂部 Hero Section (現在地點 + 天氣)
    st.markdown(f"""
    <div style="padding: 15px; background: white; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
        <div style="font-size: 12px; color: #888;">CURRENT LOCATION</div>
        <div style="font-size: 24px; font-weight: bold; color: #333;">
            {day_info['city']} <span style="font-size:18px; color: #666;">{day_info['weather']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("👇 點擊卡片查看攻略與導航")

    # 迴圈生成折疊卡片
    for event in day_info['events']:
        # 卡片標題：時間 + Icon + 地點名稱
        label_text = f"{event['time']}　{event['icon']}　{event['title']}"
        
        # 使用 st.expander 製作可展開的效果
        with st.expander(label_text):
            
            # 1. 標籤區 (Tags)
            tag_html = ""
            for tag_type, tag_text in event.get('tags', []):
                cls = "tag-tip"
                if tag_type == "必吃": cls = "tag-food"
                if tag_type == "必買": cls = "tag-buy"
                tag_html += f"<span class='tag {cls}'>{tag_text}</span>"
            st.markdown(tag_html, unsafe_allow_html=True)
            
            # 2. 簡述
            st.markdown(f"**{event['desc']}**")
            
            # 3. AI 攻略區 (重點！)
            if 'ai_tip' in event:
                st.markdown(f"""
                <div class="ai-box">
                    <b>🤖 AI 導遊筆記：</b><br>
                    {event['ai_tip']}
                </div>
                """, unsafe_allow_html=True)
            
            # 4. 導航按鈕 (直接連結 Google Maps)
            # 這裡我們做一個明顯的按鈕
            map_url = f"https://www.google.com/maps/search/?api=1&query={event['loc']}"
            st.link_button("📍 開啟 Google Maps 導航", map_url, use_container_width=True)

# --- 頁面 2: 住宿憑證 ---
elif page == "住宿憑證":
    st.title("🏨 住宿資訊")
    
    with st.expander("1/28 - 2/1 札幌里士滿 (Richmond)"):
        st.info("📅 1/28 Check-in (14:00) - 2/1 Check-out (11:00)")
        st.markdown("**Booking編號:** 12345678")
        st.markdown("**電話:** +81 11-222-0055")
        st.link_button("📍 導航到飯店", "https://maps.google.com/?q=Richmond+Hotel+Sapporo+Ekimae")
        
    with st.expander("2/1 - 2/2 洞爺湖萬世閣"):
        st.info("📅 2/1 Check-in (15:00) - 2/2 Check-out (10:00)")
        st.warning("⚠️ 記得 13:15 在札幌站北口搭接駁車！")
        st.markdown("**晚餐:** 自助餐 (18:00)")

# --- 頁面 3: 記帳 ---
elif page == "記帳小幫手":
    st.title("💰 記帳")
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
        
    with st.form("add_expense"):
        c1, c2 = st.columns([2, 1])
        item = c1.text_input("項目")
        cost = c2.number_input("日幣", min_value=0, step=100)
        if st.form_submit_button("新增"):
            st.session_state.expenses.append({"item": item, "cost": cost})
            st.rerun()
            
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.table(df)
        total = df['cost'].sum()
        st.metric("總支出", f"¥{total:,}")
        st.caption(f"約台幣 {total*0.22:,.0f} 元")
