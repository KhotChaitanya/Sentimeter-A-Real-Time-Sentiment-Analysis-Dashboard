# Sentimeter: A Real-Time Sentiment Analysis Dashboard

A dynamic, real-time, multi-tab sentiment analysis dashboard built with Python and Streamlit to provide immediate, multi-faceted insights into textual data.

## Overview

This project provides an end-to-end solution for real-time text sentiment analysis. Utilizing the VADER sentiment model, the system processes user input to deliver a comprehensive analytical overview. The dashboard is organized into a clean, multi-tab interface that allows users to seamlessly transition from a high-level summary to granular, sentence-level insights. The application is designed for anyone needing to quickly understand the emotional tone of feedback, reviews, or any other textual data.

## Technologies Used

* **Python 3.8+**
* **Streamlit:** For the interactive web application and UI.
* **Core Libraries:**
    * **Pandas:** For data manipulation and aggregation.
    * **VADER (vaderSentiment):** For the core sentiment analysis engine.
    * **Plotly:** For creating dynamic, interactive charts (pie, bar, area, histogram).
    * **Matplotlib & WordCloud:** For generating keyword cloud visualizations.
    * **Pillow:** For programmatic image generation.

## Features

* **Real-Time Analysis:** Instantly analyze text and see all dashboard components update live.
* **Multi-Tab Interface:** Organizes analysis into four distinct sections: Overall Dashboard, Latest Analysis, Historical Trends, and Keyword & Sentence Insights.
* **Comprehensive Metrics:** Calculates and displays key metrics, including Total Inputs, Average Sentiment Score, and the count of Positive, Negative, and Neutral inputs.
* **Rich Visualizations:** Generates a suite of charts to provide a multi-faceted view of the data:
    * Donut Chart for overall sentiment distribution.
    * Bar Chart comparing the sentiment of recent inputs.
    * Stacked Area Chart to track sentiment composition over time.
    * Histogram to show the distribution of sentiment scores.
* **Granular Text Insights:**
    * **Tri-Category Word Clouds:** Creates separate word clouds for Positive, Negative, and Neutral keywords.
    * **Top Sentences Tables:** Automatically extracts and tables the most impactful sentences for each sentiment category.
* **Data Export:** Includes a "Download Center" to export the complete analysis history as a CSV file.

## Dashboard Tabs Explained

The project follows a structured 4-tab layout to present the analysis:

1.   **Home Page:** This is the landing page of the Sentimeter.
<img width="1920" height="1020" alt="homepage" src="https://github.com/user-attachments/assets/9947a139-f3bd-44f8-bb16-bcdcf043adce" />

2.   **Overall Dashboard:** This is the main hub providing a holistic view of all text analyzed during the session, providing a comprehensive summary of all analyzed inputs, including top-level metrics and a 2x2 grid of key visualizations. It's ideal for understanding the big picture at a glance.
<img width="1920" height="1020" alt="sentiment_dashboard" src="https://github.com/user-attachments/assets/6dcec5a6-96bf-40e4-8ba3-bd90cfb05215" />

3.  **Latest Analysis:** This tab isolates the most recent input, allowing for a detailed examination of a single piece of feedback without the context of previous entries.
<img width="1920" height="1020" alt="LatestAnalysis" src="https://github.com/user-attachments/assets/fdaa9a0c-21dd-46f5-8938-f9fb99b5f706" />

4.  **Historical Trends:** This tab is crucial for understanding the narrative of the data. The stacked area chart visualizes how the sentiment composition has evolved over time.
<img width="1920" height="1020" alt="HistoricalTrends" src="https://github.com/user-attachments/assets/b62d93f1-0902-4e6d-895b-c9e5da1a8b18" />

5.  **Keyword & Sentence Insights:** This is the deep-dive section. It uses word clouds to identify the terms driving the sentiment and tables to display the most exemplary sentences for each category.
<img width="1920" height="1020" alt="Keyword SentimentAnalysis" src="https://github.com/user-attachments/assets/f2f345ab-d625-47a3-988d-861e6d88f7c0" />

This tab offers the most granular level of analysis, with separate word clouds and tables for positive, negative, and neutral content.
- **Keyword Clouds:**
   - Positive Keywords:
     <img width="858" height="490" alt="positive keyword" src="https://github.com/user-attachments/assets/d306ed2f-77b9-4e45-a88e-ea4c44dcb0a5" />

   - Negative Keywords:
     <img width="875" height="497" alt="NegativeKeywords" src="https://github.com/user-attachments/assets/b7f5a339-6e1d-4bc4-856f-c289ffe9ccad" />

   - Neutral Keywords :
     <img width="912" height="512" alt="NeutralKeywords" src="https://github.com/user-attachments/assets/b9b3965b-3d54-45c3-aefe-41eef83e1534" />

- **Top Sentences by Sentiment:**
   - Most Positive Sentences:
     <img width="892" height="257" alt="MPS" src="https://github.com/user-attachments/assets/a2253691-8c9a-4291-a997-4caba01604ec" />

   - Most Negative Sentences:
     <img width="862" height="262" alt="MNS" src="https://github.com/user-attachments/assets/1ddce7f7-afa8-46c4-878a-af4cd85b8822" />

   - Most Neutral Sentences:
     <img width="872" height="157" alt="MNES" src="https://github.com/user-attachments/assets/39777fc2-0dcc-404e-b4c1-d6aae014de3f" />


## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/KhotChaitanya/Sentimeter-A-Real-Time-Sentiment-Analysis-Dashboard.git](https://github.com/KhotChaitanya/Sentimeter-A-Real-Time-Sentiment-Analysis-Dashboard.git)
    cd Sentimeter-A-Real-Time-Sentiment-Analysis-Dashboard
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    The `requirements.txt` file contains all the necessary libraries.
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    Navigate to the project directory in your terminal and run:
    ```sh
    streamlit run SentimentAnalysis.py
    ```
    The application will open automatically in a new tab in your default web browser.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
