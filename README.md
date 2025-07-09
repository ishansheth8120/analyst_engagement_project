# Analyst Engagement Intelligence

A Python-based application with a Streamlit frontend that automates the analysis of weekly analyst-client engagement. It flags significant drops in client interactions or engagement duration and generates actionable insights using GenAI via OpenRouter.

## Features
- Upload weekly analyst-client interaction CSVs
- Automatic data cleaning and week-wise aggregation
- Flags significant drops in analyst engagement
- Generates professional GenAI-powered insights
- Download summarized reports in CSV format

## How It Works
- Upload Data: Upload a CSV with analyst interactions (analyst_id, client_id, date, duration_mins).
- Analyze: The app computes weekly summaries per analyst and detects engagement drops.
- Insights: Auto-generates concise weekly engagement insights using OpenRouter's LLMs (e.g., openrouter/cypher-alpha:free).
- Output: Downloadable report with insights and flags.

## Tech Stack
- Python
- Streamlit
- Pandas
- OpenRouter GenAI APIs

## Directory Structure

├── streamlit_app.py
├── scripts/
│   ├── data_cleaning.py
│   ├── engagement_analyzer.py
│   └── insight_generator.py
├── sample_data/
│   └── analyst_engagement_sample.csv
└── README.md

## Getting Started (Run Locally)
1. Clone the Repository
git clone https://github.com/your-username/analyst-engagement-intelligence.git
cd analyst-engagement-intelligence

2. Create and Activate Virtual Environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

3. Install Requirements

pip install -r requirements.txt

4. Set Your API Key
Create a .streamlit/secrets.toml file and add: (generate your api key from https://openrouter.ai/openrouter/cypher-alpha:free)
OPENROUTER_API_KEY = "your-api-key" 

5. Run the App
streamlit run streamlit_app.py

6. Open in Browser
Visit http://localhost:8501 in your browser to use the app.




