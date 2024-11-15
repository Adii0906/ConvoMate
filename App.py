import os
from dotenv import load_dotenv
import streamlit as st
from mistralai import Mistral
import pandas as pd
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("MISTRAL_API_KEY")
if api_key is None:
    raise ValueError("MISTRAL_API_KEY environment variable is not set")


# load the model
model = "mistral-large-latest"

# CALL THE API api_key
client = Mistral(api_key=api_key)

# Streamlit app title
st.title('Chatbot')

# Input for user message
user_input = st.text_input("You:")

if st.button("Send"):
    if user_input:
        # Get response from Mistral
        chat_response = client.chat.complete(
            model=model,
            messages=[{
                "role": "user",
                "content": user_input,
            }],
        )
        # Display the response
        bot_response = chat_response.choices[0].message.content
        st.text_area("Mistral:", value=bot_response, height=200, max_chars=None)
    else:
        st.error("Please enter a message.")

# Feedback form section
st.title("Feedback Form")
st.header("We'd love to hear your thoughts!")

# Define the feedback form
with st.form(key='feedback_form'):
    email = st.text_input("Your Email (optional):")
    rating = st.slider("How would you rate your experience?", 1, 5, 3)  # Slider for rating (1-5)
    comments = st.text_area("Please leave your comments or suggestions.")

    # Submit button for the form
    submit_button = st.form_submit_button(label="Submit Feedback")

# Handle form submission
if submit_button:
    # Display confirmation message
    st.success("Thank you for your feedback!")

    # Display the feedback values
    st.write("Rating:", rating)
    st.write("Comments:", comments)

    # Get the current timestamp for feedback record
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare the feedback data
    feedback_data = {
        "Email": email if email else "Anonymous",  # Use "Anonymous" if no email is provided
        "Rating": rating,
        "Comments": comments,
        "Timestamp": timestamp,
    }

    # Save the feedback to a CSV file
    df = pd.DataFrame([feedback_data])
    df.to_csv("feedback_responses.csv", mode='a', header=not pd.io.common.file_exists("feedback_responses.csv"), index=False)

    # Optionally, inform the user that their feedback has been saved
    st.write("Your feedback has been sumbited!")
