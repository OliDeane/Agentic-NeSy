This project is a simple AI-powered daily tech digest generator. It pulls top stories from Hacker News, filters for tech-relevant items, summarizes the top 5 stories using Gemini (Google AI Studio API), extracts cross-story trends, and emails the final digest to a prespecified email address.

This README explains how to set up and run the agent.

FEATURES
Fetches top stories from the Hacker News API
Filters for relevant tech topics using keyword matching
Summarizes each story using Gemini (Google AI Studio)
Generates a daily “Trends & Themes” summary
Sends a formatted report via SMTP email

Codebase Structure:

hacker_news_agent/
    src/
        main.py                     # Application entrypoint; runs agentic pipeline
        graph/
            digest_graph.py         # Builds the LangGraph workflow (HN → Filter → Summaries → Trends → Email)
        clients/
            hn_client.py            # Hacker News API interactions
            email_client.py         # SMTP email sender using a JSON config
        services/
            filter_service.py       # Keyword-based story filtering
            summarizer_service.py   # Gemini-powered story summarization and trend synthesis
            report_service.py       # Digest generator
        conncetion_tests/           # Small scripts for testing connections to relevant APIs
    email_config.json               # SMTP credentials and email settings
    requirements.txt                # Python dependencies
    README.md                       # Project documentation

REQUIREMENTS
Python version: 3.10
Install required Python packages:
pip install -r requirements.txt

API KEY AND EMAIL CONFIGURATION
Gemini API Key
Set the Gemini (Google AI Studio) API key as an environment variable:
export GOOGLE_API_KEY="YOUR_KEY_HERE"

Email Configuration
Edit the existing file named email_config.json according to required addresses:

{
"smtp_user": "your@gmail.com",
"smtp_pass": "your_app_password",
"email_from": "your@gmail.com",
"email_to": "recipient@company.com",
"smtp_host": "smtp.gmail.com",
"smtp_port": 587
}

Note: Gmail requires an App Password, not a normal password. 
My password is currently used in the config file, but this will be reset.

RUNNING THE PROGRAM
Run the script with:
python main.py

Terminal output:
The Markdown digest printed in the terminal
An email delivered to the specified inbox

OUTPUT FORMAT
The generated digest includes:
A “Trends & Themes” synthesis
The top 5 tech-relevant HN stories, including:
Title
HN Score
URL
2–3 sentence summary