import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Influence Questionnaire", layout="wide")
st.title("🗞️ Public Sphere Influence Questionnaire")

st.markdown("""
Welcome to the Influence Score project for Lebanon and Tunisia. Your insights as a researcher will help us refine how we assess the influence of media content in shaping public opinion. This work supports the broader Public Sphere Index initiative hosted at [publicspheres.org](https://www.publicspheres.org).

**Formula:** Influence = Reach × Salience × Discursiveness
""")

# Country selection
country = st.radio("Select your country context:", ["Lebanon", "Tunisia"])
st.markdown("---")

# Session state for collecting multiple samples
if "samples" not in st.session_state:
    st.session_state.samples = []

# Salient issues in their context
st.header("Section 0: Salient Issues in Your Context")
st.write("Please tell us what issues you consider most salient in your country between Jan 1 and Mar 31, 2025.")
issue_list = st.text_area("List 5–10 top public issues (one per line):")
issue_context = st.text_area("Briefly explain why these issues were prominent.")
st.markdown("---")

st.header("Section 1: Media Sample Submission")
category = st.selectbox("Select the media category:", ["TV", "Radio", "Print", "Online news", "Podcast", "Social media", "Other/hybrid"])
title = st.text_input("Media Title or Description")
platform = st.text_input("Platform or Outlet")
link = st.text_input("Link (if available)")
date_aired = st.date_input("Air/Publication Date", min_value=date(2025, 1, 1), max_value=date(2025, 3, 31))
transcript = st.radio("Transcript Available?", ["Yes", "No", "Not sure"])
transcript_details = st.text_input("Transcript Link or Notes (if available)")

# Reach
st.header("Section 2: Reach")
st.write("Reach refers to how many people were likely exposed to this content. This includes viewers, listeners, or online impressions.")
raw_reach = st.text_input("Estimated raw reach (numeric):")
reach_basis = st.text_area("How did you estimate this number? (views, shares, ratings, or professional judgment)")
norm_reach = st.slider("Normalized Reach Score (0–1)", 0.0, 1.0, 0.5, 0.01)
reach_notes = st.text_area("Additional notes about platform amplification or repeat circulation (optional)")

# Salience
st.header("Section 3: Salience")
st.write("Salience measures how relevant this content is to the public issues you listed earlier.")
salience_score = st.slider("Salience Score (0–1)", 0.0, 1.0, 0.5, 0.01)
salience_match = st.text_area("Which of your listed issues does this sample reflect?")
salience_explanation = st.text_area("Explain how the content reflects or engages with the issue(s). Is it direct, symbolic, or tangential?")

# Discursiveness
st.header("Section 4: Discursiveness")
st.write("Discursiveness refers to how persuasive or opinion-shaping the content is. This is assessed using Logos (reason), Pathos (emotion), and Ethos (credibility).")

logos_score = st.slider("Logos (Reasoning) Score (0–1)", 0.0, 1.0, 0.5, 0.01)
logos_expl = st.text_area("Does the sample use evidence, arguments, or reasoning to persuade? Are claims justified?")

pathos_score = st.slider("Pathos (Emotion) Score (0–1)", 0.0, 1.0, 0.5, 0.01)
pathos_expl = st.text_area("Does the content stir emotions—empathy, anger, inspiration? How?")

ethos_score = st.slider("Ethos (Credibility) Score (0–1)", 0.0, 1.0, 0.5, 0.01)
ethos_expl = st.text_area("Who is speaking? Do they carry public trust or professional authority?")

reflection = st.text_area("Optional: What makes this sample especially persuasive in your view?")

# Final reflection
st.header("Final Reflection")
major_events = st.text_area("Were there any major events during this period (Jan–Mar 2025) that may have shifted public opinion—political, economic, cultural, or otherwise?")

if st.button("Submit Sample"):
    sample = {
        "Country": country,
        "Category": category,
        "Title": title,
        "Platform": platform,
        "Link": link,
        "Date": str(date_aired),
        "Transcript": transcript,
        "Transcript Details": transcript_details,
        "Raw Reach": raw_reach,
        "Reach Basis": reach_basis,
        "Normalized Reach": norm_reach,
        "Reach Notes": reach_notes,
        "Salience Score": salience_score,
        "Salience Match": salience_match,
        "Salience Explanation": salience_explanation,
        "Logos Score": logos_score,
        "Logos Explanation": logos_expl,
        "Pathos Score": pathos_score,
        "Pathos Explanation": pathos_expl,
        "Ethos Score": ethos_score,
        "Ethos Explanation": ethos_expl,
        "Discursive Reflection": reflection,
        "Major Events": major_events,
        "Issues Listed": issue_list,
        "Issue Context": issue_context
    }
    st.session_state.samples.append(sample)
    st.success("Your sample has been submitted. You can now enter another or move to the next category.")

if st.session_state.samples:
    if st.button("📄 Download All Samples as CSV"):
        df = pd.DataFrame(st.session_state.samples)
        st.download_button("Download CSV", data=df.to_csv(index=False), file_name="influence_samples.csv", mime="text/csv")
