import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from langchain.chains import RetrievalQA
import re

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def parse_question_prompt(s):
    questions = []
    solutions = []
    for line in s.split("\n"):
        print(line)
        if line != "":
            if line[0].isdigit():
                question, solution = line.split("S:")
                questions.append(question)
                solutions.append(solution)
    return questions, solutions


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore, withMemory):

    llm = ChatOpenAI()

    if withMemory:
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
    else:
        conversation_chain = RetrievalQA.from_chain_type(llm,retriever=vectorstore.as_retriever())

    return conversation_chain


def handle_userinput(user_question, usecase):
    if usecase == "conversation":
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']
        
        return response, usecase

    elif usecase == "question":
        response = st.session_state.conversation_questions_and_solutions(
            {'query': user_question})

        questions, solutions = parse_question_prompt(response['result'])

        return questions, solutions, usecase


def main():
    load_dotenv()
    st.set_page_config(page_title="StudyLLM",
                       page_icon="🎓")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "conversation_questions_and_solutions" not in st.session_state:
        st.session_state.conversation_questions_and_solutions = None
    if "uploaded_docs" not in st.session_state:
        st.session_state.uploaded_docs = None
    if "visibility1" not in st.session_state:
        st.session_state.visibility1 = "hidden"
        st.session_state.horizontal1 = True
    if "visibility2" not in st.session_state:
        st.session_state.visibility2 = "hidden"
        st.session_state.horizontal2 = True
    if "visibility3" not in st.session_state:
        st.session_state.visibility3 = "hidden"
        st.session_state.horizontal3 = True
    if "visibility4" not in st.session_state:
        st.session_state.visibility4 = "hidden"
        st.session_state.horizontal4 = True
    if "visibility5" not in st.session_state:
        st.session_state.visibility5 = "hidden"
        st.session_state.horizontal5 = True
    if "visibility6" not in st.session_state:
        st.session_state.visibility6 = "hidden"
        st.session_state.horizontal6 = True
    if "visibility7" not in st.session_state:
        st.session_state.visibility7 = "hidden"
        st.session_state.horizontal7 = True
    if "visibility8" not in st.session_state:
        st.session_state.visibility8 = "hidden"
        st.session_state.horizontal8 = True
    if "visibility9" not in st.session_state:
        st.session_state.visibility9 = "hidden"
        st.session_state.horizontal9 = True
    if "visibility10" not in st.session_state:
        st.session_state.visibility10 = "hidden"
        st.session_state.horizontal10 = True   
    if "processed" not in st.session_state:
        st.session_state.processed = False
    if "questions" not in st.session_state:
        st.session_state.questions = None
    if "solutions" not in st.session_state:
        st.session_state.solutions = None

    with st.sidebar:
        st.subheader("Your course material :books:")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
            
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain for user questions
                st.session_state.conversation = get_conversation_chain(
                    vectorstore, withMemory=True)

                # create conversation for question and solution generation
                st.session_state.conversation_questions_and_solutions = get_conversation_chain(
                    vectorstore, withMemory=False)

                question_prompt = """
                    Prepare a practice exam of 10 different questions of the context you have.
                    Write a list of questions in this format:
                    "
                        1. {Insert First question} S: {Insert solution to the First question} {go next line}
                        2. {Insert Second question} S: {Insert solution to the Second question} {go next line}
                        3. {Insert Third question} S: {Insert solution to the Third question} {go next line}
                        4. {Insert Fourth question} S: {Insert solution to the Fourth question} {go next line}
                        5. {Insert Fifth question} S: {Insert solution to the Fifth question} {go next line}
                        6. {Insert Sixth question} S: {Insert solution to the Sixth question} {go next line}
                        7. {Insert Seventh question} S: {Insert solution to the Seventh question} {go next line}
                        8. {Insert Eighth question} S: {Insert solution to the Eighth question} {go next line}
                        9. {Insert Ninth question} S: {Insert solution to the Ninth question} {go next line}
                        10. {Insert Tenth question} S: {Insert solution to the Tenth question} {go next line}
                    "
                    Only return such a list and no before or after sentences.
                """
                questions, solutions, usecase = handle_userinput(question_prompt, "question")

                st.session_state.questions = questions
                st.session_state.solutions = solutions

                st.session_state.processed = True

    if st.session_state.processed:
        
        st.write("Questions and Solutions generated:")

        # st.write(st.session_state.questions)
        # st.write(st.session_state.solutions)

        for i in range(len(st.session_state.questions)):
            st.write(st.session_state.questions[i])
            sol = st.session_state.solutions[i]
            a = st.radio(
                "See the solution?",
                ["visible", "hidden"],
                key=f"visibility{i+1}",
                label_visibility="collapsed",
                horizontal=True,
                index=1
            )
            if a == "visible":
                st.write(sol)
                            

    # elif step == "Ask the Material 🤔":
        st.header("Chat with your material :books:")

        user_question = st.text_input("Ask a question about your documents:")
        if user_question:
            response, usecase = handle_userinput(user_question, "conversation")

            if usecase == "conversation":
                for i, message in enumerate(st.session_state.chat_history):
                    if i % 2 == 0:
                        st.write(user_template.replace(
                            "{{MSG}}", message.content), unsafe_allow_html=True)
                    else:
                        st.write(bot_template.replace(
                            "{{MSG}}", message.content), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
