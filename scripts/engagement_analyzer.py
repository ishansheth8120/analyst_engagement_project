"""
Module: engagement_analyzer.py
Purpose: Analyze weekly engagement and detect significant drops
"""

import pandas as pd

def analyze_engagement(df):
    # Add week number and year
    df['week'] = df['date'].dt.isocalendar().week
    df['year'] = df['date'].dt.year

    # Weekly aggregation
    weekly_summary = df.groupby(['analyst_id', 'analyst_name', 'team', 'year', 'week']).agg(
        total_duration=('duration_mins', 'sum'),
        unique_clients=('client_id', pd.Series.nunique),
        avg_duration_per_meeting=('duration_mins', 'mean')
    ).reset_index()

    # Sort for comparison
    weekly_summary = weekly_summary.sort_values(by=['analyst_id', 'year', 'week'])

    # Detect drops in engagement week-over-week
    drop_flags = []
    for analyst in weekly_summary['analyst_id'].unique():
        analyst_df = weekly_summary[weekly_summary['analyst_id'] == analyst].reset_index(drop=True)
        for i in range(1, len(analyst_df)):
            prev = analyst_df.loc[i - 1]
            curr = analyst_df.loc[i]
            duration_drop = prev['total_duration'] - curr['total_duration']
            client_drop = prev['unique_clients'] - curr['unique_clients']

            duration_pct_drop = duration_drop / prev['total_duration'] if prev['total_duration'] > 0 else 0
            client_pct_drop = client_drop / prev['unique_clients'] if prev['unique_clients'] > 0 else 0

            if duration_pct_drop > 0.5 or client_pct_drop > 0.5:
                drop_flags.append({
                    'analyst_id': curr['analyst_id'],
                    'analyst_name': curr['analyst_name'],
                    'team': curr['team'],
                    'year': curr['year'],
                    'week': curr['week'],
                    'duration_drop_%': round(duration_pct_drop * 100, 2),
                    'client_drop_%': round(client_pct_drop * 100, 2),
                    'prev_week_duration': prev['total_duration'],
                    'curr_week_duration': curr['total_duration'],
                    'prev_week_clients': prev['unique_clients'],
                    'curr_week_clients': curr['unique_clients'],
                })

    drop_flags_df = pd.DataFrame(drop_flags)
    return weekly_summary, drop_flags_df
