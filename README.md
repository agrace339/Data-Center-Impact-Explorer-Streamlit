# Data Center Impact Explorer

A Streamlit application exploring how U.S. data-center development intersects with four community concerns:

1. Drought
2. Electricity
3. Health
4. Politics

The application combines public datasets with maps, charts, and interactive controls developed for Drexel University's DSCI 591 capstone project.

## Run locally

From the project directory, install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Then start the application:

```bash
streamlit run data_center_explorer_final.py
```

## Project structure

```text
Data-Center-Impact-Explorer-Streamlit/
├── data/                         # Analysis-ready CSV files
├── images/                       # Charts and map images
├── data_center_explorer_final.py # Main Streamlit application
├── requirements.txt              # Python dependencies
└── README.md
```

## Main data sources

- FracTracker Alliance U.S. Data Centers Tracker
- U.S. Drought Monitor
- U.S. Energy Information Administration
- America's Health Rankings
- National Neighborhood Data Archive

Complete citations and source links are provided at the bottom of the application.

## Interpretation

The project compares data-center locations and development with existing environmental, electrical, health, and political conditions. The findings are descriptive and are intended to identify patterns and areas for further investigation.
