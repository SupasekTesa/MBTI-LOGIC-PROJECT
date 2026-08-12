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

    .career-card {
        background-color: #FFFFFF;
        border-left: 6px solid #3B82F6;
        border-radius: 12px;
        padding: 1.8rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }

    .detail-box {
        background-color: #F1F5F9;
        border-radius: 10px;
        padding: 1.2rem;
        margin-top: 1rem;
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

# ตัวแปรจัดการขั้นตอน
TOTAL_STEPS = 5
if "step" not in st.session_state:
    st.session_state.step = 1

progress_val = min((st.session_state.step - 1) / (TOTAL_STEPS - 1), 1.0)
st.progress(progress_val)


# ==========================================
# STEP 1: Cognitive Functions (80 ข้อ)
# ==========================================
if st.session_state.step == 1:
    st.subheader("🧠 ส่วนที่ 1: แบบประเมิน Cognitive Functions")
    st.caption("เลือกระดับคะแนน 1 (ไม่ตรงเลย) ถึง 5 (ตรงมากที่สุด)")
    
    with st.form("form_step1"):
        user_cog_responses = {}
        for q in COGNITIVE_QUESTIONS:
            st.markdown(f"**{q['text']}**")
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
    st.subheader("💼 ส่วนที่ 4: เป้าหมายอาชีพ และ ปัจจัยทุนการศึกษา")
    
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
            ["มีข้อจำกัดสูง (ต้องการทุนเรียนฟรี/จบแล้วมีงานทำทันที/คืนทุนไว)", "ไม่มีข้อจำกัด หรือมีทุนทรัพย์ปานกลางถึงสูง"]
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("⬅ ย้อนกลับ"):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.form_submit_button("🚀 ประมวลผลและดูผลลัพธ์", use_container_width=True):
                st.session_state.user_goal_responses = user_goal_responses
                st.session_state.capital = capital
                st.session_state.step = 5
                st.rerun()

# ==========================================
# STEP 5: หน้าสรุปผลลัพธ์ (เพิ่มรายละเอียดวิชา/งบ)
# ==========================================
elif st.session_state.step == 5:
    st.balloons()

    cog_resp = st.session_state.get("user_cog_responses", {})
    sub_resp = st.session_state.get("user_sub_responses", {})
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

    # 3. เตรียมประพจน์ตรรกศาสตร์
    sub_math_val = sub_resp.get("sub_math", {})
    sub_sci_val = sub_resp.get("sub_sci", {})
    sub_art_val = sub_resp.get("sub_art", {})

    a_math = (sub_math_val.get("ans") == "ใช่") if isinstance(sub_math_val, dict) else False
    a_sci = (sub_sci_val.get("ans") == "ใช่") if isinstance(sub_sci_val, dict) else False
    a_art = (sub_art_val.get("ans") == "ใช่") if isinstance(sub_art_val, dict) else False
    c_low = "มีข้อจำกัดสูง" in capital if capital else False

    rule_tech = (func_scores["Ti"] >= 12 or func_scores["Te"] >= 12) and a_math
    rule_health = (func_scores["Fe"] >= 12 or func_scores["Si"] >= 12) and a_sci
    rule_creative = (func_scores["Ne"] >= 12 or a_art)

    # ----------------------------------------------------
    # ส่วนหัวสรุป MBTI Hero Card
    # ----------------------------------------------------
    st.markdown(f"""
    <div class="mbti-hero-card">
        <div style="font-size: 1.2rem; opacity: 0.9;">ผลการประมวลผลบุคลิกภาพของคุณคือ</div>
        <div class="mbti-type-text">{predicted_type}</div>
        <div style="font-size: 1.3rem; font-weight: 500;">"{stack_info['Title']}"</div>
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # แบ่งการแสดงผลเป็น 3 แท็บ (Tabs)
    # ----------------------------------------------------
    tab1, tab2, tab3 = st.tabs([
        "✨ สรุป MBTI & Cognitive Functions", 
        "🎓 คณะ/อาชีพ & แผนการเรียนตามงบ", 
        "📐 การพิสูจน์ตรรกศาสตร์"
    ])

    # ==========================================
    # TAB 1: MBTI & กราฟแท่ง
    # ==========================================
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

    # ==========================================
    # TAB 2: คณะ/อาชีพ & แผนการเรียนตามงบ (เพิ่มใหม่!)
    # ==========================================
    with tab2:
        st.subheader("🎓 คณะที่แนะนำ แนวทางการเรียน และมหาวิทยาลัยตามงบประมาณ")

        if rule_tech:
            st.markdown("""
            <div class="career-card">
                <h2>💻 กลุ่มเทคโนโลยี คำนวณ และวิศวกรรม</h2>
                <hr>
                <h4>💡 เหตุผลที่เหมาะกับสายนี้:</h4>
                <p>สมองของคุณเด่นด้านฟังก์ชันตรรกะและการคิดวิเคราะห์ ชอบหาเหตุผลเบื้องหลังของสิ่งต่างๆ และชอบความท้าทายในการแก้ปัญหาเชิงระบบ สายนี้ตอบโจทย์ความสามารถของคุณมากที่สุด</p>
                
                <div class="detail-box">
                    <h4>📌 แนวทางการเรียนต่อ & วิชาที่ควรเน้นศึกษาเพิ่ม:</h4>
                    <ul>
                        <li><b>สายการเรียน ม.ปลาย ที่แนะนำ:</b> วิทย์-คณิต หรือ ศิลป์-คำนวณ (หรือสายอาชีพ/ปวช. ช่างอิเล็กทรอนิกส์/คอมพิวเตอร์)</li>
                        <li><b>วิชาที่ควรเน้นในโรงเรียน:</b> คณิตศาสตร์ (แคลคูลัส, สถิติ, ตรรกศาสตร์) และ ภาษาอังกฤษ</li>
                        <li><b>ทักษะที่ควรเรียนรู้เพิ่มนอกห้องเรียน:</b> การเขียนโปรแกรมภาษาพื้นฐาน (Python, C++, JavaScript), อัลกอริทึม, โครงสร้างข้อมูล และภาษาอังกฤษเพื่อการสื่อสารทางเทคโนโลยี</li>
                    </ul>
                </div>

                <div class="detail-box">
                    <h4>🏫 แนะนำมหาวิทยาลัยแยกตามงบประมาณ:</h4>
                    <ul>
                        <li><b>งบน้อย / ต้องการทุนการศึกษา (ค่าเทอมต่ำกว่า 20,000 บาท/เทอม):</b><br>
                        - มหาวิทยาลัยรามคำแหง / มสธ. (ค่าเทอมถูกมาก เรียนควบคู่ได้)<br>
                        - กลุ่มมหาวิทยาลัยราชภัฏ และ มหาวิทยาลัยเทคโนโลยีราชมงคล (RMUT) ทั่วประเทศ<br>
                        - <i>*แนะนำ:* ยื่นขอทุน กยศ. หรือทุนคณะครุศาสตร์/ศึกษาศาสตร์ (คอมพิวเตอร์) จบแล้วมีโอกาสรับทุนครูคืนถิ่น</i></li>
                        
                        <li><b>งบปานกลาง (มหาวิทยาลัยรัฐบาลหลัก ค่าเทอม 15,000 - 35,000 บาท/เทอม):</b><br>
                        - จุฬาลงกรณ์มหาวิทยาลัย, มหาวิทยาลัยเกษตรศาสตร์, มหาวิทยาลัยมหิดล, มหาวิทยาลัยเชียงใหม่, มหาวิทยาลัยขอนแก่น<br>
                        - กลุ่ม 3 พระจอมเกล้า (สจล., มจธ., มจพ.) เด่นด้านวิศวะและไอที</li>
                        
                        <li><b>งบสูง / เน้นหลักสูตรอินเตอร์ หรือเอกชน (ค่าเทอม 50,000 บาทขึ้นไป/เทอม):</b><br>
                        - มหาวิทยาลัยกรุงเทพ, มหาวิทยาลัยรังสิต, มหาวิทยาลัยศรีปทุม (อุปกรณ์ทันสมัย คอนเนกชันสายเทคกว้าง)<br>
                        - หลักสูตรนานาชาติ เช่น SIIT มธ. หรือ คณะ ICT มหิดล</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif rule_health:
            st.markdown("""
            <div class="career-card">
                <h2>🏥 กลุ่มวิทยาศาสตร์ สุขภาพ และการดูแล</h2>
                <hr>
                <h4>💡 เหตุผลที่เหมาะกับสายนี้:</h4>
                <p>คุณมีความละเอียดรอบคอบ ละเอียดอ่อนต่อความรู้สึกของผู้คนรอบข้าง หรือชอบความมั่นคงและทำตามขั้นตอนที่เป็นระบบ งานสายนี้ต้องการความใส่ใจและความรับผิดชอบสูง ซึ่งตรงกับจุดแข็งของคุณ</p>
                
                <div class="detail-box">
                    <h4>📌 แนวทางการเรียนต่อ & วิชาที่ควรเน้นศึกษาเพิ่ม:</h4>
                    <ul>
                        <li><b>สายการเรียน ม.ปลาย ที่แนะนำ:</b> วิทย์-คณิต</li>
                        <li><b>วิชาที่ควรเน้นในโรงเรียน:</b> ชีววิทยา, เคมี, และ ฟิสิกส์</li>
                        <li><b>ทักษะที่ควรเรียนรู้เพิ่มนอกห้องเรียน:</b> ทักษะจิตวิทยาการสื่อสารการจับใจความ, ความรู้พื้นฐานปฐมพยาบาล, ทักษะภาษาอังกฤษเพื่อใช้จำศัพท์เฉพาะทางวิชาการ</li>
                    </ul>
                </div>

                <div class="detail-box">
                    <h4>🏫 แนะนำมหาวิทยาลัยแยกตามงบประมาณ:</h4>
                    <ul>
                        <li><b>งบน้อย / ต้องการทุนผูกพันจบแล้วมีงานทำทันที:</b><br>
                        - วิทยาลัยพยาบาลบรมราชชนนี (สถาบันพระบรมราชชนก) มีทุนเรียนฟรี มีเบี้ยเลี้ยง และจบแล้วบรรจุทำงานในโรงพยาบาลรัฐทันที<br>
                        - วิทยาลัยพยาบาลกองทัพบก / กองทัพเรือ / ทหารอากาศ / ตำรวจ (มีทุนการศึกษาและยศราชการ)</li>
                        
                        <li><b>งบปานกลาง (มหาวิทยาลัยรัฐบาล ค่าเทอม 15,000 - 30,000 บาท/เทอม):</b><br>
                        - มหาวิทยาลัยมหิดล (ศิริราช/รามาธิบดี), จุฬาลงกรณ์มหาวิทยาลัย, มหาวิทยาลัยเชียงใหม่, มหาวิทยาลัยสงขลานครินทร์, มหาวิทยาลัยบูรพา</li>
                        
                        <li><b>งบสูง / มหาวิทยาลัยเอกชน (ค่าเทอม 40,000 - 80,000 บาทขึ้นไป/เทอม):</b><br>
                        - มหาวิทยาลัยหัวเฉียวเฉลิมพระเกียรติ (เด่นด้านพยาบาล/การแพทย์แผนจีน), มหาวิทยาลัยรังสิต, มหาวิทยาลัยสยาม</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif rule_creative:
            st.markdown("""
            <div class="career-card">
                <h2>🎨 กลุ่มสร้างสรรค์ นวัตกรรม และสื่อดิจิทัล</h2>
                <hr>
                <h4>💡 เหตุผลที่เหมาะกับสายนี้:</h4>
                <p>สมองของคุณเด่นด้านจินตนาการและการมองหาความเป็นไปได้ใหม่ๆ (Extraverted Intuition) ชอบความยืดหยุ่น คิดนอกกรอบ และไม่ชอบการถูกจำกัดให้อยู่ในกฎเกณฑ์ที่ซ้ำซาก</p>
                
                <div class="detail-box">
                    <h4>📌 แนวทางการเรียนต่อ & วิชาที่ควรเน้นศึกษาเพิ่ม:</h4>
                    <ul>
                        <li><b>สายการเรียน ม.ปลาย ที่แนะนำ:</b> ศิลป์-คำนวณ, ศิลป์-ภาษา, ศิลป์-ดิจิทัล/คอมพิวเตอร์ (หรือทุกสายที่มีความสนใจด้านศิลปะ)</li>
                        <li><b>วิชาที่ควรเน้นในโรงเรียน:</b> ศิลปะ, ภาษาอังกฤษ, ภาษาไทย (การจับใจความและเล่าเรื่อง)</li>
                        <li><b>ทักษะที่ควรเรียนรู้เพิ่มนอกห้องเรียน:</b> การใช้โปรแกรมออกแบบ (Adobe Photoshop, Illustrator, Figma), ทักษะการตัดต่อวิดีโอ (Premiere Pro, CapCut), การสะสมผลงาน (Portfolio) และการศึกษาเทรนด์การตลาดดิจิทัล</li>
                    </ul>
                </div>

                <div class="detail-box">
                    <h4>🏫 แนะนำมหาวิทยาลัยแยกตามงบประมาณ:</h4>
                    <ul>
                        <li><b>งบน้อย / เน้นประหยัด (ค่าเทอม 10,000 - 20,000 บาท/เทอม):</b><br>
                        - มหาวิทยาลัยเทคโนโลยีราชมงคล (เช่น มทร.รัตนโกสินทร์ เพาะช่าง, มทร.ธัญบุรี)<br>
                        - มหาวิทยาลัยราชภัฏ (คณะมนุษยศาสตร์/นิเทศศาสตร์/ศิลปกรรมศาสตร์) ค่าเทอมประหยัด อุปกรณ์ครบถ้วน</li>
                        
                        <li><b>งบปานกลาง (มหาวิทยาลัยรัฐบาลสายสร้างสรรค์ ค่าเทอม 18,000 - 35,000 บาท/เทอม):</b><br>
                        - มหาวิทยาลัยศิลปากร (ต้นตำรับสายศิลปะและนิเทศ), จุฬาลงกรณ์มหาวิทยาลัย (สถาปัตย์/นิเทศ), มหาวิทยาลัยธรรมศาสตร์, มหาวิทยาลัยศรีนครินทรวิโรฒ (มศว)</li>
                        
                        <li><b>งบสูง / มหาวิทยาลัยเอกชนอุปกรณ์ระดับสตูดิโอ (ค่าเทอม 45,000 - 70,000 บาทขึ้นไป/เทอม):</b><br>
                        - มหาวิทยาลัยกรุงเทพ (คณะนิเทศศาสตร์ / คณะดิจิทัลมีเดีย โดดเด่นด้านอุปกรณ์ระดับมืออาชีพ)<br>
                        - มหาวิทยาลัยรังสิต, มหาวิทยาลัยศรีปทุม (มีสาขาเกม การ์ตูน และการออกแบบดิจิทัลเฉพาะทาง)</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="career-card">
                <h2>🏛️ กลุ่มบริหารจัดการ สังคมศาสตร์ และภาษา</h2>
                <hr>
                <h4>💡 เหตุผลที่เหมาะกับสายนี้:</h4>
                <p>คุณมีทักษะในการประเมินคุณค่า การสื่อสารกับผู้คน หรือการจัดระเบียบงานและองค์กร สายงานนี้ต้องการคนที่ยืดหยุ่น สามารถทำงานร่วมกับคนหลากหลายรูปแบบได้อย่างราบรื่น</p>
                
                <div class="detail-box">
                    <h4>📌 แนวทางการเรียนต่อ & วิชาที่ควรเน้นศึกษาเพิ่ม:</h4>
                    <ul>
                        <li><b>สายการเรียน ม.ปลาย ที่แนะนำ:</b> ศิลป์-คำนวณ, ศิลป์-ภาษา หรือ วิทย์-คณิต</li>
                        <li><b>วิชาที่ควรเน้นในโรงเรียน:</b> ภาษาไทย, ภาษาอังกฤษ, สังคมศึกษา และ คณิตศาสตร์พื้นฐาน/สถิติ</li>
                        <li><b>ทักษะที่ควรเรียนรู้เพิ่มนอกห้องเรียน:</b> ภาษาที่ 3 (เช่น จีน, ญี่ปุ่น, เกาหลี, สเปน), ทักษะการพูดนำเสนอ (Presentation), ความรู้พื้นฐานการทำธุรกิจและการตลาดออนไลน์</li>
                    </ul>
                </div>

                <div class="detail-box">
                    <h4>🏫 แนะนำมหาวิทยาลัยแยกตามงบประมาณ:</h4>
                    <ul>
                        <li><b>งบน้อย / เน้นการทำงานควบคู่ (ค่าเทอมต่ำกว่า 15,000 บาท/เทอม):</b><br>
                        - มหาวิทยาลัยรามคำแหง (คณะบริหาร, รัฐศาสตร์, นิติศาสตร์, มนุษยศาสตร์ สามารถจัดเวลาเรียนเองได้ง่าย)<br>
                        - มหาวิทยาลัยสุโขทัยธรรมาธิราช (เรียนทางไกล)<br>
                        - กลุ่มมหาวิทยาลัยราชภัฏทั่วประเทศ สามารถกู้ยืม กยศ. เรียนได้สะดวก</li>
                        
                        <li><b>งบปานกลาง (มหาวิทยาลัยรัฐบาลชั้นนำ ค่าเทอม 15,000 - 30,000 บาท/เทอม):</b><br>
                        - มหาวิทยาลัยธรรมศาสตร์ (เด่นด้านนิติศาสตร์, รัฐศาสตร์, บริหารธุรกิจ ชานม/ท่าพระจันทร์)<br>
                        - จุฬาลงกรณ์มหาวิทยาลัย (พาณิชยศาสตร์และการบัญชี, อักษรศาสตร์), มหาวิทยาลัยเกษตรศาสตร์, มหาวิทยาลัยเชียงใหม่</li>
                        
                        <li><b>งบสูง / มหาวิทยาลัยนานาชาติหรือเอกชน (ค่าเทอม 45,000 บาทขึ้นไป/เทอม):</b><br>
                        - มหาวิทยาลัยอัสสัมชัญ (ABAC - เด่นการเรียนการสอนเป็นภาษาอังกฤษทั้งหมด)<br>
                        - มหาวิทยาลัยหอการค้าไทย (เด่นสายธุรกิจ คอนเนกชันหอการค้า), มหาวิทยาลัยกรุงเทพ</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # TAB 3: พิสูจน์ตรรกศาสตร์
    # ==========================================
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
        st.rerun()
