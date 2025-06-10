# LinkedIn Post Analyzer

A Streamlit application that analyzes LinkedIn posts using AI to extract insights about technology stacks, frameworks, and tools mentioned in the content.

## Features

- LinkedIn post scraping and analysis
- AI-powered technology stack detection
- Interactive Streamlit dashboard
- Rate limiting and error handling
- Fallback analysis for API failures

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/linkedin-post-analyzer.git
cd linkedin-post-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
```

4. Run the application:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `ai_analyzer.py`: AI analysis implementation using Gemini
- `linkedin_scraper.py`: LinkedIn post scraping functionality
- `config.py`: Configuration and constants
- `enrichment.py`: Additional analysis enrichment

## Requirements

- Python 3.8+
- Streamlit
- Google Generative AI
- Other dependencies listed in requirements.txt

## License

MIT License 