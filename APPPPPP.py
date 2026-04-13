import streamlit as st
import pandas as pd
import numpy as np

# Баптаулар
st.set_page_config(page_title="Культиватор Аналитикасы", layout="wide")
st.title("S-тәрізді тіреудің Физика-Экономикалық моделі")

# Бүйірлік панель (Слайдерлер)
st.sidebar.header("1. Агротехникалық параметрлер")
k = st.sidebar.slider("Топырақтың меншікті кедергісі (Па)", 30000, 80000, 50000, 1000)
a = st.sidebar.slider("Қопсыту тереңдігі, a (м)", 0.10, 0.20, 0.15, 0.01)
b = st.sidebar.slider("Табанның қамту ені, b (м)", 0.10, 0.25, 0.15, 0.01)

st.sidebar.markdown("---")
st.sidebar.header("2. Экономикалық деректер")
area = st.sidebar.number_input("Егістік аумағы (гектар)", value=500, step=50)
fuel_price = st.sidebar.number_input("Дизель бағасы (тг/литр)", value=295, step=5)

# Тұрақты шамалар
length = 0.45
width = 0.045
thickness = 0.012
E = 2.1 * 10**11       
sigma_u = 450 * 10**6  
base_fuel_rate = 7.5

# Есептеулер (Физика + Экономика)
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

# Нәтижелерді шығару
col1, col2 = st.columns(2)

with col1:
    st.header("Инженерлік көрсеткіштер")
    st.metric(label="Тарту кедергісі (бір тіреуге)", value=f"{P_v:.2f} Н", delta="-15% динамикалық үнемдеу")
    st.metric(label="Майысу деформациясы (f)", value=f"{f * 1000:.2f} мм")
    if sigma_max <= sigma_u:
        st.success(f"✅ **Құрылым сенімді!** Кернеу {sigma_max / 10**6:.2f} МПа (Шек: 450 МПа).")
    else:
        st.error(f"⚠️ **АПАТ ҚАУПІ!** Кернеу {sigma_max / 10**6:.2f} МПа. Тіреу сынуы мүмкін!")

with col2:
    st.header("Экономикалық тиімділік")
    st.metric(label="Жалпы үнемделген жанармай", value=f"{total_saved_fuel:.0f} литр")
    st.metric(label="Қаржылық үнемдеу (Маусым үшін)", value=f"{total_saved_money:,.0f} ₸".replace(",", " "))

st.markdown("---")
st.header("Аналитика: Металл кернеуінің өңдеу тереңдігіне тәуелділігі")

# Графикті Streamlit арқылы сызу
depth_array = np.linspace(0.10, 0.25, 20)
stress_array = (((k * depth_array * b * 0.85) * length) / W) / 10**6
chart_data = pd.DataFrame({'Тереңдік (м)': depth_array, 'Есептік кернеу (МПа)': stress_array})
chart_data.set_index('Тереңдік (м)', inplace=True)

st.line_chart(chart_data)
st.caption("Егер график 450 МПа шегінен асса, бұл қауіпті аймақты білдіреді.")
