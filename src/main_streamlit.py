import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the dataset
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
file_path = os.path.join(parent_dir, 'output', 'results.xlsx')

df = pd.read_excel(file_path)

# Convert string representation of lists to actual lists
df['Columns with \'No\''] = df['Columns with \'No\''].apply(eval)

# Sidebar navigation
page = st.sidebar.selectbox("Seleziona la pagina", ["Suggerimenti ai Fornitori di Servizi", "Suggerimenti piu' Comuni"])

# Function to display data for a selected Service Provider grouped by Life event
def display_provider_data(provider, service_type=None):
    provider_data = df[df['Service Provider'] == provider]
    if service_type:
        provider_data = provider_data[provider_data['Service Type'] == service_type]
    life_events = provider_data['Life event'].unique()
    
    for life_event in life_events:
        st.markdown(f"## {life_event}")
        event_data = provider_data[provider_data['Life event'] == life_event]
        for _, row in event_data.iterrows():
            st.markdown(f"**Servizio:** {row['Service']}")
            st.markdown(f"**URL:** [Link]({row['Url']})")
            st.markdown("**Azioni Suggerite:**")
            no_columns = row["Columns with 'No'"]
            for item in no_columns:
                st.markdown(f"- {item}")
            st.markdown("---")

# Page 1: Dashboard Fornitori di Servizi
if page == "Suggerimenti ai Fornitori di Servizi":
    st.title("Suggerimenti ai Fornitori di Servizi")

    # Service Provider selection
    providers = df['Service Provider'].unique()
    selected_provider = st.selectbox('Seleziona un fornitore di servizi', providers)

    # Service Type selection
    service_types = df['Service Type'].unique()
    selected_service_type = st.selectbox('Seleziona un tipo di servizio', ['Tutti'] + list(service_types))

    # Display data for the selected Service Provider grouped by Life event
    if selected_provider:
        if selected_service_type == 'Tutti':
            display_provider_data(selected_provider)
        else:
            display_provider_data(selected_provider, selected_service_type)

# Page 2: Suggerimenti Comuni
elif page == "Suggerimenti piu' Comuni":
    st.title("Suggerimenti piu' comuni per aumentare l'eGovernment Benchmark")

    # Service Type selection
    service_types = df['Service Type'].unique()
    selected_service_type = st.selectbox('Seleziona un tipo di servizio', ['Tutti'] + list(service_types))

    if selected_service_type == 'Tutti':
        filtered_df = df
    else:
        filtered_df = df[df['Service Type'] == selected_service_type]

    # Flatten the lists into a single series
    all_no_values = filtered_df['Columns with \'No\''].explode()

    # Count the most common values
    common_no_values = all_no_values.value_counts().reset_index()
    common_no_values.columns = ['Value', 'Count']

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(common_no_values['Value'], common_no_values['Count'], color='skyblue')
    ax.set_xlabel('Count')
    ax.set_title(f"Suggerimenti per aumentare l'eGovernment Benchmark ({selected_service_type})")
    ax.invert_yaxis()

    st.pyplot(fig)    

    # Life event selection
    life_events = filtered_df['Life event'].unique()
    selected_life_event = st.selectbox('Seleziona un Life Event', life_events)

    if selected_life_event:
        event_data = filtered_df[filtered_df['Life event'] == selected_life_event]
        
        # Flatten the lists into a single series
        all_no_values = event_data['Columns with \'No\''].explode()

        # Count the most common values
        common_no_values = all_no_values.value_counts().reset_index()
        common_no_values.columns = ['Value', 'Count']

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(common_no_values['Value'], common_no_values['Count'], color='skyblue')
        ax.set_xlabel('Count')
        ax.set_title(f"Suggerimenti piu' comuni per il Life event: {selected_life_event}")
        ax.invert_yaxis()

        st.pyplot(fig)
