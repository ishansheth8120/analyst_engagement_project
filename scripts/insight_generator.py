"""
Module: insight_generator.py
Purpose: Generate auto-text insights for flagged engagement drops
"""
import pandas as pd
from openai import OpenAI
import streamlit as st
import requests



def generate_insight(drop_flags_df):
    insight_list = []

    for _, row in drop_flags_df.iterrows():
        comment = (
            f"Engagement for {row['analyst_name']} (Team: {row['team']}) dropped by "
            f"{row['duration_drop_%']}% in total duration and {row['client_drop_%']}% in client interactions "
            f"during week {row['week']} of {row['year']}. "
            f"Duration dropped from {row['prev_week_duration']} mins to {row['curr_week_duration']} mins, "
            f"clients dropped from {row['prev_week_clients']} to {row['curr_week_clients']}. "
            "Please validate the data or investigate further."
        )
        insight_list.append(comment)

    # Attach insight column to original DataFrame
    drop_flags_df["insight"] = insight_list
    return drop_flags_df

# # openai
# def generate_openai_insight(row):
#     prompt = f"""Generate a concise, professional weekly analyst engagement insight:
# Analyst: {row['analyst_name']}
# Team: {row['team']}OPENAI_API_KEY
# Week: {row['week']} of {row['year']}
# Duration drop: from {row['prev_week_duration']} mins to {row['curr_week_duration']} mins
# Client drop: from {row['prev_week_clients']} to {row['curr_week_clients']}"""
#     client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


#     response = client.chat.completions.create(
#         model="gpt-4.1",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response.choices[0].message.content.strip()



# # llama2    
# API_URL = "https://openrouter.ai/v1/chat/completions"
# HF_API_TOKEN = "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"

# def generate_llama2_insight(row):
#     prompt = (
#         f"Generate a weekly engagement summary:\n"
#         f"Analyst: {row['analyst_name']}\n"
#         f"Team: {row['team']}\n"
#         f"Week: {row['week']} of {row['year']}\n"
#         f"Duration dropped from {row['prev_week_duration']} to {row['curr_week_duration']} mins\n"
#         f"Client count dropped from {row['prev_week_clients']} to {row['curr_week_clients']}."
#     )

#     headers = {
#         "Authorization": f"Bearer {HF_API_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "inputs": prompt,
#         "options": {"wait_for_model": True}
#     }

#     response = requests.post(API_URL, headers=headers, json=payload)

#     try:
#         output = response.json()
#         return output[0]["generated_text"]
#     except Exception as e:
#         return f"⚠️ GenAI Error: {e} | Raw response: {response.text}"
    
# router
OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"  # ✅ Correct endpoint

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://your-app-name.com",  # 🔁 Replace with your domain (or keep it generic)
    "X-Title": "AnalystEngagementTool"
}

def generate_genai_insight(row):
    prompt = f"""
Generate a concise, professional weekly analyst engagement insight:
Analyst: {row['analyst_name']}
Team: {row['team']}
Week: {row['week']} of {row['year']}
Duration drop: from {row['prev_week_duration']} mins to {row['curr_week_duration']} mins
Client drop: from {row['prev_week_clients']} to {row['curr_week_clients']}
"""

    try:
        payload = {
            "model": "openrouter/cypher-alpha:free",  # ✅ Choose any available model on OpenRouter
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post(OPENROUTER_API_URL, headers=HEADERS, json=payload)
        output = response.json()
        return output["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"⚠️ GenAI Error: {e} | Raw response: {getattr(response, 'text', '')}"
