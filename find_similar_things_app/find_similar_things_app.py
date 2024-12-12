import streamlit as st
from dotenv import load_dotenv
import os
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

# Load environment variables from a .env file
load_dotenv()

loader = CSVLoader(file_path='find_similar_things_app/myData.csv', csv_args={
        'delimiter': ',',
        'quotechar': '"',
        'fieldnames': ['Words']
    })

data = loader.load()


# embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

#vector db
db = FAISS.from_documents(data, embeddings)


# streamlit app

st.set_page_config(page_title="Educate Kids", page_icon=":robot:")
st.header("Hey, Ask me something & I will give out similar things")

def get_text():
    input_text = st.text_input("You: ", key=input)
    return input_text


user_input = get_text()
submit = st.button('Find similar Things')

if submit:
    # If the button is clicked, the below snippet will fetch us the similar text
    docs = db.similarity_search(user_input, k=2)
    print(docs)
    st.subheader("Top Matches:")
    #st.text(docs[0])
    #st.text(docs[1].page_content)
    for x in docs:
        st.text(x.page_content)
