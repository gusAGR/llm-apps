import streamlit as st
from langchain_community.llms import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key
api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")


def load_answer(question):
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2")  # Model link : https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2

    answer = llm.invoke(question)
    return answer


title = "LangChain demo app"
st.set_page_config(page_title=title, page_icon=":robot:")
st.header(title)


def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text


user_input = get_text()

response = ""
if user_input != "":
    response = load_answer(user_input)

submit = st.button('Generate')

# If generate button is clicked
if submit:
    st.subheader("Answer:")

    st.write(response)
