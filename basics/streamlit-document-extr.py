import streamlit as st
import PyPDF2

st.set_page_config(
    page_title="File Upload Test",
    page_icon=":page_facing_up:",
    initial_sidebar_state="expanded",
    layout="wide",
)
st.title("File Upload Test")
st.subheader("This is a test for a Streamlit app to upload files and display their content.")
st.write("You can upload a PDF or a text file, and the app will display the content of the first page or the first 1000 characters respectively.")

# Upload file
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"],accept_multiple_files=False)

submit = st.button("extract data")

# display the uploaded file on the page if it submitted
if submit and uploaded_file is not None:
    st.write("File uploaded successfully!")
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        if len(reader.pages) > 0:
            first_page = reader.pages[0]
            text = first_page.extract_text()
            st.subheader("First page content:")
            st.text(text if text else "No text found on the first page.")
        else:
            st.warning("The PDF has no pages.")
    elif uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
        first_1000_chars = content[:1000]
        st.subheader("First part of text file:")
        st.text(first_1000_chars)
    else:
        st.warning("Unsupported file type.")


# streamlit run "c:/Users/benjamin.fels/OneDrive - Hitzler Ingenieure GmbH & Co. KG/Dokumente/Python Scripts/rag/streamlit-test.py"