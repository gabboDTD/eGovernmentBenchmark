import pandas as pd
import os
from translations import service_providers_translation, life_events_translation, services_translation
from mapping import mapping_suggestions

def load_excel_sheets(file_path):
    """Load the relevant sheets into dataframes from an Excel file."""
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    
    data_frames = {
        'scores_2022_df': pd.read_excel(xls, '1. Scores 2022'),
        'nat_services_results_df': pd.read_excel(xls, '3a. Nat. Services - Results'),
        'nat_services_data_df': pd.read_excel(xls, '3b. Nat. Services - Data'),
        'cb_services_results_df': pd.read_excel(xls, '4a. CB Services - Results'),
        'cb_services_data_df': pd.read_excel(xls, '4b. CB Services - Data'),
        'nat_portals_data_df': pd.read_excel(xls, '5. Nat. Portals - Data'),
        'cb_portals_data_df': pd.read_excel(xls, '6. CB Portals - Data')
    }
    
    return data_frames

def preprocess_nat_services_data(df):
    """Preprocess the National Services Data dataframe."""
    df = df.iloc[:, 2:]
    header_row = df[df.iloc[:, 0] == 'Country'].index[0]
    df.columns = df.iloc[header_row, :].values
    df = df.drop(range(header_row + 1)).reset_index(drop=True)
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
file_path = '../data/6_eGovernment_Benchmark_2023__Final_Results_Bgn33TdFY2NnN7GOeUd64VCE84_98712.xlsx'

# Load Excel sheets
data_frames = load_excel_sheets(file_path)

# Preprocess National Services Data
nat_services_data_df = preprocess_nat_services_data(data_frames['nat_services_data_df'])

# Extract Italy's National Services Data
italy_nat_services_data = extract_italy_data(nat_services_data_df)
italy_nat_services_data.to_excel('../output/italy_nat_services_data.xlsx')

# Define relevant columns and capitalize specified columns
relevant_columns = ["Service Provider", "Life event", "Service", "Url"]
columns_to_capitalize = ["Service Provider", "Life event", "Service"]
italy_nat_services_data = apply_capitalization(italy_nat_services_data, columns_to_capitalize)

# Find 'No' columns for each service provider
no_columns_per_provider = find_no_columns(italy_nat_services_data, relevant_columns)

# Convert the result to a DataFrame
result_df = pd.DataFrame(no_columns_per_provider, columns=["Service Provider", "Life event", "Service", "Url", "Columns with 'No'"])

# Define translation dictionaries
translation_dicts = {
    'Service Provider': service_providers_translation,
    'Service': services_translation,
    'Life event': life_events_translation
}

# Translate columns
result_df = translate_columns(result_df, translation_dicts)

# Apply mapping suggestions to 'Columns with No'
result_df['Columns with \'No\''] = result_df['Columns with \'No\''].apply(lambda x: [mapping_suggestions[col] for col in x])
result_df = result_df[result_df['Columns with \'No\''].apply(lambda x: len(x) > 0)]

# Save the result to an Excel file
result_df.to_excel('../output/results.xlsx', index=False)