import streamlit as st
import pandas as pd
import plotly.express as px
from questions import (
    COGNITIVE_QUESTIONS, 
    SUBJECT_QUESTIONS, 
    HOBBY_QUESTIONS, 
    GOAL_QUESTIONS
)

# ==========================================
# 1. PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="ระบบวัดแวว MBTI & Cognitive Functions",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    .header-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        color: white;
        padding: 1.8rem 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .header-title { font-size: 2rem; font-weight: 800; }
    .mbti-result-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
        color: #1E293B;
        margin-top: 1rem;
    }
    .func-level {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 0.2rem;
    }
    .func-name {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 1.2rem;
    }
    .card-box {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ฐานข้อมูลจับคู่ Cognitive Functions สู่ MBTI 16 ประเภท
MBTI_STACKS = {
    "ENTP": {"Dom": "Ne", "Aux": "Ti", "Tert": "Fe", "Inf": "Si"},
    "INTP": {"Dom": "Ti", "Aux": "Ne", "Tert": "Si", "Inf": "Fe"},
    "ENTJ": {"Dom": "Te", "Aux": "Ni", "Tert": "Se", "Inf": "Fi"},
    "INTJ": {"Dom": "Ni", "Aux": "Te", "Tert": "Fi", "Inf": "Se"},
    "ENFP": {"Dom": "Ne", "Aux": "Fi", "Tert": "Te", "Inf": "Si"},
    "INFP": {"Dom": "Fi", "Aux": "Ne", "Tert": "Si", "Inf": "Te"},
    "ENFJ": {"Dom": "Fe", "Aux": "Ni", "Tert": "Se", "Inf": "Ti"},
    "INFJ": {"Dom": "Ni", "Aux": "Fe", "Tert": "Ti", "Inf": "Se"},
    "ESTP": {"Dom": "Se", "Aux": "Ti", "Tert": "Fe", "Inf": "Ni"},
    "ISTP": {"Dom": "Ti", "Aux": "Se", "Tert": "Ni", "Inf": "Fe"},
    "ESTJ": {"Dom": "Te", "Aux": "Si", "Tert": "Ne", "Inf": "Fi"},
    "ISTJ": {"Dom": "Si", "Aux": "Te", "Tert": "Fi", "Inf": "Ne"},
    "ESFP": {"Dom": "Se", "Aux": "Fi", "Tert": "Te", "Inf": "Ni"},
    "ISFP": {"Dom": "Fi", "Aux": "Se", "Tert": "Ni", "Inf": "Te"},
    "ESFJ": {"Dom": "Fe", "Aux": "Si", "Tert": "Ne", "Inf": "Ti"},
    "ISFJ": {"Dom": "Si", "Aux": "Fe", "Tert": "Ti", "Inf": "Ne"},
}

# ตัวแปรจัดการขั้นตอน
TOTAL_STEPS = 5
if "step" not in st.session_state:
    st.session_state.step = 1

# หลอดความคืบหน้า
progress_val = min((st.session_state.step - 1) / (TOTAL_STEPS - 1), 1.0)
st.progress(progress_val)


# ==========================================
# STEP 1: แบบสอบถามสเกลคะแนน 1-5 (ตรงตามรูปที่ 1)
# ==========================================
if st.session_state.step == 1:
    st.subheader("🧠 ส่วนที่ 1: แบบประเมิน Cognitive Functions")
    st.caption("เลือกระดับคะแนน 1 (ไม่ตรงเลย) ถึง 5 (ตรงมากที่สุด)")
    
    with st.form("form_step1"):
        user_cog_responses = {}
        for q in COGNITIVE_QUESTIONS:
            st.markdown(f"**{q['text']}**")
            # ปรับเป็น Radio Button แนวนอน สเกล 1-5 แบบในรูปเป๊ะๆ
            user_cog_responses[q["id"]] = {
                "func": q["func"],
                "score": st.radio(
                    "คะแนน:",
                    options=[1, 2, 3, 4, 5],
                    index=2,
                    horizontal=True,
                    key=q["id"],
                    label_visibility="collapsed"
                )
            }
            st.divider()

        if st.form_submit_button("ถัดไป: เลือกวิชาความถนัด ➔", use_container_width=True):
            st.session_state.user_cog_responses = user_cog_responses
            st.session_state.step = 2
            st.rerun()


# ==========================================
# STEP 2: วิชาที่ชอบ
# ==========================================
elif st.session_state.step == 2:
    st.subheader("📚 ส่วนที่ 2: วิชาความถนัดและความชอบ")
    
    with st.form("form_step2"):
        user_sub_responses = {}
        for q in SUBJECT_QUESTIONS:
            user_sub_responses[q["id"]] = {
                "category": q["category"],
                "ans": st.radio(q["text"], ["ใช่", "ไม่ใช่"], index=1, horizontal=True, key=q["id"])
            }
            st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("⬅ ย้อนกลับ"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.form_submit_button("ถัดไป: งานอดิเรก ➔", use_container_width=True):
                st.session_state.user_sub_responses = user_sub_responses
                st.session_state.step = 3
                st.rerun()


# ==========================================
# STEP 3: งานอดิเรก
# ==========================================
elif st.session_state.step == 3:
    st.subheader("🎨 ส่วนที่ 3: งานอดิเรกและสไตล์กิจกรรม")
    
    with st.form("form_step3"):
        user_hob_responses = {}
        for q in HOBBY_QUESTIONS:
            user_hob_responses[q["id"]] = {
                "category": q["category"],
                "ans": st.radio(q["text"], ["ใช่", "ไม่ใช่"], index=1, horizontal=True, key=q["id"])
            }
            st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("⬅ ย้อนกลับ"):
                st.session_state.step = 2
                st.rerun()
        with col2:
            if st.form_submit_button("ถัดไป: การเงิน/ทุนทรัพย์ ➔", use_container_width=True):
                st.session_state.user_hob_responses = user_hob_responses
                st.session_state.step = 4
                st.rerun()


# ==========================================
# STEP 4: การเงิน/ทุนการศึกษา
# ==========================================
elif st.session_state.step == 4:
    st.subheader("💼 ส่วนที่ 4: เป้าหมายอาชีพ และ ทุนการศึกษา")
    
    with st.form("form_step4"):
        user_goal_responses = {}
        for q in GOAL_QUESTIONS:
            user_goal_responses[q["id"]] = {
                "category": q["category"],
                "ans": st.radio(q["text"], ["ใช่", "ไม่ใช่"], index=1, horizontal=True, key=q["id"])
            }
            st.divider()

        capital = st.radio(
            "เงื่อนไขด้านทุนทรัพย์ในการศึกษาต่อ:",
            ["มีข้อจำกัดสูง (ต้องการทุนเรียนฟรี/จบแล้วมีงานทำทันที)", "ไม่มีข้อจำกัด หรือมีทุนทรัพย์ปานกลางถึงสูง"]
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("⬅ ย้อนกลับ"):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.form_submit_button("🚀 ประมวลผลและแสดงกราฟคะแนน", use_container_width=True):
                st.session_state.user_goal_responses = user_goal_responses
                st.session_state.capital = capital
                st.session_state.step = 5
                st.rerun()


# ==========================================
# STEP 5: แสดงผลลัพธ์ (ตรงตามรูปที่ 2 และ 3 เป๊ะๆ)
# ==========================================
elif st.session_state.step == 5:
    cog_resp = st.session_state.get("user_cog_responses", {})
    sub_resp = st.session_state.get("user_sub_responses", {})
    capital = st.session_state.get("capital", "")

    # 1. คำนวณคะแนน Cognitive Functions รวม (คะแนนเต็มตามจำนวนข้อ)
    func_scores = {"Ne": 0, "Ni": 0, "Se": 0, "Si": 0, "Te": 0, "Ti": 0, "Fe": 0, "Fi": 0}
    for q_id, val in cog_resp.items():
        func_scores[val["func"]] += val["score"]

    # 2. ทำการคำนวณ Type MBTI จากการจับคู่ Function ที่ได้คะแนนสูงสุด
    sorted_funcs = sorted(func_scores.items(), key=lambda x: x[1], reverse=True)
    top_func = sorted_funcs[0][0]
    second_func = sorted_funcs[1][0]

    # ค้นหา Type ที่เข้ากันได้ดีที่สุด
    predicted_type = "ENTP" # Default
    for mbti_name, stack in MBTI_STACKS.items():
        if stack["Dom"] == top_func and stack["Aux"] == second_func:
            predicted_type = mbti_name
            break
        elif stack["Dom"] == top_func:
            predicted_type = mbti_name

    stack_info = MBTI_STACKS.get(predicted_type, MBTI_STACKS["ENTP"])

    # --- ส่วนแสดงผล MBTI (เหมือนรูปที่ 2) ---
    st.markdown(f'<div class="mbti-result-title">✨ บุคลิกภาพของคุณคือ: {predicted_type} ✨</div>', unsafe_allow_html=True)
    st.write("")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown('<div class="func-level">Dominant (หลัก)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="func-name">{stack_info["Dom"]}</div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown('<div class="func-level">Auxiliary (รอง)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="func-name">{stack_info["Aux"]}</div>', unsafe_allow_html=True)
    with col_m3:
        st.markdown('<div class="func-level">Tertiary (สำรอง)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="func-name">{stack_info["Tert"]}</div>', unsafe_allow_html=True)
    with col_m4:
        st.markdown('<div class="func-level">Inferior (จุดอ่อน)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="func-name">{stack_info["Inf"]}</div>', unsafe_allow_html=True)

    st.info(f"**การวิเคราะห์ตรรกะการเกิด Type:** ระบบตรวจพบว่าคุณใช้ **{stack_info['Dom']}** เป็นฟังก์ชันหลัก และใช้ **{stack_info['Aux']}** เป็นฟังก์ชันสนับสนุน ตามทฤษฎีจิตวิทยาเมื่อประกอบกันจึงทำให้คุณมีรูปแบบจิตใจสอดคล้องกับ **{predicted_type}**")

    st.divider()

    # --- ส่วนแสดงกราฟแท่งแนวนอน (เหมือนรูปที่ 3 เป๊ะๆ) ---
    st.subheader("📊 กราฟคะแนน Cognitive Functions")
    
    # แปลงข้อมูลใส่ DataFrame เพื่อสร้างกราฟ
    df_scores = pd.DataFrame(list(func_scores.items()), columns=['Function', 'Score'])
    df_scores = df_scores.sort_values(by='Score', ascending=True)

    # สร้างกราฟแท่งแนวนอนด้วย Plotly
    fig = px.bar(
        df_scores, 
        x='Score', 
        y='Function', 
        orientation='h',
        text='Score',
        color='Score',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=450,
        xaxis_title="Score",
        yaxis_title="Function",
        coloraxis_showscale=True
    )
    fig.update_traces(textposition='inside')

    st.plotly_chart(fig, use_container_width=True)

    # --- ส่วนพิสูจน์ตรรกศาสตร์แนะนำคณะ ---
    st.divider()
    st.subheader("🎓 ผลการพิสูจน์ตรรกศาสตร์เพื่อการเลือกคณะ")
    
    a_math = sub_resp.get("sub_math", {}).get("ans") == "ใช่"
    c_low = "มีข้อจำกัดสูง" in capital
    
    rule_tech = (func_scores["Ti"] >= 15 or func_scores["Te"] >= 15) and a_math and c_low
    
    if rule_tech:
        st.success("**แนะนำ:** คณะวิทยาการคอมพิวเตอร์ / วิศวกรรมซอฟต์แวร์ / ครุศาสตร์คอมพิวเตอร์")
    else:
        st.success("**แนะนำ:** คณะบริหารธุรกิจ / สถาปัตยกรรมศาสตร์ / มนุษยศาสตร์ / นิเทศศาสตร์")

    if st.button("🔄 ทำแบบประเมินใหม่อีกครั้ง", use_container_width=True):
        st.session_state.step = 1
        st.rerun()
