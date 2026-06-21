import streamlit as st
from fpdf import FPDF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="ResumeIQ - AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 ResumeIQ - AI Powered Resume Analyzer")

# ------------------------
# USER INPUTS
# ------------------------

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    education = st.text_area("Education")

with col2:
    skills = st.text_area("Skills (comma separated)")
    projects = st.text_area("Projects")

template = st.selectbox(
    "Target Role",
    [
        "Data Analyst",
        "AI Engineer",
        "Business Analyst",
        "Risk Analyst"
    ]
)

job_desc = st.text_area(
    "Paste Job Description for ATS Analysis"
)

# ------------------------
# GENERATE RESUME
# ------------------------

if st.button("Generate Resume Analysis"):

    resume_text = f"""
    Name: {name}

    Education:
    {education}

    Skills:
    {skills}

    Projects:
    {projects}
    """

    # ------------------------
    # SUMMARY
    # ------------------------

    if template == "Data Analyst":
        summary = f"""
        Aspiring Data Analyst with expertise in {skills}.
        Experienced in data-driven projects including {projects}.
        Strong analytical, reporting, and problem-solving skills.
        """

    elif template == "AI Engineer":
        summary = f"""
        Aspiring AI Engineer with experience in {skills}.
        Skilled in machine learning concepts and project development including {projects}.
        Passionate about building intelligent systems.
        """

    elif template == "Business Analyst":
        summary = f"""
        Aspiring Business Analyst with strong analytical abilities and experience in {projects}.
        Skilled in extracting insights and supporting business decisions using {skills}.
        """

    else:
        summary = f"""
        Aspiring Risk Analyst with experience in analytical projects such as {projects}.
        Skilled in identifying patterns, assessing risks, and working with {skills}.
        """

    st.subheader("Professional Summary")
    st.success(summary)

    # ------------------------
    # ATS SCORE
    # ------------------------

    if job_desc.strip() != "":

        cv = CountVectorizer()

        matrix = cv.fit_transform([
            resume_text.lower(),
            job_desc.lower()
        ])

        similarity = cosine_similarity(matrix)[0][1]

        ats_score = round(similarity * 100, 2)

        st.subheader("ATS Match Score")

        st.metric(
            "ATS Score",
            f"{ats_score}%"
        )

        # ------------------------
        # SKILL GAP ANALYSIS
        # ------------------------

        resume_words = set(
            resume_text.lower().split()
        )

        job_words = set(
            job_desc.lower().split()
        )

        missing = list(
            job_words - resume_words
        )

        st.subheader("Missing Keywords")

        if len(missing) > 0:
            st.write(missing[:20])
        else:
            st.success("No major missing keywords found.")

    # ------------------------
    # RESUME STRENGTH
    # ------------------------

    score = 0

    if len(skills.split(",")) >= 5:
        score += 25

    if len(projects) >= 50:
        score += 25

    if len(education) >= 30:
        score += 25

    if name and email:
        score += 25

    st.subheader("Resume Strength")

    st.progress(score / 100)

    st.write(f"Resume Strength Score: {score}/100")

    # ------------------------
    # SUGGESTIONS
    # ------------------------

    suggestions = []

    if len(skills.split(",")) < 5:
        suggestions.append(
            "Add more technical skills."
        )

    if len(projects) < 50:
        suggestions.append(
            "Add detailed project descriptions."
        )

    if "certification" not in resume_text.lower():
        suggestions.append(
            "Add certifications section."
        )

    if len(education) < 30:
        suggestions.append(
            "Provide more education details."
        )

    st.subheader("Resume Improvement Suggestions")

    for s in suggestions:
        st.write("•", s)

    # ------------------------
    # WORD CLOUD
    # ------------------------

    st.subheader("Resume Keyword Cloud")

    try:
        wc = WordCloud(
            width=800,
            height=400,
            background_color="white"
        ).generate(resume_text)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.imshow(wc)

        ax.axis("off")

        st.pyplot(fig)

    except:
        st.warning(
            "Not enough text to generate word cloud."
        )

    # ------------------------
    # PDF EXPORT
    # ------------------------

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        "B",
        16
    )

    pdf.cell(
        200,
        10,
        name,
        ln=True
    )

    pdf.set_font(
        "Arial",
        size=12
    )

    pdf.cell(
        200,
        10,
        email,
        ln=True
    )

    pdf.ln(5)

    pdf.multi_cell(
        0,
        10,
        "Professional Summary:\n" + summary
    )

    pdf.ln(3)

    pdf.multi_cell(
        0,
        10,
        "Education:\n" + education
    )

    pdf.ln(3)

    pdf.multi_cell(
        0,
        10,
        "Skills:\n" + skills
    )

    pdf.ln(3)

    pdf.multi_cell(
        0,
        10,
        "Projects:\n" + projects
    )

    pdf.output("resume.pdf")

    with open(
        "resume.pdf",
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download Resume PDF",
            data=file,
            file_name="resume.pdf",
            mime="application/pdf"
        )
