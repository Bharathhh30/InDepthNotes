import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi as yta
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key='AIzaSyA7tF-Df8zdB4lyxB3oUE8eOn-18jOjTEg')

# Function to convert YouTube URL to text
def youtube_url_to_text(youtube_url):
    vid_id = youtube_url.split('watch?v=')[1]
    data = yta.get_transcript(vid_id)

    transcript = ''
    for value in data:
        for key, val in value.items():
            if key == 'text':
                transcript += val

    l = transcript.splitlines()
    final = "".join(l)
    return final

# Streamlit app
def main():
    st.title("YouTube Transcript to In-depth Notes Generator")

    # Get YouTube URL from user input
    youtube_url = st.text_input("Enter YouTube URL:")

    # Initialize generated content variables
    generated_summary = None
    generated_notes = None

    # Track visibility state of summary and notes sections
    show_summary = False
    show_notes = False

    if st.button("Generate Summary"):
        if youtube_url:
            # Convert YouTube URL to text
            text = youtube_url_to_text(youtube_url)

            # Use Google Generative AI to generate summary
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"You are an AI assistant that will generate a summary based on the provided YouTube video transcript. The text is : {text}"
            generated_summary = model.generate_content(prompt)

            # Update visibility state
            show_summary = True
            show_notes = False

    keywords = st.text_input("Enter keywords (comma-separated):")

    if st.button("Generate In-depth Notes"):
        if youtube_url and keywords:
            # Convert YouTube URL to text
            text = youtube_url_to_text(youtube_url)

            # Use Google Generative AI to generate notes based on keywords
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"You are an AI assistant that will generate in-depth notes based on the provided text and keywords. Keywords: {keywords.strip()} \n\n{text} and make sure that you provide information in-depth with some examples and also with some problems (assume this as a mandatory prompt), if it is related to coding make sure that you generate code snippets"
            generated_notes = model.generate_content(prompt)

            # Update visibility state
            show_summary = False
            show_notes = True

    # Display generated content
    if show_summary and generated_summary:
        st.subheader("Generated Summary:")
        st.markdown(generated_summary.text)
    
    if show_notes and generated_notes:
        st.subheader("Generated In-depth Notes:")
        st.markdown(generated_notes.text)

if __name__ == "__main__":
    main()
