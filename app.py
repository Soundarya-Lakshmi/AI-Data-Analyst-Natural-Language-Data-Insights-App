import streamlit as st
from ai_pipeline import ask_question
import matplotlib.pyplot as plt

st.title("AI Hotel Analytics Assistant")


# Text input for question
question = st.text_input("Enter your question about hotel bookings:")

# Button to execute
if st.button("Get Answer"):
    if question:
        result = ask_question(question)

        # If the result is a matplotlib figure, display chart
        if isinstance(result, plt.Figure):
            st.pyplot(result)
        else:
            # Otherwise, show text/table
            st.write(result)