import streamlit as st
import pandas as pd
import requests
from datetime import date

st.set_page_config(page_title="Influence Questionnaire", layout="wide")
st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400&display=swap'); html, body, [class*='css']  { font-family: 'Lato', sans-serif; }</style>", unsafe_allow_html=True)

st.title("🗞️ Public Sphere Influence Questionnaire")

st.markdown("""
Welcome to the Influence Score project for Lebanon and Tunisia. Your insights as a researcher will help us refine how we assess the influence of media content in shaping public opinion. This work supports the broader Public Sphere Index initiative hosted at [publicspheres.org](https://www.publicspheres.org).

**Formula:** Influence = Reach × Salience × Discursiveness
""")

st.markdown("<hr style='height:5px;border:none;background-color:#ff5c5c;'>", unsafe_allow_html=True)

country = st.radio("Select your country context:", ["Lebanon", "Tunisia"])
st.markdown("<hr style='height:5px;border:none;background-color:#ff5c5c;'>", unsafe_allow_html=True)

if "samples" not in st.session_state:
    st.session_state.samples = []

# Section 0
st.header("Section 0: Salient Issues in Your Context")
st.write("Please tell us what issues you consider most salient in your country between Jan 1 and Mar 31, 2025.")
issue_list = st.text_area("List 5–10 top public issues (one per line):")
issue_context = st.text_area("Briefly explain why these issues were prominent.")
st.markdown("<hr style='height:5px;border:none;background-color:#ff5c5c;'>", unsafe_allow_html=True)

# Section 1
st.header("Section 1: Media Sample Submission")
category = st.selectbox("Select the media category:", ["TV", "Radio", "Print", "Online news", "Podcast", "Social media", "Other/hybrid"])
title = st.text_input("Media Title or Description")
platform = st.text_input("Platform or Outlet")
link = st.text_input("Link (if available)")
date_aired = st.date_input("Air/Publication Date", min_value=date(2025, 1, 1), max_value=date(2025, 3, 31))
transcript = st.radio("Transcript Available?", ["Yes", "No", "Not sure"])
transcript_details = st.text_input("Transcript Link or Notes (if available)")
st.markdown("<hr style='height:5px;border:none;background-color:#ff5c5c;'>", unsafe_allow_html=True)

# Section 2
st.header("Section 2: Reach")
st.write("Reach refers to how many people were likely exposed to this content.")
raw_reach = st.text_input("Estimated raw reach (text or number):")
reach_basis = st.text_area("How did you estimate this number?")
norm_reach = st.slider("Reach Score (0–1)", 0.0, 1.0, 0.5, 0.01)
reach_notes = st.text_area("Additional notes about platform amplification or repeat circulation (optional)")
st.markdown("<hr style='height:5px;border:none;background-color:#ff5c5c;'>", unsafe_allow_html=True)

# Section 3
st.header("Section 3: Salience")
st.write("Salience measures how relevant this content is to the public issues you listed earlier.")
salience_score = st.slider("Salience Score (0–1)", 0.0, 1.0, 0.5, 0.01)
salience_match = st.text_area("Which of your listed issues does this sample reflect?")
salience_explanation = st.text_area("Explain how the content reflects or engages with the issue(s).")
st.markdown("<hr style='height:5px;border:none;background-color:#ff5c5c;'>", unsafe_allow_html=True)

# Section 4
st.header("Section 4: Discursiveness")
st.write("Discursiveness refers to how persuasive or opinion-shaping the content is.")
logos_score = st.slider("Logos (Reasoning) Score (0–1)", 0.0, 1.0, 0.5, 0.01)
logos_expl = st.text_area("Does the sample use evidence, arguments, or reasoning to persuade?")
pathos_score = st.slider("Pathos (Emotion) Score (0–1)", 0.0, 1.0, 0.5, 0.01)
pathos_expl = st.text_area("Does the content stir emotions—empathy, anger, inspiration?")
ethos_score = st.slider("Ethos (Credibility) Score (0–1)", 0.0, 1.0, 0.5, 0.01)
ethos_expl = st.text_area("Who is speaking? Do they carry public trust or professional authority?")
reflection = st.text_area("Optional: What makes this sample especially persuasive in your view?")
st.markdown("<hr style='height:5px;border:none;background-color:#ff5c5c;'>", unsafe_allow_html=True)

# Final Reflection
st.header("Final Reflection")
major_events = st.text_area("Were there any major events during this period (Jan–Mar 2025)?")

# Submit
if st.button("Submit Sample"):
    sample = {
        "country": country,
        "mediaCategory": category,
        "mediaTitle": title,
        "mediaPlatform": platform,
        "mediaLink": link,
        "mediaDate": str(date_aired),
        "transcriptAvailable": transcript,
        "transcriptNotes": transcript_details,
        "rawReach": raw_reach,
        "reachEstimation": reach_basis,
        "reachScore": norm_reach,
        "amplificationNotes": reach_notes,
        "salienceScore": salience_score,
        "reflectedIssues": salience_match,
        "issueEngagement": salience_explanation,
        "logosScore": logos_score,
        "logosExplanation": logos_expl,
        "pathosScore": pathos_score,
        "pathosExplanation": pathos_expl,
        "ethosScore": ethos_score,
        "ethosExplanation": ethos_expl,
        "persuasiveNote": reflection,
        "finalReflection": major_events,
        "publicIssues": issue_list,
        "issuesExplanation": issue_context
    }

    st.session_state.samples.append(sample)
    st.success("✅ Your sample has been submitted locally. Now sending to Google Sheet...")

    try:
        response = requests.post(
            "https://script.google.com/macros/s/AKfycbyezHJ7K5y8ulNgfMJbKL639MWDcXQDW3GtYtkH_inoXJfYLy-UoMcdq_yRci8Ko_lWIA/exec",
            json=sample,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            st.success("✅ Sample sent to Google Sheet!")
        else:
            st.warning(f"⚠️ Submission failed: status {response.status_code}")
    except Exception as e:
        st.error(f"❌ Error sending to sheet: {e}")

# Download
if st.session_state.samples:
    if st.button("📄 Download All Samples as CSV"):
        df = pd.DataFrame(st.session_state.samples)
        st.download_button("Download CSV", data=df.to_csv(index=False), file_name="influence_samples.csv", mime="text/csv")
