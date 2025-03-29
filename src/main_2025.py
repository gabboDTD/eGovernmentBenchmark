import pandas as pd
import numpy as np
import os
from translations import service_providers_translation, life_events_translation, services_translation
from mapping import mapping_services_suggestions_2025

def load_excel_sheets(file_path):
    """Load the relevant sheets into dataframes from an Excel file."""
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    
    data_frames = {
        'scores_2024_df': pd.read_excel(xls, '1. Results overview'),
        'nat_services_results_df': pd.read_excel(xls, '2.a Results National Services'),
        'nat_services_data_df': pd.read_excel(xls, '2b. National Services'),
        'cb_services_results_df': pd.read_excel(xls, '3a. Results CB Services'),
        'cb_services_data_df': pd.read_excel(xls, '3b. Cross-border Services'),
        'nat_portals_data_df': pd.read_excel(xls, '4b. National Portals'),
        'cb_portals_data_df': pd.read_excel(xls, '4c. Cross-border portals')
    }
    
    return data_frames

def preprocess_services_data(df):
    """Preprocess the National Services Data dataframe."""
    df = df.iloc[:, 2:]
    header_row = df[df.iloc[:, 0] == 'Country'].index[0]
    df.columns = df.iloc[header_row, :].values
    df = df.drop(range(header_row + 1)).reset_index(drop=True)
    # Rimuove le righe completamente vuote
    df = df.dropna(how='all').reset_index(drop=True)
    return df

def extract_italy_data(df):
    """Extract data for Italy from the preprocessed National Services Data dataframe."""
    italy_df = df[df['Country'] == 'IT'].reset_index(drop=True)
    return italy_df

def capitalize_words(text):
    """Capitalize the first letter of each word in a text."""
    return ' '.join([word.capitalize() for word in text.split()])

def find_no_columns(df, relevant_columns):
    """Find columns containing 'No' for each Service Provider and Url."""
    result = []
    for _, row in df.iterrows():
        provider_url = tuple(row[relevant_columns])
        no_columns = [col for col in df.columns if row[col] == "No"]
        result.append((*provider_url, no_columns))
    return result

def apply_capitalization(df, columns):
    """Apply capitalization function to specified columns."""
    for column in columns:
        df[column] = df[column].apply(capitalize_words)
    return df

def translate_columns(df, translation_dicts):
    """Translate columns based on provided translation dictionaries."""
    for column, translation_dict in translation_dicts.items():
        df[column] = df[column].map(translation_dict)
    return df

newpath = '../output'
if not os.path.exists(newpath):
    os.makedirs(newpath)

# Load the Excel file
file_path = '../data/Results_2024_IT.xlsx'

# Load Excel sheets
data_frames = load_excel_sheets(file_path)

# Preprocess National Services Data
nat_services_data_df = preprocess_services_data(data_frames['nat_services_data_df'])
# Preprocess Cross Border Services Data
cb_services_data_df = preprocess_services_data(data_frames['cb_services_data_df'])

# Extract Italy's National Services Data
italy_nat_services_data = extract_italy_data(nat_services_data_df)
italy_nat_services_data.to_excel('../output/italy_nat_services_data_2025.xlsx')

# Extract Italy's National Services Data
italy_cb_services_data = extract_italy_data(cb_services_data_df)
italy_cb_services_data.to_excel('../output/italy_cb_services_data_2025.xlsx')

# Define relevant columns and capitalize specified columns
relevant_columns = ["Service Provider", "Life event", "Service", "Url"]
columns_to_capitalize = ["Service Provider", "Life event", "Service"]
italy_nat_services_data = apply_capitalization(italy_nat_services_data, columns_to_capitalize)
italy_cb_services_data = apply_capitalization(italy_cb_services_data, columns_to_capitalize)

# Find 'No' columns for each service provider
no_columns_nat_services_per_provider = find_no_columns(italy_nat_services_data, relevant_columns)

# Replace 'Yes' with 'No' in specified columns
columns_to_replace = [
    "Barrier national eID required",
    "Barrier eDoc required",
    "Barrier translation/recognition documents?",
    "Barrier language issues",
    "The translation provided on the website is unclear or incorrect",
    "Barrier lack of information",
    "Barrier need to meet face to face? ", #TODO: fix trailing space in excel
    "Other barriers (explain)"
]
italy_cb_services_data[columns_to_replace] = italy_cb_services_data[columns_to_replace].replace('Yes', 'No')
no_columns_cb_services_per_provider = find_no_columns(italy_cb_services_data, relevant_columns)

# Convert the result to a DataFrame
result_nat_services_df = pd.DataFrame(no_columns_nat_services_per_provider, columns=["Service Provider", "Life event", "Service", "Url", "Columns with 'No'"])
# Convert the result to a DataFrame
result_cb_services_df = pd.DataFrame(no_columns_cb_services_per_provider, columns=["Service Provider", "Life event", "Service", "Url", "Columns with 'No'"])

# Add a column specifying if it is a national service or a cross-border service
result_nat_services_df['Service Type'] = 'Servizio Nazionale'
result_cb_services_df['Service Type'] = 'Servizio Transfrontaliero'

# Append the two DataFrames
result_df = pd.concat([result_nat_services_df, result_cb_services_df], ignore_index=True)

# Define translation dictionaries
translation_dicts = {
    'Service Provider': service_providers_translation,
    'Service': services_translation,
    'Life event': life_events_translation
}

services_to_translate = result_df['Service'].unique()
missing_translations = [s for s in services_to_translate if s not in services_translation]

service_providers_to_translate = result_df['Service Provider'].unique()
missing_translations = [s for s in service_providers_to_translate if s not in service_providers_translation]

# Translate columns
result_df = translate_columns(result_df, translation_dicts)

# Apply mapping suggestions to 'Columns with No'
result_df['Columns with \'No\''] = result_df['Columns with \'No\''].apply(lambda x: [mapping_services_suggestions_2025[col] for col in x])
result_df = result_df[result_df['Columns with \'No\''].apply(lambda x: len(x) > 0)]

# Save the result to an Excel file
result_df.to_excel('../output/results_2024.xlsx', index=False)

# Explode the list into separate rows
exploded_df = result_df.explode("Columns with 'No'")

# Rename the exploded column for clarity
exploded_df = exploded_df.rename(columns={"Columns with 'No'": "Suggerimento"})

# Optional: reorder columns
columns_order = ["Service Provider", "Life event", "Service", "Suggerimento", "Service Type", "Url"]
exploded_df = exploded_df[columns_order]

# Replace Python None with NaN (interpreted as NULL)
exploded_df = exploded_df.replace({None: np.nan})

# Save as CSV ready for Superset
exploded_df.to_csv('../output/results_2024_exploded.csv', index=False)