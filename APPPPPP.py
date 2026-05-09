import streamlit as st
import pandas as pd
import numpy as np

# 1. Баптаулар және Брендтеу
st.set_page_config(page_title="Агро Аналитика: АСЫЛ ТҰҚЫМ", page_icon="🌾", layout="wide")
st.title("🌾 «АСЫЛ ТҰҚЫМ» ЖШС: Культиватор тіреуінің Физика-Экономикалық моделі")
st.markdown("---")

# 2. Бүйірлік панель және Нұсқаулық
with st.sidebar:
    st.header("📌 Нұсқаулық")
    st.info("""
    Бұл веб-қосымша **«АСЫЛ ТҰҚЫМ» ЖШС** үшін әзірленген.
    Мұнда S-тәрізді тіреудің физикалық төзімділігін және одан келетін экономикалық үнемдеуді есептей аласыз.
    """)
    st.success("Дипломдық жұмыстың тәжірибелік бөлімі")
    st.markdown("---")
    
    st.header("1. Агротехникалық параметрлер")
    k = st.slider("Топырақтың меншікті кедергісі (Па)", 30000, 80000, 50000, 1000)
    a = st.slider("Қопсыту тереңдігі, a (м)", 0.10, 0.20, 0.15, 0.01)
    b = st.slider("Табанның қамту ені, b (м)", 0.10, 0.25, 0.15, 0.01)

    st.markdown("---")
    st.header("2. Экономикалық деректер")
    # min_value=1.0 арқылы теріс сан енгізуге тыйым салынды (Валидация)
    area = st.number_input("Егістік аумағы (гектар)", min_value=1.0, value=500.0, step=50.0)
    fuel_price = st.number_input("Дизель бағасы (тг/литр)", min_value=1.0, value=295.0, step=5.0)

# 3. Тұрақты шамалар
length = 0.45
width = 0.045
thickness = 0.012
E = 2.1 * 10**11       
sigma_u = 450 * 10**6  
base_fuel_rate = 7.5

# 4. Есептеулер (Физика + Экономика)
P_0 = k * a * b          
P_v = P_0 * 0.85         
J = (width * thickness ** 3) / 12  
W = (width * thickness ** 2) / 6   
M_max = P_v * length     
sigma_max = M_max / W    
f = (P_v * length ** 3) / (3 * E * J)  

saved_fuel_per_ha = base_fuel_rate * 0.12
total_saved_fuel = saved_fuel_per_ha * area
total_saved_money = total_saved_fuel * fuel_price

# 5. Нәтижелерді шығару
col1, col2 = st.columns(2)

with col1:
    st.header("⚙️ Инженерлік көрсеткіштер")
    st.metric(label="Тарту кедергісі (бір тіреуге)", value=f"{P_v:.2f} Н", delta="-15% динамикалық үнемдеу")
    st.metric(label="Майысу деформациясы (f)", value=f"{f * 1000:.2f} мм")
    if sigma_max <= sigma_u:
        st.success(f"✅ **Құрылым сенімді!** Кернеу {sigma_max / 10**6:.2f} МПа (Шек: 450 МПа).")
    else:
        st.error(f"⚠️ **АПАТ ҚАУПІ!** Кернеу {sigma_max / 10**6:.2f} МПа. Тіреу сынуы мүмкін!")

with col2:
    st.header("💰 Экономикалық тиімділік")
    # Сандарды мыңдықтарға бөліп, әдемі көрсету
    st.metric(label="Жалпы үнемделген жанармай", value=f"{total_saved_fuel:,.0f} литр".replace(",", " "))
    st.metric(label="Қаржылық үнемдеу (Маусым үшін)", value=f"{total_saved_money:,.0f} ₸".replace(",", " "))

st.markdown("---")
st.header("📊 Аналитика: Металл кернеуінің өңдеу тереңдігіне тәуелділігі")

# 6. Графикті Streamlit арқылы сызу (Шекті сызықты қосу)
depth_array = np.linspace(0.10, 0.25, 20)
stress_array = (((k * depth_array * b * 0.85) * length) / W) / 10**6
limit_array = np.full_like(depth_array, 450) # 450 МПа шегін көрсететін тұрақты сызық

chart_data = pd.DataFrame({
    'Тереңдік (м)': depth_array, 
    'Есептік кернеу (МПа)': stress_array,
    'Шекті кернеу (450 МПа)': limit_array
})
chart_data.set_index('Тереңдік (м)', inplace=True)

st.line_chart(chart_data)

# Үзіліп қалған мәтін толықтырылды
st.caption("Ескерту: Егер есептік кернеу графигі 450 МПа шегінен асып кетсе, культиватор тіреуінің сыну қаупі бар деген сөз. Сондықтан топырақ кедергісіне қарай тереңдікті немесе қамту енін азайту қажет.")
