import streamlit as st
import pandas as pd

# Load the dataset
file_path = '../output/results.xlsx'  # Update with the correct file path if necessary
df = pd.read_excel(file_path)


# Function to display data for a selected Service Provider grouped by Life event
def display_provider_data(provider):
    provider_data = df[df['Service Provider'] == provider]
    life_events = provider_data['Life event'].unique()
    
    for life_event in life_events:
        st.markdown(f"## Life Event: {life_event}")
        event_data = provider_data[provider_data['Life event'] == life_event]
        for _, row in event_data.iterrows():
            st.markdown(f"**Service:** {row['Service']}")
            st.markdown(f"**URL:** [Link]({row['Url']})")
            st.markdown("**Columns with 'No':**")
            no_columns = eval(row["Columns with 'No'"])
            for item in no_columns:
                st.markdown(f"- {item}")
            st.markdown("---")

# Streamlit app layout
st.title("Service Provider Dashboard")

# Service Provider selection
providers = df['Service Provider'].unique()
selected_provider = st.selectbox('Select a Service Provider', providers)

# Display data for the selected Service Provider grouped by Life event
if selected_provider:
    display_provider_data(selected_provider)