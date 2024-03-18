import streamlit as st


def main():
    st.set_page_config(page_title="Pythonic Golu!", page_icon=":books:")
    st.header("Pythonic Golu :books:")
    select_option = st.selectbox(
        r'$\textsf{\large What is the preferred datasource?}$',
        ('All', 'Q&A', 'Books')
    )
    st.text_area(r"$\textsf{\large Ask Golu a Python question:}$")
    with st.sidebar:
        st.subheader("You can upload you Python book / Q&A Excel")
        st.subheader("This will be uploaded to S3 for review. I will"
                     " upload the document if it passes my sanity check"
                     )
        st.file_uploader("Upload your Python pdf books / Q&A:",
                         accept_multiple_files=True,
                         type=["xlsx", "pdf", "doc", "docx", "md"]
                         )
        st.button("Submit for Review")


if __name__ == '__main__':
    main()
