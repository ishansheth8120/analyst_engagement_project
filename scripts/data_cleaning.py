# Functions to clean and preprocess the data
"""
Module: data_cleaning.py
Purpose: Clean and preprocess analyst engagement data
"""


import pandas as pd

def clean_engagement_data(df):
    # Parse date with day-first format (important for DD-MM-YYYY like 01-06-2024)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

    # Drop rows with invalid or missing dates
    df = df.dropna(subset=['date'])

    # Filter out records where engagement is <= 5 minutes
    df = df[df['duration_mins'] > 5].reset_index(drop=True)

    return df


