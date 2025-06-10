import streamlit as st
import pandas as pd
from linkedin_scraper import LinkedInScraper
from ai_analyzer import AIAnalyzer
from enrichment import PostEnricher
import config
import time

# Set page config
st.set_page_config(
    page_title="LinkedIn Lead Generator",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
# Initialize analysis_errors in session state
if 'analysis_errors' not in st.session_state:
    st.session_state.analysis_errors = []
# Initialize the minimum lead score slider value in session state using the slider's key
if 'min_lead_score_slider' not in st.session_state:
    st.session_state.min_lead_score_slider = float(config.MIN_LEAD_SCORE)

def update_min_score_state():
    """Callback function to update min_lead_score_slider_value in session state."""
    # Explicitly get the slider value from the widget's key and update the session state variable
    st.session_state.min_lead_score_slider = float(st.session_state.min_lead_score_slider)

def main():
    st.title("🔍 LinkedIn Lead Generator")
    st.markdown("""
    This tool analyzes LinkedIn posts from startup founders and technical builders to identify potential business opportunities.
    Enter your search criteria below to get started.
    """)

    # Search inputs
    col1, col2 = st.columns(2)
    with col1:
        keywords = st.text_input(
            "Search Keywords",
            placeholder="e.g., 'Built with Streamlit', 'Made a dashboard in Gradio'",
            key='search_keywords_input' # Add a key for the text input
        )
    with col2:
        tags = st.text_input(
            "Optional Tags",
            placeholder="e.g., #buildinpublic, #indiehacker",
            key='tags_input' # Add a key for the text input
        )

    # Advanced options
    with st.expander("Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            enable_enrichment = st.checkbox("Enable Email & Website Extraction", value=True, key='enable_enrichment_checkbox') # Add a key
        with col2:
            enable_sentiment = st.checkbox("Enable Sentiment Analysis", value=True, key='enable_sentiment_checkbox') # Add a key

    # Search button
    if st.button("🔍 Search Posts", type="primary", key='search_button'): # Add a key
        if not keywords:
            st.error("Please enter search keywords")
            return

        with st.spinner("Searching LinkedIn posts..."):
            try:
                # Initialize components
                scraper = LinkedInScraper()
                analyzer = AIAnalyzer()
                enricher = PostEnricher()

                # Search posts
                posts = scraper.search_posts(keywords, tags)

                if not posts:
                    st.warning("No posts found matching your criteria")
                    # Clear previous results if no new posts are found
                    st.session_state.results = None
                    return

                # Process posts
                results = []
                # Clear previous analysis errors
                st.session_state.analysis_errors = []
                progress_bar = st.progress(0)

                for i, post in enumerate(posts):
                    # Extract post data
                    post_data = scraper.extract_post_data(post)

                    # Analyze post
                    # Ensure post_text is a string before passing to analyzer
                    post_text = str(post_data.get("post_text", "")) # Use .get() with default for safety
                    try:
                        analysis = analyzer.analyze_post(post_text)
                        analysis = analyzer.enrich_analysis(analysis)

                        # Combine data - Use .get() with default values to handle potential missing keys
                        result = {
                            "Post Text": post_data.get("post_text", ""),
                            "Post URL": post_data.get("post_url", ""),
                            "Post Date": post_data.get("post_date", ""),
                            "Tech Stack": ", ".join(analysis.get("tech_stack", [])),
                            "Project Stage": analysis.get("project_stage", "unknown"),
                            "Missing Features": ", ".join(analysis.get("missing_features", [])),
                            "Potential Needs": ", ".join(analysis.get("potential_needs", [])),
                            "Suggested Services": ", ".join(analysis.get("suggested_services", [])),
                            "Lead Score": float(analysis.get("lead_score", 0.0)) # Ensure lead score is float
                        }

                        # Apply enrichment if enabled
                        if st.session_state.get('enable_enrichment_checkbox', True) or st.session_state.get('enable_sentiment_checkbox', True):
                             result = enricher.enrich_post(result)

                        results.append(result)

                    except Exception as e:
                         error_message = f"Error analyzing post \"{post_data.get('post_text', '...')[:50]}...\": {str(e)}"
                         st.session_state.analysis_errors.append(error_message)
                         # Append a placeholder result to maintain structure even if analysis fails for a post
                         results.append({
                             "Post Text": post_data.get("post_text", ""),
                             "Post URL": post_data.get("post_url", ""),
                             "Post Date": post_data.get("post_date", ""),
                             "Tech Stack": "Error",
                             "Project Stage": "Error",
                             "Missing Features": "Error",
                             "Potential Needs": "Error",
                             "Suggested Services": "Error",
                             "Lead Score": 0.0 # Assign a low score on error
                         })


                    # Update progress
                    progress_bar.progress((i + 1) / len(posts))
                    time.sleep(0.05)  # Small delay to show progress

                # Store results
                if results:
                    st.session_state.results = pd.DataFrame(results)
                else:
                     st.session_state.results = None

            except Exception as e:
                st.error(f"An error occurred during search or processing: {str(e)}")
                st.session_state.results = None # Clear results on major error
                return

    # Display results
    if st.session_state.results is not None:
        st.markdown("### 📊 Analysis Results")

        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            # Access the slider value directly from session state using its key and ensure it's float
            min_score_value = float(st.session_state.get('min_lead_score_slider', config.MIN_LEAD_SCORE))

            st.slider(
                "Minimum Lead Score",
                min_value=0.0,
                max_value=10.0,
                value=min_score_value,
                step=0.5,
                key='min_lead_score_slider',  # Use the key to manage state
                on_change=update_min_score_state # Add the callback function
            )
            # Use the value from session state for filtering
            min_score = st.session_state.get('min_lead_score_slider', float(config.MIN_LEAD_SCORE))

        with col2:
            project_stage = st.multiselect(
                "Project Stage",
                options=config.PROJECT_STAGES,
                default=config.PROJECT_STAGES,
                key='project_stage_multiselect' # Add a key
            )
        with col3:
            if st.session_state.get('enable_sentiment_checkbox', True): # Check the checkbox state via session state
                sentiment = st.multiselect(
                    "Sentiment",
                    options=["Positive", "Neutral", "Negative"],
                    default=["Positive", "Neutral", "Negative"],
                    key='sentiment_multiselect' # Add a key
                )
            else:
                # If sentiment analysis is disabled, filter by all sentiments implicitly
                sentiment = ["Positive", "Neutral", "Negative"]

        # Filter results
        # Ensure min_score is float for comparison
        filtered_results = st.session_state.results[
            (st.session_state.results["Lead Score"] >= float(min_score)) &
            (st.session_state.results["Project Stage"].isin(project_stage))
        ]

        if st.session_state.get('enable_sentiment_checkbox', True):
             # Ensure Sentiment column exists before filtering
            if "Sentiment" in filtered_results.columns:
                 filtered_results = filtered_results[
                     filtered_results["Sentiment"].isin(sentiment)
                 ]

        # Display table
        st.dataframe(
            filtered_results,
            use_container_width=True,
            hide_index=True
        )

        # Download button
        csv = filtered_results.to_csv(index=False).encode('utf-8') # Encode for download
        st.download_button(
            "📥 Download Results",
            csv,
            "linkedin_leads.csv",
            "text/csv",
            key='download-csv'
        )

        # Display insights
        if not filtered_results.empty:
            st.markdown("### 📈 Insights")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Average Lead Score",
                    f"{filtered_results['Lead Score'].mean():.1f}"
                )
                if st.session_state.get('enable_sentiment_checkbox', True) and "Sentiment" in filtered_results.columns:
                    st.metric(
                        "Positive Sentiment %",
                        f"{(filtered_results['Sentiment'] == 'Positive').mean() * 100:.1f}%"
                    )

            with col2:
                if st.session_state.get('enable_enrichment_checkbox', True) and ("Email" in filtered_results.columns or "Website" in filtered_results.columns):
                     contact_info_count = 0
                     if "Email" in filtered_results.columns: contact_info_count += filtered_results['Email'].notna().sum()
                     if "Website" in filtered_results.columns: contact_info_count += filtered_results['Website'].notna().sum()
                     st.metric(
                         "Posts with Contact Info",
                         f"{contact_info_count}"
                     )

                # Check if 'Engagement Score' column exists before accessing
                if 'Engagement Score' in filtered_results.columns:
                    st.metric(
                        "Average Engagement",
                        f"{filtered_results['Engagement Score'].mean():.1f}"
                    )
        else:\
             st.info("No leads found matching the selected filters.")

    # Display errors from analysis if any
    if st.session_state.get('analysis_errors', []):
        st.markdown("### ⚠️ Analysis Errors")
        for error in st.session_state.analysis_errors:
            st.warning(error)
        # Decide whether to clear errors here or let them persist until next search
        # For now, let's keep them until the next successful search or app reload.
        # st.session_state.analysis_errors = [] # Uncomment to clear errors after display


if __name__ == "__main__":
    # Initialize session state variables before calling main
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'analysis_errors' not in st.session_state:
        st.session_state.analysis_errors = []
    if 'min_lead_score_slider' not in st.session_state:
         st.session_state.min_lead_score_slider = float(config.MIN_LEAD_SCORE)

    main() 