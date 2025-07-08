"""
Main script for Analyst Engagement Intelligence Project
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.data_cleaning import clean_engagement_data
from scripts.engagement_analyzer import analyze_engagement
from scripts.insight_generator import generate_insight
import pandas as pd
import os,sys
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Set Paths
DATA_FOLDER = 'data'
OUTPUT_FOLDER = 'output'
INPUT_FILE = os.path.join(DATA_FOLDER, "analyst_engagement.csv")


def main():
    print("Starting Analyst Engagement Intelligence Workflow...")

    # 1. Load and Clean Data 
    df = pd.read_csv(INPUT_FILE)
    clean_df = clean_engagement_data(df)


    # 2. Analyze engagement
    weekly_summary, drop_flags = analyze_engagement(clean_df)

    # 3.  Generate Insights
    insights = generate_insight(drop_flags)

    # Step 4: Save output
    today_str = datetime.today().strftime("%Y%m%d")
    output_file = os.path.join(OUTPUT_FOLDER, f"weekly_report_{today_str}.xlsx")

    with pd.ExcelWriter(output_file) as writer:
        weekly_summary.to_excel(writer, sheet_name = 'Weekly Summary', index = False )
        drop_flags.to_excel(writer, sheet_name ='Drop Flags', index = False)
        pd.DataFrame({"Insights":insights}).to_excel(writer, sheet_name="Insights", index=False)

    print(f"Report saved to {output_file}")

if __name__ == "__main__":
    main()



