import os
import pandas as pd

cwd = os.getcwd()
project_dir = 'D:\\GitHubProjects\\covid_mortality_prediction'
data_dir = 'D:\\GitHubProjects\\synthea_covid19_data\\100k_synthea_covid19_csv\\'


# ========================================================================================================
# Explore all patients who have covid-related records
# ========================================================================================================

# Select patients who have COVID-19 listed as a condition
conditions_df = pd.read_csv(data_dir+'conditions.csv', usecols=['PATIENT', 'DESCRIPTION'])
conditions_covid_df = conditions_df[conditions_df['DESCRIPTION']=='COVID-19']
conditions_covid_df.rename(columns={'PATIENT':'patient_id'}, inplace=True)
#88166 rows of COVID conditions

# Read in all patients.csv
patients = pd.read_csv(data_dir+'patients.csv', usecols=['Id', 'BIRTHDATE', 'DEATHDATE', 'RACE', 'ETHNICITY', 'GENDER'])
patients.rename(columns={'Id':'patient_id'}, inplace=True)

# Filter patients.csv for only covid patients
covid_patient_df = pd.merge(conditions_covid_df, patients, on ='patient_id', how ="left")
covid_patient_df.patient_id.nunique() 
#88166 rows and each is a unique patient who had COVID diagnosis

# Save disk space
del patients

# How many COVID patients have died?
covid_patients_deceased = covid_patient_df[covid_patient_df.DEATHDATE.notna()]
# 3,641

# ==============================================================================
# Explore how COVID patients died
# ==============================================================================
# Read in encounters, filter for COVID patients who died 
encounters = pd.read_csv(data_dir+'encounters.csv', usecols=['Id', 'START', 'STOP', 'PATIENT', 'ENCOUNTERCLASS', 'DESCRIPTION', 'REASONDESCRIPTION'])
encounters.rename(columns={'PATIENT':'patient_id'}, inplace=True)

encounters_deceased_covid_patients = pd.merge(covid_patients_deceased.patient_id, encounters, on ='patient_id', how ="left")

# Save disk space
del encounters

# Explore their encounters
encounters_deceased_covid_patients.ENCOUNTERCLASS.value_counts()
# Not helpful

encounters_deceased_covid_patients.DESCRIPTION.value_counts()
# 3,601 have a death certification encounter, will look at those records first then the rest

# first, will make sure each patient only has one death certification
deceased_covid_patients_w_death_cert = encounters_deceased_covid_patients[encounters_deceased_covid_patients.DESCRIPTION=='Death Certification']
deceased_covid_patients_w_death_cert.patient_id.nunique()
# 3,601 unique patient_ids for 3,601 death certifications, confirms that there are no duplicate death certs

# Explore REASONDESCRIPTION of Death Certification encounters 
print("========== Death Certification 'Reason Description' ==========")
print(deceased_covid_patients_w_death_cert.REASONDESCRIPTION.value_counts())
'''
'REASONDESCRIPTION' for the 3,601 patients with a 'Death Certification' encounter
COVID-19                                                  3518
Stroke                                                      12
Pneumonia                                                   12
Myocardial Infarction                                       11
Alzheimer's disease (disorder)                               9
Pulmonary emphysema (disorder)                               5
Malignant tumor of colon                                     4
Non-small cell lung cancer (disorder)                        4
Drug overdose                                                4
Secondary malignant neoplasm of colon                        3
Familial Alzheimer's disease of early onset (disorder)       3
Sudden Cardiac Death                                         3
Cardiac Arrest                                               3
Overlapping malignant neoplasm of colon                      2
Neoplasm of prostate                                         2
Bullet wound                                                 2
Concussion injury of brain                                   1
Pneumonia (disorder)                                         1
Burn injury(morphologic abnormality)                         1
Chronic obstructive bronchitis (disorder)                    1
'''
# 3518 were documented death due to COVID

# ====================================================
# Explore the patients with history of COVID who do not have a Death Certification Record
# ====================================================
encounters_deceased_covid_patients.patient_id.unique()

deceased_covid_patients_without_death_cert = [patient for patient in covid_patients_deceased if patient not in deceased_covid_patients_w_death_cert.patient_id.tolist()]
len(deceased_covid_patients_without_death_cert)
# 40 patients, which = 3,641 covid patients deceased minus 3,601 with death certificate

# I'll start by exploring one of these patients
deceased_covid_patients_without_death_cert_df = pd.merge(pd.Series(deceased_covid_patients_without_death_cert, name="patient_id"), covid_patients_deceased, on='patient_id', how='left')

# Add deathdate column in datetime format
deceased_covid_patients_without_death_cert_df['DEATHDATE']
deceased_covid_patients_without_death_cert_df['deathdate_dt'] = pd.to_datetime(deceased_covid_patients_without_death_cert_df['DEATHDATE'], format='%Y-%m-%d')

# ==========================
# Explore patient 1
# ==========================
patient1_deathdate = deceased_covid_patients_without_death_cert_df.iloc[0].deathdate_dt

patient1_id = deceased_covid_patients_without_death_cert_df.iloc[0].patient_id

patient1_encounters = encounters_deceased_covid_patients[encounters_deceased_covid_patients['patient_id']==patient1_id]
patient1_encounters['START']

# Convert dates to datetime objects
patient1_encounters['start_dt'] = pd.to_datetime(patient1_encounters['START'], format='%Y-%m-%dT%H:%M:%SZ')
patient1_encounters['stop_dt'] = pd.to_datetime(patient1_encounters['STOP'], format='%Y-%m-%dT%H:%M:%SZ')

patient1_encounters = patient1_encounters.sort_values(by='stop_dt')
patient1_encounters.tail(1).T

# death date = 2020-05-17
# most recent encounter = 2020-05-15 to 2020-05-16, inpatient, reason = heart failure

# Date of covid diagnosis?
conditions_df = pd.read_csv(data_dir+'conditions.csv')
patient1_conditions = conditions_df[conditions_df['PATIENT']==deceased_covid_patients_without_death_cert_df.iloc[0].patient_id]
patient1_covid_condition = patient1_conditions[patient1_conditions['DESCRIPTION']=='COVID-19']
patient1_covid_start = patient1_covid_condition.START
patient1_covid_stop = patient1_covid_condition.STOP
# COVID start 2020-03-10
# COVID stop 2020-04-11

# Encounter associated with covid diagnosis
covid_encounter = patient1_encounters[patient1_encounters['Id']==patient1_covid_condition.ENCOUNTER.iloc[0]]
covid_encounter.T
# Encounter does NOT specify COVID, DESCRIPTION = Encounter for symptom (procedure), REASONDESCRIPTION = NaN
# Encounter start/stop = 2020-03-10

patient1_encounters.REASONDESCRIPTION.value_counts()
patient1_encounters.DESCRIPTION.value_counts()
# No encounters with COVID information

# Check if there is an associated procedure for this encounter
procedures = pd.read_csv(data_dir+'procedures.csv')
covid_procedure = procedures[procedures['ENCOUNTER']==covid_encounter.Id.iloc[0]]
covid_procedure.T
# DESCRIPTION = face mask, REASONDESCRIPTION = Suspected COVID-19

# Look up careplans for the patient
careplans = pd.read_csv(data_dir+'careplans.csv')

patient1_careplans = careplans[careplans.PATIENT==patient1_id]

patient1_careplans.columns

patient1_careplans[['START', 'STOP']]
patient1_careplans[['DESCRIPTION', 'REASONDESCRIPTION']]
patient1_careplans[['CODE', 'REASONCODE']]
# DESCRIPTION for Suspected COVID-19 and COVID-19 REASONDESCRIPTIONs is 'Infectious disease care plan (record artifact) '
# I assume that is an outpatient careplan, I can check encounters to be sure


covid_careplan = patient1_careplans[patient1_careplans.REASONDESCRIPTION=='COVID-19']
covid_careplan.START
covid_careplan.STOP
covid_careplan.DESCRIPTION

# To summarize:
# Had COVID start and stop dates, most recent encounter was inpatient for heart failure, which was a month after covid stop date and ended
# one day before death date
# COVID encounter was just an 'Encounter for symptom (procedure)' and 'ambulatory' for ENCOUNTERCLASS
# COVID careplan was called 'Infectious disease care plan (record artifact)' and the dates lined up with diagosis start and stop dates


# ==========================
# For all patients without death certification encounter, what is the amount of time between their
# most recent encounter and their death date?
# ==========================