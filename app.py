import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import json

# ==============================================================================
# 0. PAGE CONFIGURATION & SETUP
# ==============================================================================
st.set_page_config(
    page_title="Dynamic E-commerce Propensity Engine",
    page_icon="✨",
    layout="wide"
)

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, [class*="st-"], [class*="css-"] { font-family: 'Poppins', sans-serif; }
    .stApp { background-color: #1C1C1C; }
    #MainMenu, footer, header { visibility: hidden; }
    div[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        border-radius: 10px; border: 1px solid #3A3A3A;
        background-color: #2C2C2C; padding: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

# ==============================================================================
# 1. CACHED DATA LOADING
# ==============================================================================
@st.cache_resource
def load_model_and_files():
    try:
        model, scaler, model_columns = (joblib.load(f) for f in ['return_prediction_model.joblib', 'scaler.joblib', 'model_columns.joblib'])
        return model, scaler, model_columns
    except FileNotFoundError: return None, None, None

@st.cache_data
def load_geojson():
    try:
        with open('europe.geojson') as f: return json.load(f)
    except FileNotFoundError: return None

model, scaler, model_columns = load_model_and_files()
europe_geojson = load_geojson()

if model is None or europe_geojson is None:
    st.error("Error: A required file (.joblib or europe.geojson) could not be loaded.")
    st.stop()

# ==============================================================================
# 2. SESSION STATE MANAGEMENT
# ==============================================================================
if 'quantity' not in st.session_state: st.session_state.quantity = 1
if 'unit_price' not in st.session_state: st.session_state.unit_price = 10.0
if 'customer_unique_products' not in st.session_state: st.session_state.customer_unique_products = 10
if 'customer_avg_price' not in st.session_state: st.session_state.customer_avg_price = 20.0
if 'selected_country' not in st.session_state: st.session_state.selected_country = 'United Kingdom'
if 'prediction_made' not in st.session_state: st.session_state.prediction_made = False
if 'prediction_proba' not in st.session_state: st.session_state.prediction_proba = 0.0

# ==============================================================================
# 3. HELPER FUNCTIONS FOR CHARTS
# ==============================================================================
def create_country_map(selected_country):
    countries_data = [{"name": n} for n in ["United Kingdom", "Germany", "France", "Ireland", "Spain", "Netherlands"]]
    df_countries = pd.DataFrame(countries_data)
    df_countries['value'] = df_countries['name'].apply(lambda x: 1 if x == selected_country else 0.2)
    fig = px.choropleth(df_countries, geojson=europe_geojson, locations="name", featureidkey="properties.NAME",
                        color="value", color_continuous_scale=[(0, "#4A4A4A"), (1, "#FFB800")], height=250)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', geo=dict(bgcolor='rgba(0,0,0,0)'), coloraxis_showscale=False)
    return fig

def create_indicator_chart(value, title):
    fig = go.Figure(go.Indicator(mode = "gauge+number", value = value,
                                 title = {'text': title, 'font': {'size': 18}},
                                 gauge = {'axis': {'range': [1, 100]}, 'bar': {'color': "#FFB800"}, 'bgcolor': "#3A3A3A"}))
    fig.update_layout(height=150, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(t=40, b=20, l=20, r=20))
    return fig

# --- FUNCTION FOR PRICE GRAPH (RESTORED) ---
def create_price_bar(current_price):
    fig = go.Figure(go.Indicator(
        mode = "number+gauge", value = current_price,
        title = {'text': "Unit Price (€)", 'font': {'size': 18}},
        gauge = {
            'shape': "bullet", 'axis' : {'range': [None, 100]},
            'bar': {'color': "#FFB800"},
            'steps': [{'range': [0, 100], 'color': "#3A3A3A"}]
        }
    ))
    fig.update_layout(height=100, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(t=40, b=20))
    return fig

def create_animated_gauge(probability):
    target_value = probability * 100
    is_high_risk = probability >= 0.5
    fill_color = "#FF4D4D" if is_high_risk else '#00E676'
    fig = go.Figure(go.Indicator(mode = "gauge+number", value = target_value, number = {'suffix': "%", 'font': {'size': 40}},
                                 title = {'text': "Return Risk Probability", 'font': {'size': 24}},
                                 gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': fill_color}}))
    fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
    return fig

# ==============================================================================
# 4. DASHBOARD LAYOUT
# ==============================================================================
st.markdown("<h1 style='text-align: center; font-weight: 700;'>✨E-commerce Propensity Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AAAAAA;'>AI-Powered Risk Assessment for E-commerce Returns</p>", unsafe_allow_html=True)

# --- Input Section ---
st.subheader("Interactive Transaction Inputs")
col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown("<h5><i class='fa-solid fa-box-open'></i> Product Metrics</h5>", unsafe_allow_html=True)
        st.session_state.quantity = st.number_input("Product Quantity", 1, 1000, st.session_state.quantity)
        st.plotly_chart(create_indicator_chart(st.session_state.quantity, "Quantity"), use_container_width=True, config={'displayModeBar': False})
        
        st.session_state.unit_price = st.number_input("Unit Price (€)", 0.1, 5000.0, st.session_state.unit_price, 0.1)
        # --- UNIT PRICE GRAPH (RESTORED) ---
        st.plotly_chart(create_price_bar(st.session_state.unit_price), use_container_width=True, config={'displayModeBar': False})

with col2:
    with st.container():
        st.markdown("<h5><i class='fa-solid fa-user-tag'></i> Customer Metrics</h5>", unsafe_allow_html=True)
        st.session_state.customer_unique_products = st.number_input("Unique Products Previously Bought", 1, 1000, st.session_state.customer_unique_products)
        st.session_state.customer_avg_price = st.number_input("Avg. Price of Previous Purchases (€)", 0.1, 5000.0, st.session_state.customer_avg_price, 0.1)

with col3:
    with st.container():
        st.markdown("<h5><i class='fa-solid fa-globe-europe'></i> Select Country of Purchase</h5>", unsafe_allow_html=True)
        country_options_map = {'United Kingdom': 'United Kingdom', 'Germany': 'Germany', 'France': 'France', 'Ireland': 'Ireland', 'Spain': 'Spain', 'Netherlands': 'Netherlands', 'Other': 'Other'}
        selected_display_country = st.selectbox("Country", list(country_options_map.keys()))
        st.session_state.selected_country = country_options_map[selected_display_country]
        st.plotly_chart(create_country_map(st.session_state.selected_country), use_container_width=True, config={'displayModeBar': False})

st.divider()

# --- Prediction Button & Output Section ---
if st.button("🚀 GET PREDICTION", use_container_width=True):
    with st.spinner("Calculating return risk..."):
        input_data = pd.DataFrame(0, index=[0], columns=model_columns)
        input_data.at[0, 'Quantity'] = st.session_state.quantity
        input_data.at[0, 'Price'] = st.session_state.unit_price
        input_data.at[0, 'customer_unique_products'] = st.session_state.customer_unique_products
        input_data.at[0, 'customer_avg_price'] = st.session_state.customer_avg_price
        country_col_name = f'Country_{selected_display_country}'
        if country_col_name in input_data.columns:
            input_data.at[0, country_col_name] = 1
        
        scaled_input = scaler.transform(input_data)
        prediction_proba = model.predict_proba(scaled_input)[0][1]
        
        st.session_state.prediction_made = True
        st.session_state.prediction_proba = prediction_proba

if st.session_state.prediction_made:
    st.markdown("## Prediction Outcome")
    
    gauge_placeholder = st.empty()
    final_proba = st.session_state.prediction_proba
    
    for i in range(0, int(final_proba * 100), 5):
        gauge_placeholder.plotly_chart(create_animated_gauge(i / 100.0), use_container_width=True, config={'displayModeBar': False})
        time.sleep(0.02)
    
    final_gauge_fig = create_animated_gauge(final_proba)
    gauge_placeholder.plotly_chart(final_gauge_fig, use_container_width=True, config={'displayModeBar': False})
    
    is_high_risk = final_proba >= 0.5
    if is_high_risk:
        st.error(f"**HIGH RETURN RISK** (Probability: {final_proba:.0%})")
    else:
        st.success(f"**LOW RETURN RISK** (Probability: {final_proba:.0%})")
        st.balloons()