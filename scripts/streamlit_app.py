import os
import sys
import streamlit as st
import pandas as pd
import openai


# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.data_cleaning import clean_engagement_data
from scripts.engagement_analyzer import analyze_engagement
from scripts.insight_generator import generate_insight,generate_genai_insight

st.title("📊 Analyst Engagement Intelligence")

uploaded_file = st.file_uploader("Upload Analyst Engagement CSV", type=["csv"])

if uploaded_file:
    try:
        # Step 1: Read and show raw data
        df_raw = pd.read_csv(uploaded_file)
        st.subheader("🔍 Raw Uploaded Data")
        st.dataframe(df_raw)

        # Step 2: Clean and analyze
        df_cleaned = clean_engagement_data(df_raw)
        df_summary = analyze_engagement(df_cleaned)

        # Step 3: Generate insights
        weekly_summary, drop_flags_df = analyze_engagement(df_cleaned)
        df_summary = generate_insight(drop_flags_df)

        # Step 4: Display summary with insights
        st.subheader("✅ Weekly Summary with Insights")
        st.dataframe(df_summary)

        # Step 5: Download option
        csv = df_summary.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Weekly Report",
            data=csv,
            file_name="weekly_engagement_report.csv",
            mime="text/csv"
        )


                
        if st.button("✨ Generate GenAI Insights"):
            st.subheader("🤖 GPT-Powered Insights")
            genai_insights = df_summary.apply(generate_genai_insight, axis=1)
            for i, insight in enumerate(genai_insights):
                st.markdown(f"**{i+1}.** {insight}")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
