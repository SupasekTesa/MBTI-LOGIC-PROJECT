import streamlit as st
import pandas as pd
import plotly.express as px
from questions import (
    COGNITIVE_QUESTIONS, 
    SUBJECT_QUESTIONS, 
    HOBBY_QUESTIONS, 
    GOAL_QUESTIONS,
    FINANCIAL_QUESTIONS
)

# ==========================================
# 1. PAGE CONFIG & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="ระบบวิเคราะห์ MBTI & Cognitive Functions",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    
    /* การ์ดคำถามแบบสอบถาม Step 1 */
    .question-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .question-badge {
        display: inline-block;
        background-color: #EFF6FF;
        color: #2563EB;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    .question-text {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }

    /* การ์ดคำถาม Step 2-4 */
    .category-badge {
        display: inline-block;
        background-color: #F1F5F9;
        color: #475569;
        font-weight: 700;
        font-size: 0.8rem;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        margin-bottom: 0.4rem;
        border: 1px solid #CBD5E1;
    }
    .sub-question-card {
        background-color: #FFFFFF;
        border-left: 5px solid #3B82F6;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }

    /* การ์ดสรุปผล MBTI */
    .mbti-hero-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 2.5rem 1.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        margin-bottom: 2rem;
    }
    .mbti-type-text {
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .func-card {
        background-color: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }
    .func-badge {
        font-size: 0.85rem;
        font-weight: bold;
        color: #64748B;
        text-transform: uppercase;
    }
    .func-title {
        font-size: 2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin: 0.3rem 0;
    }
    .func-desc {
        font-size: 0.85rem;
        color: #475569;
    }

    .logic-box {
        background-color: #0F172A;
        color: #38BDF8;
        border-radius: 12px;
        padding: 1.5rem;
        font-family: 'Courier New', monospace;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# ฐานข้อมูลจับคู่ MBTI & ลำดับฟังก์ชัน
MBTI_STACKS = {
    "ENTP": {"Dom": "Ne", "Aux": "Ti", "Tert": "Fe", "Inf": "Si", "Title": "นักประดิษฐ์และนักโต้วิเคราะห์"},
    "INTP": {"Dom": "Ti", "Aux": "Ne", "Tert": "Si", "Inf": "Fe", "Title": "นักคิดเชิงตรรกะและนักสืบค้น"},
    "ENTJ": {"Dom": "Te", "Aux": "Ni", "Tert": "Se", "Inf": "Fi", "Title": "ผู้บังคับบัญชาและนักวางกลยุทธ์"},
    "INTJ": {"Dom": "Ni", "Aux": "Te", "Tert": "Fi", "Inf": "Se", "Title": "นักวางแผนและนักคิดเชิงวิสัยทัศน์"},
    "ENFP": {"Dom": "Ne", "Aux": "Fi", "Tert": "Te", "Inf": "Si", "Title": "ผู้สร้างแรงบันดาลใจและนักจุดประกาย"},
    "INFP": {"Dom": "Fi", "Aux": "Ne", "Tert": "Si", "Inf": "Te", "Title": "นักอุดมคติและผู้แสวงหาความจริงแท้"},
    "ENFJ": {"Dom": "Fe", "Aux": "Ni", "Tert": "Se", "Inf": "Ti", "Title": "ตัวแทนผู้สร้างความเปลี่ยนแปลง"},
    "INFJ": {"Dom": "Ni", "Aux": "Fe", "Tert": "Ti", "Inf": "Se", "Title": "ผู้แนะนำและนักหยั่งรู้จิตใจ"},
    "ESTP": {"Dom": "Se", "Aux": "Ti", "Tert": "Fe", "Inf": "Ni", "Title": "ผู้ลุยแก้ปัญหาและนักปรับตัว"},
    "ISTP": {"Dom": "Ti", "Aux": "Se", "Tert": "Ni", "Inf": "Fe", "Title": "ช่างฝีมือและนักวิเคราะห์เครื่องกล"},
    "ESTJ": {"Dom": "Te", "Aux": "Si", "Tert": "Ne", "Inf": "Fi", "Title": "ผู้บริหารและนักจัดการระบบ"},
    "ISTJ": {"Dom": "Si", "Aux": "Te", "Tert": "Fi", "Inf": "Ne", "Title": "ผู้ตรวจสอบและนักลงมือทำตามหน้าที่"},
    "ESFP": {"Dom": "Se", "Aux": "Fi", "Tert": "Te", "Inf": "Ni", "Title": "ผู้สร้างความบันเทิงและมีชีวิตชีวา"},
    "ISFP": {"Dom": "Fi", "Aux": "Se", "Tert": "Ni", "Inf": "Te", "Title": "ศิลปินและผู้หลงใหลในสุนทรียภาพ"},
    "ESFJ": {"Dom": "Fe", "Aux": "Si", "Tert": "Ne", "Inf": "Ti", "Title": "ผู้ดูแลความสงบและผู้ประสานงาน"},
    "ISFJ": {"Dom": "Si", "Aux": "Fe", "Tert": "Ti", "Inf": "Ne", "Title": "ผู้ปกป้องและผู้เอื้ออารี"},
}

FUNC_DESCRIPTIONS = {
    "Ne": "คิดนอกกรอบ หาไอเดียใหม่ๆ เชื่อมโยงสิ่งรอบตัว",
    "Ni": "มองเห็นวิสัยทัศน์ ภาพรวมในอนาคต มีลางสังหรณ์แม่นยำ",
    "Se": "อยู่กับปัจจุบัน รับรู้ประสาทสัมผัส ปรับตัวไว",
    "Si": "ละเอียดยอดเยี่ยม ทำตามขั้นตอน จดจำประสบการณ์อดีต",
    "Te": "เน้นผลลัพธ์ จัดระบบ วางแผนเด็ดขาด บริหารงานเก่ง",
    "Ti": "วิเคราะห์ตรรกะภายใน ตั้งคำถาม หาเหตุผลลึกซึ้ง",
    "Fe": "แคร์ความรู้สึกกลุ่ม สร้างบรรยากาศ มารยาทสังคม",
    "Fi": "ยึดมั่นค่านิยมส่วนตัว ความจริงแท้ จริงใจกับความรู้สึก"
}

# ตัวแปรจัดการขั้นตอนหลัก
TOTAL_STEPS = 5
if "step" not in st.session_state:
    st.session_state.step = 1

# ตัวแปรสำหรับแบ่งคำถามใน Step 1 (Pagination)
QUESTIONS_PER_PAGE = 10
TOTAL_COG_QUESTIONS = len(COGNITIVE_QUESTIONS)
TOTAL_COG_PAGES = (TOTAL_COG_QUESTIONS + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE

if "cog_page" not in st.session_state:
    st.session_state.cog_page = 0

if "user_cog_responses" not in st.session_state:
    st.session_state.user_cog_responses = {}

progress_val = min((st.session_state.step - 1) / (TOTAL_STEPS - 1), 1.0)
st.progress(progress_val)


# ==========================================
# STEP 1: แบบประเมิน Cognitive Functions
# ==========================================
if st.session_state.step == 1:
    current_page = st.session_state.cog_page
    start_idx = current_page * QUESTIONS_PER_PAGE
    end_idx = min(start_idx + QUESTIONS_PER_PAGE, TOTAL_COG_QUESTIONS)
    current_questions = COGNITIVE_QUESTIONS[start_idx:end_idx]

    st.subheader("🧠 ส่วนที่ 1: แบบประเมิน Cognitive Functions")
    
    col_p1, col_p2 = st.columns([3, 1])
    with col_p1:
        st.caption(f"📌 **หน้า {current_page + 1} จาก {TOTAL_COG_PAGES}** (คำถามข้อที่ {start_idx + 1} - {end_idx} จากทั้งหมด {TOTAL_COG_QUESTIONS} ข้อ)")
    with col_p2:
        sub_progress = (current_page + 1) / TOTAL_COG_PAGES
        st.progress(sub_progress)

    st.info("💡 **ระดับการให้คะแนน:** 1 = ไม่ตรงเลย | 2 = ไม่ค่อยตรง | 3 = ปานกลาง | 4 = ค่อนข้างตรง | 5 = ตรงมากที่สุด")

    with st.form(key=f"form_step1_page_{current_page}"):
        page_responses = {}
        
        for idx, q in enumerate(current_questions, start=start_idx + 1):
            st.markdown(f"""
            <div class="question-card">
                <div class="question-badge">คำถามข้อที่ {idx} / {TOTAL_COG_QUESTIONS}</div>
                <div class="question-text">{q['text']}</div>
            </div>
            """, unsafe_allow_html=True)

            saved_score = st.session_state.user_cog_responses.get(q["id"], {}).get("score", 3)

            selected_score = st.radio(
                label=f"เลือกคะแนนสำหรับข้อ {idx}",
                options=[1, 2, 3, 4, 5],
                index=saved_score - 1,
                horizontal=True,
                key=f"q_{q['id']}",
                label_visibility="collapsed"
            )

            page_responses[q["id"]] = {
                "func": q["func"],
                "score": selected_score
            }
            st.markdown("<br>", unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if current_page > 0:
                submit_prev = st.form_submit_button("⬅ หน้าก่อนหน้า", use_container_width=True)
            else:
                submit_prev = False

        with col_btn2:
            if current_page < TOTAL_COG_PAGES - 1:
                submit_next = st.form_submit_button("หน้าถัดไป ➔", use_container_width=True)
            else:
                submit_next = st.form_submit_button("ถัดไป: เลือกวิชาความถนัด ➔", use_container_width=True)

        if submit_prev:
            st.session_state.user_cog_responses.update(page_responses)
            st.session_state.cog_page -= 1
            st.rerun()

        if submit_next:
            st.session_state.user_cog_responses.update(page_responses)
            if current_page < TOTAL_COG_PAGES - 1:
                st.session_state.cog_page += 1
                st.rerun()
            else:
                st.session_state.step = 2
                st.rerun()

# ==========================================
# STEP 2: วิชาที่ชอบ
# ==========================================
elif st.session_state.step == 2:
    st.subheader("📚 ส่วนที่ 2: ความสนใจและความถนัดรายวิชา")
    st.caption("โปรดเลือกการประเมินตามความเป็นจริง เพื่อความแม่นยำในการวิเคราะห์")

    with st.form("form_step2"):
        user_sub_responses = {}
        for idx, q in enumerate(SUBJECT_QUESTIONS, 1):
            st.markdown(f"""
            <div class="sub-question-card">
                <span class="category-badge">🏷️ {q['category']}</span>
                <div style="font-weight: 600; color: #1E293B; font-size: 1.05rem;">ข้อ {idx}. {q['text']}</div>
            </div>
            """, unsafe_allow_html=True)

            col_ans, _ = st.columns([1, 2])
            with col_ans:
                ans = st.radio(
                    f"ตอบข้อ {idx}:", 
                    ["ใช่", "ไม่ใช่"], 
                    index=1, 
                    horizontal=True, 
                    key=q["id"],
                    label_visibility="collapsed"
                )

            user_sub_responses[q["id"]] = {
                "category": q["category"],
                "ans": ans
            }
            st.markdown("<br>", unsafe_allow_html=True)

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
    st.subheader("🎨 ส่วนที่ 3: งานอดิเรกและสไตล์กิจกรรมในเวลาว่าง")
    st.caption("เลือกกิจกรรมที่คุณทำแล้วรู้สึกสนุก มีพลัง หรือทำเป็นประจำ")

    with st.form("form_step3"):
        user_hob_responses = {}
        for idx, q in enumerate(HOBBY_QUESTIONS, 1):
            st.markdown(f"""
            <div class="sub-question-card" style="border-left-color: #8B5CF6;">
                <span class="category-badge">🎯 {q['category']}</span>
                <div style="font-weight: 600; color: #1E293B; font-size: 1.05rem;">ข้อ {idx}. {q['text']}</div>
            </div>
            """, unsafe_allow_html=True)

            col_ans, _ = st.columns([1, 2])
            with col_ans:
                ans = st.radio(
                    f"ตอบข้อ {idx}:", 
                    ["ใช่", "ไม่ใช่"], 
                    index=1, 
                    horizontal=True, 
                    key=q["id"],
                    label_visibility="collapsed"
                )

            user_hob_responses[q["id"]] = {
                "category": q["category"],
                "ans": ans
            }
            st.markdown("<br>", unsafe_allow_html=True)

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
# STEP 4: การเงิน/เป้าหมายอาชีพ (5 ข้อทุนการศึกษา)
# ==========================================
elif st.session_state.step == 4:
    st.subheader("💼 ส่วนที่ 4: เป้าหมายอาชีพ และ ปัจจัยทุนการศึกษา")
    st.caption("โปรดระบุเงื่อนไขตามความเป็นจริง เพื่อให้ระบบวิเคราะห์เส้นทางศึกษาต่อและทุนที่เหมาะสมที่สุด")

    with st.form("form_step4"):
        user_goal_responses = {}
        
        # 1. คำถามเป้าหมายอาชีพ
        st.markdown("#### 🎯 1. สไตล์เป้าหมายการทำงานในอนาคต")
        for idx, q in enumerate(GOAL_QUESTIONS, 1):
            st.markdown(f"""
            <div class="sub-question-card" style="border-left-color: #10B981;">
                <span class="category-badge">🚀 {q['category']}</span>
                <div style="font-weight: 600; color: #1E293B; font-size: 1.05rem;">ข้อ {idx}. {q['text']}</div>
            </div>
            """, unsafe_allow_html=True)

            col_ans, _ = st.columns([1, 2])
            with col_ans:
                ans = st.radio(
                    f"ตอบข้อ {idx}:", 
                    ["ใช่", "ไม่ใช่"], 
                    index=1, 
                    horizontal=True, 
                    key=q["id"],
                    label_visibility="collapsed"
                )
            user_goal_responses[q["id"]] = {"category": q["category"], "ans": ans}
            st.markdown("<br>", unsafe_allow_html=True)

        st.divider()

        # 2. คำถามเจาะลึกการเงินและทุนทรัพย์ 5 ข้อ
        st.markdown("#### 💰 2. เงื่อนไขด้านทุนทรัพย์และภาระทางการเงิน (5 ข้อ)")
        
        user_fin_responses = {}
        for f_q in FINANCIAL_QUESTIONS:
            st.markdown(f"""
            <div class="sub-question-card" style="border-left-color: #F59E0B;">
                <span class="category-badge">💳 {f_q['category']}</span>
                <div style="font-weight: 600; color: #1E293B; font-size: 1.05rem;">{f_q['label']}</div>
            </div>
            """, unsafe_allow_html=True)

            selected_opt = st.radio(
                f_q['label'],
                options=f_q['options'],
                index=0,
                key=f_q['id'],
                label_visibility="collapsed"
            )
            user_fin_responses[f_q['id']] = selected_opt
            st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("⬅ ย้อนกลับ"):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.form_submit_button("🚀 ประมวลผลและดูผลลัพธ์", use_container_width=True):
                st.session_state.user_goal_responses = user_goal_responses
                st.session_state.user_fin_responses = user_fin_responses
                st.session_state.capital = user_fin_responses.get("fin_budget", "")
                st.session_state.step = 5
                st.rerun()

# ==========================================
# STEP 5: หน้าสรุปผลลัพธ์
# ==========================================
elif st.session_state.step == 5:
    st.balloons()

    cog_resp = st.session_state.get("user_cog_responses", {})
    sub_resp = st.session_state.get("user_sub_responses", {})
    fin_resp = st.session_state.get("user_fin_responses", {})
    capital = st.session_state.get("capital", "")

    # 1. คำนวณคะแนน Cognitive Functions
    func_scores = {"Ne": 0, "Ni": 0, "Se": 0, "Si": 0, "Te": 0, "Ti": 0, "Fe": 0, "Fi": 0}
    for q_id, val in cog_resp.items():
        if isinstance(val, dict) and "func" in val and "score" in val:
            func_scores[val["func"]] += val["score"]

    # 2. ค้นหา Type MBTI
    sorted_funcs = sorted(func_scores.items(), key=lambda x: x[1], reverse=True)
    top_func = sorted_funcs[0][0]
    second_func = sorted_funcs[1][0]

    predicted_type = "ENTP"
    for mbti_name, stack in MBTI_STACKS.items():
        if stack["Dom"] == top_func and stack["Aux"] == second_func:
            predicted_type = mbti_name
            break
        elif stack["Dom"] == top_func:
            predicted_type = mbti_name

    stack_info = MBTI_STACKS.get(predicted_type, MBTI_STACKS["ENTP"])

    # 3. ตรวจสอบเงื่อนไขจากคำถามย่อยหมวดวิชา
    a_math = any(sub_resp.get(f"sub_math_{i}", {}).get("ans") == "ใช่" for i in range(1, 4))
    a_sci = any(sub_resp.get(f"sub_sci_{i}", {}).get("ans") == "ใช่" for i in range(1, 4))
    a_art = any(sub_resp.get(f"sub_art_{i}", {}).get("ans") == "ใช่" for i in range(1, 4))
    c_low = "จำกัดสูง" in capital if capital else False

    rule_tech = (func_scores["Ti"] >= 12 or func_scores["Te"] >= 12) and a_math
    rule_health = (func_scores["Fe"] >= 12 or func_scores["Si"] >= 12) and a_sci
    rule_creative = (func_scores["Ne"] >= 12 or a_art)

    # Header MBTI Hero Card
    st.markdown(f"""
    <div class="mbti-hero-card">
        <div style="font-size: 1.2rem; opacity: 0.9;">ผลการประมวลผลบุคลิกภาพของคุณคือ</div>
        <div class="mbti-type-text">{predicted_type}</div>
        <div style="font-size: 1.3rem; font-weight: 500;">"{stack_info['Title']}"</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "✨ สรุป MBTI & Cognitive Functions", 
        "🎓 คณะ/อาชีพ & แนะนำมหาวิทยาลัยตามงบ", 
        "📐 การพิสูจน์ตรรกศาสตร์"
    ])

    with tab1:
        st.subheader("🧩 ลำดับกระบวนการทางความคิด (Cognitive Function Hierarchy)")
        st.caption("สมองของคุณประมวลผลข้อมูลและตัดสินใจผ่านฟังก์ชันหลัก 4 ลำดับนี้:")

        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        funcs_to_show = [
            ("Dominant (ฟังก์ชันหลัก)", stack_info["Dom"]),
            ("Auxiliary (ฟังก์ชันรอง)", stack_info["Aux"]),
            ("Tertiary (ฟังก์ชันสำรอง)", stack_info["Tert"]),
            ("Inferior (จุดอ่อน)", stack_info["Inf"])
        ]
        
        cols = [col_f1, col_f2, col_f3, col_f4]
        for idx, (label, f_code) in enumerate(funcs_to_show):
            with cols[idx]:
                st.markdown(f"""
                <div class="func-card">
                    <div class="func-badge">{label}</div>
                    <div class="func-title">{f_code}</div>
                    <div class="func-desc">{FUNC_DESCRIPTIONS.get(f_code, '')}</div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        st.subheader("📊 กราฟเปรียบเทียบคะแนน Cognitive Functions ทั้ง 8 ด้าน")
        df_scores = pd.DataFrame(list(func_scores.items()), columns=['Function', 'Score'])
        df_scores = df_scores.sort_values(by='Score', ascending=True)

        fig = px.bar(
            df_scores, 
            x='Score', 
            y='Function', 
            orientation='h',
            text='Score',
            color='Score',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            height=400,
            xaxis_title="คะแนนที่ได้",
            yaxis_title="ฟังก์ชัน",
            coloraxis_showscale=False
        )
        fig.update_traces(textposition='inside', textfont_size=14)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("🎓 คณะที่แนะนำ และ สถาบันการศึกษาที่ตรงกับเงื่อนไขทุนทรัพย์ของคุณ")

        budget_choice = fin_resp.get("fin_budget", "")
        job_goal = fin_resp.get("fin_job_goal", "")
        debt_burden = fin_resp.get("fin_debt_burden", "")
        scholarship_need = fin_resp.get("fin_scholarship_need", "")
        location_limit = fin_resp.get("fin_location", "")

        st.markdown(f"""
        <div style="background-color: #F1F5F9; border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem; border: 1px solid #CBD5E1;">
            <h5 style="margin-top:0; color: #1E293B;">📊 สรุปโปรไฟล์ทางการเงินและเป้าหมายของคุณ:</h5>
            <ul style="margin-bottom:0; color: #334155; font-size: 0.95rem;">
                <li><b>งบประมาณค่าเทอม:</b> {budget_choice.split('(')[0] if budget_choice else 'ไม่ได้ระบุ'}</li>
                <li><b>เป้าหมายอาชีพ:</b> {job_goal.split('(')[0] if job_goal else 'ไม่ได้ระบุ'}</li>
                <li><b>เงื่อนไขทุนผูกพัน:</b> {scholarship_need.split('(')[0] if scholarship_need else 'ไม่ได้ระบุ'}</li>
                <li><b>ข้อจำกัดการเดินทาง/หอพัก:</b> {location_limit.split('(')[0] if location_limit else 'ไม่ได้ระบุ'}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if rule_tech:
            field_title = "💻 กลุ่มเทคโนโลยี คำนวณ และวิศวกรรม"
            field_desc = "เด่นด้านตรรกะและการคิดวิเคราะห์ เหมาะกับงานแก้ปัญหาเชิงระบบ เทคโนโลยี และการคำนวณ"
            subjects_to_focus = "คณิตศาสตร์ (แคลคูลัส, สถิติ) และ ภาษาอังกฤษ / ทักษะเพิ่ม: เขียนโปรแกรม (Python, C++)"
        elif rule_health:
            field_title = "🏥 กลุ่มวิทยาศาสตร์ สุขภาพ และการดูแล"
            field_desc = "เด่นด้านความละเอียดรอบคอบ ใส่ใจมนุษย์ หรือชอบงานที่เป็นระบบมั่นคง"
            subjects_to_focus = "ชีววิทยา, เคมี, ฟิสิกส์ / ทักษะเพิ่ม: ศัพท์เทคนิคภาษาอังกฤษ, จิตวิทยาการสื่อสาร"
        elif rule_creative:
            field_title = "🎨 กลุ่มสร้างสรรค์ นวัตกรรม และสื่อดิจิทัล"
            field_desc = "เด่นด้านจินตนาการ การคิดนอกกรอบ และการถ่ายทอดไอเดียผ่านสื่อ"
            subjects_to_focus = "ศิลปะ, ภาษา / ทักษะเพิ่ม: โปรแกรมออกแบบ (Photoshop, Figma), การทำ Portfolio"
        else:
            field_title = "🏛️ กลุ่มบริหารจัดการ สังคมศาสตร์ และภาษา"
            field_desc = "เด่นด้านการประเมินคุณค่า การสื่อสาร และการบริหารจัดการองค์กร"
            subjects_to_focus = "ภาษาไทย, ภาษาอังกฤษ, สังคมศึกษา / ทักษะเพิ่ม: ภาษาที่ 3, ทักษะการนำเสนอ"

        st.success(f"### {field_title}")
        st.write(f"**เหตุผลที่เหมาะกับคุณ:** {field_desc}")
        
        with st.expander("📌 **แนวทางการเรียนต่อ & วิชาที่ควรเน้นศึกษาเพิ่ม**", expanded=False):
            st.write(f"* **วิชาและทักษะที่ควรเน้น:** {subjects_to_focus}")

        st.divider()

        st.markdown("### 🏫 มหาวิทยาลัยและเส้นทางศึกษาต่อที่ 'ตรงกับทุนของคุณ'")

        if "จำกัดสูง" in budget_choice or "สนใจมาก" in scholarship_need:
            st.info("💡 **ระบบคัดกรองเฉพาะ:** สถาบันที่มีทุนเรียนฟรี ทุนผูกพันมีงานรองรับ หรือค่าเทอมประหยัดตอบโจทย์งบประมาณของคุณ")

            col_uni1, col_uni2 = st.columns(2)
            with col_uni1:
                st.markdown("""
                <div style="background-color: #FFFFFF; border: 2px solid #3B82F6; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                    <h4 style="color: #1E3A8A; margin-top:0;">🎓 สถาบันทุนผูกพัน (จบแล้วมีงานทำทันที)</h4>
                    <ul>
                        <li><b>วิทยาลัยพยาบาลบรมราชชนนี / สถาบันพระบรมราชชนก:</b> มีทุนเรียนฟรี มีเบี้ยเลี้ยง จบแล้วบรรจุเป็นพยาบาลรัฐทันที</li>
                        <li><b>วิทยาลัยพยาบาลเหล่าทัพ / ตำรวจ:</b> ทุนการศึกษาพร้อมสวัสดิการ บรรจุรับราชการทันทีหลังจบ</li>
                        <li><b>โครงการทุนครูคืนถิ่น (คณะศึกษาศาสตร์/ครุศาสตร์):</b> เรียนฟรีพร้อมการันตีตำแหน่งบรรจุครูในภูมิลำเนา</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with col_uni2:
                st.markdown("""
                <div style="background-color: #FFFFFF; border: 2px solid #10B981; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                    <h4 style="color: #065F46; margin-top:0;">🏛️ มหาวิทยาลัยค่าเทอมประหยัด & ยืดหยุ่น</h4>
                    <ul>
                        <li><b>มหาวิทยาลัยรามคำแหง / มสธ.:</b> ค่าเทอมเริ่มต้นหลักพัน สามารถเรียนไปทำงานไปได้ ตอบโจทย์การคืนทุนไว</li>
                        <li><b>มหาวิทยาลัยเทคโนโลยีราชมงคล (RMUT) ทั่วประเทศ:</b> ค่าเทอมประหยัด เน้นทักษะปฏิบัติจริง กู้ กยศ. ได้ 100%</li>
                        <li><b>มหาวิทยาลัยราชภัฏในภูมิลำเนา:</b> ช่วยประหยัดค่าหอพักและค่าครองชีพได้อย่างมาก</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        elif "ปานกลาง" in budget_choice:
            st.info("💡 **ระบบคัดกรองเฉพาะ:** มหาวิทยาลัยรัฐบาลชั้นนำที่ค่าเทอมอยู่ในระดับปานกลาง (15,000 - 40,000 บาท/เทอม)")

            st.markdown("""
            <div style="background-color: #FFFFFF; border: 2px solid #3B82F6; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                <h4 style="color: #1E3A8A; margin-top:0;">🏛️ มหาวิทยาลัยรัฐบาลหลักที่แนะนำ</h4>
                <ul>
                    <li><b>สายเทค/วิศวะ:</b> กลุ่ม 3 พระจอมเกล้า (สจล., มจธ., มจพ.), มหาวิทยาลัยเกษตรศาสตร์, มหาวิทยาลัยเชียงใหม่</li>
                    <li><b>สายการแพทย์/สุขภาพ:</b> มหาวิทยาลัยมหิดล, จุฬาลงกรณ์มหาวิทยาลัย, มหาวิทยาลัยขอนแก่น, มหาวิทยาลัยสงขลานครินทร์</li>
                    <li><b>สายบริหาร/สังคม/ศิลปะ:</b> มหาวิทยาลัยธรรมศาสตร์, มหาวิทยาลัยศิลปากร, มหาวิทยาลัยศรีนครินทรวิโรฒ (มศว)</li>
                </ul>
                <p style="font-size: 0.85rem; color: #64748B; margin-bottom:0;">* ทุกสถาบันมีทุนจ้างงานในมหาลัย และทุนกู้ยืม กยศ./กอศ. รองรับ</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.info("💡 **ระบบคัดกรองเฉพาะ:** หลักสูตรนานาชาติ มหาวิทยาลัยเอกชนอุปกรณ์ทันสมัย หรือสถาบันที่มีคอนเนกชันธุรกิจสูง")

            st.markdown("""
            <div style="background-color: #FFFFFF; border: 2px solid #8B5CF6; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                <h4 style="color: #5B21B6; margin-top:0;">🌟 สถาบันเอกชนชั้นนำ & หลักสูตรนานาชาติ</h4>
                <ul>
                    <li><b>มหาวิทยาลัยกรุงเทพ / มหาวิทยาลัยรังสิต / มหาวิทยาลัยศรีปทุม:</b> โดดเด่นด้านอุปกรณ์ระดับมืออาชีพ คอนเนกชันสายงานตรง</li>
                    <li><b>มหาวิทยาลัยอัสสัมชัญ (ABAC):</b> เด่นหลักสูตรนานาชาติและการสร้างเครือข่ายธุรกิจระดับสากล</li>
                    <li><b>หลักสูตรนานาชาติมหาลัยรัฐ (เช่น SIIT มธ. / ICT มหิดล / ISE จุฬาฯ):</b> เรียนเป็นภาษาอังกฤษพร้อมโอกาสฝึกงานต่างประเทศ</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        if "ส่งเสียครอบครัว" in debt_burden or "คืนทุนไว" in job_goal:
            st.warning("⚠️ **คำแนะนำพิเศษสำหรับเป้าหมายรายได้เร็ว/ภาระครอบครัว:** แนะนำให้เลือกเรียนสายที่มีการฝึกงานตรงกับบริษัทตั้งแต่ปี 3-4 หรือเลือกสายงานเทค/ดิจิทัล ซึ่งสามารถรับงาน Freelance สร้างรายได้ระหว่างเรียนได้ทันที")

    with tab3:
        st.subheader("📐 โครงสร้างการพิสูจน์ทางตรรกศาสตร์ (Logic Proof)")
        st.caption("อธิบายกระบวนการคำนวณเบื้องหลังด้วยทฤษฎีประพจน์ทางคณิตศาสตร์")

        st.markdown(f"""
        <div class="logic-box">
        <b>1. สรุปคะแนน Cognitive Functions (รวมจากแบบสอบถาม 80 ข้อ):</b><br>
        • Ne = {func_scores['Ne']} | Ni = {func_scores['Ni']}<br>
        • Se = {func_scores['Se']} | Si = {func_scores['Si']}<br>
        • Te = {func_scores['Te']} | Ti = {func_scores['Ti']}<br>
        • Fe = {func_scores['Fe']} | Fi = {func_scores['Fi']}<br><br>
        
        <b>2. กำหนดตัวแปรประพจน์ (Propositions):</b><br>
        • p_Dom = {top_func} (ฟังก์ชันหลักที่ได้คะแนนสูงสุด)<br>
        • a_math (ชอบสายคำนวณ) = {a_math}<br>
        • a_sci (ชอบสายวิทย์) = {a_sci}<br>
        • c_low (เงื่อนไขข้อจำกัดทุนสูง) = {c_low}<br><br>
        
        <b>3. การสรุปผลตามกฎเงื่อนไข (Rule Inference):</b><br>
        • Rule_Tech = (Ti ∨ Te) ∧ a_math ∧ c_low → <b>{rule_tech}</b><br>
        • Rule_Health = (Fe ∨ Si) ∧ a_sci ∧ c_low → <b>{rule_health}</b><br>
        • Rule_Creative = (Ne ∨ a_art) → <b>{rule_creative}</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 ทำแบบประเมินใหม่อีกครั้ง", use_container_width=True):
        st.session_state.step = 1
        st.session_state.cog_page = 0
        st.session_state.user_cog_responses = {}
        st.rerun()
