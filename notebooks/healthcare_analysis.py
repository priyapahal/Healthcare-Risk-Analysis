# ============================================
# Healthcare Risk Analysis Project
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

# ============================================
# File Paths (FULL ABSOLUTE PATHS)
# ============================================

BASE_PATH = "/Users/admin/Documents/Healthcare-Risk-Analysis"

RAW_DATA = BASE_PATH + "/data/raw/insurance.csv"
CLEAN_DATA = BASE_PATH + "/data/processed/cleaned_insurance.csv"
DASHBOARD_PATH = BASE_PATH + "/dashboard/"

# Create dashboard folder if it doesn't exist
os.makedirs(DASHBOARD_PATH, exist_ok=True)

# ============================================
# Load Dataset
# ============================================

print("\nLoading dataset...\n")

df = pd.read_csv(RAW_DATA)

print("Dataset loaded successfully!\n")
print(df.head())

print("\nDataset shape:", df.shape)
print("\nDataset info:")
print(df.info())

print("\nStatistical summary:")
print(df.describe())

print("\nMissing values:")
print(df.isnull().sum())

# ============================================
# Data Cleaning
# ============================================

print("\n--- Data Cleaning ---\n")

duplicates = df.duplicated().sum()
print("Duplicate rows:", duplicates)

df = df.drop_duplicates()

df.columns = df.columns.str.lower().str.strip()

print("\nUpdated column names:")
print(df.columns)

print("\nUnique categorical values:")
for col in ['sex', 'smoker', 'region']:
    print(f"{col}: {df[col].unique()}")

df.to_csv(CLEAN_DATA, index=False)
print(f"\nCleaned dataset saved to: {CLEAN_DATA}")

# ============================================
# Exploratory Data Analysis (EDA)
# ============================================

print("\n--- Exploratory Data Analysis ---\n")

# Distribution of charges
plt.figure(figsize=(8,5))
sns.histplot(df['charges'], kde=True)
plt.title("Distribution of Medical Charges")
plt.savefig(DASHBOARD_PATH + "charges_distribution.png")
plt.show()

# Smoker vs charges
plt.figure(figsize=(8,5))
sns.boxplot(x='smoker', y='charges', data=df)
plt.title("Medical Charges by Smoking Status")
plt.savefig(DASHBOARD_PATH + "smoker_vs_charges.png")
plt.show()

# Age vs charges
plt.figure(figsize=(8,5))
sns.scatterplot(x='age', y='charges', data=df)
plt.title("Age vs Medical Charges")
plt.savefig(DASHBOARD_PATH + "age_vs_charges.png")
plt.show()

# BMI vs charges
plt.figure(figsize=(8,5))
sns.scatterplot(x='bmi', y='charges', data=df)
plt.title("BMI vs Medical Charges")
plt.savefig(DASHBOARD_PATH + "bmi_vs_charges.png")
plt.show()

# Region average charges
region_avg = df.groupby('region')['charges'].mean()

plt.figure(figsize=(8,5))
region_avg.plot(kind='bar')
plt.title("Average Charges by Region")
plt.ylabel("Average Charges")
plt.savefig(DASHBOARD_PATH + "region_avg_charges.png")
plt.show()

# ============================================
# Key Insights
# ============================================

print("\n--- Key Insights ---\n")

print("1. Smokers have significantly higher medical costs.")
print("2. Medical charges increase with age.")
print("3. Higher BMI contributes to increased healthcare expenses.")
print("4. Regional variations exist in healthcare costs.")

print("\nAnalysis completed successfully!")


# ============================================
# SQL Database Creation & KPI Analysis
# ============================================

import sqlite3

print("\n==============================")
print(" SQL DATABASE & KPI ANALYSIS ")
print("==============================\n")

DB_PATH = BASE_PATH + "/healthcare.db"

conn = sqlite3.connect(DB_PATH)

df.to_sql("insurance", conn, if_exists="replace", index=False)

print("Database created and data loaded successfully.\n")

# KPI 1
print("KPI 1: Average Medical Cost")
result = pd.read_sql_query(
    "SELECT ROUND(AVG(charges), 2) AS avg_cost FROM insurance;",
    conn
)
print(result, "\n")

# KPI 2
print("KPI 2: Average Cost by Smoking Status")
result = pd.read_sql_query(
    """
    SELECT smoker,
           ROUND(AVG(charges), 2) AS avg_cost
    FROM insurance
    GROUP BY smoker;
    """,
    conn
)
print(result, "\n")

# KPI 3
print("KPI 3: Average Cost by Region")
result = pd.read_sql_query(
    """
    SELECT region,
           ROUND(AVG(charges), 2) AS avg_cost
    FROM insurance
    GROUP BY region;
    """,
    conn
)
print(result, "\n")

# KPI 4
print("KPI 4: Top 5 Highest Charges")
result = pd.read_sql_query(
    """
    SELECT age, bmi, smoker, charges
    FROM insurance
    ORDER BY charges DESC
    LIMIT 5;
    """,
    conn
)
print(result, "\n")

conn.close()

print("SQL KPI analysis completed successfully!")


