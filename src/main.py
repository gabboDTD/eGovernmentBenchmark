import pandas as pd

# Load the Excel file
file_path = '../data/6_eGovernment_Benchmark_2023__Final_Results_Bgn33TdFY2NnN7GOeUd64VCE84_98712.xlsx'
xls = pd.ExcelFile(file_path)

# Display sheet names to understand the structure of the file
sheet_names = xls.sheet_names

# Load the relevant sheets into dataframes
scores_2022_df = pd.read_excel(xls, '1. Scores 2022')
nat_services_results_df = pd.read_excel(xls, '3a. Nat. Services - Results')
nat_services_data_df = pd.read_excel(xls, '3b. Nat. Services - Data')
cb_services_results_df = pd.read_excel(xls, '4a. CB Services - Results')
cb_services_data_df = pd.read_excel(xls, '4b. CB Services - Data')
nat_portals_data_df = pd.read_excel(xls, '5. Nat. Portals - Data')
cb_portals_data_df = pd.read_excel(xls, '6. CB Portals - Data')

# Analysing Nat Services Data
# Identify the row that contains 'Country' and use it as column names
nat_services_data_df = nat_services_data_df.iloc[:,2:]
header_row = nat_services_data_df[nat_services_data_df.iloc[:, 0] == 'Country'].index[0]
nat_services_data_df.columns = nat_services_data_df.iloc[header_row,:].values
nat_services_data_df = nat_services_data_df.drop(range(header_row + 1))
italy_nat_services_data = nat_services_data_df[nat_services_data_df['Country'] == 'IT'].reset_index(drop=True)
italy_nat_services_data.to_excel('../output/italy_nat_services_data.xlsx')

# Define the relevant columns
relevant_columns = ["Service Provider", "Life event", "Service", "Url"]

# Function to find columns containing "No" for each Service Provider and Url
def find_no_columns(df, relevant_columns):
    result = []
    for _, row in df.iterrows():
        provider_url = tuple(row[relevant_columns])
        no_columns = [col for col in df.columns if row[col] == "No"]
        result.append((*provider_url, no_columns))
    return result

# Function to capitalize the first letter of each word and make the rest lowercase
def capitalize_words(text):
    return ' '.join([word.capitalize() for word in text.split()])

# Apply the function to the specified columns
italy_nat_services_data['Service Provider'] = italy_nat_services_data['Service Provider'].apply(capitalize_words)
italy_nat_services_data['Life event'] = italy_nat_services_data['Life event'].apply(capitalize_words)
italy_nat_services_data['Service'] = italy_nat_services_data['Service'].apply(capitalize_words)

# Apply the function to the data
no_columns_per_provider = find_no_columns(italy_nat_services_data, relevant_columns)
# Convert the result to a DataFrame for better readability
result_df = pd.DataFrame(no_columns_per_provider, columns=["Service Provider", "Life event", "Service", "Url", "Columns with 'No'"])


# mapping = {
#     "A1: information available online?": "Is information about the service available online?",
#     "A2: service available online?": "Is the actual service available online?",
#     "A3: available through portal?": "Is the service/information about the service available through (one of the) relevant portal(s)?",
#     "A4: Descriptive title? ": "(not scored) on a content page, does the website page provide a descriptive title?",
#     "A5: Breadcrumbs?": "(not scored) does the website show breadcrumbs or descriptive labels at the top of the page to navigate towards other (sub)pages?",
#     "B1: FAQ section available?": "Is a Frequently-Asked-Questions (FAQ) section available?",
#     "B2: Demo or live support?": "Is a demo available (any type: click-through demo, online video, downloadable manual explaining the steps the user has to take, ...) on how to obtain the service? OR Is there a live support functionality ‘click to chat’ available on the website with a human or a chatbot response?",
#     "B3: Identifiable contact?": "Can the division/department responsible for delivery be identified and contacted (generic contact details do not suffice to positively score on this metric)?",
#     "B4: Other channels available?": "Can the service be obtained via other channels than a website? (For instance, call centres, email, and small private businesses providing government services, customized applications (apps) or authorised intermediaries)",
#     "B5: Feedback mechanisms?": "Are feedback mechanisms available to the user to give his opinion on the service? (any type: user satisfaction monitoring, polls, surveys, ...; the provision of contact details does not suffice to positively score on this metric. A reference must be made to user satisfaction surveys, feedback options, complaints management and alike, clearly encouraging the user to provide feedback.",
#     "B6: Discussion fora or social media?": "Are discussion fora or social media available? (any type: for online discussions amongst users and with the public administration, directed from/to the domain website(s))",
#     "B7: Complaint procedures?": "Are complaint procedures available? (any type: redress, dispute resolutions)",
#     "C1: delivery notice completion?": "Does one receive a delivery notice of successful completion of the process step online?",
#     "C2: is progress tracked?": "During the course of the service, is progress tracked? (i.e. is it clear what all process steps look like, how much of the process step you have accomplished and how much of it still remains to be done?)",
#     "C3: save as draft?": "During the course of the service, can you save work done as a draft (i.e. could you return to your draft work at another moment in time)?",
#     "C4: expectations duration process?": "Does the site communicate expectations on how long the entire process is estimated to take before starting the service (i.e. how long it takes to fill in the online form)?",
#     "C5: delivery timelines clear?": "Is it clear what the delivery timelines of the service are (i.e. when the service is expected to be provided, ideally this is sooner than the legal maximum time limit)?",
#     "C6: maximum time limit delivery?": "Is there a maximum time limit set within which the administration has to deliver (i.e. the legal and formal deadline that cannot be exceeded by the service provider)?",
#     "C7: service performance info avail?": "Is information publicly available about service performance (any type: service levels, performance assessment, user satisfaction, user duration and completion rates)?",
#     "C8: error messages?": "When entering an input field in an online form, does the website show an error message when input identified is erroneous and (e.g. a pop-up or warning message appears whenever your phone number is requested but you enter characters instead of numbers, or your postal code is requested but you enter a non-existing postal code in your country)?",
#     "C9: visual aid & suggestions": "When entering an input field in an online form, does the website show any visual aids and suggestions to fill in the form correctly (e.g. text boxes, pop-up question mark icons or other visual cues that show examples of field entries, common mistakes to avoid or tips to fill in the form fields)?",
#     "D1: online access to own data?": "What is the degree of online access for users to their own data (i.e. personal data held by the government):",
#     "D2: notify incorrect data?": "Is it possible for users to notify the government online if they think that the personal data held by government is incorrect/incomplete?",
#     "D3: modify personal data online?": "Is it possible for users to modify the personal data held by government online?",
#     "D4: personal data complaint procedure?": "Is a complaint procedure available for users as regards their personal data?",
#     "D5: monitor data usage?": "Can you monitor who has consulted your personal data and for what purpose? (Monitoring in this case refers to the situation where a user can see – online – whether, when, by whom and why personal data was used; e.g. a civil servant looked up personal data for the purpose of answering a certain application):",
#     "E1: key policy making processes?": "Does the website provide information on the administrations' key policy making processes?",
#     "E2: user participation in policy making?": "Does the website provide information on the user's ability to participate in policy making processes?",
#     "E3: digital service design process?": "Does the website provide information on the process via which digital services are designed (e.g. panels, expert groups and consultations involving citizen and stakeholders such as businesses, researchers and non-profit organisations) and are any guidelines, standards, toolkits or design templates prescribed for other administrations to structure their own services?",
#     "E4: user enrolment for service improvement?": "Does the website provide information on how users can enrol in any activity to improve the design and delivery of services (e.g. via panels, expert groups and consultations)?",
#     "F1: authentication required?": "Is any kind of (online/offline) identification needed to access or obtain the service? (no score is attributed to this question, the question intends to landscape for how many/which process steps an eID is required)",
#     "F2: online authentication possible?": "If identification is needed, is it possible to identify oneself online?",
#     "F3: can you use national eID?": "If it is possible to identify oneself online, do you use an official electronic identifier (e.g. a national eID solution)? If the service requires a specific electronic identifier only suited for services from a single provider (e.g. a student account), or does not concern eID login (e.g. matricule number), the answer to this question is ‘no’.",
#     "F4: access another service without re-auth?": "If it is possible to identify oneself online for a service, is it also possible to access another service in this life event (but provided by a different service provider) without re-authenticating? (if there is only 1 service provider in a life event, this question is redundant)",
#     "F5: can decide using private eID?": "If it is possible to identify oneself online for a service, can one also decide to use a private eID (like eBanking token)? This question is not scored, but aims to increase insights into the use of various electronic identification tools.",
#     "F6: documentation required?": "Is any kind of documentation needed to access or apply for the service? (no score is attributed to this question; the question intends to landscape for how many/which process steps an eDocument is relevant)",
#     "F7_1: possible to submit eDoc?": "Is it possible for the user to submit the document that is required by the service provider to complete procedures and formalities necessary to establish or to carry out a process step online (certificate, diploma, proof of registration, etc.) in an electronic form?",
#     "F7_2: possible to obtain eDoc?": "Is it possible to obtain the document that is to be provided by the service provider to the service recipient when completing procedures and formalities necessary to establish or to carry out a process step online (certificate, diploma, proof of registration etc.) in an electronic form?",
#     "F8: personal info required?": "Is any kind of eForm needed to access or apply for the service? (no score is attributed to this question, the question intends to landscape for how many/which process steps an eForm is required)",
#     "F9: personal data pre-filled?": "When applying for this service is personal data pre-filled by the service provider? (based on data from authentic sources17 such as National register, Tax registers, Company registers etc.)",
# }
mapping_suggestions = {
    "A1: information available online?": "Rendere le informazioni sul servizio disponibili online",
    "A2: service available online?": "Rendere il servizio effettivo disponibile online",
    "A3: available through portal?": "Garantire che il servizio/le informazioni sul servizio siano disponibili tramite i portali rilevanti",
    "A4: Descriptive title? ": "Fornire un titolo descrittivo su una pagina di contenuto",
    "A5: Breadcrumbs?": "Mostrare i breadcrumb o le etichette descrittive nella parte superiore della pagina per navigare verso altre pagine",
    "B1: FAQ section available?": "Fornire una sezione di Domande Frequenti (FAQ)",
    "B2: Demo or live support?": "Offrire una demo o una funzionalità di supporto live (click to chat) sul sito web",
    "B3: Identifiable contact?": "Rendere identificabile e contattabile la divisione/dipartimento responsabile dell'erogazione",
    "B4: Other channels available?": "Consentire di ottenere il servizio tramite canali diversi da un sito web",
    "B5: Feedback mechanisms?": "Fornire meccanismi di feedback per consentire all'utente di esprimere la propria opinione sul servizio",
    "B6: Discussion fora or social media?": "Offrire forum di discussione o social media per discussioni online tra utenti e con l'amministrazione pubblica",
    "B7: Complaint procedures?": "Fornire procedure di reclamo (rettifiche, risoluzione delle controversie)",
    "C1: delivery notice completion?": "Inviare una notifica di consegna del completamento con successo del passaggio del processo online",
    "C2: is progress tracked?": "Tracciare i progressi durante il corso del servizio",
    "C3: save as draft?": "Consentire di salvare il lavoro come bozza durante il corso del servizio",
    "C4: expectations duration process?": "Comunicare le aspettative su quanto tempo si stima che l'intero processo richiederà prima di iniziare il servizio",
    "C5: delivery timelines clear?": "Rendere chiari i tempi di consegna del servizio",
    "C6: maximum time limit delivery?": "Stabilire un limite massimo di tempo entro il quale l'amministrazione deve consegnare",
    "C7: service performance info avail?": "Fornire informazioni pubbliche sulle prestazioni del servizio",
    "C8: error messages?": "Mostrare messaggi di errore quando l'input identificato è errato",
    "C9: visual aid & suggestions": "Fornire aiuti visivi e suggerimenti per compilare correttamente il modulo",
    "D1: online access to own data?": "Fornire accesso online agli utenti ai propri dati",
    "D2: notify incorrect data?": "Consentire agli utenti di notificare online al governo se ritengono che i dati personali detenuti dal governo siano errati/incompleti",
    "D3: modify personal data online?": "Consentire agli utenti di modificare online i dati personali detenuti dal governo",
    "D4: personal data complaint procedure?": "Fornire una procedura di reclamo per gli utenti riguardo ai propri dati personali",
    "D5: monitor data usage?": "Consentire agli utenti di monitorare chi ha consultato i propri dati personali e per quale scopo",
    "E1: key policy making processes?": "Fornire informazioni sui principali processi di definizione delle politiche dell'amministrazione",
    "E2: user participation in policy making?": "Fornire informazioni sulla capacità dell'utente di partecipare ai processi di definizione delle politiche",
    "E3: digital service design process?": "Fornire informazioni sul processo tramite il quale vengono progettati i servizi digitali",
    "E4: user enrolment for service improvement?": "Fornire informazioni su come gli utenti possono iscriversi a qualsiasi attività per migliorare la progettazione e l'erogazione dei servizi",
    "F1: authentication required?": "Identificare se è richiesta qualche forma di identificazione (online/offline) per accedere o ottenere il servizio",
    "F2: online authentication possible?": "Consentire agli utenti di identificarsi online",
    "F3: can you use national eID?": "Consentire agli utenti di utilizzare un identificatore elettronico ufficiale (ad es. una soluzione eID nazionale)",
    "F4: access another service without re-auth?": "Consentire agli utenti di accedere a un altro servizio in questo evento di vita senza ri-autenticarsi",
    "F5: can decide using private eID?": "Consentire agli utenti di decidere di utilizzare un eID privato (come il token eBanking)",
    "F6: documentation required?": "Identificare se è richiesta qualche documentazione per accedere o richiedere il servizio",
    "F7_1: possible to submit eDoc?": "Consentire agli utenti di inviare i documenti richiesti in formato elettronico",
    "F7_2: possible to obtain eDoc?": "Consentire agli utenti di ottenere i documenti richiesti in formato elettronico",
    "F8: personal info required?": "Identificare se è richiesto qualche modulo elettronico per accedere o richiedere il servizio",
    "F9: personal data pre-filled?": "Precompilare i dati personali nei moduli basati su dati provenienti da fonti autentiche"
}

result_df['Columns with \'No\''] = result_df['Columns with \'No\''].apply(lambda x: [mapping_suggestions[col] for col in x])
# Remove rows where 'Columns with \'No\'' is an empty list
result_df = result_df[result_df['Columns with \'No\''].apply(lambda x: len(x) > 0)]

result_df.to_excel('../output/results.xlsx')