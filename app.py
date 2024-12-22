import os
from pathlib import Path
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders import AmazonTextractPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from utils.helpers import (
    get_table_csv_results,
    store_objectIn_s3,
    get_signed_s3_Object
)

# Constants
LOGO_IMAGE = 'cap_logo.png'
PDF_FOLDER = 'pdfs'

# Ensure the PDF folder exists
os.makedirs(PDF_FOLDER, exist_ok=True)

def get_pdf_text(pdf_docs):
    """Extracts text from uploaded PDFs."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_from_textract(pdf_path):
    """Uses Amazon Textract to extract text from a PDF."""
    loader = AmazonTextractPDFLoader(pdf_path)
    return loader.load()

def convert_pdf_to_csv(pdf_file, output_name):
    """Converts PDF table data into a CSV file."""
    table_csv = get_table_csv_results(pdf_file)
    output_file = f'{output_name}.csv'
    with open(output_file, 'wt') as fout:
        fout.write(table_csv)
    return output_file

def extract_table_from_pdf(pdf_path):
    """Extracts tables from a PDF using pdfplumber."""
    import pdfplumber
    table_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                table_data.extend(table)
    return table_data

def get_text_chunks(text):
    """Splits text into manageable chunks."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(text)

def get_vectorstore(text_chunks):
    """Creates a vectorstore from text chunks."""
    embeddings = OpenAIEmbeddings()  # Using OpenAIEmbeddings for better flexibility
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

def get_conversation_chain(vectorstore):
    """Initializes a conversational retrieval chain."""
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

def handle_userinput(user_question):
    """Handles user input and generates a response."""
    if st.session_state.conversation is None:
        st.warning("Please process a document first.")
        return

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        template = user_template if i % 2 == 0 else bot_template
        st.write(template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit app."""
    load_dotenv()
    st.set_page_config(page_title="ChatBot")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("ChatBot")
    user_question = st.text_input("Please ask any questions related to your invoices or receipts.")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.sidebar.image(LOGO_IMAGE)
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)

        if st.button("Process"):
            final_text = ""
            with st.spinner("Processing"):
                for pdf_file in pdf_docs:
                    save_path = Path(PDF_FOLDER, pdf_file.name)
                    with open(save_path, mode='wb') as w:
                        w.write(pdf_file.getvalue())

                    docs = get_text_from_textract(str(save_path))
                    final_text += "".join([doc.page_content for doc in docs])

                text_chunks = get_text_chunks(final_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.success("Documents processed successfully!")

        if st.button("Convert PDFs to CSV"):
            if not pdf_docs:
                st.warning("Please upload some PDFs first.")
            else:
                with st.spinner("Converting PDFs to CSV..."):
                    for pdf_file in pdf_docs:
                        save_path = Path(PDF_FOLDER, pdf_file.name)
                        with open(save_path, mode='wb') as w:
                            w.write(pdf_file.getvalue())

                        csv_path = convert_pdf_to_csv(str(save_path), pdf_file.name)
                        st.download_button(
                            label=f"Download {pdf_file.name}.csv",
                            data=open(csv_path, "rb").read(),
                            file_name=f"{pdf_file.name}.csv"
                        )

if __name__ == '__main__':
    main()
