import streamlit as st
import anthropic
import re

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

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }

/* Constrained centered layout */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1000px !important; /* reduce this to ~900 for narrower layout */
    margin-left: auto !important;
    margin-right: auto !important;
}

/* ── Header ── */
.ds-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 16px;
    padding: 1.75rem 2.5rem;
    margin-bottom: 1.25rem;
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
.ds-header h1 { color: #f8fafc; font-size: 1.8rem; font-weight: 600; margin: 0 0 0.25rem 0; letter-spacing: -0.02em; }
.ds-header p { color: #94a3b8; font-size: 0.9rem; margin: 0; }
.ds-header .accent { color: #818cf8; }

/* ── Selector label ── */
.selector-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}

/* ── Stats bar ── */
.stat-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    text-align: center;
}
.stat-number { font-size: 1.5rem; font-weight: 600; color: #0f172a; font-family: 'DM Mono', monospace; line-height: 1; }
.stat-label { font-size: 0.72rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px; }
.stat-card.highlight { background: #eef2ff; border-color: #c7d2fe; }
.stat-card.highlight .stat-number { color: #4f46e5; }

/* ── Chat container ── */
.chat-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    min-height: 420px;
    max-height: 560px;
    overflow-y: auto;
}
.msg-user { display: flex; justify-content: flex-end; margin-bottom: 1.25rem; }
.msg-assistant { display: flex; justify-content: flex-start; margin-bottom: 1.25rem; }
.bubble-user {
    background: #4f46e5;
    color: white;
    padding: 0.85rem 1.1rem;
    border-radius: 16px 16px 4px 16px;
    max-width: 70%;
    font-size: 0.9rem;
    line-height: 1.6;
    white-space: pre-wrap;
}
.bubble-assistant {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    color: #1e293b;
    padding: 1rem 1.25rem;
    border-radius: 16px 16px 16px 4px;
    max-width: 78%;
    font-size: 0.9rem;
    line-height: 1.7;
}
.bubble-label { font-size: 0.7rem; color: #94a3b8; margin-bottom: 4px; font-weight: 500; letter-spacing: 0.04em; text-transform: uppercase; }

/* ── Feedback sections inside bubble ── */
.fb-section { margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #e2e8f0; }
.fb-tag {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 6px;
}
.fb-score   { background: #eef2ff; color: #4338ca; }
.fb-good    { background: #f0fdf4; color: #166534; }
.fb-missing { background: #fef2f2; color: #991b1b; }
.fb-model   { background: #f0f9ff; color: #0369a1; }

/* ── Streamlit overrides ── */
div.stButton > button {
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.88rem;
    padding: 0.5rem 1.2rem;
    transition: all 0.15s;
    width: 100%;
}
div.stButton > button:first-child { background: #4f46e5; color: white; border: none; }
div.stButton > button:first-child:hover { background: #4338ca; }

div[data-testid="stSelectbox"] > div > div { border-radius: 10px; font-family: 'DM Sans', sans-serif; }

/* Textarea bigger */
div[data-testid="stTextArea"] textarea {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.92rem;
    border-radius: 12px;
    border: 1.5px solid #e2e8f0;
    line-height: 1.6;
    padding: 0.85rem 1rem;
}
div[data-testid="stTextArea"] textarea:focus { border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }

/* Summary card */
.summary-card { background: #0f172a; border-radius: 16px; padding: 1.5rem 2rem; color: white; margin-top: 1rem; }
.summary-card h3 { color: #e2e8f0; font-size: 1.1rem; margin-bottom: 1rem; }
.summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.summary-stat { text-align: center; }
.summary-num { font-size: 2rem; font-weight: 600; font-family: 'DM Mono', monospace; color: #818cf8; }
.summary-lbl { font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; }
</style>
""", unsafe_allow_html=True)

# ── Anthropic client ──────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# ── Session state init ────────────────────────────────────────────────────────
defaults = {
    "messages": [],
    "applied_topic": "Data Science",
    "applied_diff": "Beginner",
    "applied_mode": "Free Chat",
    "total_questions": 0,
    "score_sum": 0,
    "score_count": 0,
    "session_active": False,
    "session_qs_done": 0,
    "session_total": 5,
    "session_results": [],
    "input_key": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ds-header">
    <h1>📊 DS Buddy <span class="accent">— Interview Prep</span></h1>
    <p>Practice Data Science, Analytics & Engineering interviews with AI-powered feedback and scoring</p>
</div>
""", unsafe_allow_html=True)

# ── Controls row with Apply button ───────────────────────────────────────────
c1, c2, c3, c4 = st.columns([3, 3, 3, 1.5])

with c1:
    st.markdown('<div class="selector-label">Topic</div>', unsafe_allow_html=True)
    sel_topic = st.selectbox("topic", ["Data Science", "Data Analytics", "Data Engineering"], label_visibility="collapsed")

with c2:
    st.markdown('<div class="selector-label">Difficulty</div>', unsafe_allow_html=True)
    sel_diff = st.selectbox("difficulty", ["Beginner", "Intermediate", "Senior"], label_visibility="collapsed")

with c3:
    st.markdown('<div class="selector-label">Mode</div>', unsafe_allow_html=True)
    sel_mode = st.selectbox("mode", ["Free Chat", "Structured Session (5 Questions)"], label_visibility="collapsed")

with c4:
    st.markdown('<div class="selector-label">&nbsp;</div>', unsafe_allow_html=True)
    apply = st.button("Apply ✓", use_container_width=True)

if apply:
    st.session_state.applied_topic = sel_topic
    st.session_state.applied_diff = sel_diff
    st.session_state.applied_mode = sel_mode
    st.session_state.messages = []
    st.session_state.total_questions = 0
    st.session_state.score_sum = 0
    st.session_state.score_count = 0
    st.session_state.session_active = False
    st.session_state.session_qs_done = 0
    st.session_state.session_results = []
    st.session_state.input_key += 1
    st.rerun()

st.markdown("<div style='margin:0.75rem 0'></div>", unsafe_allow_html=True)

# ── Stats bar ─────────────────────────────────────────────────────────────────
s1, s2, s3, s4 = st.columns(4)

avg_score = round(st.session_state.score_sum / st.session_state.score_count, 1) if st.session_state.score_count > 0 else None
qs_left = (st.session_state.session_total - st.session_state.session_qs_done) if st.session_state.session_active else "-"

with s1:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number">{st.session_state.total_questions}</div>
        <div class="stat-label">Questions Asked</div>
    </div>""", unsafe_allow_html=True)
with s2:
    score_display = f"{avg_score}/10" if avg_score is not None else "-"
    st.markdown(f"""<div class="stat-card highlight">
        <div class="stat-number">{score_display}</div>
        <div class="stat-label">Avg Score</div>
    </div>""", unsafe_allow_html=True)
with s3:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number">{len(st.session_state.messages) // 2}</div>
        <div class="stat-label">Exchanges</div>
    </div>""", unsafe_allow_html=True)
with s4:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number">{qs_left}</div>
        <div class="stat-label">Session Q's Left</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin:0.75rem 0'></div>", unsafe_allow_html=True)

# ── Active settings badges ────────────────────────────────────────────────────
topic_colors = {"Data Science": "#ede9fe|#5b21b6", "Data Analytics": "#dbeafe|#1e40af", "Data Engineering": "#dcfce7|#166534"}
diff_colors  = {"Beginner": "#f0f9ff|#0369a1", "Intermediate": "#fef9c3|#854d0e", "Senior": "#fce7f3|#9d174d"}
mode_colors  = {"Free Chat": "#f1f5f9|#475569", "Structured Session (5 Questions)": "#fef3c7|#92400e"}

def badge(text, colors):
    bg, fg = colors.split("|")
    return f'<span style="background:{bg};color:{fg};padding:3px 12px;border-radius:20px;font-size:0.75rem;font-weight:500;margin-right:6px">{text}</span>'

st.markdown(
    badge(st.session_state.applied_topic, topic_colors[st.session_state.applied_topic]) +
    badge(st.session_state.applied_diff, diff_colors[st.session_state.applied_diff]) +
    badge(st.session_state.applied_mode, mode_colors[st.session_state.applied_mode]),
    unsafe_allow_html=True
)

st.markdown("<div style='margin:0.5rem 0'></div>", unsafe_allow_html=True)

# ── System prompt ─────────────────────────────────────────────────────────────
def build_system_prompt():
    mode = st.session_state.applied_mode
    diff = st.session_state.applied_diff
    topic = st.session_state.applied_topic

    if mode == "Free Chat":
        mode_instr = """MODE: Free Chat
When the user asks for a question, ask one clear interview question and wait.
When they give an answer, structure your response EXACTLY like this — use these exact headers:

SCORE: X/10

WHAT YOU GOT RIGHT:
- specific point 1
- specific point 2

WHAT WAS MISSING:
- specific point 1
- specific point 2

MODEL ANSWER:
Write a clear, concise model answer here.

Always use this exact structure when evaluating an answer."""
    else:
        mode_instr = """MODE: Structured Session (5 questions)
Ask questions one at a time, labelling each as Question N of 5.
After each answer, use EXACTLY this structure:

SCORE: X/10

WHAT YOU GOT RIGHT:
- specific point 1
- specific point 2

WHAT WAS MISSING:
- specific point 1
- specific point 2

MODEL ANSWER:
Write a clear, concise model answer here.

Then ask if they are ready for the next question.
After question 5, give a FINAL SUMMARY with total score."""

    diff_guide = {
        "Beginner": "Focus on fundamental concepts, definitions, and basic examples.",
        "Intermediate": "Focus on practical application, trade-offs, and real scenarios.",
        "Senior": "Focus on system design, architectural decisions, trade-offs, and depth."
    }[diff]

    return f"""You are DS Buddy, a professional and encouraging interview coach.
Topic: {topic}
Difficulty: {diff} — {diff_guide}
{mode_instr}
Tone: Professional, specific, encouraging. Always give concrete and actionable feedback."""

# ── Format assistant response ─────────────────────────────────────────────────
def format_response(text):
    lines = text.split('\n')
    html_out = ""
    in_section = False

    section_map = {
        "SCORE:": ("fb-score", "Score"),
        "WHAT YOU GOT RIGHT:": ("fb-good", "What you got right"),
        "WHAT WAS MISSING:": ("fb-missing", "What was missing"),
        "MODEL ANSWER:": ("fb-model", "Model answer"),
    }

    for line in lines:
        stripped = line.strip()
        matched = False

        for key, (cls, label) in section_map.items():
            if stripped.upper().startswith(key):
                if in_section:
                    html_out += "</div>"
                in_section = True
                inline = stripped[len(key):].strip()
                html_out += f'<div class="fb-section"><span class="fb-tag {cls}">{label}</span>'
                if inline:
                    html_out += f'<br><span style="font-weight:600;display:block;margin-top:4px">{inline}</span>'
                matched = True
                break

        if not matched:
            if stripped.startswith("- ") or stripped.startswith("• "):
                html_out += f'<span style="display:block;margin:3px 0 3px 10px">• {stripped[2:]}</span>'
            elif stripped == "":
                html_out += '<br>'
            else:
                html_out += f'<span style="display:block;margin:2px 0">{stripped}</span>'

    if in_section:
        html_out += "</div>"

    return html_out

# ── Chat display ──────────────────────────────────────────────────────────────
chat_html = '<div class="chat-container">'
if not st.session_state.messages:
    chat_html += """<div class="msg-assistant"><div>
        <div class="bubble-label">DS Buddy</div>
        <div class="bubble-assistant">
            👋 Hi! I'm <b>DS Buddy</b>. Here's how to get started:<br><br>
            1. Select your <b>Topic</b>, <b>Difficulty</b>, and <b>Mode</b> above<br>
            2. Click <b>Apply ✓</b> to confirm your settings<br>
            3. Use the quick buttons below to jump in<br><br>
            <b>Free Chat</b> — ask anything or request a question anytime<br>
            <b>Structured Session</b> — 5 questions with scoring and a final summary
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

# ── Answer input — key changes after each send to clear the box ───────────────
user_input = st.text_area(
    "Your answer",
    value="",
    placeholder="Type your answer here... Be as detailed as you can.",
    label_visibility="collapsed",
    height=180,
    key=f"answer_box_{st.session_state.input_key}"
)

# ── Buttons ───────────────────────────────────────────────────────────────────
bc1, bc2, bc3, bc4, bc5 = st.columns([2, 2, 2, 2, 2])
with bc1:
    send = st.button("Send answer →", use_container_width=True)
with bc2:
    q1 = st.button("Ask me a question", use_container_width=True)
with bc3:
    q2 = st.button("Start 5Q Session", use_container_width=True)
with bc4:
    q3 = st.button("Explain simpler", use_container_width=True)
with bc5:
    q4 = st.button("Give me a hint", use_container_width=True)

# ── Message handler ───────────────────────────────────────────────────────────
def send_message(text):
    if not text.strip():
        return

    st.session_state.messages.append({"role": "user", "content": text})

    with st.spinner("DS Buddy is thinking..."):
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            system=build_system_prompt(),
            messages=st.session_state.messages
        )
        reply = response.content[0].text

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.total_questions += 1
    st.session_state.input_key += 1  # clears the text area

    # ── Score extraction — only accept values 0-10 ──
    score_matches = re.findall(r'SCORE:\s*(\d+)\s*/\s*10', reply, re.IGNORECASE)
    if score_matches:
        score = int(score_matches[0])
        if 0 <= score <= 10:
            st.session_state.score_sum += score
            st.session_state.score_count += 1
            st.session_state.session_results.append(score)
            if st.session_state.session_active:
                st.session_state.session_qs_done += 1

    st.rerun()

# ── Handle inputs ─────────────────────────────────────────────────────────────
if send and user_input.strip():
    send_message(user_input)
elif q1:
    send_message(f"Ask me a {st.session_state.applied_diff.lower()} level {st.session_state.applied_topic} interview question")
elif q2:
    st.session_state.session_active = True
    st.session_state.session_qs_done = 0
    st.session_state.session_results = []
    st.session_state.score_sum = 0
    st.session_state.score_count = 0
    send_message(f"Start a structured 5-question {st.session_state.applied_diff.lower()} {st.session_state.applied_topic} interview session. Ask Question 1 of 5 now.")
elif q3:
    send_message("Can you explain that in simpler terms with a concrete example?")
elif q4:
    send_message("Give me a hint without revealing the full answer")

# ── Session summary ───────────────────────────────────────────────────────────
if st.session_state.session_active and st.session_state.session_qs_done >= 5:
    results = st.session_state.session_results[-5:]
    avg = round(sum(results) / len(results), 1)
    grade = "Strong Performance 🎯" if avg >= 7 else "Good Progress 📈" if avg >= 5 else "Keep Practicing 💪"
    color = "#22c55e" if avg >= 7 else "#f59e0b" if avg >= 5 else "#ef4444"

    st.markdown(f"""
    <div class="summary-card">
        <h3>🏁 Session Complete</h3>
        <div class="summary-grid">
            <div class="summary-stat">
                <div class="summary-num">{avg}/10</div>
                <div class="summary-lbl">Average Score</div>
            </div>
            <div class="summary-stat">
                <div class="summary-num" style="color:{color};font-size:1.1rem;padding-top:0.5rem">{grade}</div>
                <div class="summary-lbl">Rating</div>
            </div>
            <div class="summary-stat">
                <div class="summary-num" style="font-size:1rem;padding-top:0.5rem">{" · ".join([str(s) for s in results])}</div>
                <div class="summary-lbl">Scores per question</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Reset ─────────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
if st.button("🔄 Reset conversation"):
    st.session_state.messages = []
    st.session_state.total_questions = 0
    st.session_state.score_sum = 0
    st.session_state.score_count = 0
    st.session_state.session_active = False
    st.session_state.session_qs_done = 0
    st.session_state.session_results = []
    st.session_state.input_key += 1
    st.rerun()