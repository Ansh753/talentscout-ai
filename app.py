# app.py - FINAL FIXED VERSION
import streamlit as st
import requests
import json
from datetime import datetime

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="TalentScout AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS - FIXED VERSION ==========
st.markdown("""
<style>
    /* Main container - Black background */
    .stApp {
        background: #0a0a0f;
        color: white;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Elegant header with gradient */
    .main-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem 0;
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
        border-bottom: 1px solid rgba(99, 102, 241, 0.2);
        margin-bottom: 1.5rem;
    }
    
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea, #764ba2, #6b46c1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    
    .tagline {
        color: #a5b4fc;
        font-size: 1rem;
        font-weight: 400;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 850px;
        margin: 0 auto;
        padding: 0 1.5rem;
        min-height: 60vh;
    }
    
    /* Message bubbles */
    .assistant-msg {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
        padding: 1.3rem 1.8rem;
        border-radius: 20px 20px 20px 8px;
        margin: 1rem 0;
        border-left: 4px solid #6366f1;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.15);
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .user-msg {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        padding: 1.3rem 1.8rem;
        border-radius: 20px 20px 8px 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
        animation: slideInRight 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Progress indicator */
    .progress-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1.5rem;
        margin: 2rem 0;
        padding: 1.2rem;
        background: rgba(15, 23, 42, 0.7);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .progress-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }
    
    .step-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: rgba(99, 102, 241, 0.2);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .step-dot.active {
        background: #6366f1;
        box-shadow: 0 0 15px #6366f1;
        transform: scale(1.2);
    }
    
    .step-label {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .step-label.active {
        color: #a5b4fc;
        font-weight: 600;
    }
    
    /* Input area */
    .stChatInput > div > div {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 0.8rem;
        margin-top: 1.5rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    /* Info cards */
    .info-card {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 14px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-left: 3px solid #8b5cf6;
        transition: all 0.3s ease;
    }
    
    .info-icon {
        display: inline-block;
        width: 24px;
        height: 24px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 6px;
        text-align: center;
        line-height: 24px;
        margin-right: 10px;
        font-size: 0.8rem;
    }
    
    .info-label {
        color: #cbd5e1;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
    }
    
    .info-value {
        color: white;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Question item styling */
    .question-item {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-left: 3px solid #6366f1;
    }
    
    .question-number {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        width: 26px;
        height: 26px;
        border-radius: 8px;
        text-align: center;
        line-height: 26px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 12px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }
    
    /* Status badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(34, 197, 94, 0.1);
        color: #4ade80;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4ade80;
    }
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown("""
<div class="main-header">
    <div class="main-title">TalentScout</div>
    <div class="tagline">AI-Powered Screening</div>
</div>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.candidate = {
        "name": "", "email": "", "phone": "",
        "experience": "", "role": "", "location": "", 
        "tech": []
    }

# ========== PROGRESS INDICATOR ==========
steps = [
    {"label": "NAME", "icon": ""},
    {"label": "EMAIL", "icon": ""},
    {"label": "PHONE", "icon": ""},
    {"label": "EXP", "icon": ""},
    {"label": "ROLE", "icon": ""},
    {"label": "LOCATION", "icon": ""},
    {"label": "TECH", "icon": ""}
]

collected = sum(1 for v in st.session_state.candidate.values() if (v if isinstance(v, list) else bool(v)))

st.markdown('<div class="progress-container">', unsafe_allow_html=True)
for i, step in enumerate(steps):
    is_active = i == collected
    is_completed = i < collected
    
    st.markdown(f"""
    <div class="progress-step">
        <div class="step-dot {"active" if is_active else ""}"></div>
        <div class="step-label {"active" if is_active or is_completed else ""}">
            {step['icon']} {step['label']}
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ========== CHAT CONTAINER ==========
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f'<div class="assistant-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)

# Show initial greeting if no messages
if len(st.session_state.messages) == 0:
    greeting = """Welcome to **TalentScout AI Screening** 

I'll guide you through a quick initial assessment to understand your profile better.

**Let's begin with your full name:**"""
    st.markdown(f'<div class="assistant-msg">{greeting}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": greeting})

st.markdown('</div>', unsafe_allow_html=True)

# ========== AI RESPONSE FUNCTION - FIXED VERSION ==========
def get_response(user_input):
    """Smart response generator with PROPER formatting"""
    user_lower = user_input.lower()
    candidate = st.session_state.candidate
    
    # Extract and respond based on current step
    if not candidate["name"]:
        if "name" in user_lower or "i'm" in user_lower or "i am" in user_lower:
            words = user_input.split()
            if len(words) >= 2:
                candidate["name"] = " ".join(words[-2:]).title()
            return f"""Perfect! 

**{candidate['name']}**, pleased to meet you!

What's your **professional email address**?"""
        return "Let's start with your **full name**:"
    
    elif not candidate["email"]:
        if "@" in user_input:
            import re
            emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', user_input)
            if emails:
                candidate["email"] = emails[0]
            return f""" **Email registered!**

Great, I've noted your contact email.

What's the best **phone number** to reach you?"""
        return "What's your **professional email address**?"
    
    elif not candidate["phone"]:
        if any(char.isdigit() for char in user_input):
            candidate["phone"] = user_input
            return f""" **Contact details saved!**

Thanks for providing your contact information.

How many **years of professional experience** do you have in tech?"""
        return "What's your **phone number**?"
    
    elif not candidate["experience"]:
        if any(char.isdigit() for char in user_input):
            candidate["experience"] = user_input
            return f""" **{candidate['experience']} years of experience**

That's valuable experience!

What specific **role or position** are you targeting?"""
        return "How many **years of professional experience** do you have?"
    
    elif not candidate["role"]:
        candidate["role"] = user_input
        return f""" **{candidate['role'].title()}**

Excellent choice! That's a high-demand role.

Where are you **currently based or looking to work** from?"""
    
    elif not candidate["location"]:
        candidate["location"] = user_input
        return f"""**{candidate['location']}**

Great location!

Finally, what's your **primary tech stack**?
*(List your main technologies like Python, React, AWS, etc.)*"""
    
    elif not candidate["tech"]:
        # Extract technologies
        techs = []
        tech_list = ["python", "java", "javascript", "typescript", "react", 
                    "angular", "vue", "node", "django", "flask", "fastapi",
                    "spring", "aws", "azure", "gcp", "docker", "kubernetes",
                    "sql", "mongodb", "postgres", "mysql", "redis", "graphql"]
        
        for tech in tech_list:
            if tech in user_lower:
                techs.append(tech.title())
        
        if techs:
            candidate["tech"] = techs
            
            # Generate tech questions WITH PROPER FORMATTING
            questions = [
                "**Python Fundamentals** - Core concepts, best practices, and common patterns",
                "**Problem Solving** - Approach to debugging complex issues and optimization",
                "**System Design** - Scalable architecture and database design considerations",
                "**Development Workflow** - Testing strategies, CI/CD, and deployment processes",
                "**Industry Trends** - Staying current with evolving technologies and methodologies"
            ]
            
            # Build questions as plain text (NOT HTML)
            questions_text = ""
            for i, q in enumerate(questions, 1):
                questions_text += f"\n{i}. {q}"
            
            return f""" **Technical Assessment**

Based on your experience with **{', '.join(techs)}**, here are some areas to explore:

{questions_text}

 **Tip**: Provide specific examples from your experience for each area. Quality over quantity!"""
        else:
            return "What **technologies and frameworks** are you proficient with?"
    
    else:
        return """ **Screening Complete**

 **Thank you for completing the initial screening!**

Your profile has been successfully recorded. Our recruitment team will review your responses and contact you within **24-48 hours** for the next steps.

**Next Steps:**
1. Technical interview with senior engineers
2. Portfolio/code review session  
3. Cultural fit discussion
4. Final offer process

*You can export your profile data using the sidebar controls.*"""

# ========== CHAT INPUT ==========
if prompt := st.chat_input("Type your response here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    response = get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()

# ========== SIDEBAR ==========
with st.sidebar:
    # Status badge
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <div class="status-badge">
            <div class="status-dot"></div>
            <span>ACTIVE SCREENING</span>
        </div>
        <div style="color: #94a3b8; font-size: 0.85rem;">ID: TS-2024</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress
    completion = int((collected / 7) * 100)
    st.progress(completion / 100)
    st.caption(f"Profile Completion: {completion}% ({collected}/7)")
    
    st.markdown("---")
    
    # Candidate info
    st.markdown("**CANDIDATE PROFILE**")
    
    candidate = st.session_state.candidate
    info_items = [
        ("", "Name", candidate["name"]),
        ("", "Email", candidate["email"]),
        ("", "Phone", candidate["phone"]),
        ("", "Experience", f"{candidate['experience']} years" if candidate["experience"] else ""),
        ("", "Target Role", candidate["role"]),
        ("", "Location", candidate["location"]),
        ("", "Tech Stack", ", ".join(candidate["tech"][:4]) if candidate["tech"] else "")
    ]
    
    for icon, label, value in info_items:
        if value:
            st.markdown(f"""
            <div class="info-card">
                <div>
                    <span class="info-icon">{icon}</span>
                    <span class="info-label">{label}</span>
                </div>
                <div class="info-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Restart", use_container_width=True):
            st.session_state.messages = []
            st.session_state.candidate = {k: "" for k in candidate.keys()}
            st.session_state.candidate["tech"] = []
            st.rerun()
    
    with col2:
        if st.button(" Example", use_container_width=True):
            example_responses = [
                "Alex Johnson",
                "alex@techcorp.com",
                "+1 (555) 123-4567",
                "5 years",
                "Senior Python Developer",
                "San Francisco, CA",
                "Python, Django, AWS, Docker, PostgreSQL"
            ]
            for resp in example_responses:
                st.session_state.messages.append({"role": "user", "content": resp})
                response = get_response(resp)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # Export button
    st.markdown("---")
    if st.button(" Export Profile", type="secondary", use_container_width=True):
        data = {
            "profile": candidate,
            "screening_complete": collected == 7,
            "completion_percentage": completion,
            "timestamp": datetime.now().isoformat(),
            "message_count": len(st.session_state.messages)
        }
        st.download_button(
            label="Download JSON",
            data=json.dumps(data, indent=2),
            file_name=f"talent_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    # Footer
    st.markdown("""
    <div style="margin-top: 2rem; text-align: center;">
        <div style="color: #64748b; font-size: 0.75rem;">
            TalentScout AI v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)