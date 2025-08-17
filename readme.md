# USDA Agricultural Production Analysis

## 📖 Project Overview
This project was inspired by the [UC Davis SQL for Data Science](https://www.coursera.org/learn/sql-for-data-science) course on Coursera.  
The goal is to showcase **SQL querying, data engineering, and analytical skills** by building a reproducible pipeline that moves data from CSV files into a SQLite database, and then uses **Python (Pandas + SQL)** to analyze agricultural production trends across the United States.

The datasets include production information for:
- Milk  
- Cheese  
- Coffee  
- Honey  
- Yogurt  
- State lookup reference table  

Data spans **multiple years and states**, enabling insights into **trends, anomalies, and strategic recommendations**.

---

## ⚙️ Pipeline
The project includes a custom Python module:

- **`cvs_to_sqlite_v4.py`**  
  - Converts multiple CSV files into a single SQLite database (`.db`)  
  - Each CSV becomes its own **table**  
  - Ensures a clean, query-ready dataset for analysis  

This pipeline highlights **data engineering skills** such as ETL (Extract, Transform, Load), modular coding, and reproducible workflows.

---

## 📊 Analysis Notebook
- **`production_query.ipynb`**  
  - Walks through connecting to the SQLite database  
  - Runs **SQL queries directly from Python**  
  - Uses **Pandas** to visualize and explore results  
  - Produces tables, charts, and insights for reporting  

The notebook is structured as follows:
1. **Data Exploration** – Loading and previewing data  
2. **SQL Queries** – State-level and time-series analysis  
3. **Visualization** – Highlighting trends and anomalies  
4. **Insights & Recommendations** – Data-driven findings  

---

## 🔧 Tools & Technologies
- **Python** – main driver for data pipeline and analysis  
- **SQLite** – relational database for structured queries  
- **Pandas** – data cleaning, transformation, and visualization  

---

## ✅ Current Deliverables
- CSV-to-SQLite pipeline module  
- Query-ready SQLite database  
- Jupyter notebook with analysis and visualizations  

---

## 🚀 Future Work
Planned enhancements include:
- Advanced SQL querying: **joins, subqueries, groupings**  
- Expanded **trend and anomaly detection**  
- Dashboard-style reporting of key findings  
- Integration into a broader **data engineering portfolio**  

