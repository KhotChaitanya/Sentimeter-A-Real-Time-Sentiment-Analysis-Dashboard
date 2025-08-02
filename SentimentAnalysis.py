import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    page_icon="📊",
    layout="wide",
)

# --- Custom CSS for a Light, Vibrant Theme ---
def local_css(file_name):
    with open(file_name, "w") as f:
        f.write("""
        body {
            background-color: #F0F2F6;
        }
        .main-title {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            color: #2C3E50;
        }
        .stMetric {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .stTextArea textarea {
            background-color: #FFFFFF;
            color: #2C3E50;
            border: 1px solid #BDC3C7;
            border-radius: 5px;
        }
        """)
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# --- VADER Sentiment Analyzer ---
@st.cache_resource
def get_analyzer():
    return SentimentIntensityAnalyzer()

# --- Helper Functions ---
def analyze_sentiment(text):
    analyzer = get_analyzer()
    return analyzer.polarity_scores(text)

def split_into_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', text)
    return [s.strip() for s in sentences if s.strip()]

def generate_wordcloud(text, background_color="white", max_words=100):
    if not text:
        return None
    wordcloud = WordCloud(width=800, height=400, background_color=background_color, max_words=max_words, colormap='viridis').generate(text)
    return wordcloud

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# --- Initialize Session State ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['text', 'compound', 'pos', 'neg', 'neu', 'timestamp'])
if 'last_analysis' not in st.session_state:
    st.session_state.last_analysis = None

# --- UI Layout ---
st.markdown("<h1 class='main-title'>📊 Comprehensive Sentiment Dashboard</h1>", unsafe_allow_html=True)

# --- Input Area ---
text_input = st.text_area(
    "Enter text for analysis:",
    height=150,
    placeholder="Enter one or more sentences. For example: 'Streamlit is an amazing tool! It makes building apps so easy and fun. However, some parts can be tricky to learn at first.'"
)

if st.button("Analyze"):
    if text_input:
        scores = analyze_sentiment(text_input)
        st.session_state.last_analysis = {'text': text_input, **scores}
        
        new_entry = pd.DataFrame([{'text': text_input, **scores, 'timestamp': pd.Timestamp.now()}])
        st.session_state.history = pd.concat([st.session_state.history, new_entry], ignore_index=True)

# --- TABS FOR VISUALIZATIONS ---
if not st.session_state.history.empty:
    tab1, tab2, tab3, tab4 = st.tabs(["Overall Dashboard", "Latest Analysis", "Historical Trends", "Keyword & Sentence Insights"])

    # --- TAB 1: Overall Dashboard ---
    with tab1:
        st.header("Overall Analysis of All Inputs")
        history_df = st.session_state.history
        
        # Correctly count sentiments based on VADER thresholds
        pos_mask = history_df['compound'] > 0.05
        neg_mask = history_df['compound'] < -0.05
        neu_mask = ~pos_mask & ~neg_mask

        pos_count = pos_mask.sum()
        neg_count = neg_mask.sum()
        neu_count = neu_mask.sum()
        
        avg_score = history_df['compound'].mean()
        all_text = ' '.join(history_df['text'])
        
        # Display Metrics
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Total Inputs", len(history_df))
        m2.metric("Avg. Sentiment", f"{avg_score:.2f}")
        m3.metric("Positive Inputs", pos_count)
        m4.metric("Negative Inputs", neg_count)
        m5.metric("Neutral Inputs", neu_count)
        
        st.info("Sentiment is classified as 'Positive' if score > 0.05, 'Negative' if score < -0.05, and 'Neutral' otherwise.")
        
        c1, c2 = st.columns(2)
        with c1:
            # Overall Sentiment Distribution
            st.subheader("Overall Sentiment Distribution")
            overall_counts = {'Positive': pos_count, 'Negative': neg_count, 'Neutral': neu_count}
            fig_pie_overall = px.pie(names=list(overall_counts.keys()), values=list(overall_counts.values()), title="Distribution of All Inputs", color_discrete_map={'Positive':'#00CC96', 'Negative':'#EF553B', 'Neutral':'#636EFA'}, hole=0.3)
            st.plotly_chart(fig_pie_overall, use_container_width=True)

            # Overall Word Cloud
            st.subheader("Overall Keyword Cloud")
            if all_text:
                overall_wc = generate_wordcloud(all_text)
                st.image(overall_wc.to_image())
            else:
                st.info("No text available for word cloud.")

        with c2:
            # Sentiment Comparison of Last 5 Entries
            st.subheader("Sentiment of Last 5 Entries")
            last_5 = history_df.tail(5).copy()
            last_5['Entry'] = [f"Input {len(history_df) - len(last_5) + i + 1}" for i in range(len(last_5))]
            fig_bar_comp = px.bar(last_5, x='Entry', y=['pos', 'neg', 'neu'], title="Sentiment Breakdown of Recent Inputs", labels={'value': 'Score', 'variable': 'Sentiment'}, color_discrete_map={'pos':'#00CC96', 'neg':'#EF553B', 'neu':'#636EFA'})
            st.plotly_chart(fig_bar_comp, use_container_width=True)
            
            # Histogram of All Scores
            st.subheader("Distribution of All Sentiment Scores")
            fig_hist = px.histogram(history_df, x='compound', title="Frequency of Sentiment Scores", nbins=20, color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig_hist, use_container_width=True)
        
        st.markdown("---")
        # --- Simplified Download Center ---
        st.header("Download Center")
        st.download_button(
            label="📥 Download Full Data (CSV)",
            data=convert_df_to_csv(history_df),
            file_name='sentiment_analysis_history.csv',
            mime='text/csv',
        )

    # --- TAB 2: Latest Analysis ---
    with tab2:
        st.header("Analysis of Latest Input")
        latest_analysis = st.session_state.last_analysis
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric(label="Overall Sentiment Score", value=f"{latest_analysis['compound']:.2f}", delta="Positive" if latest_analysis['compound'] > 0 else "Negative" if latest_analysis['compound'] < 0 else "Neutral")
            sentiment_counts = {'Positive': latest_analysis['pos'], 'Negative': latest_analysis['neg'], 'Neutral': latest_analysis['neu']}
            fig_pie = px.pie(names=list(sentiment_counts.keys()), values=list(sentiment_counts.values()), title="Sentiment Distribution", color_discrete_map={'Positive':'#00CC96', 'Negative':'#EF553B', 'Neutral':'#636EFA'})
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.subheader("Color-Coded Sentence Analysis")
            sentences = split_into_sentences(latest_analysis['text'])
            for sentence in sentences:
                score = analyze_sentiment(sentence)['compound']
                if score > 0.05:
                    st.markdown(f"<p style='color: green; border-left: 5px solid green; padding-left: 10px;'>{sentence}</p>", unsafe_allow_html=True)
                elif score < -0.05:
                    st.markdown(f"<p style='color: red; border-left: 5px solid red; padding-left: 10px;'>{sentence}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='color: gray; border-left: 5px solid gray; padding-left: 10px;'>{sentence}</p>", unsafe_allow_html=True)

    # --- TAB 3: Historical Trends ---
    with tab3:
        st.header("Historical Trends")
        
        if len(history_df) > 1:
            st.subheader("Sentiment Composition Over Time")
            history_df_long = history_df.melt(id_vars='timestamp', value_vars=['pos', 'neg', 'neu'], var_name='Sentiment', value_name='Score')
            fig_area = px.area(history_df_long, x='timestamp', y='Score', color='Sentiment', title="Sentiment Composition Over Time", labels={'timestamp': 'Time', 'Score': 'Proportion'}, color_discrete_map={'pos':'#00CC96', 'neg':'#EF553B', 'neu':'#636EFA'})
            st.plotly_chart(fig_area, use_container_width=True)
        else:
            st.info("Analyze more text to see historical trends.")

    # --- TAB 4: Keyword & Sentence Insights ---
    with tab4:
        st.header("Text & Keyword Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Keyword Clouds")
            positive_text = ' '.join(history_df[pos_mask]['text'])
            negative_text = ' '.join(history_df[neg_mask]['text'])
            neutral_text = ' '.join(history_df[neu_mask]['text'])

            if positive_text:
                st.write("Positive Keywords")
                st.image(generate_wordcloud(positive_text).to_image())
            
            if negative_text:
                st.write("Negative Keywords")
                st.image(generate_wordcloud(negative_text, background_color='#EAEAEA').to_image())
            
            if neutral_text:
                st.write("Neutral Keywords")
                st.image(generate_wordcloud(neutral_text).to_image())

        with col2:
            st.subheader("Top Sentences by Sentiment")
            all_sentences = []
            for _, row in history_df.iterrows():
                sentences = split_into_sentences(row['text'])
                for sentence in sentences:
                    score = analyze_sentiment(sentence)['compound']
                    all_sentences.append({'Sentence': sentence, 'Score': score})
            
            if all_sentences:
                sentence_df = pd.DataFrame(all_sentences).drop_duplicates(subset=['Sentence'])
                
                pos_sentences_df = sentence_df[sentence_df['Score'] > 0.05]
                neg_sentences_df = sentence_df[sentence_df['Score'] < -0.05]
                neu_sentences_df = sentence_df[(sentence_df['Score'] >= -0.05) & (sentence_df['Score'] <= 0.05)]
                
                st.write("Most Positive Sentences")
                st.table(pos_sentences_df.nlargest(5, 'Score'))
                
                st.write("Most Negative Sentences")
                st.table(neg_sentences_df.nsmallest(5, 'Score'))

                st.write("Most Neutral Sentences")
                neu_sentences_df['abs_score'] = neu_sentences_df['Score'].abs()
                st.table(neu_sentences_df.nsmallest(5, 'abs_score').drop(columns=['abs_score']))

else:
    st.info("Please enter some text and click 'Analyze' to see the dashboard.")
