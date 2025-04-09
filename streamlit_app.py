import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Public Sphere Media Influence Questionnaire", layout="wide")
st.title("🗞️ Media Influence Questionnaire")
st.markdown("""
Welcome to the Public Sphere Influence Survey for Lebanon and Tunisia.
This tool is part of a project hosted at [publicspheres.org](https://www.publicspheres.org). Your responses will help us refine our Influence Score model.

👉 **Influence = Reach × Salience × Persuasiveness**

Please fill in the following fields for each media sample from **Jan 1 – Mar 31, 2025**. Aim for 8–10 per media type. Click **Submit Sample** at the end of each sample, and use **Start New Sample** to enter another.
""")

if "samples" not in st.session_state:
    st.session_state.samples = []

st.header("1. Media Sample Details")
title = st.text_input("Media Title or Description")
platform = st.text_input("Platform or Outlet (e.g., channel, page, newspaper)")
link = st.text_input("Link (if available)")
date = st.date_input("Date of Broadcast/Publication", min_value=datetime.date(2025,1,1), max_value=datetime.date(2025,3,31))
media_type = st.selectbox("Media Type", ["TV", "Radio", "Print", "Online News", "Podcast", "Social Media", "Hybrid/Other"])
transcript = st.radio("Transcript Available?", ["Yes", "No", "Not Sure"])
transcript_details = st.text_input("Transcript Link or Access Notes (if known)")

st.header("2. Reach")
reach_score = st.slider("Estimated Reach (0–1)", 0.0, 1.0, 0.5, step=0.01)
reach_basis = st.text_area("Basis for Reach Estimate (audience ratings, views, impressions, professional judgment, etc.)")
reach_notes = st.text_area("Additional Notes on Reach (optional)")

st.header("3. Salience")
salience_score = st.slider("Salience Score (0–1)", 0.0, 1.0, 0.5, step=0.01)
issues = st.multiselect("Which public issues are reflected in the content?", [
    "Economy / Cost of Living", "Government Leadership / Corruption", "Security / Civil Unrest",
    "Health", "Immigration / Emigration", "Freedom of Speech / Civil Liberties", "Other"
])
salience_notes = st.text_area("Explanation of Salience (1–4 sentences)")

st.header("4. Persuasiveness (Discursiveness)")

st.subheader("Logos (Reasoning)")
logos_score = st.slider("Logos Score (0–1)", 0.0, 1.0, 0.5, step=0.01)
logos_notes = st.text_area("Explanation of Logos")

st.subheader("Pathos (Emotion)")
pathos_score = st.slider("Pathos Score (0–1)", 0.0, 1.0, 0.5, step=0.01)
pathos_notes = st.text_area("Explanation of Pathos")

st.subheader("Ethos (Credibility)")
ethos_score = st.slider("Ethos Score (0–1)", 0.0, 1.0, 0.5, step=0.01)
ethos_notes = st.text_area("Explanation of Ethos")

st.header("5. Final Reflections")
reflections = st.text_area("What are we missing in how we assess influence? Any suggestions to improve the model?")

if st.button("✅ Submit Sample"):
    sample = {
        "Title": title,
        "Platform": platform,
        "Link": link,
        "Date": str(date),
        "Type": media_type,
        "Transcript Available": transcript,
        "Transcript Details": transcript_details,
        "Reach Score": reach_score,
        "Reach Basis": reach_basis,
        "Reach Notes": reach_notes,
        "Salience Score": salience_score,
        "Issues": issues,
        "Salience Notes": salience_notes,
        "Logos": logos_score,
        "Logos Notes": logos_notes,
        "Pathos": pathos_score,
        "Pathos Notes": pathos_notes,
        "Ethos": ethos_score,
        "Ethos Notes": ethos_notes,
        "Reflections": reflections
    }
    st.session_state.samples.append(sample)
    st.success("Sample submitted! You can now start a new one.")

if st.button("📄 Download All Samples"):
    df = pd.DataFrame(st.session_state.samples)
    st.download_button("Download CSV", data=df.to_csv(index=False), file_name="influence_samples.csv", mime="text/csv")

if st.button("➕ Start New Sample"):
    st.experimental_rerun()
