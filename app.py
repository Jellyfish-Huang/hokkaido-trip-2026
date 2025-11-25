import streamlit as st
import streamlit.components.v1 as components # 這是用來嵌入天氣小工具的元件

# ==========================================
# 1. 介面設定
# ==========================================
st.set_page_config(
    page_title="2026 北海道旅",
    page_icon="🗻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* 背景色：日式米白 */
    .stApp {
        background-color: #fcfaf2;
        font-family: "Helvetica Neue", "Microsoft JhengHei", sans-serif;
    }
    #MainMenu, footer {visibility: hidden;}
    
    /* 標籤 Tag 樣式 */
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        margin-right: 5px;
        font-weight: 500;
    }
    .tag-food {background-color: #e8f5e9; color: #2e7d32; border: 1px solid #c8e6c9;}
    .tag-buy {background-color: #fff3e0; color: #ef6c00; border: 1px solid #ffe0b2;}
    .tag-tip {background-color: #e3f2fd; color: #1565c0; border: 1px solid #bbdefb;}
    
    /* AI 攻略區塊 */
    .ai-box {
        background-color: #f5f5f5;
        border-left: 4px solid #6c5ce7;
        padding: 10px;
        border-radius: 4px;
        margin-top: 10px;
        font-size: 14px;
        color: #444;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 天氣小工具函式 (Magic Box)
# ==========================================
def show_weather_widget(city_code, city_name):
    """
    這裡使用 WeatherWidget.io 的免費服務
    """
    # 這是嵌入碼的模板
    html_code = f"""
    <a class="weatherwidget-io" href="https://forecast7.com/en/{city_code}/" data-label_1="{city_name}" data-label_2="WEATHER" data-font="Roboto" data-icons="Climacons Animated" data-mode="Current" data-theme="pure" >{city_name} WEATHER</a>
    <script>
    !function(d,s,id){{var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){{js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}}}(document,'script','weatherwidget-io-js');
    </script>
    """
    # 在 Streamlit 中渲染 HTML，高度設為 100px 剛好
    components.html(html_code, height=110)

# ==========================================
# 3. 行程資料庫 (新增了 weather_code 欄位)
# ==========================================
# 代碼對照：
# 札幌: 43d06141d35/sapporo
# 小樽: 43d19141d00/otaru
# 函館: 41d77140d73/hakodate
# 洞爺湖: 42d56140d79/toyako (使用虻田郡代碼)

schedule_data = {
    "Day 1 (1/28 抵達)": {
        "city": "SAPPORO", 
        "weather_code": "43d06141d35/sapporo", # 札幌代碼
        "events": [
            {
                "time": "17:20", "icon": "🛬", "title": "抵達新千歲空港", "loc": "New Chitose Airport",
                "desc": "入境、領行李、買伴手禮",
                "tags": [("必買", "Kinotoya起司塔"), ("必買", "美瑛選果玉米麵包")],
                "ai_tip": "💡 國內線航廈比較好逛！建議先去國內線 2F 買伴手禮。JR 車站在 B1。"
            },
            {
                "time": "19:30", "icon": "🏨", "title": "Check-in 里士滿", "loc": "Richmond Hotel Sapporo Ekimae",
                "desc": "JR 札幌站南口步行 5 分鐘",
                "tags": [("重要", "護照"), ("訂單", "123456")],
                "ai_tip": "💡 飯店對面就有 Lawson，建議先買好隔天要去動物園的早餐與大瓶水。"
            },
             {
                "time": "20:30", "icon": "🍛", "title": "晚餐：湯咖哩 GARAKU", "loc": "Soup Curry GARAKU",
                "desc": "狸小路排隊名店",
                "tags": [("必吃", "雞腿湯咖哩"), ("必加", "起司飯")],
                "ai_tip": "💡 這裡不能預約，要現場抽號碼牌。如果等太久，轉角有一家「Suage+」也是名店。"
            }
        ]
    },
    "Day 2 (1/29 市區)": {
        "city": "SAPPORO",
        "weather_code": "43d06141d35/sapporo",
        "events": [
            {
                "time": "08:00", "icon": "🦀", "title": "二條市場早餐", "loc": "Nijo Market",
                "desc": "體驗當地人的廚房",
                "tags": [("必吃", "海膽丼"), ("必吃", "哈密瓜")],
                "ai_tip": "💡 推薦「大磯」或「丼兵衛」。別忘了買乾干貝當零食！"
            },
            {
                "time": "10:30", "icon": "⛩️", "title": "北海道神宮", "loc": "Hokkaido Jingu",
                "desc": "圓山公園散步",
                "tags": [("必買", "拉拉熊繪馬"), ("必吃", "六花亭判官餅")],
                "ai_tip": "💡 判官餅是神宮內的六花亭茶屋限定，現場烤熱熱的超好吃。"
            },
             {
                "time": "14:00", "icon": "☕", "title": "森彥咖啡", "loc": "Morihico Coffee",
                "desc": "木造老屋文青咖啡",
                "tags": [("氣氛", "安靜"), ("推薦", "手沖")],
                "ai_tip": "💡 這是本店（木造房），氣氛最好。座位不多，不能大聲喧嘩。"
            }
        ]
    },
    "Day 3 (1/30 小樽)": {
        "city": "OTARU",
        "weather_code": "43d19141d00/otaru", # 小樽代碼
        "events": [
            {
                "time": "10:30", "icon": "🍰", "title": "堺町通商店街", "loc": "Sakaimachi Street",
                "desc": "甜點與玻璃藝品",
                "tags": [("必吃", "北菓樓泡芙"), ("必吃", "LeTAO紅茶巧克力")],
                "ai_tip": "💡 六花亭二樓有位子可以坐著吃買來的點心，牛奶也很濃！"
            },
            {
                "time": "15:00", "icon": "🚠", "title": "天狗山夜景", "loc": "Otaru Tenguyama Ropeway",
                "desc": "情書拍攝地，北海道三大夜景",
                "tags": [("注意", "保暖"), ("攝影", "藍調時刻")],
                "ai_tip": "💡 冬天這裡風超級大！圍巾帽子手套一定要戴好。建議 15:30 左右上山。"
            }
        ]
    },
    "Day 4 (1/31 札幌)": { # 假設這天回札幌
        "city": "SAPPORO",
        "weather_code": "43d06141d35/sapporo",
        "events": [
            { "time": "10:00", "icon": "🏫", "title": "北海道大學", "loc": "Hokkaido University", "desc": "白楊林蔭道", "tags":[], "ai_tip": "博物館免費參觀" }
        ]
    },
    "Day 5 (2/1 洞爺湖)": {
        "city": "LAKE TOYA",
        "weather_code": "42d56140d79/toyako", # 洞爺湖代碼
        "events": [
            { "time": "13:15", "icon": "🚌", "title": "搭乘接駁車", "loc": "Sapporo Station North Exit", "desc": "往洞爺湖萬世閣", "tags":[("重要","別遲到")], "ai_tip": "車程約 2.5 小時" },
            { "time": "20:45", "icon": "🎆", "title": "洞爺湖煙火", "loc": "Lake Toya", "desc": "冬季煙火", "tags":[], "ai_tip": "在房間或露天溫泉看都很棒" }
        ]
    },
    "Day 6 (2/2 函館)": {
        "city": "HAKODATE",
        "weather_code": "41d77140d73/hakodate", # 函館代碼
        "events": [
            { "time": "16:00", "icon": "🌃", "title": "函館山夜景", "loc": "Mount Hakodate", "desc": "百萬夜景", "tags":[("必看","世界三大夜景")], "ai_tip": "日落時間約 16:50，建議提早一小時上山卡位。" }
        ]
    }
}

# ==========================================
# 4. 頁面呈現
# ==========================================

with st.sidebar:
    st.title("🗻 2026 北海道")
    page = st.radio("MENU", ["行程規劃", "住宿憑證", "記帳小幫手"])
    st.divider()
    st.caption("Designed for 2026 Trip")

if page == "行程規劃":
    # 1. 選擇日期
    days = list(schedule_data.keys())
    selected_day = st.selectbox("📅 選擇日期", days)
    day_info = schedule_data[selected_day]
    
    # 2. 顯示天氣小工具 (Magic Happens Here!)
    st.caption(f"📍 Current Weather in {day_info['city']}")
    # 呼叫函式，傳入該城市的代碼與名稱
    show_weather_widget(day_info['weather_code'], day_info['city'])
    
    st.divider() # 分隔線
    st.caption("👇 點擊卡片查看詳細攻略")

    # 3. 顯示行程卡片
    for event in day_info['events']:
        label_text = f"{event['time']}　{event['icon']}　{event['title']}"
        
        with st.expander(label_text):
            # Tags
            tag_html = ""
            for tag_type, tag_text in event.get('tags', []):
                cls = "tag-tip"
                if tag_type == "必吃": cls = "tag-food"
                if tag_type == "必買": cls = "tag-buy"
                tag_html += f"<span class='tag {cls}'>{tag_text}</span>"
            st.markdown(tag_html, unsafe_allow_html=True)
            
            # 描述
            st.markdown(f"**{event['desc']}**")
            
            # AI Tip
            if 'ai_tip' in event:
                st.markdown(f"""
                <div class="ai-box">
                    <b>🤖 AI 導遊筆記：</b><br>
                    {event['ai_tip']}
                </div>
                """, unsafe_allow_html=True)
            
            # Google Maps Button
            map_url = f"https://www.google.com/maps/search/?api=1&query={event['loc']}"
            st.link_button("📍 開啟 Google Maps 導航", map_url, use_container_width=True)

# 其他頁面保持精簡 (避免程式碼太長)
elif page == "住宿憑證":
    st.title("🏨 住宿資訊")
    with st.expander("1/28 - 2/1 札幌里士滿"):
        st.info("Booking ID: 123456")
        st.link_button("📍 導航到飯店", "https://maps.google.com/?q=Richmond+Hotel+Sapporo+Ekimae")
elif page == "記帳小幫手":
    st.title("💰 記帳")
    st.info("此功能請參考上一版程式碼加入即可")
