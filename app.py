import streamlit as st
import anthropic

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DS Buddy — Interview Prep",
    page_icon="📊",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 900px; }

/* ── Header ── */
.ds-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid #334155;
    position: relative;
    overflow: hidden;
}
.ds-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.ds-header h1 {
    color: #f8fafc;
    font-size: 1.8rem;
    font-weight: 600;
    margin: 0 0 0.25rem 0;
    letter-spacing: -0.02em;
}
.ds-header p {
    color: #94a3b8;
    font-size: 0.9rem;
    margin: 0;
}
.ds-header .accent { color: #818cf8; }

/* ── Selector pills ── */
.selector-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 0.5rem;
}
.selector-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}

/* ── Stats bar ── */
.stats-bar {
    display: flex;
    gap: 12px;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.stat-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.75rem 1.25rem;
    flex: 1;
    min-width: 120px;
    text-align: center;
}
.stat-number {
    font-size: 1.5rem;
    font-weight: 600;
    color: #0f172a;
    font-family: 'DM Mono', monospace;
    line-height: 1;
}
.stat-label {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 4px;
}
.stat-card.highlight { background: #eef2ff; border-color: #c7d2fe; }
.stat-card.highlight .stat-number { color: #4f46e5; }

/* ── Mode tabs ── */
.mode-container {
    background: #f1f5f9;
    border-radius: 12px;
    padding: 4px;
    display: inline-flex;
    gap: 2px;
    margin-bottom: 1.5rem;
}

/* ── Chat bubbles ── */
.chat-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    min-height: 300px;
    max-height: 500px;
    overflow-y: auto;
}
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
}
.msg-assistant {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 1rem;
}
.bubble-user {
    background: #4f46e5;
    color: white;
    padding: 0.75rem 1rem;
    border-radius: 16px 16px 4px 16px;
    max-width: 75%;
    font-size: 0.9rem;
    line-height: 1.5;
}
.bubble-assistant {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    color: #1e293b;
    padding: 0.75rem 1rem;
    border-radius: 16px 16px 16px 4px;
    max-width: 75%;
    font-size: 0.9rem;
    line-height: 1.5;
}
.bubble-label {
    font-size: 0.7rem;
    color: #94a3b8;
    margin-bottom: 4px;
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── Score card ── */
.score-card {
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-top: 0.75rem;
    border: 1px solid;
}
.score-card.strong { background: #f0fdf4; border-color: #86efac; }
.score-card.partial { background: #fffbeb; border-color: #fcd34d; }
.score-card.weak    { background: #fef2f2; border-color: #fca5a5; }
.score-title { font-weight: 600; font-size: 0.9rem; margin-bottom: 0.4rem; }
.score-card.strong .score-title { color: #166534; }
.score-card.partial .score-title { color: #92400e; }
.score-card.weak    .score-title { color: #991b1b; }
.score-body { font-size: 0.85rem; line-height: 1.6; }
.score-card.strong .score-body { color: #14532d; }
.score-card.partial .score-body { color: #78350f; }
.score-card.weak    .score-body { color: #7f1d1d; }

/* ── Topic badge ── */
.topic-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.badge-ds  { background: #ede9fe; color: #5b21b6; }
.badge-da  { background: #dbeafe; color: #1e40af; }
.badge-de  { background: #dcfce7; color: #166534; }
.badge-beg { background: #f0f9ff; color: #0369a1; }
.badge-mid { background: #fef9c3; color: #854d0e; }
.badge-sen { background: #fce7f3; color: #9d174d; }

/* ── Session summary ── */
.summary-card {
    background: #0f172a;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    color: white;
    margin-top: 1rem;
}
.summary-card h3 { color: #e2e8f0; font-size: 1.1rem; margin-bottom: 1rem; }
.summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.summary-stat { text-align: center; }
.summary-num { font-size: 2rem; font-weight: 600; font-family: 'DM Mono', monospace; color: #818cf8; }
.summary-lbl { font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; }

/* ── Streamlit widget overrides ── */
div[data-testid="stTextInput"] input {
    border-radius: 10px;
    border: 1.5px solid #e2e8f0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    padding: 0.6rem 1rem;
}
div[data-testid="stTextInput"] input:focus { border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }

div.stButton > button {
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.88rem;
    padding: 0.5rem 1.2rem;
    transition: all 0.15s;
}
div.stButton > button:first-child {
    background: #4f46e5;
    color: white;
    border: none;
}
div.stButton > button:first-child:hover { background: #4338ca; }

div[data-testid="stSelectbox"] > div > div {
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
}

.stRadio > div { gap: 8px; }
.stRadio label { 
    background: #f8fafc;
    border: 1.5px solid #e2e8f0;
    border-radius: 8px;
    padding: 6px 14px !important;
    font-size: 0.88rem !important;
    cursor: pointer;
    transition: all 0.15s;
}
</style>
""", unsafe_allow_html=True)

# ── Anthropic client ──────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# ── Session state init ────────────────────────────────────────────────────────
defaults = {
    "messages": [],
    "mode": "Free Chat",
    "topic": "Data Science",
    "difficulty": "Beginner",
    "session_questions": 0,
    "session_score": 0,
    "session_active": False,
    "session_q_count": 0,
    "awaiting_answer": False,
    "current_question": "",
    "session_results": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ds-header">
    <h1>📊 DS Buddy <span class="accent">— Interview Prep</span></h1>
    <p>Practice Data Science, Analytics & Engineering interviews with AI-powered feedback</p>
</div>
""", unsafe_allow_html=True)

# ── Controls row ──────────────────────────────────────────────────────────────
col_topic, col_diff, col_mode = st.columns([2, 2, 2])

with col_topic:
    st.markdown('<div class="selector-label">Topic</div>', unsafe_allow_html=True)
    topic = st.selectbox(
        "topic", 
        ["Data Science", "Data Analytics", "Data Engineering"],
        label_visibility="collapsed",
        key="topic_select"
    )
    st.session_state.topic = topic

with col_diff:
    st.markdown('<div class="selector-label">Difficulty</div>', unsafe_allow_html=True)
    difficulty = st.selectbox(
        "difficulty",
        ["Beginner", "Intermediate", "Senior"],
        label_visibility="collapsed",
        key="diff_select"
    )
    st.session_state.difficulty = difficulty

with col_mode:
    st.markdown('<div class="selector-label">Mode</div>', unsafe_allow_html=True)
    mode = st.selectbox(
        "mode",
        ["Free Chat", "Structured Session (5 Questions)"],
        label_visibility="collapsed",
        key="mode_select"
    )
    st.session_state.mode = mode

# ── Stats bar ─────────────────────────────────────────────────────────────────
topic_badges = {"Data Science": "badge-ds", "Data Analytics": "badge-da", "Data Engineering": "badge-de"}
diff_badges  = {"Beginner": "badge-beg", "Intermediate": "badge-mid", "Senior": "badge-sen"}

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number">{st.session_state.session_questions}</div>
        <div class="stat-label">Questions Asked</div>
    </div>""", unsafe_allow_html=True)
with s2:
    score_pct = round(st.session_state.session_score / max(st.session_state.session_questions, 1) * 100)
    st.markdown(f"""<div class="stat-card highlight">
        <div class="stat-number">{score_pct}%</div>
        <div class="stat-label">Avg Score</div>
    </div>""", unsafe_allow_html=True)
with s3:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number">{len(st.session_state.messages) // 2}</div>
        <div class="stat-label">Exchanges</div>
    </div>""", unsafe_allow_html=True)
with s4:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number">{st.session_state.session_q_count if st.session_state.mode == "Structured Session (5 Questions)" else "-"}</div>
        <div class="stat-label">Session Q's Left</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

# ── System prompt builder ─────────────────────────────────────────────────────
def build_system_prompt():
    mode_instructions = ""
    if st.session_state.mode == "Free Chat":
        mode_instructions = """You are in FREE CHAT mode. The user can ask anything — questions, 
        concepts, clarifications. When they ask for an interview question, ask one and wait for their answer.
        When they answer, give structured feedback with: 
        1. A score out of 10
        2. What they got right (specific points)
        3. What was missing or could be improved
        4. A model answer for reference"""
    else:
        mode_instructions = """You are in STRUCTURED SESSION mode running a 5-question interview session.
        Ask one question at a time. After each answer give:
        1. Score out of 10
        2. What they got right
        3. What was missing  
        4. Brief model answer
        Then move to the next question. After 5 questions give a final session summary with overall score."""

    return f"""You are DS Buddy, a professional and encouraging interview coach for data roles.

Topic focus: {st.session_state.topic}
Difficulty level: {st.session_state.difficulty}
Mode: {st.session_state.mode}

{mode_instructions}

Tone: Professional, encouraging, specific. Never vague. Always give actionable feedback.
For {st.session_state.difficulty} level: {"Focus on fundamentals and core concepts." if st.session_state.difficulty == "Beginner" else "Focus on practical application and problem solving." if st.session_state.difficulty == "Intermediate" else "Focus on system design, trade-offs, leadership, and depth."}"""

# ── Chat display ──────────────────────────────────────────────────────────────
chat_html = '<div class="chat-container" id="chat-box">'
if not st.session_state.messages:
    chat_html += """<div class="msg-assistant">
        <div>
            <div class="bubble-label">DS Buddy</div>
            <div class="bubble-assistant">👋 Hi! I'm DS Buddy. Select your topic and difficulty above, then:<br><br>
            • <b>Free Chat</b> — Ask me anything or say "give me a question"<br>
            • <b>Structured Session</b> — I'll run a 5-question interview and score you at the end<br><br>
            Ready when you are!</div>
        </div>
    </div>"""
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f"""<div class="msg-user">
                <div>
                    <div class="bubble-label" style="text-align:right">You</div>
                    <div class="bubble-user">{msg["content"]}</div>
                </div>
            </div>"""
        else:
            content = msg["content"].replace("\n", "<br>")
            chat_html += f"""<div class="msg-assistant">
                <div>
                    <div class="bubble-label">DS Buddy</div>
                    <div class="bubble-assistant">{content}</div>
                </div>
            </div>"""
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# ── Input area ────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])

with col_input:
    user_input = st.text_input(
        "message",
        placeholder="Type your answer or ask a question...",
        label_visibility="collapsed",
        key="user_input"
    )

with col_btn:
    send = st.button("Send →", use_container_width=True)

# ── Quick action buttons ──────────────────────────────────────────────────────
qc1, qc2, qc3, qc4 = st.columns(4)
with qc1:
    q1 = st.button("Ask me a question", use_container_width=True)
with qc2:
    q2 = st.button("Start 5Q Session", use_container_width=True)
with qc3:
    q3 = st.button("Explain that simpler", use_container_width=True)
with qc4:
    q4 = st.button("Give me a hint", use_container_width=True)

# ── Message handler ───────────────────────────────────────────────────────────
def send_message(text):
    if not text.strip():
        return

    st.session_state.messages.append({"role": "user", "content": text})

    with st.spinner("DS Buddy is thinking..."):
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=build_system_prompt(),
            messages=st.session_state.messages
        )
        reply = response.content[0].text

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.session_questions += 1

    # Auto score detection — look for "score" or "/10" in reply
    reply_lower = reply.lower()
    if "/10" in reply_lower or "score:" in reply_lower:
        import re
        numbers = re.findall(r'(\d+)\s*/\s*10', reply)
        if numbers:
            score = int(numbers[0])
            st.session_state.session_score += score
            st.session_state.session_results.append(score)

    st.rerun()

# ── Handle inputs ─────────────────────────────────────────────────────────────
if send and user_input:
    send_message(user_input)
elif q1:
    send_message(f"Ask me a {st.session_state.difficulty.lower()} level {st.session_state.topic} interview question")
elif q2:
    st.session_state.session_q_count = 5
    st.session_state.session_active = True
    send_message(f"Start a structured 5-question {st.session_state.difficulty.lower()} {st.session_state.topic} interview session. Ask the first question now.")
elif q3:
    send_message("Can you explain that in simpler terms?")
elif q4:
    send_message("Give me a hint without revealing the full answer")

# ── Session summary (shown after 5Q session) ──────────────────────────────────
if len(st.session_state.session_results) >= 5:
    avg = round(sum(st.session_state.session_results[-5:]) / 5, 1)
    if avg >= 7:
        grade, color = "Strong Performance", "#22c55e"
    elif avg >= 5:
        grade, color = "Good Progress", "#f59e0b"
    else:
        grade, color = "Needs Practice", "#ef4444"

    st.markdown(f"""
    <div class="summary-card">
        <h3>Session Summary</h3>
        <div class="summary-grid">
            <div class="summary-stat">
                <div class="summary-num">{avg}/10</div>
                <div class="summary-lbl">Avg Score</div>
            </div>
            <div class="summary-stat">
                <div class="summary-num" style="color:{color}">{grade}</div>
                <div class="summary-lbl">Rating</div>
            </div>
            <div class="summary-stat">
                <div class="summary-num">{len(st.session_state.session_results)}</div>
                <div class="summary-lbl">Questions Done</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Reset button ──────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
if st.button("🔄 Reset conversation"):
    for k in ["messages", "session_questions", "session_score", "session_results", "session_q_count", "session_active", "awaiting_answer"]:
        st.session_state[k] = [] if k in ["messages", "session_results"] else 0 if k in ["session_questions", "session_score", "session_q_count"] else False
    st.rerun()