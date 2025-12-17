import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import zipfile
import io

# ---------------- CONFIG ----------------
st.set_page_config(page_title="🚩AI Portfolio Generator", page_icon="🚩")
st.title("🚩AI-Generated Portfolio Website from Resume")

st.markdown("Upload your resume (PDF/DOCX) and generate a portfolio website.")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

resume_text = ""

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            if page.extract_text():
                resume_text += page.extract_text() + "\n"

    elif uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        resume_text = "\n".join(p.text for p in doc.paragraphs)

    st.success("Resume text extracted successfully")

    st.subheader("Extracted Resume Text")
    st.text_area("", resume_text, height=200)

# ---------------- GENERATE WEBSITE ----------------
if st.button("Generate Portfolio Website"):
    if not resume_text:
        st.warning("Please upload a resume first")
        st.stop()

    # ---------------- AI SIMULATED OUTPUT ----------------
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Professional Portfolio</h1>

    <section>
        <h2>About Me</h2>
        <p>{resume_text[:400]}</p>
    </section>

    <section>
        <h2>Skills</h2>
        <p>Python, SQL, Data Analysis, Machine Learning, Deep Learning</p>
    </section>

    <section>
        <h2>Projects</h2>
        <p>Resume-based AI Portfolio Generator</p>
    </section>

    <section>
        <h2>Education</h2>
        <p>Extracted from resume</p>
    </section>

    <section>
        <h2>Contact</h2>
        <p>Email: your@email.com</p>
    </section>

<script src="script.js"></script>
</body>
</html>
"""

    css = """
body {
    background:#111;
    color:#fff;
    font-family:Arial;
    padding:20px;
}
h1 { color:#00ffd5; }
section { margin-bottom:20px; }
"""

    js = """
console.log("Portfolio website loaded");
"""

    # ---------------- SAVE FILES ----------------
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    with open("style.css", "w", encoding="utf-8") as f:
        f.write(css)

    with open("script.js", "w", encoding="utf-8") as f:
        f.write(js)

    # ---------------- ZIP ----------------
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as z:
        z.write("index.html")
        z.write("style.css")
        z.write("script.js")

    st.subheader("Website Preview")
    st.components.v1.html(html, height=500, scrolling=True)

    st.download_button(
        "Download Website ZIP",
        data=zip_buffer.getvalue(),
        file_name="portfolio_website.zip",
        mime="application/zip"
    )

    st.success("Portfolio Website Generated Successfully")
