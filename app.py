import streamlit as st
import anthropic
import re
import random
import base64
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DS Buddy — Interview Prep",
    page_icon="📊",
    layout="wide"
)


# ── Question bank ─────────────────────────────────────────────────────────────
QUESTION_BANK = {
    "Data Science": {
        "Beginner": [
            "What is the difference between supervised and unsupervised learning?",
            "What is overfitting and how do you prevent it?",
            "Explain the bias-variance tradeoff.",
            "What is a confusion matrix and what metrics can you derive from it?",
            "What is the difference between classification and regression?",
            "What is cross-validation and why is it used?",
            "What does p-value mean in statistics?",
            "What is the difference between mean, median, and mode?",
            "What is a normal distribution and why is it important?",
            "What is feature scaling and when would you use it?",
            "What is the difference between correlation and causation?",
            "What is a train/test split and why do we need it?",
            "What is logistic regression and when is it used?",
            "What is a decision tree?",
            "What is the difference between bagging and boosting?",
        ],
        "Intermediate": [
            "How does a Random Forest work and why is it better than a single decision tree?",
            "Explain precision vs recall and when you'd prioritize each.",
            "What is regularization? Explain L1 vs L2.",
            "How does gradient descent work?",
            "What is the ROC curve and what does AUC represent?",
            "Explain how k-means clustering works.",
            "What is PCA and when would you use it?",
            "What is the curse of dimensionality?",
            "How do you handle imbalanced datasets?",
            "What is the difference between parametric and non-parametric models?",
            "Explain how XGBoost works at a high level.",
            "What is feature importance and how is it calculated in tree models?",
            "What is SMOTE and when would you use it?",
            "How do you detect and handle outliers in a dataset?",
            "What is a pipeline in machine learning?",
        ],
        "Senior": [
            "How would you design an ML system for a highly imbalanced dataset at scale?",
            "Explain the tradeoffs between model interpretability and performance.",
            "How do you approach model monitoring in production?",
            "What is concept drift and how do you detect it?",
            "How would you design an A/B testing framework for an ML model?",
            "Explain the differences between online and batch learning.",
            "What is a feature store and why is it important in ML systems?",
            "How do you ensure fairness and avoid bias in ML models?",
            "What is the difference between model accuracy and model reliability?",
            "How would you handle a model that performs well offline but poorly in production?",
        ],
    },
    "Data Analytics": {
        "Beginner": [
            "What is the difference between a JOIN and a UNION in SQL?",
            "What are the different types of SQL JOINs?",
            "What is a KPI and can you give an example?",
            "What is the difference between a dimension and a fact table?",
            "How would you find duplicate records in a SQL table?",
            "What is GROUP BY used for in SQL?",
            "What is the difference between WHERE and HAVING in SQL?",
            "What is a subquery?",
            "What is data granularity?",
            "How do you calculate a percentage change between two values?",
            "What is a pivot table and when would you use one?",
            "What is the difference between COUNT(*) and COUNT(column)?",
            "What is a NULL value in SQL and how do you handle it?",
            "What is a rolling average and how would you calculate it?",
            "What does DISTINCT do in SQL?",
        ],
        "Intermediate": [
            "What is a window function in SQL? Give an example.",
            "How would you design an A/B test for a new feature?",
            "What is cohort analysis and when would you use it?",
            "Explain the difference between RANK(), DENSE_RANK(), and ROW_NUMBER().",
            "What is a common table expression (CTE) and when would you use one?",
            "How do you calculate customer lifetime value?",
            "What is funnel analysis?",
            "How would you investigate a sudden drop in a key metric?",
            "What is seasonality and how do you account for it in analysis?",
            "What is the difference between a star schema and a snowflake schema?",
            "How do you calculate retention rate?",
            "What is statistical significance and why does it matter in analytics?",
            "What is the difference between leading and lagging indicators?",
            "How would you build a churn prediction analysis?",
            "What is the difference between correlation and regression in analytics?",
        ],
        "Senior": [
            "How would you build a metrics framework for a new product from scratch?",
            "Describe how you would approach a data quality issue discovered in production.",
            "How do you prioritize which metrics matter most to a business?",
            "What is a North Star metric and how do you identify one?",
            "How would you design a reporting system that scales to thousands of users?",
            "What is survivorship bias and how can it affect analysis?",
            "How do you communicate complex analysis to non-technical stakeholders?",
            "What is Goodhart's Law and how does it apply to metrics?",
            "How would you set up experimentation infrastructure from scratch?",
            "What tradeoffs do you consider when choosing between real-time and batch reporting?",
        ],
    },
    "Data Engineering": {
        "Beginner": [
            "What is the difference between a data warehouse and a data lake?",
            "What is ETL and what does each step mean?",
            "What is Apache Spark and why is it used?",
            "What is data partitioning and why does it matter?",
            "What is the difference between batch and stream processing?",
            "What is a primary key vs a foreign key?",
            "What is data normalization?",
            "What is an index in a database and why is it useful?",
            "What is the difference between SQL and NoSQL databases?",
            "What is a data pipeline?",
            "What is idempotency in data pipelines?",
            "What is the difference between structured and unstructured data?",
            "What is a message queue and what is it used for?",
            "What is schema-on-read vs schema-on-write?",
            "What is a data catalog?",
        ],
        "Intermediate": [
            "How would you design a data pipeline that handles failures reliably?",
            "What is data modeling and what's the difference between star and snowflake schema?",
            "What is Apache Airflow and what problem does it solve?",
            "What is the difference between Kafka and a traditional message queue?",
            "How do you handle late-arriving data in a streaming pipeline?",
            "What is a medallion architecture (bronze/silver/gold)?",
            "What is Change Data Capture (CDC) and when would you use it?",
            "How do you optimize a slow SQL query?",
            "What is data lineage and why is it important?",
            "What is the difference between OLTP and OLAP systems?",
            "How does Apache Kafka ensure message delivery guarantees?",
            "What is a slowly changing dimension (SCD)?",
            "What is dbt and what problem does it solve?",
            "How would you implement data quality checks in a pipeline?",
            "What is the difference between push and pull in data pipelines?",
        ],
        "Senior": [
            "How would you design a real-time platform handling 1 million events per second?",
            "How do you ensure data quality across a large distributed pipeline?",
            "What is the Lambda architecture and what are its tradeoffs?",
            "How would you migrate a legacy data warehouse to a modern cloud platform?",
            "How do you approach capacity planning for a data platform?",
            "What are the tradeoffs between a centralised data warehouse and a data mesh?",
            "How would you handle GDPR data deletion requests across a data lake?",
            "What is exactly-once semantics in streaming and how is it achieved?",
            "How would you design a multi-tenant data platform?",
            "What is backpressure in streaming systems and how do you handle it?",
        ],
    },
    "AI Engineering": {
        "Beginner": [
            "What is the difference between a large language model (LLM) and a traditional ML model?",
            "What is prompt engineering?",
            "What is a token in the context of LLMs?",
            "What is the difference between zero-shot and few-shot prompting?",
            "What is an API and how do you use one to call an AI model?",
            "What is a system prompt?",
            "What is temperature in LLM generation and what does it control?",
            "What is the difference between GPT and BERT?",
            "What is hallucination in AI models?",
            "What is the context window of an LLM?",
            "What is fine-tuning and when would you use it?",
            "What is embedding in the context of AI?",
            "What is a vector database?",
            "What is the difference between generative AI and discriminative AI?",
            "What is RAG (Retrieval-Augmented Generation)?",
        ],
        "Intermediate": [
            "How does RAG work and when would you use it over fine-tuning?",
            "What is chain-of-thought prompting?",
            "How do you evaluate the quality of an LLM application?",
            "What is semantic search and how does it differ from keyword search?",
            "What are AI agents and how do they work?",
            "What is LangChain and what problem does it solve?",
            "How do you handle context window limitations in LLM applications?",
            "What is the difference between streaming and non-streaming LLM responses?",
            "What is a vector similarity search and what algorithms power it?",
            "How do you prevent prompt injection attacks?",
            "What is model quantization and why does it matter for deployment?",
            "What is the difference between open-source and closed-source LLMs?",
            "How would you build a document Q&A system?",
            "What is RLHF (Reinforcement Learning from Human Feedback)?",
            "How do you manage costs when building LLM applications at scale?",
        ],
        "Senior": [
            "How would you design a production-grade RAG system for an enterprise?",
            "What are the tradeoffs between fine-tuning and prompt engineering?",
            "How do you build reliable evals for LLM applications?",
            "How would you design an AI agent system that handles complex multi-step tasks?",
            "What are the key considerations when choosing between different LLM providers?",
            "How do you handle latency and reliability in LLM-powered products?",
            "What is Constitutional AI and how does it relate to AI safety?",
            "How would you design guardrails for an AI application?",
            "What is multi-modal AI and what engineering challenges does it introduce?",
            "How would you build an LLM observability and monitoring system?",
        ],
    },
}

# ── Anthropic client ──────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "messages": [],
    "applied_topic": "Data Science",
    "applied_diff": "Beginner",
    "total_interactions": 0,
    "score_sum": 0,
    "score_count": 0,
    "session_active": False,
    "session_qs_done": 0,
    "session_total": 5,
    "session_results": [],
    "input_key": 0,
    "logged_in": False,
    "username": "",
    "show_login": False,
    "diff_counts": {"Beginner": 0, "Intermediate": 0, "Senior": 0},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 0 !important;
    padding-bottom: 4rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1500px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* ── Sticky header ── */
.sticky-header {
    position: sticky;
    top: 0;
    z-index: 999;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 0 0 16px 16px;
    padding: 1rem 2rem;
    margin-bottom: 1.25rem;
    border: 1px solid #334155;
    border-top: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}
.sticky-header::before {
    content: '';
    position: absolute;
    top: -20px; right: 40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.header-left { display: flex; align-items: center; gap: 1rem; }
.header-logo img { height: 48px; width: auto; }
.header-title h1 { color: #f8fafc; font-size: 1.5rem; font-weight: 600; margin: 0 0 2px 0; letter-spacing: -0.02em; }
.header-title p { color: #94a3b8; font-size: 0.8rem; margin: 0; }
.header-title .accent { color: #818cf8; }
.header-right { display: flex; align-items: center; gap: 10px; }

/* ── Login button styles ── */
.login-btn {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 8px;
    color: #e2e8f0;
    padding: 6px 16px;
    font-size: 0.82rem;
    font-family: 'DM Sans', sans-serif;
    cursor: pointer;
    transition: all 0.15s;
}
.login-btn:hover { background: rgba(255,255,255,0.15); }
.user-badge {
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 8px;
    color: #a5b4fc;
    padding: 5px 14px;
    font-size: 0.82rem;
    font-weight: 500;
}
.guest-badge {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    color: #64748b;
    padding: 5px 14px;
    font-size: 0.82rem;
}

/* ── Login modal ── */
.login-modal {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.login-modal h3 { color: #f1f5f9; font-size: 1rem; font-weight: 500; margin: 0 0 1rem 0; }

/* ── Selector label ── */
.selector-label {
    font-size: 0.75rem; font-weight: 500; color: #64748b;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem;
}

/* ── Stats bar ── */
.stat-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 0.75rem 1rem; text-align: center;
}
.stat-number { font-size: 1.5rem; font-weight: 600; color: #0f172a; font-family: 'DM Mono', monospace; line-height: 1; }
.stat-label { font-size: 0.72rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px; }
.stat-card.highlight { background: #eef2ff; border-color: #c7d2fe; }
.stat-card.highlight .stat-number { color: #4f46e5; }
.stat-card.session { background: #f0fdf4; border-color: #86efac; }
.stat-card.session .stat-number { color: #166534; }

/* ── Chat container ── */
.chat-container {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px;
    padding: 1.5rem; margin-bottom: 1rem; min-height: 420px; max-height: 560px; overflow-y: auto;
}
.msg-user { display: flex; justify-content: flex-end; margin-bottom: 1.25rem; }
.msg-assistant { display: flex; justify-content: flex-start; margin-bottom: 1.25rem; }
.bubble-user {
    background: #4f46e5; color: white; padding: 0.85rem 1.1rem;
    border-radius: 16px 16px 4px 16px; max-width: 70%;
    font-size: 0.9rem; line-height: 1.6; white-space: pre-wrap;
}
.bubble-assistant {
    background: #f8fafc; border: 1px solid #e2e8f0; color: #1e293b;
    padding: 1.1rem 1.4rem; border-radius: 16px 16px 16px 4px;
    max-width: 80%; font-size: 0.9rem; line-height: 1.75;
}
.bubble-label { font-size: 0.7rem; color: #94a3b8; margin-bottom: 6px; font-weight: 500; letter-spacing: 0.04em; text-transform: uppercase; }

/* ── Feedback sections ── */
.fb-block { border-radius: 10px; padding: 0.85rem 1rem; margin-top: 0.6rem; border-left: 4px solid; }
.fb-block.score   { background: #eef2ff; border-color: #6366f1; }
.fb-block.good    { background: #f0fdf4; border-color: #22c55e; }
.fb-block.missing { background: #fff7ed; border-color: #f97316; }
.fb-block.model   { background: #f0f9ff; border-color: #0ea5e9; }
.fb-header { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }
.fb-header.score   { color: #4338ca; }
.fb-header.good    { color: #166534; }
.fb-header.missing { color: #9a3412; }
.fb-header.model   { color: #0369a1; }
.fb-score-value { font-size: 1.6rem; font-weight: 700; font-family: 'DM Mono', monospace; color: #4338ca; line-height: 1; }
.fb-point { display: flex; gap: 8px; align-items: flex-start; margin: 4px 0; font-size: 0.88rem; }
.fb-dot-good { color: #22c55e; font-size: 1rem; margin-top: 1px; }
.fb-dot-miss { color: #f97316; font-size: 1rem; margin-top: 1px; }
.fb-point-text { line-height: 1.5; }
.fb-model-text { font-size: 0.88rem; line-height: 1.7; color: #0c4a6e; }
.score-bar-bg { background: #e0e7ff; border-radius: 99px; height: 6px; overflow: hidden; margin-top: 6px; }
.score-bar-fill { height: 6px; border-radius: 99px; }

/* ── Streamlit overrides ── */
div.stButton > button {
    border-radius: 10px; font-family: 'DM Sans', sans-serif;
    font-weight: 500; font-size: 0.88rem; padding: 0.5rem 1.2rem;
    transition: all 0.15s; width: 100%;
}
div.stButton > button:first-child { background: #4f46e5; color: white; border: none; }
div.stButton > button:first-child:hover { background: #4338ca; }
div[data-testid="stSelectbox"] > div > div { border-radius: 10px; font-family: 'DM Sans', sans-serif; }
div[data-testid="stTextArea"] textarea {
    font-family: 'DM Sans', sans-serif; font-size: 0.92rem;
    border-radius: 12px; border: 1.5px solid #e2e8f0; line-height: 1.6; padding: 0.85rem 1rem;
}
div[data-testid="stTextArea"] textarea:focus { border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
div[data-testid="stTextInput"] input {
    border-radius: 10px; font-family: 'DM Sans', sans-serif; font-size: 0.9rem;
    border: 1.5px solid #334155; background: #0f172a; color: #e2e8f0; padding: 0.5rem 0.85rem;
}

/* ── Summary card ── */
.summary-card { background: #0f172a; border-radius: 16px; padding: 1.5rem 2rem; color: white; margin-top: 1rem; }
.summary-card h3 { color: #e2e8f0; font-size: 1.1rem; margin-bottom: 1rem; }
.summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.summary-stat { text-align: center; }
.summary-num { font-size: 2rem; font-weight: 600; font-family: 'DM Mono', monospace; color: #818cf8; }
.summary-lbl { font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; }

/* ── Copyright footer ── */
.ds-footer {
    margin-top: 2rem;
    padding: 1rem 0 0.5rem;
    border-top: 1px solid #e2e8f0;
    text-align: center;
    font-size: 0.75rem;
    color: #94a3b8;
}
.ds-footer a { color: #6366f1; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ── Sticky header ─────────────────────────────────────────────────────────────
login_html = ""
if st.session_state.logged_in:
    login_html = f'<span class="user-badge">👤 {st.session_state.username}</span>'
else:
    login_html = '<span class="guest-badge">Guest</span>'

st.markdown(f"""
<div class="sticky-header">
    <div class="header-left">
        <div class="header-logo">
            <img src="data:image/png;base64,{LOGO_B64}" alt="DS Buddy Logo"/>
        </div>
        <div class="header-title">
            <h1>DS Buddy <span class="accent">— Interview Prep</span></h1>
            <p>Practice Data Science, Analytics, Engineering & AI interviews</p>
        </div>
    </div>
    <div class="header-right">
        {login_html}
    </div>
</div>
""", unsafe_allow_html=True)


# ── Controls row ──────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([4, 4, 1.5])
with c1:
    st.markdown('<div class="selector-label">Topic</div>', unsafe_allow_html=True)
    sel_topic = st.selectbox(
        "topic",
        ["Data Science", "Data Analytics", "Data Engineering", "AI Engineering"],
        label_visibility="collapsed"
    )
with c2:
    st.markdown('<div class="selector-label">Difficulty</div>', unsafe_allow_html=True)
    sel_diff = st.selectbox(
        "difficulty", ["Beginner", "Intermediate", "Senior"],
        label_visibility="collapsed"
    )
with c3:
    st.markdown('<div class="selector-label">&nbsp;</div>', unsafe_allow_html=True)
    apply = st.button("Apply ✓", use_container_width=True)

if apply:
    st.session_state.applied_topic = sel_topic
    st.session_state.applied_diff = sel_diff
    st.session_state.messages = []
    st.session_state.total_interactions = 0
    st.session_state.score_sum = 0
    st.session_state.score_count = 0
    st.session_state.session_active = False
    st.session_state.session_qs_done = 0
    st.session_state.session_results = []
    st.session_state.input_key += 1
    st.rerun()

st.markdown("<div style='margin:0.75rem 0'></div>", unsafe_allow_html=True)

# ── Stats bar ─────────────────────────────────────────────────────────────────
s1, s2, s3 = st.columns(3)
avg_score = round(st.session_state.score_sum / st.session_state.score_count, 1) if st.session_state.score_count > 0 else None
score_display = f"{avg_score}/10" if avg_score is not None else "—"
session_display = f"{st.session_state.session_qs_done}/{st.session_state.session_total}" if st.session_state.session_active else "—"
qs_left = (st.session_state.session_total - st.session_state.session_qs_done) if st.session_state.session_active else "—"

with s1:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number">{st.session_state.total_interactions}</div>
        <div class="stat-label">Chat Interactions</div>
    </div>""", unsafe_allow_html=True)
with s2:
    st.markdown(f"""<div class="stat-card highlight">
        <div class="stat-number">{score_display}</div>
        <div class="stat-label">Avg Score</div>
    </div>""", unsafe_allow_html=True)
with s3:
    st.markdown(f"""<div class="stat-card session">
        <div class="stat-number">{session_display}</div>
        <div class="stat-label">Session Progress ({qs_left} left)</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin:0.75rem 0'></div>", unsafe_allow_html=True)

# ── Active settings badges ────────────────────────────────────────────────────
topic_colors = {
    "Data Science": "#ede9fe|#5b21b6",
    "Data Analytics": "#dbeafe|#1e40af",
    "Data Engineering": "#dcfce7|#166534",
    "AI Engineering": "#fef3c7|#92400e"
}
diff_colors = {"Beginner": "#f0f9ff|#0369a1", "Intermediate": "#fef9c3|#854d0e", "Senior": "#fce7f3|#9d174d"}

def badge(text, colors):
    bg, fg = colors.split("|")
    return f'<span style="background:{bg};color:{fg};padding:3px 12px;border-radius:20px;font-size:0.75rem;font-weight:500;margin-right:6px">{text}</span>'

st.markdown(
    badge(st.session_state.applied_topic, topic_colors[st.session_state.applied_topic]) +
    badge(st.session_state.applied_diff, diff_colors[st.session_state.applied_diff]),
    unsafe_allow_html=True
)
st.markdown("<div style='margin:0.5rem 0'></div>", unsafe_allow_html=True)

# ── Two-column layout: chat + donut chart ────────────────────────────────────
main_col, chart_col = st.columns([3, 1])

with chart_col:
    # Donut chart — questions answered per difficulty
    counts = st.session_state.diff_counts
    total_done = sum(counts.values())
    beg = counts["Beginner"]
    mid = counts["Intermediate"]
    sen = counts["Senior"]

    def donut_arc(cx, cy, r, start_deg, end_deg, color, stroke_w):
        import math
        start = math.radians(start_deg - 90)
        end = math.radians(end_deg - 90)
        x1 = cx + r * math.cos(start)
        y1 = cy + r * math.sin(start)
        x2 = cx + r * math.cos(end)
        y2 = cy + r * math.sin(end)
        large = 1 if (end_deg - start_deg) > 180 else 0
        return f'<path d="M {x1:.2f} {y1:.2f} A {r} {r} 0 {large} 1 {x2:.2f} {y2:.2f}" fill="none" stroke="{color}" stroke-width="{stroke_w}" stroke-linecap="round"/>'

    def make_donut(cx, cy, r, val, total, color, stroke_w=14):
        if total == 0:
            return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e2e8f0" stroke-width="{stroke_w}"/>'
        pct = min(val / total, 1.0)
        deg = pct * 359.99
        bg = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e2e8f0" stroke-width="{stroke_w}"/>'
        arc = donut_arc(cx, cy, r, 0, deg, color, stroke_w)
        return bg + arc

    # Three concentric rings
    svg_parts = []
    svg_parts.append(make_donut(80, 80, 58, beg, max(beg, 1) if total_done == 0 else total_done, "#6366f1", 12))
    svg_parts.append(make_donut(80, 80, 40, mid, max(mid, 1) if total_done == 0 else total_done, "#22c55e", 10))
    svg_parts.append(make_donut(80, 80, 22, sen, max(sen, 1) if total_done == 0 else total_done, "#f59e0b", 8))

    center_label = str(total_done) if total_done > 0 else "0"

    chart_svg = f"""
    <svg width="140" height="140" viewBox="0 0 140 140" xmlns="http://www.w3.org/2000/svg">
        {''.join(svg_parts)}
        <text x="80" y="76" text-anchor="middle" font-size="22" font-weight="600" fill="#0f172a" font-family="DM Mono,monospace">{center_label}</text>
        <text x="80" y="94" text-anchor="middle" font-size="10" fill="#94a3b8" font-family="DM Sans,sans-serif">QUESTIONS</text>
    </svg>"""

    st.markdown(f"""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;padding:1rem;text-align:center">
        <div style="font-size:0.72rem;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.75rem">Questions by Difficulty</div>
        {chart_svg}
        <div style="display:flex;flex-direction:column;gap:6px;margin-top:0.75rem;text-align:left">
            <div style="display:flex;align-items:center;gap:8px;font-size:0.78rem">
                <span style="width:10px;height:10px;border-radius:50%;background:#6366f1;flex-shrink:0"></span>
                <span style="color:#64748b">Beginner</span>
                <span style="margin-left:auto;font-weight:600;color:#0f172a;font-family:DM Mono,monospace">{beg}</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;font-size:0.78rem">
                <span style="width:10px;height:10px;border-radius:50%;background:#22c55e;flex-shrink:0"></span>
                <span style="color:#64748b">Intermediate</span>
                <span style="margin-left:auto;font-weight:600;color:#0f172a;font-family:DM Mono,monospace">{mid}</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;font-size:0.78rem">
                <span style="width:10px;height:10px;border-radius:50%;background:#f59e0b;flex-shrink:0"></span>
                <span style="color:#64748b">Senior</span>
                <span style="margin-left:auto;font-weight:600;color:#0f172a;font-family:DM Mono,monospace">{sen}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with main_col:
    # ── System prompt ─────────────────────────────────────────────────────────
    def build_system_prompt(mode="free"):
        topic = st.session_state.applied_topic
        diff = st.session_state.applied_diff
        diff_guide = {
            "Beginner": "Focus on fundamental concepts, definitions, and basic examples.",
            "Intermediate": "Focus on practical application, trade-offs, and real scenarios.",
            "Senior": "Focus on system design, architectural decisions, trade-offs, and depth."
        }[diff]
        feedback_format = """When evaluating an answer, ALWAYS use EXACTLY this structure:

SCORE: X/10

WHAT YOU GOT RIGHT:
- specific point
- specific point

WHAT WAS MISSING:
- specific point
- specific point

MODEL ANSWER:
Your model answer here."""
        if mode == "session":
            mode_instr = f"You are running a structured 5-question interview. Ask the given question, wait for the answer, then give structured feedback.\n{feedback_format}"
        else:
            mode_instr = f"Free chat mode. When asked for a question, ask one and wait. When user answers, give feedback.\n{feedback_format}"
        return f"You are DS Buddy, a professional interview coach.\nTopic: {topic} | Difficulty: {diff} — {diff_guide}\n{mode_instr}\nTone: Professional, specific, encouraging."

    # ── Format response ───────────────────────────────────────────────────────
    def format_response(text):
        lines = text.split('\n')
        html_out = ""
        current_block = None
        section_map = {
            "SCORE:": "score", "WHAT YOU GOT RIGHT:": "good",
            "WHAT WAS MISSING:": "missing", "MODEL ANSWER:": "model",
        }
        icons = {"score": "🎯", "good": "✅", "missing": "🔶", "model": "💡"}
        labels = {"score": "Score", "good": "What you got right", "missing": "What was missing", "model": "Model answer"}

        def close_block():
            return "</div></div>" if current_block else ""

        for line in lines:
            stripped = line.strip()
            matched = False
            for key, block_type in section_map.items():
                if stripped.upper().startswith(key):
                    html_out += close_block()
                    current_block = block_type
                    inline = stripped[len(key):].strip()
                    if block_type == "score":
                        score_val = inline if inline else "?"
                        try:
                            score_num = int(re.search(r'\d+', score_val).group())
                            bar_w = score_num * 10
                            bar_c = "#22c55e" if score_num >= 7 else "#f59e0b" if score_num >= 5 else "#ef4444"
                        except:
                            bar_w, bar_c = 0, "#94a3b8"
                        html_out += f"""<div class="fb-block score">
                            <div class="fb-header score">{icons['score']} {labels['score']}</div>
                            <div class="fb-score-value">{score_val}/10</div>
                            <div class="score-bar-bg"><div class="score-bar-fill" style="width:{bar_w}%;background:{bar_c}"></div></div>
                        <div>"""
                    else:
                        html_out += f"""<div class="fb-block {block_type}">
                            <div class="fb-header {block_type}">{icons[block_type]} {labels[block_type]}</div>
                        <div>"""
                        if inline:
                            if block_type == "model":
                                html_out += f'<span class="fb-model-text">{inline}</span>'
                            else:
                                dot = "fb-dot-good" if block_type == "good" else "fb-dot-miss"
                                html_out += f'<div class="fb-point"><span class="{dot}">●</span><span class="fb-point-text">{inline}</span></div>'
                    matched = True
                    break
            if not matched:
                if stripped.startswith("- ") or stripped.startswith("• "):
                    content = stripped[2:]
                    if current_block == "good":
                        html_out += f'<div class="fb-point"><span class="fb-dot-good">●</span><span class="fb-point-text">{content}</span></div>'
                    elif current_block == "missing":
                        html_out += f'<div class="fb-point"><span class="fb-dot-miss">●</span><span class="fb-point-text">{content}</span></div>'
                    elif current_block == "model":
                        html_out += f'<span class="fb-model-text">• {content}<br></span>'
                    else:
                        html_out += f'<span style="display:block;margin:3px 0 3px 10px">• {content}</span>'
                elif stripped == "":
                    html_out += '<br>'
                else:
                    if current_block == "model":
                        html_out += f'<span class="fb-model-text">{stripped}<br></span>'
                    else:
                        html_out += f'<span style="display:block;margin:2px 0">{stripped}</span>'
        html_out += close_block()
        return html_out

    # ── Chat display ──────────────────────────────────────────────────────────
    chat_html = '<div class="chat-container">'
    if not st.session_state.messages:
        name_part = f", {st.session_state.username}!" if st.session_state.logged_in else "!"
        chat_html += f"""<div class="msg-assistant"><div>
            <div class="bubble-label">DS Buddy</div>
            <div class="bubble-assistant">
                👋 Hi{name_part} I'm <b>DS Buddy</b>. Here's how to get started:<br><br>
                1. Select your <b>Topic</b> and <b>Difficulty</b> above and click <b>Apply ✓</b><br>
                2. Use the buttons below to start practicing<br><br>
                <b>Free Chat</b> — ask anything or request a question anytime<br>
                <b>5-Question Session</b> — structured interview with scoring and a final summary
            </div>
        </div></div>"""
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                content = msg["content"].replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
                chat_html += f"""<div class="msg-user"><div>
                    <div class="bubble-label" style="text-align:right">You</div>
                    <div class="bubble-user">{content}</div>
                </div></div>"""
            else:
                formatted = format_response(msg["content"])
                chat_html += f"""<div class="msg-assistant"><div>
                    <div class="bubble-label">DS Buddy</div>
                    <div class="bubble-assistant">{formatted}</div>
                </div></div>"""
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # ── Answer text area ──────────────────────────────────────────────────────
    user_input = st.text_area(
        "answer", value="",
        placeholder="Type your answer here... Be as detailed as you can.",
        label_visibility="collapsed", height=180,
        key=f"answer_box_{st.session_state.input_key}"
    )

    # ── Buttons ───────────────────────────────────────────────────────────────
    bc1, bc2, bc3, bc4, bc5 = st.columns([2, 2, 2, 2, 2])
    with bc1: send = st.button("Send answer →", use_container_width=True)
    with bc2: q1 = st.button("Ask me a question", use_container_width=True)
    with bc3: q2 = st.button("Start 5Q Session", use_container_width=True)
    with bc4: q3 = st.button("Explain simpler", use_container_width=True)
    with bc5: q4 = st.button("Give me a hint", use_container_width=True)

    # ── Message handler ───────────────────────────────────────────────────────
    def send_message(text, mode="free"):
        if not text.strip():
            return
        st.session_state.messages.append({"role": "user", "content": text})
        with st.spinner("DS Buddy is thinking..."):
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1500,
                system=build_system_prompt(mode),
                messages=st.session_state.messages
            )
            reply = response.content[0].text
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.total_interactions += 1
        st.session_state.input_key += 1

        score_matches = re.findall(r'SCORE:\s*(\d+)\s*/\s*10', reply, re.IGNORECASE)
        if score_matches:
            score = int(score_matches[0])
            if 0 <= score <= 10:
                st.session_state.score_sum += score
                st.session_state.score_count += 1
                st.session_state.session_results.append(score)
                diff = st.session_state.applied_diff
                st.session_state.diff_counts[diff] += 1
                if st.session_state.session_active:
                    st.session_state.session_qs_done += 1
        st.rerun()

    # ── Handle inputs ─────────────────────────────────────────────────────────
    if send and user_input.strip():
        mode = "session" if st.session_state.session_active else "free"
        send_message(user_input, mode)
    elif q1:
        pool = QUESTION_BANK[st.session_state.applied_topic][st.session_state.applied_diff]
        q = random.choice(pool)
        send_message(f"Please ask me this interview question and wait for my answer: {q}", "free")
    elif q2:
        pool = QUESTION_BANK[st.session_state.applied_topic][st.session_state.applied_diff]
        questions = random.sample(pool, min(5, len(pool)))
        st.session_state.session_active = True
        st.session_state.session_qs_done = 0
        st.session_state.session_results = []
        st.session_state.score_sum = 0
        st.session_state.score_count = 0
        q_list = "\n".join([f"Q{i+1}: {q}" for i, q in enumerate(questions)])
        send_message(
            f"Start a 5-question {st.session_state.applied_diff} {st.session_state.applied_topic} session.\n"
            f"Use these questions:\n{q_list}\nAsk Question 1 of 5 now.",
            "session"
        )
    elif q3:
        send_message("Can you explain that in simpler terms with a concrete example?", "free")
    elif q4:
        send_message("Give me a hint without revealing the full answer.", "free")

    # ── Session summary ───────────────────────────────────────────────────────
    if st.session_state.session_active and st.session_state.session_qs_done >= 5:
        results = st.session_state.session_results[-5:]
        avg = round(sum(results) / len(results), 1)
        grade = "Strong Performance 🎯" if avg >= 7 else "Good Progress 📈" if avg >= 5 else "Keep Practicing 💪"
        color = "#22c55e" if avg >= 7 else "#f59e0b" if avg >= 5 else "#ef4444"
        bar_width = int(avg * 10)
        st.markdown(f"""
        <div class="summary-card">
            <h3>🏁 Session Complete — {st.session_state.applied_topic} · {st.session_state.applied_diff}</h3>
            <div class="summary-grid">
                <div class="summary-stat">
                    <div class="summary-num">{avg}/10</div>
                    <div class="summary-lbl">Average Score</div>
                    <div style="background:#1e293b;border-radius:99px;height:6px;margin-top:8px;overflow:hidden">
                        <div style="width:{bar_width}%;height:6px;background:{color};border-radius:99px"></div>
                    </div>
                </div>
                <div class="summary-stat">
                    <div style="font-size:1.1rem;font-weight:600;color:{color};padding-top:0.4rem">{grade}</div>
                    <div class="summary-lbl" style="margin-top:6px">Rating</div>
                </div>
                <div class="summary-stat">
                    <div style="display:flex;justify-content:center;gap:8px;flex-wrap:wrap;padding-top:0.3rem">
                        {"".join([f'<span style="background:#1e3a5f;color:#93c5fd;border-radius:6px;padding:4px 10px;font-family:DM Mono,monospace;font-size:0.9rem">{s}</span>' for s in results])}
                    </div>
                    <div class="summary-lbl" style="margin-top:8px">Scores per question</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Reset ─────────────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
    if st.button("🔄 Reset conversation"):
        st.session_state.messages = []
        st.session_state.total_interactions = 0
        st.session_state.score_sum = 0
        st.session_state.score_count = 0
        st.session_state.session_active = False
        st.session_state.session_qs_done = 0
        st.session_state.session_results = []
        st.session_state.input_key += 1
        st.rerun()

# ── Copyright footer ──────────────────────────────────────────────────────────
st.markdown("""
<div class="ds-footer">
    © 2026 DS Buddy. All rights reserved. &nbsp;|&nbsp;
    Built for data professionals preparing for their next role.
</div>
""", unsafe_allow_html=True)
