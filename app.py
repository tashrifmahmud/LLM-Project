import streamlit as st
import torch
from transformers import pipeline

# Title
st.title(":bar_chart: Sentiment Analysis with LLM Model")
st.markdown(":cat: [GitHub Repository](https://github.com/tashrifmahmud/Sentiment-Analysis-Model) | :hugging_face: [Hugging Face Model](https://huggingface.co/tashrifmahmud/sentiment_analysis_model_v2)")

# Banner
st.image("https://www.qdegrees.com/uploads/blogs-img/sentiment-analysis-and-overview.jpg", use_container_width=True)

# Sidebar for links
with st.sidebar:
    st.header("More about this Project:")
    st.markdown("### :space_invader: Created by: Tashrif Mahmud\n- This model is a finetuned DistilBERT transformer for binary sentiment analysis. Initially trained on the IMDB dataset and later tuned with Rotten Tomatoes dataset, it distinguishes positive and negative text based movie reviews.")
    st.markdown("### :link: Links:\n- :cat: [GitHub](https://github.com/tashrifmahmud/Sentiment-Analysis-Model)\n- :hugging_face: [Hugging Face](https://huggingface.co/tashrifmahmud/sentiment_analysis_model_v2)")

# Check if GPU is available
device = 0 if torch.cuda.is_available() else -1

# Load the sentiment analysis model
st.write(f"Using {'GPU' if device == 0 else 'CPU'} for inference.")
pipe = pipeline("text-classification", model="tashrifmahmud/sentiment_analysis_model_v2", device=device)

# Input text box with session state management
if 'text_input' not in st.session_state:
    st.session_state.text_input = ""

text_input = st.text_area("Enter text for sentiment analysis:", value=st.session_state.text_input, key="text_input")

# Buttons for user interaction
run_button = st.button("Run Prediction")
reset_button = st.button("Reset")

# State management: Run prediction or reset input
if run_button:
    if text_input.strip():
        result = pipe(text_input)
        
        # Highlight the result with custom styling
        sentiment = result[0]['label']
        confidence = result[0]['score']

        # Display Sentiment and Confidence with background color for better visibility
        if sentiment == 'LABEL_1':  # LABEL_1 represents positive sentiment
            sentiment_color = "#2dbe3e"  # Green for positive
        else:
            sentiment_color = "#ff6f61"  # Red for negative

        st.markdown(f"""
        <div style="background-color:{sentiment_color}; padding: 10px; border-radius: 5px; text-align: center;">
            <h2 style="color: white;">Sentiment: {'Positive' if sentiment == 'LABEL_1' else 'Negative'}</h2>
            <h3 style="color: white;">Confidence: {confidence:.2f}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()  # Fun animation
        st.success("Prediction complete!")
    else:
        st.warning("Please enter some text before running the prediction.")

if reset_button:
    st.session_state.text_input = ""  # Clear the text input