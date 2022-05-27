# COVID Mortality Prediction
## Overview
In this project I use synthetic patient data to predict COVID-19 mortality. Similar to real-world projects, the data is represented in a high-dimensional multi-table relational format. As such, plenty of time and effort is given to flattening and transforming the data such that it is optimized for binary classification machine learning to predict mortality. 

### Data
**Source:** [Synthea™ Novel coronavirus (COVID-19) synthetic data set](https://synthea.mitre.org/downloads)

**Format:** 16 relational tables (patients, conditions, encounters, medications, procedures, etc.)

**Background:** Per Synthea's publication (referenced below) "March through May 2020, a model of novel coronavirus (COVID-19) disease progression and treatment was constructed for the open-source Synthea patient simulation. The model was constructed using three peer-reviewed publications published in the early stages of the global pandemic ... The simulation outputs synthetic Electronic Health Records (EHR) ... For this simulation, we generated 124,150 synthetic patients, with 88,166 infections and 18,177 hospitalized patients. Patient symptoms, disease severity, and morbidity outcomes were calibrated using clinical data from the peer-reviewed publications ... The resulting model, data, and analysis are available as open-source code on GitHub and an open-access data set is available for download."

**Reference:** Walonoski J, Klaus S, Granger E, Hall D, Gregorowicz A, Neyarapally G, Watson A, Eastman J. Synthea™ Novel coronavirus (COVID-19) model and synthetic data set. Intelligence-Based Medicine. 2020 Nov;1:100007. https://doi.org/10.1016/j.ibmed.2020.100007

# EDA
## Entity Relationship Diagram
I was unable to find additional information on the relationships between the tables, so I created a basic entity relationship diagram. For the sake of simplicity, I did not include every feature. The large box of tables on the left is meant to signify that each of those tables have exactly two foreign keys: 'PATIENT' and 'ENCOUNTER' which relate them to their respective tables. Clicking on the diagram displays the full size.

<p align="center"><img src="/bin/EntityRelationshipDiagram.png" width="1000"/></p>

## Initial Exploration
Jupyter notebook (for ease of visualizing large tables): [covid_eda.ipynb](covid_eda.ipynb)

Python script: [covid_eda.py](covid_eda.py)

### Findings: 
- patients.csv
  - 124,150 unique patients
  - 24,150 patients (19%) with a 'death date'
- encounters.csv
  - Of 24,150 patients with 'death date' 18,134 (75%) had a 'death certification' encounter
  - Not all patients with 'death date' had an encounter related to COVID-19
- conditions.csv
  - Not all patients with 'death date' had a condition related to COVID-19
- observations.csv
  - Not all patients with 'death date' had an observation related to COVID-19

So this confirms what Synthea spelled out in their publication: this data is not limited to patients admitted for COVID, or even patients who ever had a diagnosis of COVID. It is not COVID-19 mortality data, but data which can be used to predict COVID-19 mortality. So the next step is to filter specifically for COVID-19 data.

## Exploring patients with diagnosis of COVID
Python script: [covid_eda3.py](covid_eda3.py)
### Findings: 
- 88,166 patients (71%) have had a diagnosis of COVID-19 at some point (this is in agreements with Synthea's data summary above)
- Of those patients, 3,641 have a death date
- Of those with a death date, 3,601 have a 'Death Certfication' encounter with the following 'Reason Description':

<p align="center"><img src="/bin/covid_death_cert_reason_description.png" width="500"/></p>

- Next steps:
  - Explore the timing of the COVID-19 diagnosis in those patients who do not have COVID-19 in the death certification encounter
  - Explore the patients who have a COVID-19 diagnosis who do not have death certification records
