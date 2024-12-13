import streamlit as st

st.set_page_config(page_title="Marketing Tool", page_icon='✅', layout="centered", initial_sidebar_state="collapsed")
st.header("Hey, how can I help you?")

form_input = st.text_area("Enter text", height=275)

task_type_option = st.selectbox("Please select the action to be performed",
                                ['Write a sales copy', 'Create a tweet', 'Write a product description'], key=1)
age_option = st.selectbox("For which age group?",
                          ('Kid', 'Adult', 'senior Citizen'), key=2)
number_of_words = st.slider("Word limit", 1, 200, 25)

submit = st.button("Generate")

if submit:
    st.write(f"Action performed: {task_type_option}, age: {age_option} words: {number_of_words}.")

