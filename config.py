import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configuration
MAX_POSTS = 20  # Maximum number of posts to analyze
MIN_LEAD_SCORE = 5  # Minimum lead score to consider
TECH_STACK_KEYWORDS = [
    'streamlit', 'gradio', 'flask', 'django', 'react', 'vue', 'angular',
    'node.js', 'python', 'javascript', 'typescript', 'next.js', 'tailwind',
    'bootstrap', 'material-ui'
]

# Project stages
PROJECT_STAGES = ['idea', 'prototype', 'mvp', 'launched']

# Missing features to look for
MISSING_FEATURES = [
    'login', 'authentication', 'user roles', 'analytics', 'mobile responsive',
    'database', 'api', 'payment integration', 'email notifications'
]

# GPT-4 Analysis Prompt Template
ANALYSIS_PROMPT = """You are a product development expert. Analyze the following startup/product post.

Post:
{post_text}

Return a JSON object with the following structure:
{{
    "tech_stack": [list of technologies used],
    "project_stage": "idea/prototype/mvp/launched",
    "missing_features": [list of missing features],
    "potential_needs": [list of potential business needs],
    "lead_score": float between 0 and 10
}}

Consider the following for scoring:
- Higher score if using minimal UI tools (Streamlit, Gradio)
- Higher score if missing critical features
- Higher score if project shows potential for monetization
- Higher score if project has traction (comments, likes)
"""

# Default analysis when AI fails
DEFAULT_ANALYSIS = {
    "tech_stack": [],
    "project_stage": "unknown",
    "missing_features": [],
    "potential_needs": [],
    "lead_score": 0.0
} 