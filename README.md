# AADHAAR SAMIKSHA
### Beyond Numbers. Towards Digital Inclusion.

## Team Name : Dominex
## Team Members: Archit Mittal, Harshda 

An interactive data analytics platform that transforms Aadhaar enrolment and biometric datasets into meaningful insights through geographical, temporal, and demographic analysis.

**[Live Demo](https://aadhaar-samiksha-g9pwkm7qicncja4qkuf4jw.streamlit.app/) · [Project Presentation (PPT)](https://drive.google.com/file/d/1kV49nSCeh5OZ8mjRFd6usrfPQx0xWnkM/view?usp=sharing)**

---

## Problem Statement

Aadhaar generates large volumes of enrolment and biometric data across different regions, age groups, and time periods. However, extracting meaningful insights from this complex data remains challenging.

Identifying regional variations, demographic patterns, and changing enrolment trends is essential for understanding data gaps and supporting informed planning and decision-making.

## Our Solution

AADHAAR SAMIKSHA bridges this gap by converting raw Aadhaar datasets into an interactive analytical platform.

It enables users to explore enrolment and biometric trends, compare geographical regions, understand age-wise patterns, and obtain meaningful insights through visual dashboards and an integrated analytical chatbot.

## Key Features

- **Interactive Dashboard:** Centralized view of important metrics and analytical summaries.
- **Temporal Analysis:** Explore daily and monthly enrolment trends and growth patterns.
- **Geographical Analysis:** Compare states, districts, and pincodes to identify regional variations.
- **Age-wise Analysis:** Examine enrolment and biometric activity across different age groups.
- **Automated Insights:** Generate data-driven observations based on selected filters.
- **SAMIKSHA Chatbot:** Interact with the dataset through predefined analytical questions.
- **Dynamic Filters:** Explore data using date, state, district, and pincode filters.

## System Architecture

The project follows a data-processing and visualization pipeline:

`
       Aadhaar Dataset (CSV)
                |
                v
       Data Preprocessing
         (Pandas, NumPy)
                |
                v
        Cleaned Dataset
       (Compressed Pickle)
                |
                v
       Data Processing Layer
      (Filtering & Aggregation)
                |
                v
        Streamlit Application
                |
       +--------+---------+
       |        |         |
       v        v         v
    Overview Analytics  Chatbot
       |        |         |
       v        v         v
      KPIs   Plotly     Query-based
             Charts      Insights
       |        |         |
       +--------+---------+
                |
                v
       Meaningful Insights
``

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Data Visualization | Plotly |
| Frontend & Dashboard | Streamlit |
| Data Storage | CSV, Pickle (GZIP compression) |
| Version Control | Git, GitHub |
| Deployment | Streamlit Community Cloud |

## Dashboard Modules

| Module | Description |
|---|---|
| Overview | Key metrics, enrolment trends, and top districts |
| Temporal Analysis | Monthly trends, yearly patterns, and growth analysis |
| Geographical Analysis | District-wise and pincode-wise comparisons |
| Age Analysis | Age-group enrolment and biometric distribution |
| SAMIKSHA Chatbot | Interactive exploration of dataset insights |

## Outputs & Analytical Findings

The platform provides:

- Overall enrolment and biometric activity metrics.
- Daily and monthly trends to understand changes over time.
- Identification of districts and pincodes with higher or lower recorded activity.
- Age-group comparisons across enrolment and biometric categories.
- Correlation analysis between selected numerical variables.
- Filter-based insights to support deeper regional and temporal exploration.

**Analytical Value:** These outputs help users identify variations and patterns in the available dataset and highlight areas that may require further investigation.

*Note: The dashboard reports patterns in the available dataset. These patterns do not independently establish the causes of regional differences or prove service exclusion.*

## Dataset

The project uses an Aadhaar enrolment and biometric dataset containing fields such as:

- Date
- State
- District
- Pincode
- Age-wise enrolment counts
- Age-wise biometric counts

The dataset is preprocessed before analysis to handle data types, missing values, and invalid records.

## Project Impact

AADHAAR SAMIKSHA aims to make large-scale Aadhaar data easier to understand and explore.

It can support:
- Data-driven regional comparisons.
- Better understanding of demographic patterns.
- Identification of unusual trends for further investigation.
- More informed planning and resource-allocation discussions.
- Accessible analytical exploration for researchers and stakeholders.

## Future Scope

- Integration of more recent datasets for continuous analysis.
- Advanced anomaly detection for unusual enrolment patterns.
- Interactive geographical maps.
- Predictive analytics for trend forecasting.
- Enhanced natural-language querying using AI.

## Run Locally

**1. Clone the repository**

`
git clone https://github.com/Harshda-69/AADHAAR-SAMIKSHA.git
cd AADHAAR-SAMIKSHA
``

**2. Install dependencies**

`
pip install -r requirements.txt
``

**3. Run the application**

`
streamlit run app.py
``

## Project Links

- **Live Application:** https://aadhaar-samiksha-g9pwkm7qicncja4qkuf4jw.streamlit.app/
- **Project Presentation:** https://drive.google.com/file/d/1kV49nSCeh5OZ8mjRFd6usrfPQx0xWnkM/view?usp=sharing
- **GitHub Repository:** https://github.com/Harshda-69/AADHAAR-SAMIKSHA

---

### AADHAAR SAMIKSHA
**Beyond Numbers. Towards Digital Inclusion.**
