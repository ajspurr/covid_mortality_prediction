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
covid_patients_deceased = covid_patient_df[covid_patient_df.DEATHDATE.notna()].patient_id
# 3,641

# ====================================================
# Explore how COVID patients died
# ====================================================
# Read in encounters, filter for COVID patients who died 
encounters = pd.read_csv(data_dir+'encounters.csv', usecols=['Id', 'START', 'STOP', 'PATIENT', 'ENCOUNTERCLASS', 'DESCRIPTION', 'REASONDESCRIPTION'])
encounters.rename(columns={'PATIENT':'patient_id'}, inplace=True)

encounters_deceased_covid_patients = pd.merge(covid_patients_deceased, encounters, on ='patient_id', how ="left")

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
deceased_covid_patients_w_death_cert.REASONDESCRIPTION.value_counts()
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

# ==========================
# Explore the patients with history of COVID who do not have a Death Certification Record
# ==========================
encounters_deceased_covid_patients.patient_id.unique()

deceased_covid_patients_without_death_cert = [patient for patient in covid_patients_deceased if patient not in deceased_covid_patients_w_death_cert.patient_id.tolist()]
len(deceased_covid_patients_without_death_cert)
# 40 patients, which = 3,641 covid patients deceased minus 3,601 with death certificate





