import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64

# st.set_page_config(page_title="eGovernment Benchmark", page_icon="blue-fill.svg")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .block-container {
        padding-left: 0rem;
        padding-right: 0rem;
        /* padding-top: 1rem; */
        /* padding-bottom: 0rem; */
        # padding-top: 10px; /* Adjust this value to reduce space */
        margin-top: -66px;
    }

    /* Set the background color of the sidebar */
    .css-18e3th9 {
        background-color: #0056b3;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;  /* Align content to the top */
        padding-top: 20px; /* Adjust padding to align with the main content */
    }

    /* Align the button icon with the "D" in "Dettaglio dei controlli" */
    .stButton {
        display: inline-block;
        margin-left: -21px;  /* Adjust this value to align with the text */
        vertical-align: middle;
    }

    /* Optional: Adjust the button text and icon appearance */
    .stButton > button {
        background-color: transparent;
        color: black; /* Black text */
        border: none;
        padding: 10px 24px;
        text-align: left; /* Align text to the left to match Dettaglio */
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        cursor: pointer;
        font-family: 'Titillium Web', sans-serif;
    }

    .stButton > button:hover {
        background-color: transparent; /* Darker green on hover */
    }

    .fake-button {
        background-color: transparent;
        color: black; /* Black text */
        border: none;
        border-radius: 5px; /* Rounded corners */
        padding: 10px 24px; /* Padding */
        font-size: 16px;
        text-align: left;
        display: inline-block;
        text-decoration: none;
        margin-left: -21px;  /* Adjust this value to align with the text */
    }

    /* Center logo vertically within the sidebar */
    .logo-container {
        padding-top: 0px;
        padding-bottom: 20px;
        margin-top: 0;
    }

    /* Set the font color and style for the sidebar */
    .css-18e3th9, .css-1d391kg, .css-1v3fvcr, .css-1l02zno {
        color: white;  /* White text */
        font-family: 'Titillium Web', sans-serif;
    }

    /* Set the main content background and font style */
    .css-1outpf7 {
        background-color: #f7f9fc;  /* Light gray background */
        color: #0056b3;  /* Blue text */
        font-family: 'Titillium Web', sans-serif;
        padding-top: 30px;  /* Increased padding for breathing room */
        width: 100%;  /* Use full width */
        max-width: 1200px;  /* Set a max width */
        margin-left: auto;  /* Center the content horizontally */
        margin-right: auto; /* Center the content horizontally */
        padding-left: 20px; /* Add some padding for content readability */
        padding-right: 20px; /* Add some padding for content readability */
    }

    /* Style the header */
    .css-145kmo2 {
        font-size: 24px;
        font-weight: bold;
        color: #003366;  /* Darker blue */
        margin-top: 20px; /* Add margin to prevent squeezing */
        padding-top: 10px; /* Add padding to ensure alignment with the sidebar */
    }

    /* Style the subheaders */
    .css-1cpxqw2 {
        color: #003366;  /* Darker blue */
        font-size: 20px;
        font-weight: bold;
    }

    /* Success message styling with green checkmark */
    .success-message {
        color: green;
        font-family: 'Titillium Web', sans-serif;
        font-weight: bold;
        display: flex;
        align-items: center;
    }
    .success-message::before {
        content: "✅";  /* Green checkmark icon */
        font-size: 1.5em;
        margin-right: 8px;
    }

    /* Unknown message styling with questionmark */
    .unknown-message {
        color:  #0056b3;  /* Blue text */
        font-family: 'Titillium Web', sans-serif;
        font-weight: bold;
        display: flex;
        align-items: center;
    }
    .unknown-message::before {
        content: "❓";  /* Blue circle icon */
        font-size: 1.5em;
        margin-right: 8px;
    }

    /* Header styling */
    .normal-message {
        color: black;
        font-family: 'Titillium Web', sans-serif;        
        display: flex;
        align-items: center;
    }

    /* Error message styling with an icon */
    .error-message {
        color: red;
        font-weight: bold;
        display: flex;
        align-items: center;
    }

    .error-message::before {
        content: "❌";  /* Red cross icon */
        font-size: 1.5em;
        margin-right: 8px;
    }

    /* Stronger contrast for warning message */
    .warning-box {
        background-color: #fff3cd;
        border: 2px solid #ffc107;  /* Stronger yellow border */
        color: #856404;
        padding: 10px;
        border-radius: 5px;
    }

    /* Neutral message styling (for other esito values) */
    .box-message {
        color: #6C757D;  /* Blue text */
        font-weight: bold;
        display: flex;
        align-items: center;
    }

    .box-message::before {
        content: "ℹ️";  /* Info icon */
        font-size: 1.5em;
        margin-right: 8px;
    }

    /* Center the iframe and make it responsive */
    .pdf-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin: 20px auto;
        width: 90%; /* Responsive width */
    }

    .pdf-frame {
        width: 110%;
        height: 900px;
        border: 1px solid #0056b3; /* Optional border for a better look */
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True
)


# Load the dataset
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
file_path = os.path.join(parent_dir, 'output', 'results_2024.xlsx')

df = pd.read_excel(file_path)
df['Columns with \'No\''] = df['Columns with \'No\''].apply(eval)

# Sidebar navigation
# Add SVG logo in the sidebar
svg_path = "blue-fill-text-right.svg"
if os.path.exists(svg_path):
    with open(svg_path, "rb") as svg_file:
        encoded_svg = base64.b64encode(svg_file.read()).decode("utf-8")
    st.sidebar.markdown(
        f"""
        <div class="logo-container">
            <img src="data:image/svg+xml;base64,{encoded_svg}" />
        </div>
        """,
        unsafe_allow_html=True
    )
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
    st.title("📘 eGovernment Benchmark Monitoraggio dei Servizi Digitali")
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
        providers = sorted(df['Service Provider'].dropna().unique())
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