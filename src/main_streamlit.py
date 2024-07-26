import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to display data for a selected Service Provider grouped by Life event
def display_provider_data(provider):
    provider_data = df[df['Service Provider'] == provider]
    life_events = provider_data['Life event'].unique()
    
    for life_event in life_events:
        # st.markdown(f"## Life Event: {life_event}")
        st.markdown(f"## {life_event}")
        event_data = provider_data[provider_data['Life event'] == life_event]
        for _, row in event_data.iterrows():
            st.markdown(f"**Servizio:** {row['Service']}")
            st.markdown(f"**URL:** [Link]({row['Url']})")
            st.markdown("**Azioni Suggerite:**")
            no_columns = eval(row["Columns with 'No'"])
            for item in no_columns:
                st.markdown(f"- {item}")
            st.markdown("---")


# Load the dataset
file_path = '../output/results.xlsx'  # Update with the correct file path if necessary
df = pd.read_excel(file_path)

# Streamlit app layout
st.title("eGovernment Benchmark Dashboard")

# Service Provider selection
providers = df['Service Provider'].unique()
selected_provider = st.selectbox('Seleziona un fornitore di servizi', providers)

# Display data for the selected Service Provider grouped by Life event
if selected_provider:
    display_provider_data(selected_provider)


# Plot the most common values in 'Columns with 'No''
st.title("Suggerimenti piu' comuni per aumentare l'eGovernment Benchmark")

# Convert string representation of lists to actual lists
df['Columns with \'No\''] = df['Columns with \'No\''].apply(eval)

# Flatten the lists into a single series
all_no_values = df['Columns with \'No\''].explode()

# Count the most common values
common_no_values = all_no_values.value_counts().reset_index()
common_no_values.columns = ['Value', 'Count']

fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(common_no_values['Value'], common_no_values['Count'], color='skyblue')
ax.set_xlabel('Count')
ax.set_title("Suggerimenti per aumentare l'eGovernment Benchmark")
ax.invert_yaxis()

st.pyplot(fig)    


# life_events = df['Life event'].unique()

# for life_event in life_events:
#     st.markdown(f"### Life Event: {life_event}")
#     event_data = df[df['Life event'] == life_event]
    
#     # Flatten the lists into a single series
#     all_no_values = event_data['Columns with \'No\''].explode()

#     # Count the most common values
#     common_no_values = all_no_values.value_counts().reset_index()
#     common_no_values.columns = ['Value', 'Count']

#     fig, ax = plt.subplots(figsize=(10, 8))
#     ax.barh(common_no_values['Value'], common_no_values['Count'], color='skyblue')
#     ax.set_xlabel('Count')
#     ax.set_title(f'Most Common Values in "Columns with \'No\'" for {life_event}')
#     ax.invert_yaxis()

#     st.pyplot(fig)

# Life event selection
life_events = df['Life event'].unique()
selected_life_event = st.selectbox('Seleziona un Life Event', life_events)

if selected_life_event:
    event_data = df[df['Life event'] == selected_life_event]
        
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