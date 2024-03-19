import streamlit as st
from libs import upload_file


def main():
    st.set_page_config(page_title="Pythonic Golu!", page_icon=":books:")
    st.header("Pythonic Golu :books:")
    select_option = st.selectbox(
        r'$\textsf{\large What is the preferred datasource?}$',
        ('All', 'Q&A', 'Books')
    )
    user_question = st.text_area(r"$\textsf{\large Ask Golu a Python question:}$")
    if st.button("Ask Golu", type="primary"):
        if user_question:
            st.write(user_question)

    with st.sidebar:
        st.subheader("You can upload you Python book here:")
        st.subheader("This will be uploaded to S3 for review. I will"
                     " upload the document if it passes my sanity check"
                     )
        upload_docs = st.file_uploader("Upload your Python pdf/docx books:",
                                       accept_multiple_files=True,
                                       type=["xlsx", "pdf", "doc", "docx", "md"]
                                       )
        if st.button("Submit for Review"):
            with st.spinner("Uploading to S3"):
                if upload_docs is not None:
                    for doc in upload_docs:
                        upload_file(doc)


if __name__ == '__main__':
    main()
