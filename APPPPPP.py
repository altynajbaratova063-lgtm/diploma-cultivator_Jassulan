import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px  # Жаңа интерактивті графиктерге арналған кітапхана

# 1. Баптаулар және Брендтеу
st.set_page_config(page_title="Агро Аналитика: КОН-2,8", page_icon="🚜", layout="wide")
st.title("🚜 «АСЫЛ ТҰҚЫМ» ЖШС: КОН-2,8 культиваторының тиімділігі")
st.markdown("---")

# 2. Бүйірлік панель және Нұсқаулық
with st.sidebar:
    st.header("📌 Нұсқаулық")
    st.info("""
    Бұл веб-қосымша **КОН-2,8** (Қатар аралығын өңдейтін культиватор) агрегаты үшін әзірленген.
    Сызбада көрсетілгендей, оңтайлы жылдамдық 6-9 км/сағ аралығында болуы тиіс.
    """)
    st.success("Дипломдық жұмыстың конструкторлық бөліміне негізделген")
    st.markdown("---")
    
    st.header("1. Агротехникалық параметрлер")
    B = st.slider("Қамту ені, B (м)", 2.0, 4.0, 2.8, 0.1) 
    a = st.slider("Өңдеу тереңдігі, a (см)", 6, 15, 10, 1)
    v = st.slider("Жұмыс жылдамдығы, V (км/сағ)", 5.0, 12.0, 7.5, 0.5)
    k = st.slider("Топырақтың меншікті кедергісі, k (кН/м²)", 10.0, 30.0, 15.0, 1.0)

    st.markdown("---")
    st.header("2. Экономикалық деректер")
    area = st.number_input("Егістік аумағы (гектар)", min_value=1.0, value=500.0, step=50.0)
    fuel_price = st.number_input("Дизель бағасы (тг/литр)", min_value=1.0, value=295.0, step=5.0)

# 3. Физикалық және Экономикалық есептеулер
a_meters = a / 100  # см-ді метрге айналдыру
R_kn = k * a_meters * B  
R_n = R_kn * 1000

eta_t = 0.7  
N_kw = (R_kn * (v / 3.6)) / eta_t
N_hp = N_kw * 1.36  

tau = 0.8  
W_hour = 0.1 * B * v * tau
W_shift = W_hour * 8  

fuel_norm = 6.5  
saved_fuel = fuel_norm * 0.10 * area
saved_money = saved_fuel * fuel_price

# 4. Нәтижелерді экранға шығару
col1, col2 = st.columns(2)

with col1:
    st.header("⚙️ Техникалық көрсеткіштер")
    st.metric(label="Жалпы тарту кедергісі (R)", value=f"{R_n:,.0f} Н".replace(",", " "))
    st.metric(label="Трактордың қажетті қуаты", value=f"{N_hp:.1f} а.к.", delta="МТЗ-80/82 тракторларына сәйкес")
    
    if N_hp <= 80:
        st.success("✅ **Агрегатталу дұрыс!** МТЗ-82 тракторы бұл кедергіні еркін тарта алады.")
    else:
        st.error("⚠️ **Қуат жеткіліксіз!** Бұл тереңдікте жоғары тарту класындағы трактор қажет.")

with col2:
    st.header("📊 Пайдалану тиімділігі")
    st.metric(label="Ауысымдық өнімділік (8 сағ)", value=f"{W_shift:.1f} га/ауысым")
    st.metric(label="Маусымдық қаржылық үнемдеу", value=f"{saved_money:,.0f} ₸".replace(",", " "), delta="Жаңа жұлдызшалы қопсытқыш есебінен")

st.markdown("---")
st.header("📈 Аналитика: Жылдамдықтың жұмыс өнімділігіне әсері")

# 5. Көркем графика құру (Plotly кітапханасымен)
speed_array = np.linspace(5.0, 12.0, 20)
prod_array = 0.1 * B * speed_array * tau * 8  

# Мәліметтерді DataFrame-ге жинау
chart_data = pd.DataFrame({
    'Жылдамдық (км/сағ)': speed_array, 
    'Өнімділік (га/ауысым)': prod_array
})

# Plotly арқылы әдемі график құру
fig = px.line(chart_data, x='Жылдамдық (км/сағ)', y='Өнімділік (га/ауысым)', 
              title='Жылдамдық пен Өнімділік тәуелділігі',
              labels={'Өнімділік (га/ауысым)': 'Ауысымдық өнімділік (га/ауысым)'},
              markers=True  # Деректер нүктелерін көрсету
             )

# Графиктің дизайнын теңшеу
fig.update_traces(line=dict(width=3, color='forestgreen'), marker=dict(size=8, color='darkorange')) # Сызық пен нүкте түсі
fig.update_layout(title_font_size=20, font_size=14, template='plotly_white') # Артқы фон түсі

# Оңтайлы жылдамдық аймағын бояп көрсету (Оңтайлы 6-9 км/сағ)
fig.add_vrect(x0=6.0, x1=9.0, fillcolor="lightgreen", opacity=0.3, layer="below", line_width=0,
              annotation_text="Оңтайлы жылдамдық", annotation_position="top left")

# Жаңа көркем графикті шығару
st.plotly_chart(fig, use_container_width=True)

st.caption("График жұмыс жылдамдығы артқан сайын ауысымдық өнімділіктің қалай өсетінін көрсетеді. Сызбаға сәйкес оңтайлы жұмыс жылдамдығы 6-9 км/сағ (жасыл аймақ) аралығында сақталуы тиіс.")
