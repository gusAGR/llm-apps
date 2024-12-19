import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain_core.example_selectors import LengthBasedExampleSelector
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_community.llms import HuggingFaceEndpoint

load_dotenv()
api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")


def getResponse(query, age_option, task_type_option, number_of_words):

    # Model link : https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2
    llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2")

    prompt = generate_prompt(age_option, query, task_type_option, number_of_words)
    print(prompt)

    return llm.invoke(prompt)


def generate_prompt(age_option, query, task_type_option, number_of_words):
    example_template = """
          Question: {query}
          Response: {answer}
        """

    example_prompt = PromptTemplate(
        input_variables=["query", "answer"],
        template=example_template)

    example_selector = LengthBasedExampleSelector(
        examples=get_examples(age_option),
        example_prompt=example_prompt,
        max_length=number_of_words
    )

    prefix = """You are a {age_option}, and {task_type_option}: 
        Here are some examples: 
        """

    suffix = """
       Question: {userInput}
       Response: """

    prompt_template = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["userInput", "age_option", "task_type_option"],
        example_separator="\n"
    )

    return prompt_template.format(userInput=query, age_option=age_option,
                                  task_type_option=task_type_option)


def get_examples(age_option):
    file = f"./marketing_campaign_app/examples/{age_option.replace(" ", "").lower()}.json"

    data = []
    with open(file, 'r') as json_file:
        data = json.load(json_file)
    return data


####UI#######

st.set_page_config(page_title="Marketing Tool", page_icon='✅', layout="centered", initial_sidebar_state="collapsed")
st.header("Hey, how can I help you?")

form_input = st.text_area("Enter text", height=275)

task_type_option = st.selectbox("Please select the action to be performed",
                                ['Write a sales copy', 'Create a tweet', 'Write a product description'], key=1)
age_option = st.selectbox("For which age group?",

                          ('Kid', 'Adult', 'senior Citizen'), key=2)
number_of_words = st.slider("Word limit for examples", 1, 2000, 500)

submit = st.button("Generate")

if submit:
    st.write(getResponse(form_input, age_option, task_type_option, number_of_words))

# st.write(f"Action performed: {task_type_option}, age: {age_option} words: {number_of_words}.")
