
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AADHAAR SAMIKSHA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. CUSTOM CSS
# =====================================================

st.markdown("""
<style>
    .main {
        background-color: var(--background-color);
    }

    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
    }

    .hero {
        padding: 28px;
        border-radius: 15px;
        background: linear-gradient(120deg, #123c69, #2874a6);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 38px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #eaf2f8;
        font-size: 16px;
    }

    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        padding: 16px;
        border-radius: 12px;
    }

    .insight-box {
        background-color: var(--secondary-background-color);
        border-left: 4px solid #2874a6;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 10px;
    }

    .chat-user {
        background-color: #d6eaf8;
        color: #17202a;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
    }

    .chat-bot {
        background-color: var(--secondary-background-color);
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
    }

    .section-heading {
        font-size: 22px;
        font-weight: 700;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. LOAD DATA USING PICKLE
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
PKL_PATH = BASE_DIR / "aadhaar_data.pkl.gz"


@st.cache_data
def load_data():

    if not PKL_PATH.exists():
        raise FileNotFoundError(
            "aadhaar_data.pkl not found. "
            "Keep it in the same folder as app.py."
        )

    df = pd.read_pickle(PKL_PATH, compression="gzip")

    required = [
        "date",
        "state",
        "district",
        "pincode",
        "age_0_5",
        "age_5_17",
        "age_18_greater",
        "bio_age_5_17",
        "bio_age_17_"
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    numeric_columns = [
        "age_0_5",
        "age_5_17",
        "age_18_greater",
        "bio_age_5_17",
        "bio_age_17_"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    for col in ["state", "district", "pincode"]:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    df = df.dropna(
        subset=["date", "state", "district", "pincode"]
    ).copy()

    if df.empty:
        raise ValueError("No valid records found in dataset.")

    df["total_enrolment"] = (
        df["age_0_5"]
        + df["age_5_17"]
        + df["age_18_greater"]
    )

    df["total_biometric"] = (
        df["bio_age_5_17"]
        + df["bio_age_17_"]
    )

    return df


try:
    df = load_data()

except Exception as e:
    st.error(f"Dataset loading error: {e}")
    st.stop()


# =====================================================
# 4. HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <h1>📊 AADHAAR SAMIKSHA</h1>
    <p>
        Data-driven insights into Aadhaar enrolment,
        biometric activity and demographic patterns.
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# 5. SIDEBAR FILTERS
# =====================================================

st.sidebar.title("🔎 Data Filters")
st.sidebar.markdown("Customize your analysis")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

states = sorted(df["state"].dropna().unique().tolist())

selected_states = st.sidebar.multiselect(
    "Select State",
    options=states,
    default=states
)

if selected_states:
    district_options = sorted(
        df[df["state"].isin(selected_states)]["district"]
        .dropna()
        .unique()
        .tolist()
    )
else:
    district_options = []

selected_districts = st.sidebar.multiselect(
    "Select District",
    options=district_options,
    default=district_options
)

if selected_districts:
    pincode_options = sorted(
        df[df["district"].isin(selected_districts)]["pincode"]
        .dropna()
        .unique()
        .tolist()
    )
else:
    pincode_options = []

selected_pincodes = st.sidebar.multiselect(
    "Select Pincode",
    options=pincode_options,
    default=pincode_options
)

# =====================================================
# 6. APPLY FILTERS
# =====================================================

filtered_df = df[
    (df["date"].dt.date >= start_date)
    & (df["date"].dt.date <= end_date)
    & (df["state"].isin(selected_states))
    & (df["district"].isin(selected_districts))
    & (df["pincode"].isin(selected_pincodes))
].copy()

if filtered_df.empty:
    st.warning(
        "No records found for the selected filters. "
        "Please change your filter selection."
    )
    st.stop()


# =====================================================
# 7. KEY PERFORMANCE INDICATORS
# =====================================================

st.markdown("## 📌 Key Performance Indicators")

total_enrolment = filtered_df["total_enrolment"].sum()
total_biometric = filtered_df["total_biometric"].sum()

active_pincodes = filtered_df["pincode"].nunique()
total_districts = filtered_df["district"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Enrolment",
    f"{total_enrolment:,.0f}"
)

col2.metric(
    "Biometric Activity",
    f"{total_biometric:,.0f}"
)

col3.metric(
    "Active Pincodes",
    f"{active_pincodes:,}"
)

col4.metric(
    "Districts Covered",
    f"{total_districts:,}"
)


# =====================================================
# 8. AUTOMATIC INSIGHTS
# =====================================================

st.markdown("## 💡 Automatic Insights")

district_summary = (
    filtered_df.groupby("district", as_index=False)
    .agg(
        total_enrolment=("total_enrolment", "sum"),
        total_biometric=("total_biometric", "sum")
    )
)

pincode_summary = (
    filtered_df.groupby("pincode", as_index=False)
    .agg(total_enrolment=("total_enrolment", "sum"))
)

daily_summary = (
    filtered_df.groupby("date", as_index=False)
    .agg(total_enrolment=("total_enrolment", "sum"))
)

top_district = district_summary.loc[
    district_summary["total_enrolment"].idxmax()
]

top_biometric_district = district_summary.loc[
    district_summary["total_biometric"].idxmax()
]

top_pincode = pincode_summary.loc[
    pincode_summary["total_enrolment"].idxmax()
]

peak_date = daily_summary.loc[
    daily_summary["total_enrolment"].idxmax()
]

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>Highest Enrolment District</b><br>
            {top_district['district']} —
            {top_district['total_enrolment']:,.0f} enrolments
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight-box">
            <b>Top Performing Pincode</b><br>
            {top_pincode['pincode']} —
            {top_pincode['total_enrolment']:,.0f} enrolments
        </div>
        """,
        unsafe_allow_html=True
    )

with insight_col2:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>Highest Biometric Activity</b><br>
            {top_biometric_district['district']} —
            {top_biometric_district['total_biometric']:,.0f}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight-box">
            <b>Peak Enrolment Date</b><br>
            {peak_date['date'].strftime('%d %B %Y')} —
            {peak_date['total_enrolment']:,.0f} enrolments
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 9. DASHBOARD TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "📅 Temporal Analysis",
    "📍 Geographic Analysis",
    "👥 Age Analysis",
    "🤖 SAMIKSHA Chatbot"
])


# =====================================================
# TAB 1: OVERVIEW
# =====================================================

with tab1:

    st.markdown("## Enrolment Overview")

    daily_data = (
        filtered_df.groupby("date", as_index=False)
        .agg(total_enrolment=("total_enrolment", "sum"))
        .sort_values("date")
    )

    fig = px.line(
        daily_data,
        x="date",
        y="total_enrolment",
        title="Daily Aadhaar Enrolment Trend",
        markers=True,
        labels={
            "date": "Date",
            "total_enrolment": "Total Enrolment"
        }
    )

    fig.update_layout(
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    top10 = district_summary.nlargest(
        10,
        "total_enrolment"
    ).sort_values("total_enrolment")

    fig2 = px.bar(
        top10,
        x="total_enrolment",
        y="district",
        orientation="h",
        title="Top 10 Districts by Enrolment",
        color="total_enrolment",
        labels={
            "district": "District",
            "total_enrolment": "Total Enrolment"
        }
    )

    st.plotly_chart(fig2, use_container_width=True)


# =====================================================
# TAB 2: TEMPORAL ANALYSIS
# =====================================================

with tab2:

    st.markdown("## Temporal Analysis")

    temporal_df = filtered_df.copy()

    temporal_df["year"] = temporal_df["date"].dt.year
    temporal_df["month"] = temporal_df["date"].dt.month
    temporal_df["month_name"] = temporal_df["date"].dt.strftime("%b")
    temporal_df["day_of_year"] = temporal_df["date"].dt.dayofyear

    monthly = (
        temporal_df.groupby(
            ["year", "month", "month_name"],
            as_index=False
        )
        .agg(
            total_enrolment=("total_enrolment", "sum"),
            total_biometric=("total_biometric", "sum")
        )
        .sort_values(["year", "month"])
    )

    fig = px.bar(
        monthly,
        x="month_name",
        y=["total_enrolment", "total_biometric"],
        color_discrete_sequence=["#2874a6", "#e67e22"],
        barmode="group",
        title="Monthly Enrolment vs Biometric Activity",
        labels={
            "month_name": "Month",
            "value": "Count",
            "variable": "Activity"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Year-wise Activity Heatmap")

    heatmap_data = (
        temporal_df.groupby(
            ["year", "day_of_year"],
            as_index=False
        )["total_enrolment"]
        .sum()
    )

    heatmap_pivot = heatmap_data.pivot(
        index="year",
        columns="day_of_year",
        values="total_enrolment"
    )

    fig_heat = px.imshow(
        heatmap_pivot,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Enrolment Intensity by Year and Day of Year",
        labels={
            "x": "Day of Year",
            "y": "Year",
            "color": "Enrolment"
        }
    )

    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("### Monthly Growth Analysis")

    monthly["growth_percentage"] = (
        monthly["total_enrolment"]
        .pct_change() * 100
    )

    st.dataframe(
        monthly[
            [
                "year",
                "month_name",
                "total_enrolment",
                "total_biometric",
                "growth_percentage"
            ]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# TAB 3: GEOGRAPHIC ANALYSIS
# =====================================================

with tab3:

    st.markdown("## Geographic Analysis")

    geo_col1, geo_col2 = st.columns(2)

    with geo_col1:

        st.markdown("### Top 10 Pincodes")

        top_pincodes = (
            pincode_summary
            .nlargest(10, "total_enrolment")
            .sort_values("total_enrolment")
        )

        fig_pin = px.bar(
            top_pincodes,
            x="total_enrolment",
            y="pincode",
            orientation="h",
            title="Top Pincodes by Enrolment",
            color="total_enrolment"
        )

        st.plotly_chart(
            fig_pin,
            use_container_width=True
        )

    with geo_col2:

        st.markdown("### District Enrolment vs Biometric")

        fig_scatter = px.scatter(
            district_summary,
            x="total_enrolment",
            y="total_biometric",
            hover_name="district",
            size="total_enrolment",
            color="total_biometric",
            title="District-level Activity Comparison",
            labels={
                "total_enrolment": "Total Enrolment",
                "total_biometric": "Total Biometric"
            }
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

    st.markdown("### Enrolment and Biometric Correlation")

    correlation = district_summary[
        ["total_enrolment", "total_biometric"]
    ].corr()

    fig_corr = px.imshow(
        correlation,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title="Correlation Heatmap"
    )

    st.plotly_chart(
        fig_corr,
        use_container_width=True
    )

    corr_value = correlation.loc[
        "total_enrolment",
        "total_biometric"
    ]

    st.metric(
        "Enrolment-Biometric Correlation",
        f"{corr_value:.3f}"
    )

    st.markdown("### District-wise Summary")

    st.dataframe(
        district_summary.sort_values(
            "total_enrolment",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# TAB 4: AGE ANALYSIS
# =====================================================

with tab4:

    st.markdown("## Age Group Analysis")

    age_col1, age_col2 = st.columns(2)

    age_data = pd.DataFrame({
        "Age Group": [
            "0–5 Years",
            "5–17 Years",
            "18+ Years"
        ],
        "Enrolment": [
            filtered_df["age_0_5"].sum(),
            filtered_df["age_5_17"].sum(),
            filtered_df["age_18_greater"].sum()
        ]
    })

    biometric_data = pd.DataFrame({
        "Age Group": [
            "5–17 Years",
            "17+ Years"
        ],
        "Biometric Activity": [
            filtered_df["bio_age_5_17"].sum(),
            filtered_df["bio_age_17_"].sum()
        ]
    })

    with age_col1:

        fig_age = px.pie(
            biometric_data,
            names="Age Group",
            values="Biometric Activity",
            title="Biometric Activity by Age Group",
            hole=0.4
        )

        st.plotly_chart(
            fig_age,
            use_container_width=True
        )

    with age_col2:

        fig_enrolment = px.bar(
            age_data,
            x="Age Group",
            y="Enrolment",
            color="Age Group",
            title="Enrolment Distribution by Age Group",
            text_auto=True
        )

        st.plotly_chart(
            fig_enrolment,
            use_container_width=True
        )

    st.markdown("### Age-wise Enrolment Data")

    st.dataframe(
        age_data,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Age-wise Biometric Data")

    st.dataframe(
        biometric_data,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# TAB 5: SAMIKSHA CHATBOT
# =====================================================

def chatbot_answer(question, data):

    q = question.lower().strip()

    district_data = (
        data.groupby("district")
        .agg(
            enrolment=("total_enrolment", "sum"),
            biometric=("total_biometric", "sum")
        )
        .sort_values("enrolment", ascending=False)
    )

    pincode_data = (
        data.groupby("pincode")["total_enrolment"]
        .sum()
        .sort_values(ascending=False)
    )

    state_data = (
        data.groupby("state")["total_enrolment"]
        .sum()
        .sort_values(ascending=False)
    )

    # Greetings

    if any(word in q for word in [
        "hello", "hi", "hey", "hii", "namaste"
    ]):
        return (
            "Hello! Welcome to SAMIKSHA. "
            "I can help you explore Aadhaar enrolment, "
            "biometric activity, districts, states and age groups."
        )

    # Help

    if "help" in q or "what can you do" in q:
        return (
            "You can ask me questions such as:\n"
            "- Which district has the highest enrolment?\n"
            "- Which pincode has maximum enrolment?\n"
            "- What is the total biometric activity?\n"
            "- Which state has maximum enrolment?\n"
            "- Compare two districts.\n"
            "- What is the age-wise enrolment distribution?"
        )

    # Overall Summary

    if any(word in q for word in [
        "overall", "summary", "total", "how many"
    ]):

        if "biometric" in q:
            return (
                f"Total biometric activity is "
                f"{data['total_biometric'].sum():,.0f}."
            )

        if "enrolment" in q or "enrollment" in q:
            return (
                f"Total Aadhaar enrolment is "
                f"{data['total_enrolment'].sum():,.0f}."
            )

        return (
            f"Your selected dataset contains "
            f"{data['total_enrolment'].sum():,.0f} total enrolments, "
            f"{data['total_biometric'].sum():,.0f} biometric activities, "
            f"{data['district'].nunique()} districts and "
            f"{data['pincode'].nunique()} pincodes."
        )

    # Top District

    if "district" in q and any(word in q for word in [
        "highest", "top", "maximum", "most"
    ]):

        if "biometric" in q:
            district = district_data["biometric"].idxmax()
            value = district_data.loc[district, "biometric"]

            return (
                f"{district} has the highest biometric activity "
                f"with {value:,.0f} activities."
            )

        district = district_data["enrolment"].idxmax()
        value = district_data.loc[district, "enrolment"]

        return (
            f"{district} has the highest enrolment "
            f"with {value:,.0f} enrolments."
        )

    # District Comparison / Specific District

    matched_districts = [
        district
        for district in district_data.index
        if str(district).lower() in q
    ]

    if len(matched_districts) >= 2:

        d1, d2 = matched_districts[:2]

        return (
            f"{d1} has {district_data.loc[d1, 'enrolment']:,.0f} "
            f"enrolments and {d2} has "
            f"{district_data.loc[d2, 'enrolment']:,.0f} enrolments."
        )

    if len(matched_districts) == 1:

        district = matched_districts[0]

        return (
            f"District: {district}\n"
            f"Total Enrolment: "
            f"{district_data.loc[district, 'enrolment']:,.0f}\n"
            f"Biometric Activity: "
            f"{district_data.loc[district, 'biometric']:,.0f}"
        )

    # Pincode

    matched_pincodes = [
        pin
        for pin in pincode_data.index
        if str(pin) in q
    ]

    if matched_pincodes:

        pin = matched_pincodes[0]

        return (
            f"Pincode {pin} has "
            f"{pincode_data.loc[pin]:,.0f} total enrolments."
        )

    if "pincode" in q and any(word in q for word in [
        "highest", "top", "maximum", "most"
    ]):

        pin = pincode_data.idxmax()

        return (
            f"Pincode {pin} has the highest enrolment "
            f"with {pincode_data.loc[pin]:,.0f}."
        )

    # State

    matched_states = [
        state
        for state in state_data.index
        if str(state).lower() in q
    ]

    if matched_states:

        state = matched_states[0]

        return (
            f"{state} has "
            f"{state_data.loc[state]:,.0f} total enrolments."
        )

    if "state" in q and any(word in q for word in [
        "highest", "top", "maximum", "most"
    ]):

        state = state_data.idxmax()

        return (
            f"{state} has the highest enrolment "
            f"with {state_data.loc[state]:,.0f}."
        )

    # Age Analysis

    if "age" in q or "children" in q:

        age_0_5 = data["age_0_5"].sum()
        age_5_17 = data["age_5_17"].sum()
        age_18 = data["age_18_greater"].sum()

        return (
            "Age-wise enrolment:\n"
            f"0–5 Years: {age_0_5:,.0f}\n"
            f"5–17 Years: {age_5_17:,.0f}\n"
            f"18+ Years: {age_18:,.0f}"
        )

    # Correlation

    if "correlation" in q or "relationship" in q:

        corr = data[
            ["total_enrolment", "total_biometric"]
        ].corr().iloc[0, 1]

        return (
            f"The correlation between enrolment and "
            f"biometric activity is {corr:.3f}."
        )

    # Peak Date

    if "date" in q or "day" in q:

        daily = (
            data.groupby("date")["total_enrolment"]
            .sum()
        )

        peak = daily.idxmax()

        return (
            f"The peak enrolment date is "
            f"{peak.strftime('%d %B %Y')} "
            f"with {daily.max():,.0f} enrolments."
        )

    # Top Ranking

    if "top" in q or "ranking" in q:

        top = district_data.head(5)

        result = "Top 5 districts by enrolment:\n"

        for district, row in top.iterrows():
            result += (
                f"- {district}: {row['enrolment']:,.0f}\n"
            )

        return result

    return (
        "Sorry, I couldn't understand that question. "
        "Try asking about total enrolment, biometric activity, "
        "districts, states, pincodes or age groups."
    )


with tab5:

    st.markdown("## 🤖 SAMIKSHA AI Assistant")

    st.write(
        "Ask questions about your selected Aadhaar dataset "
        "and get instant data-driven responses."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I am SAMIKSHA. "
                    "Ask me anything about your Aadhaar data."
                )
            }
        ]

    # Display chat history

    for message in st.session_state.chat_history:

        if message["role"] == "user":

            st.markdown(
                f"""
                <div class="chat-user">
                    <b>You:</b> {message['content']}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="chat-bot">
                    <b>SAMIKSHA:</b><br>
                    {message['content'].replace(chr(10), '<br>')}
                </div>
                """,
                unsafe_allow_html=True
            )

    # Chat input

    user_question = st.chat_input(
        "Ask something about Aadhaar data..."
    )

    if user_question:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        response = chatbot_answer(
            user_question,
            filtered_df
        )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()

    st.markdown("### Suggested Questions")

    suggestions = [
        "Which district has highest enrolment?",
        "Which state has maximum enrolment?",
        "What is the total biometric activity?",
        "Show age-wise enrolment",
        "Which pincode has highest enrolment?"
    ]

    suggestion_cols = st.columns(2)

    for i, suggestion in enumerate(suggestions):

        with suggestion_cols[i % 2]:

            if st.button(
                suggestion,
                key=f"suggestion_{i}",
                use_container_width=True
            ):

                st.session_state.chat_history.append({
                    "role": "user",
                    "content": suggestion
                })

                response = chatbot_answer(
                    suggestion,
                    filtered_df
                )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })

                st.rerun()

    if st.button("🗑️ Clear Chat"):

        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I am SAMIKSHA. "
                    "Ask me anything about your Aadhaar data."
                )
            }
        ]

        st.rerun()


# =====================================================
# 10. FILTERED DATASET
# =====================================================

st.markdown("---")

with st.expander("📂 View Filtered Dataset"):

    st.write(
        f"Showing {len(filtered_df):,} records "
        "based on your selected filters."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 11. FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; padding:15px;">
        <h4>AADHAAR SAMIKSHA</h4>
        <p>
            Data-driven insights for understanding
            Aadhaar enrolment and biometric patterns.
        </p>
        <p>Developed for data analysis and research purposes.</p>
    </div>
    """,
    unsafe_allow_html=True
)
