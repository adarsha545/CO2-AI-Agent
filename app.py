import streamlit as st
import pandas as pd
import ollama
from rag import generate_rag_response
from sentence_transformers import SentenceTransformer
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import chromadb
import matplotlib.pyplot as plt
import time

# ---------------------- FUNCTIONS ----------------------
def get_tip(activity):
    with open("tips.txt", "r") as file:
        tips = file.readlines()

    for tip in tips:
        if ":" in tip:
            key, value = tip.split(":", 1)
            if key.strip() == activity:
                return value.strip()

    return "No suggestion available."
def get_ai_recommendation(activity, emission):
    prompt = f"""
You are an Environmental Sustainability Expert.

Current Activity:
{activity}

Current CO₂ Emission:
{emission} kg/day

Give ONLY exactly 3 practical eco-friendly suggestions.

Rules:
- Return only the numbered suggestions.
- Do not write headings.
- Do not repeat the activity.
- Do not mention CO₂ values.
- Do not mention better alternatives.
- Keep each suggestion short (1 sentence).
- Maximum 60 words total.

Example:

1. Use public transport whenever possible.
2. Combine multiple trips into one journey.
3. Walk or cycle for short distances.
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": 0.2,
            "num_predict": 80
        }
    )

    return response["message"]["content"]

from io import BytesIO

def create_pdf(report_text):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    for line in report_text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)

    buffer.seek(0)

    return buffer
# ---------------------- PAGE ----------------------

st.set_page_config(
    page_title="CO₂ AI Agent",
    page_icon="🌍",
    layout="wide"
)
# ---------------- Sidebar ----------------

st.sidebar.title("🌍 Carbon Footprint AI")

st.sidebar.info(
"""
Estimate your daily carbon emissions,
explore greener alternatives,
and receive AI-powered sustainability insights.
"""
)

st.sidebar.markdown("---")

st.sidebar.success("🏆 TCS APEX Capstone Project")

st.sidebar.markdown("### 🛠 Tech Stack")

st.sidebar.write("🐍 Python")
st.sidebar.write("🎈 Streamlit")
st.sidebar.write("🤖 Ollama (Llama 3)")
st.sidebar.write("🧠 ChromaDB")
st.sidebar.write("📄 Sentence Transformers")
st.sidebar.write("📊 Matplotlib")

st.sidebar.markdown("---")

st.sidebar.caption(
"Developed using Retrieval-Augmented Generation (RAG) and Large Language Models."
)
# ---------------------- DATA ----------------------

df = pd.read_csv("dataset.csv")
st.title("🌍 Carbon Footprint AI Assistant")

st.markdown(
    """
Estimate your carbon emissions, discover eco-friendly alternatives,
and receive AI-powered sustainability recommendations.
"""
)

st.markdown("---")


st.subheader("🌱 Select an Assessment Method")
input_method = st.radio(
    "Select one:",
    [
        "Choose from List",
        "Type Your Activity",
        "Upload CSV File"
    ]
)
if input_method == "Choose from List":

    activity = st.selectbox(
        "Select an activity",
        df["Activity"]
    )
elif input_method == "Type Your Activity":

    activity = st.text_input(
        "Describe your activity",
        placeholder="Example: I drive 20 km daily using a petrol car"
    )
elif input_method == "Upload CSV File":

    uploaded_file = st.file_uploader(
        "📂 Upload your activity CSV",
        type=["csv"]
    )

    activity = ""

    if uploaded_file is not None:

        uploaded_df = pd.read_csv(uploaded_file)

        st.success("✅ CSV uploaded successfully!")

        st.dataframe(uploaded_df)

        st.subheader("📊 Uploaded Dataset Summary")

        total_emission = uploaded_df["Avg_CO2_Emission"].sum()
        average_emission = uploaded_df["Avg_CO2_Emission"].mean()

        highest = uploaded_df.loc[
            uploaded_df["Avg_CO2_Emission"].idxmax()
        ]

        st.metric("🌍 Total CO₂ Emission", f"{total_emission:.2f} kg/day")
        st.metric("📈 Average CO₂ Emission", f"{average_emission:.2f} kg/day")
        st.metric("⚠ Highest Emission Activity", highest["Activity"])

        if st.button(
            "🤖 Analyze Uploaded Dataset",
            type="primary"
        ):

            summary = uploaded_df.to_string(index=False)

            prompt = f"""
You are an Environmental Sustainability Expert.

The dataset has already been analyzed.

The results are:

Total CO₂ Emission: {total_emission:.2f} kg

Average CO₂ Emission: {average_emission:.2f} kg/day

Highest Emission Activity:
{highest["Activity"]}

Highest Emission Value:
{highest["Avg_CO2_Emission"]:.2f} kg/day

IMPORTANT:
Do NOT recalculate or change these values.
Use them exactly as provided.

Only provide:

1. Overall Sustainability Assessment (about 70 words)

2. Exactly 3 practical eco-friendly recommendations.

Do not repeat the statistics.
Do not invent new numbers.
"""

            status = st.status(
            "🚀 Starting analysis...",
            expanded=True
            )

            status.write("📄 Reading uploaded CSV...")
            time.sleep(0.5)

            status.write("📊 Calculating carbon emissions...")
            time.sleep(0.5)

            status.write("🤖 Sending data to Llama 3...")

            response = ollama.chat(
            model="llama3",
            messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

            status.write("📋 Preparing report...")

            status.update(
             label="✅ Analysis Complete",
             state="complete"
            )
            st.subheader("📊 Dataset Analysis Summary")
            col1, col2, col3 = st.columns(3)

            with col1:
             st.metric(
            "🌍 Total CO₂ Emission",
            f"{total_emission:.2f} kg"
            )

            with col2:
             st.metric(
            "📈 Average CO₂ Emission",
            f"{average_emission:.2f} kg/day"
            )

            with col3:
             st.metric(
            "⚠ Highest Emission Activity",
            highest["Activity"]
            )
            st.subheader("🤖 AI Sustainability Analysis")

            st.markdown(response["message"]["content"])
            report = f"""
            CSV DATASET ANALYSIS

            Total CO₂ Emission:
            {total_emission:.2f} kg/day

            Average CO₂ Emission:
            {average_emission:.2f} kg/day

            Highest Emission Activity:
            {highest["Activity"]}

            AI Analysis:

            {response["message"]["content"]}
            """

            pdf = create_pdf(report)

            st.download_button(
            "📄 Download PDF Analysis Report",
            data=pdf,
            file_name="Dataset_Analysis_Report.pdf",
            mime="application/pdf"
            )
            

            st.subheader("📊 Top 10 Highest CO₂ Activities")

            top10 = uploaded_df.sort_values(
            "Avg_CO2_Emission",
            ascending=False
            ).head(10)

            fig, ax = plt.subplots(figsize=(7,3.5))

            ax.bar(
            top10["Activity"],
            top10["Avg_CO2_Emission"]
            )

            plt.xticks(rotation=45, ha="right")

            ax.set_ylabel("CO₂ (kg/day)")
            ax.set_title("Top 10 CO₂ Emitting Activities")

            plt.tight_layout()

            st.pyplot(fig)
            
            st.subheader("🥧 Category-wise CO₂ Emission")

            category_sum = uploaded_df.groupby("Category")["Avg_CO2_Emission"].sum()

            fig2, ax2 = plt.subplots(figsize=(6,6))

            ax2.pie(
            category_sum,
            labels=category_sum.index,
            autopct="%1.1f%%",
            startangle=90
            )

            ax2.set_title("CO₂ Emission by Category")

            st.pyplot(fig2)
            st.subheader("📋 Category Summary")

            summary_df = uploaded_df.groupby("Category").agg(
            Activities=("Activity", "count"),
            Total_CO2=("Avg_CO2_Emission", "sum"),
            Average_CO2=("Avg_CO2_Emission", "mean")
            )

            st.dataframe(summary_df)
            st.stop()
            

if input_method != "Upload CSV File":

    if "last_activity" not in st.session_state:
        st.session_state.last_activity = activity

    if st.session_state.last_activity != activity:
        st.session_state.ai_response = ""
        st.session_state.last_activity = activity

# ---------------- GET DATA ----------------

if input_method == "Choose from List":

    row = df[df["Activity"] == activity].iloc[0]

elif input_method == "Type Your Activity":

    if activity == "":
        st.info("Please type your activity.")
        st.stop()

    if st.button("🔍 Analyze Activity", type="primary"):

        progress = st.progress(0)

        progress.progress(20, text="🔍 Searching environmental database...")
        time.sleep(0.5)

        progress.progress(60, text="🤖 Generating AI recommendation...")

        matched_activity, answer = generate_rag_response(activity)

        progress.progress(100, text="✅ Completed")
        time.sleep(0.3)
        progress.empty()

        row = df[df["Activity"] == matched_activity].iloc[0]

        activity = matched_activity

        st.session_state.ai_response = answer

    else:
        st.stop()

elif input_method == "Upload CSV File":

    # Upload CSV is handled above.
    st.stop()

emission = row["Avg_CO2_Emission"]
category = row["Category"]
# ---------------- Better Alternative ----------------
alternative = row["Better_Alternative"]

alternative_emission = row["Alternative_CO2"]

if emission == 0:
    reduction = 0
else:
    reduction = round(
        ((emission - alternative_emission) / emission) * 100
    )


daily = emission
monthly = emission * 30
yearly = emission * 365

# ---------------------- DETAILS ----------------------
st.subheader("📊 Emission Details")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="🌍 Current CO₂ Emission",
        value=f"{emission:.2f} kg/day"
    )

with col2:
    st.metric(
        label="📂 Category",
        value=category
    )

st.write("")

col3, col4, col5 = st.columns(3)

with col3:
    st.metric(
        "📅 Daily",
        f"{daily:.2f} kg"
    )

with col4:
    st.metric(
        "🗓 Monthly",
        f"{monthly:.2f} kg"
    )

with col5:
    st.metric(
        "📆 Yearly",
        f"{yearly:.2f} kg"
    )

# ---------------------- STATUS ----------------------

st.subheader("🌍 Carbon Footprint Status")

if emission <= 1:
    st.success("🟢 Low Carbon Footprint")

elif emission <= 5:
    st.warning("🟡 Medium Carbon Footprint")

else:
    st.error("🔴 High Carbon Footprint")

# ---------------------- ECO SCORE ----------------------

st.subheader("⭐ Eco Score")

score = max(0, int(100 - emission * 10))

st.progress(score)

st.write(f"**Your Eco Score: {score}/100**")

# ---------------------- TIPS ----------------------

st.subheader("🌱 Eco-Friendly Suggestion")

tip = get_tip(activity)

st.success(tip)


# ---------------------- AI ----------------------
st.subheader("🤖 AI Recommendation")

if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""
if input_method == "Choose from List":

    if st.button("🚀 Generate AI Recommendation"):

        with st.spinner("Generating AI recommendation..."):
            st.session_state.ai_response = get_ai_recommendation(activity, emission)
            
            

if st.session_state.ai_response:

    st.success("✅ AI Recommendation Generated")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🌍 Current CO₂", f"{emission:.2f} kg/day")

    with col2:
        st.metric("💡 Better Alternative", alternative)

    with col3:
        st.metric("📉 Reduction", f"{reduction}%")

    st.markdown("---")
    st.markdown("### 🌱 AI Suggestions")
    st.markdown(st.session_state.ai_response)
        
report = f"""
CO₂ EMISSION REPORT

Activity:
{activity}

Category:
{category}

Daily:
{daily:.2f} kg

Monthly:
{monthly:.2f} kg

Yearly:
{yearly:.2f} kg

Eco Tip:
{tip}

AI Recommendation:

{st.session_state.ai_response}
"""

pdf = create_pdf(report)

st.download_button(
    "📄 Download PDF Report",
    data=pdf,
    file_name="CO2_Report.pdf",
    mime="application/pdf"
)

# ---------------------- CHARTS ----------------------

col1, col2 = st.columns(2)

# Bar Chart
with col1:
    st.subheader("📈 Carbon Emission Summary")

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.bar(
        ["Daily", "Monthly", "Yearly"],
        [daily, monthly, yearly],
        color=["#4CAF50", "#42A5F5", "#5C6BC0"]
    )
    bars = ax.bar(
    ["Daily", "Monthly", "Yearly"],
    [daily, monthly, yearly],
    color=["#4CAF50", "#42A5F5", "#5C6BC0"]
)

    for bar in bars:
      height = bar.get_height()
      ax.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{height:.1f}",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold"
    )

    ax.set_ylabel("CO₂ (kg)")
    ax.set_title("Emission Summary")

    plt.tight_layout()

    st.pyplot(fig)

# Current vs Better Alternative
with col2:

    st.subheader("💡 Current vs Better Alternative")

    fig2, ax2 = plt.subplots(figsize=(5, 4))

    activities = ["Current", "Alternative"]
    emissions = [
    emission,
    max(alternative_emission, 0.05)]

    ax2.bar(
        activities,
        emissions,
        color=["red", "green"]
    )

    ax2.set_ylabel("CO₂ (kg/day)")
    ax2.set_title("Emission Comparison")

    plt.tight_layout()

    st.pyplot(fig2)
st.subheader("📊 Average CO₂ by Category")

category_avg = (
    df.groupby("Category")["Avg_CO2_Emission"]
      .mean()
)

fig3, ax3 = plt.subplots(figsize=(6,4))

ax3.bar(
    category_avg.index,
    category_avg.values,
    color=[
        "steelblue",
        "green",
        "orange",
        "purple",
        "red"
    ]
)

ax3.set_ylabel("Average CO₂ (kg/day)")
ax3.set_title("Category-wise Average CO₂")

plt.tight_layout()

st.pyplot(fig3)