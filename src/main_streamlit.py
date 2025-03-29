import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="eGovernment Benchmark", layout="wide")

# Load the dataset
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
file_path = os.path.join(parent_dir, 'output', 'results_2024.xlsx')

df = pd.read_excel(file_path)
df['Columns with \'No\''] = df['Columns with \'No\''].apply(eval)

# Sidebar navigation
st.sidebar.title("📚 **Menu di navigazione**")
page = st.sidebar.radio("Scegli una sezione per iniziare:", ["📘 **Guida introduttiva**", "🏛️ **Suggerimenti per gli enti**", "📊 **Azioni più raccomandate**"])

# Function to display data for a selected Service Provider grouped by Life event
def display_provider_data(provider, service_type=None):
    provider_data = df[df['Service Provider'] == provider]
    if service_type and service_type != 'Tutto':
        provider_data = provider_data[provider_data['Service Type'] == service_type]
    life_events = provider_data['Life event'].unique()

    for life_event in life_events:
        with st.expander(f"📌 {life_event}"):
            event_data = provider_data[provider_data['Life event'] == life_event]
            for _, row in event_data.iterrows():
                st.markdown(f"**🔹 Servizio:** {row['Service']}")
                st.markdown(f"**🔗 URL:** [Vai al servizio]({row['Url']})")
                st.markdown("**📋 Azioni consigliate per il miglioramento:**")
                for item in row["Columns with 'No'"]:
                    st.markdown(f"- {item}")
                st.markdown("---")

# Page 1: Instructions
if page == "📘 **Guida introduttiva**":
    st.title("📘 Benvenuti nell’applicazione eGovernment Benchmark")
    st.markdown("""
        ### Come iniziare:
        - 🏛️ Accedi a suggerimenti mirati per ciascun ente pubblico nella sezione **Suggerimenti per gli enti**.
        - 📊 Consulta le **azioni più frequenti** per l’ottimizzazione dei servizi digitali.
        - 🔘 Utilizza la barra laterale per esplorare le sezioni disponibili.
    """)

# Page 2: Dashboard Eenti di Servizi
elif page == "🏛️ **Suggerimenti per gli enti**":
    st.title("🏛️ Suggerimenti personalizzati per migliorare i servizi digitali")
    with st.expander("ℹ️ Come vengono generati i suggerimenti", expanded=False):
        st.markdown(
            "I suggerimenti sono generati automaticamente sulla base dei dati raccolti nel benchmark europeo 2024. "
            "Per ciascun servizio digitale che non soddisfa determinati criteri (valutati con *No*), "
            "il sistema propone azioni concrete di miglioramento, utilizzando una mappatura curata di possibili interventi."
        )
    col1, col2 = st.columns(2)
    with col1:
        providers = df['Service Provider'].unique()
        selected_provider = st.selectbox('Ente erogatore', providers)

    with col2:
        service_types = df['Service Type'].unique()
        selected_service_type = st.selectbox('Tipologia di servizio (opzionale)', ['Tutto'] + list(service_types))

    if selected_provider:
        display_provider_data(selected_provider, selected_service_type)

# Page 3: Suggerimenti Comuni
elif page == "📊 **Azioni più raccomandate**":
    st.title("📊 Azioni più raccomandate per migliorare i servizi digitali pubblici")

    col1, col2 = st.columns(2)
    with col1:
        selected_service_type = st.selectbox('Tipologia di servizio (opzionale)', ['Tutto'] + list(df['Service Type'].unique()))
    with col2:
        life_events = df['Life event'].unique()
        selected_life_event = st.selectbox('Evento della vita (Life Event) (opzionale)', ['Tutti'] + list(life_events))

    filtered_df = df.copy()
    if selected_service_type != 'Tutto':
        filtered_df = filtered_df[filtered_df['Service Type'] == selected_service_type]
    if selected_life_event != 'Tutti':
        filtered_df = filtered_df[filtered_df['Life event'] == selected_life_event]

    all_no_values = filtered_df['Columns with \'No\''].explode()
    common_no_values = all_no_values.value_counts().reset_index()
    common_no_values.columns = ['Suggerimento', 'Frequenza']

    st.subheader("📌 Azioni suggerite più frequentemente")

    st.markdown(
        "Le azioni riportate di seguito sono quelle più frequentemente **raccomandate** "
        "per migliorare la qualità dei servizi digitali pubblici. "
        "Usa i filtri in alto per affinare la visualizzazione."
    )

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(common_no_values['Suggerimento'], common_no_values['Frequenza'], color='skyblue')
    ax.set_xlabel('Frequenza')
    ax.set_title("Azioni suggerite")
    ax.invert_yaxis()
    st.pyplot(fig)