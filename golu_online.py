import streamlit as st
from libs import ask_question_openai, ask_question_zephyr, ask_question_mistral, ask_question_phi3
import timeit
from libs import load_python_book_into_zila
import os


def main():

    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    st.set_page_config(page_title="Pythonic Golu! - AI chatbot for Python question answering",
                       page_icon=":books:",
                       layout="wide",
                       menu_items={
                           'Get Help': 'https://github.com/SaubhikBanerjee/Pythonic-Golu/blob/master-new/readME.md',
                           'Report a bug': "https://github.com/SaubhikBanerjee/Pythonic-Golu/issues",
                           'About': "Developed by Saubhik Banerjee. *Source Code:* "
                                    "https://github.com/SaubhikBanerjee/Pythonic-Golu"

                       }
                       )
    st.write("Developed by Saubhik Banerjee, "
             "Source Code: https://github.com/SaubhikBanerjee/Pythonic-Golu")
    st.markdown(":rainbow[Golu is an AI chatbot (RAG application) to answer your Python questions!!"
                " You can take preparation of your PCEP, PCAP and interview with Golu. She is equipped with"
                " huge question dumps and related material! You can upload your study material also.]")
    st.subheader("Pythonic Golu :books:")
    select_option = st.selectbox(
        r'$\textsf{\large What is the preferred LLM?}$',
        ('OpenAI - Faster and efficient - NOT free!',
         'HuggingFaceHub - zephyr-7b-beta',
         'HuggingFaceHub - Mistral-7B-Instruct-v0.2',
         'HuggingFaceHub - Phi-3-mini-4k-instruct'
         ),
        index=None,
        placeholder="Select your LLM..."
    )
    st.warning("If you use HuggingFace Hub, sometimes you might get an error, depending"
               " on the availability. To use OpenAI, please provide you own OpenAI API key.")
    api_key = st.text_input("Enter your OpenAI API key:")  # type="password"
    user_question = st.text_area(r"$\textsf{\large Ask Golu a Python question:}$")
    if st.button("Ask Golu", type="primary"):
        if user_question:
            start_time = timeit.default_timer()  # Start timer
            with st.spinner("Golu is searching.."):
                if select_option == 'HuggingFaceHub - Mistral-7B-Instruct-v0.2':
                    response = ask_question_mistral(user_question)
                elif select_option == 'OpenAI - Faster and efficient - NOT free!':
                    response = ask_question_openai(user_question, api_key)
                elif select_option == 'HuggingFaceHub - zephyr-7b-beta':
                    response = ask_question_zephyr(user_question)
                elif select_option == 'HuggingFaceHub - Phi-3-mini-4k-instruct':
                    response = ask_question_phi3(user_question)
                else:
                    response = ask_question_zephyr(user_question)
            st.balloons()
            with st.chat_message("assistant"):
                st.markdown(response["result"])
                end_time = timeit.default_timer()  # End timer
                total_time = (end_time - start_time) / 60
                st.markdown("Time to retrieve response %.2f minutes" % total_time)
            source_docs = response['source_documents']
            for i, doc in enumerate(source_docs):
                st.info(f'\nSource Document {i + 1}\n')
                st.info(f'Source Text: {doc.page_content}')

    with st.sidebar:
        st.subheader("You can upload your Python book here:")
        st.write("Please try to upload books/documents related to Python, AI, RAG or Data Science."
                 " I will have a periodic check on the data uploaded. Anything not matching with the sprit"
                 " of the application will be deleted."
                 )
        upload_docs = st.file_uploader("Upload your Python books:",
                                       accept_multiple_files=False,
                                       type=["xlsx", "pdf", "doc", "docx", "md"]
                                       )
        book_name_val = st.text_input("Enter the book name:", value="Unknown")
        book_author_val = st.text_input("Enter the author name:", value="Unknown")
        if st.button("Upload to Milvus"):
            with st.spinner("Uploading to Milvus..."):
                if upload_docs is not None:
                    file_path = os.path.join(os.getcwd(), upload_docs.name)

                    # Save the uploaded file to disk
                    with open(file_path, "wb") as f:
                        f.write(upload_docs.getvalue())
                        print(file_path)
                        # Load to Milvus
                        load_python_book_into_zila(file_path, book_name_val, book_author_val)
                        st.snow()
                    os.remove(file_path)


if __name__ == '__main__':
    main()
