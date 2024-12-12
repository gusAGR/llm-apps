import streamlit as st
from langchain_community.llms import HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# Load environment variables from a .env file
load_dotenv()
# Retrieve the API key
api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")


chat = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2")  # Model link : https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2


#####################
#streamlit
#####################

st.set_page_config(page_title="LangChain demo app", page_icon=":robot:")
st.header("Hey, I'm your Chat GPT")

if "sessionMessages" not in st.session_state:
     st.session_state.sessionMessages = [
        SystemMessage("You are a helpful assistant.")
    ]

def load_answer(question):
    st.session_state.sessionMessages.append(HumanMessage(question))

    assistant_answer  = chat.invoke(st.session_state.sessionMessages )

    st.session_state.sessionMessages.append(AIMessage(assistant_answer))

    print_context(st.session_state.sessionMessages)

    return assistant_answer


def print_context(sessionMessages):
    for m in sessionMessages:
        print(m.content)


def get_text():
    input_text = st.text_input("You: ")
    return input_text


user_input = get_text()
submit = st.button('Generate')

# If generate button is clicked
if submit:
    response = load_answer(user_input)
    st.subheader("Answer:")
    st.write(response)
