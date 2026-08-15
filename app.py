import streamlit as st
from questions import (
    COGNITIVE_QUESTIONS, 
    SUBJECT_QUESTIONS, 
    HOBBY_QUESTIONS, 
    GOAL_QUESTIONS, 
    FINANCIAL_QUESTIONS,
    MBTI_DESCRIPTIONS
)

# ---------------------------------------------------------
# 1. การตั้งค่าหน้าตาเว็บ (Page Configuration)
# ---------------------------------------------------------
st.set_page_config(
    page_title="ระบบวิเคราะห์เส้นทางเรียนและอาชีพตามตัวตน",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------------------------------------
# 2. จัดการ Session State (ระบบจำสถานะแบบ Step-by-Step)
# ---------------------------------------------------------
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'mbti_result' not in st.session_state:
    st.session_state.mbti_result = "ENTP"
if 'top_functions' not in st.session_state:
    st.session_state.top_functions = []
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {}

# สเกลการตอบคำถาม 1-5 (Likert Scale)
SCALE_OPTIONS = {
    "1 - ไม่ตรงเลย": 1,
    "2 - ไม่ค่อยตรง": 2,
    "3 - ปานกลาง / ไม่แน่ใจ": 3,
    "4 - ค่อนข้างตรง": 4,
    "5 - ตรงมากที่สุด": 5
}

# ---------------------------------------------------------
# STEP 1: ประเมิน Cognitive Functions (80 ข้อ)
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.title("🧩 ขั้นตอนที่ 1: ประเมินบุคลิกภาพ (Cognitive Functions 80 ข้อ)")
    st.write("โปรดเลือกสเกลที่ตรงกับความเป็นจริงของคุณมากที่สุด (1 = ไม่ตรงเลย, 5 = ตรงมากที่สุด)")
    
    with st.form("mbti_form"):
        cog_responses = {}
        
        # วนลูปคำถาม 80 ข้อ
        for idx, q in enumerate(COGNITIVE_QUESTIONS, 1):
            st.markdown(f"**ข้อที่ {idx}:** {q['text']}")
            ans = st.radio(
                f"ระดับความตรง (ข้อ {idx}):", 
                options=list(SCALE_OPTIONS.keys()), 
                index=2, 
                key=f"cog_{q['id']}",
                horizontal=True
            )
            cog_responses[q["func"]] = cog_responses.get(q["func"], 0) + SCALE_OPTIONS[ans]
            st.markdown("<hr style='margin: 0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)
            
        submitted = st.form_submit_button("🚀 ประมวลผลบุคลิกภาพ MBTI (Step 1)")
        
        if submitted:
            # รวมคะแนนหา Cognitive Functions หลัก
            sorted_funcs = sorted(cog_responses.items(), key=lambda x: x[1], reverse=True)
            top_funcs = [f[0] for f in sorted_funcs[:4]]
            st.session_state.top_functions = top_funcs
            
            # คำนวณรหัส MBTI เบื้องต้นจาก Cognitive Functions
            ne_ni = cog_responses.get("Ne", 0) + cog_responses.get("Ni", 0)
            se_si = cog_responses.get("Se", 0) + cog_responses.get("Si", 0)
            ti_te = cog_responses.get("Ti", 0) + cog_responses.get("Te", 0)
            fi_fe = cog_responses.get("Fi", 0) + cog_responses.get("Fe", 0)
            
            p_or_s = "N" if ne_ni >= se_si else "S"
            t_or_f = "T" if ti_te >= fi_fe else "F"
            e_or_i = "E" if (cog_responses.get("Ne", 0) + cog_responses.get("Se", 0) + cog_responses.get("Te", 0) + cog_responses.get("Fe", 0)) >= \
                           (cog_responses.get("Ni", 0) + cog_responses.get("Si", 0) + cog_responses.get("Ti", 0) + cog_responses.get("Fi", 0)) else "I"
            j_or_p = "P" if (cog_responses.get("Ne", 0) + cog_responses.get("Se", 0)) >= (cog_responses.get("Ni", 0) + cog_responses.get("Si", 0)) else "J"
            
            mbti_code = f"{e_or_i}{p_or_s}{t_or_f}{j_or_p}"
            if mbti_code not in MBTI_DESCRIPTIONS:
                mbti_code = "ENFP"
                
            st.session_state.mbti_result = mbti_code
            st.session_state.step = 2
            st.rerun()

# ---------------------------------------------------------
# STEP 2: สรุปผลลัพธ์ MBTI ทันที (คุยโต้ตอบทีละขั้น)
# ---------------------------------------------------------
elif st.session_state.step == 2:
    st.title("🌟 ขั้นตอนที่ 2: สรุปผลลัพธ์บุคลิกภาพของคุณ")
    
    mbti = st.session_state.mbti_result
    info = MBTI_DESCRIPTIONS.get(mbti, MBTI_DESCRIPTIONS["ENTP"])
    funcs = st.session_state.top_functions
    
    st.success(f"### ผลการวิเคราะห์: คุณมีบุคลิกภาพแบบ **{mbti}** ({info['title']})")
    st.info(f"**ลักษณะตัวตนของคุณ:** {info['desc']}")
    
    if funcs:
        st.write(f"🧩 **Cognitive Functions โดดเด่นของคุณ:** {', '.join(funcs)}")
    
    st.markdown("---")
    st.write("📌 *ยืนยันผลลัพธ์บุคลิกภาพข้างต้น แล้วกดไปต่อเพื่อทำแบบประเมินความชอบและเงื่อนไขของคุณ*")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ ทำแบบประเมิน MBTI ใหม่"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("➡️ ไปต่อ: ประเมินความชอบ & ทุนการเงิน (Step 3)"):
            st.session_state.step = 3
            st.rerun()

# ---------------------------------------------------------
# STEP 3: ประเมินความชอบ วิชา งานอดิเรก เป้าหมาย ทุนการเงิน
# ---------------------------------------------------------
elif st.session_state.step == 3:
    st.title("🎯 ขั้นตอนที่ 3: ระบุวิชาที่ชอบ งานอดิเรก เป้าหมาย และทุนการเงิน")
    st.write("ส่วนนี้จะนำความชอบจริงของคุณไปผสมผสานกับ MBTI เพื่อให้อาชีพไม่แคบและตรงใจมากที่สุด")
    
    with st.form("preference_form"):
        # 1. หมวดวิชา
        st.subheader("📚 1. ความชอบหมวดวิชาการ")
        sub_scores = {}
        for q in SUBJECT_QUESTIONS:
            ans = st.radio(f"{q['text']} ({q['category']}):", options=list(SCALE_OPTIONS.keys()), index=2, key=f"sub_{q['id']}", horizontal=True)
            sub_scores[q["category"]] = sub_scores.get(q["category"], 0) + SCALE_OPTIONS[ans]
            
        st.markdown("---")
        # 2. งานอดิเรก
        st.subheader("🎨 2. ความสนใจและงานอดิเรก")
        hob_scores = {}
        for q in HOBBY_QUESTIONS:
            ans = st.radio(f"{q['text']} ({q['category']}):", options=list(SCALE_OPTIONS.keys()), index=2, key=f"hob_{q['id']}", horizontal=True)
            hob_scores[q["category"]] = hob_scores.get(q["category"], 0) + SCALE_OPTIONS[ans]
            
        st.markdown("---")
        # 3. เป้าหมายการทำงาน
        st.subheader("🎯 3. สไตล์และเป้าหมายการทำงาน")
        goal_scores = {}
        for q in GOAL_QUESTIONS:
            ans = st.radio(f"{q['text']} ({q['category']}):", options=list(SCALE_OPTIONS.keys()), index=2, key=f"goal_{q['id']}", horizontal=True)
            goal_scores[q["category"]] = goal_scores.get(q["category"], 0) + SCALE_OPTIONS[ans]

        st.markdown("---")
        # 4. เงื่อนไขทางการเงิน 5 ข้อ
        st.subheader("💰 4. เงื่อนไขและงบประมาณการศึกษา")
        fin_answers = {}
        for q in FINANCIAL_QUESTIONS:
            ans = st.selectbox(q["label"], options=q["options"], key=f"fin_{q['id']}")
            fin_answers[q["id"]] = ans

        submitted_step3 = st.form_submit_button("🚀 ประมวลผลสรุปเส้นทางอนาคต (Step 4)")
        
        if submitted_step3:
            # สรุปอันดับวิชาและงานอดิเรกที่ได้คะแนนสูงสุด
            top_subject = max(sub_scores, key=sub_scores.get)
            top_hobby = max(hob_scores, key=hob_scores.get)
            
            st.session_state.user_preferences = {
                "top_subject": top_subject,
                "top_hobby": top_hobby,
                "financial": fin_answers
            }
            st.session_state.step = 4
            st.rerun()

# ---------------------------------------------------------
# STEP 4: สรุปผลลัพธ์อาชีพและสถาบันการศึกษา
# ---------------------------------------------------------
elif st.session_state.step == 4:
    st.balloons()
    st.title("🎓 ขั้นตอนที่ 4: สรุปผลลัพธ์อาชีพและสถาบันการศึกษาที่ใช่สำหรับคุณ")
    
    mbti = st.session_state.mbti_result
    prefs = st.session_state.user_preferences
    top_subject = prefs.get("top_subject", "Math & Logic")
    top_hobby = prefs.get("top_hobby", "Tech & Gaming")
    fin = prefs.get("financial", {})

    budget_ans = fin.get("fin_budget", "")
    scholar_ans = fin.get("fin_scholarship_need", "")

    # แสดงโปรไฟล์ผู้ใช้
    st.markdown(f"""
    <div style="background-color: #F0F9FF; border: 1px solid #BAE6FD; padding: 1.2rem; border-radius: 10px; margin-bottom: 1.5rem;">
        <b>👤 โปรไฟล์สรุปของคุณ:</b><br>
        • MBTI: <b>{mbti}</b><br>
        • วิชาที่โดดเด่นที่สุด: <b>{top_subject}</b><br>
        • หมวดงานอดิเรกที่ใช่: <b>{top_hobby}</b><br>
        • เงื่อนไขการเงิน: <b>{budget_ans}</b>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # วิเคราะห์อาชีพ dynamic ผสม MBTI + วิชา + งานอดิเรก
    # -----------------------------------------------------
    st.subheader("💼 เส้นทางอาชีพที่แนะนำสำหรับคุณ")
    
    career_list = []
    if top_subject == "Natural Science" or top_hobby == "Hands-on":
        career_list = [
            {"title": f"พยาบาลวิชาชีพ / บุคลากรทางการแพทย์ (สไตล์ {mbti})", "desc": "เหมาะกับผู้ที่สนใจสายสุขภาพ นำทักษะการดูแลและตรรกะมาประยุกต์ใช้กับชีวิตมนุษย์จริง"},
            {"title": "นักวิชาการสาธารณสุข / นักวิจัยวิทยาศาสตร์", "desc": "เน้นการวิเคราะห์ข้อมูลและสร้างนวัตกรรมเพื่อพัฒนาสุขภาวะในสังคม"}
        ]
    elif top_subject == "Technology" or top_subject == "Math & Logic" or top_hobby == "Tech & Gaming":
        career_list = [
            {"title": f"Software Engineer / Data Scientist (สไตล์ {mbti})", "desc": "นำตรรกะและการวิเคราะห์เชิงระบบมาสร้างสรรค์เทคโนโลยีและแก้ปัญหาซับซ้อน"},
            {"title": "นักออกแบบระบบไอที / Cybersecurity Specialist", "desc": "ใช้วิธีคิดเชิงโครงสร้างเพื่อวางระบบความปลอดภัยและเทคโนโลยีแห่งอนาคต"}
        ]
    elif top_subject == "Art & Design" or top_hobby == "Creative":
        career_list = [
            {"title": f"UX/UI Designer / Creative Director (สไตล์ {mbti})", "desc": "ผสมผสานศิลปะ ความเข้าใจมนุษย์ และเทคโนโลยีเข้าด้วยกันเพื่อสร้างประสบการณ์ผู้ใช้"},
            {"title": "นักจัดทำคอนเทนต์ / สื่อมวลชนดิจิทัล", "desc": "สื่อสารเรื่องราวและสร้างแรงบันดาลใจผ่านสื่อหลากหลายรูปแบบ"}
        ]
    else:
        career_list = [
            {"title": f"นักวางแผนกลยุทธ์ / นักการตลาด (สไตล์ {mbti})", "desc": "บริหารจัดการ บริหารคน และวางแผนการตลาดเพื่อให้บรรลุเป้าหมายองค์กร"},
            {"title": "นักการทูต / นักวิเคราะห์นโยบายสังคม", "desc": "ใช้วาทศิลป์และความเข้าใจพฤติกรรมมนุษย์ในการสร้างความร่วมมือ"}
        ]

    col_c1, col_c2 = st.columns(2)
    for idx, c in enumerate(career_list):
        with (col_c1 if idx % 2 == 0 else col_c2):
            st.markdown(f"""
            <div style="background-color: white; border: 2px solid #3B82F6; padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;">
                <h4 style="color: #1E3A8A; margin-top:0;">{c['title']}</h4>
                <p style="color: #475569;">{c['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # วิเคราะห์สถาบันตามเงื่อนไขงบประมาณและทุน
    # -----------------------------------------------------
    st.subheader("🏛️ สถาบันการศึกษาและทุนการศึกษาที่แนะนำ")
    
    if "จำกัดสูง" in budget_ans or "สนใจมาก" in scholar_ans:
        st.success("""
        **🎓 แนะนำสถาบันทุนเรียนฟรี / มีเบี้ยเลี้ยง / มีประกันงานทำ 100%:**
        - **สถาบันพระบรมราชชนก / วิทยาลัยพยาบาลบรมราชชนนี:** ทุนเรียนฟรี มีเบี้ยเลี้ยง จบแล้วบรรจุเป็นข้าราชการทันที
        - **วิทยาลัยพยาบาลเหล่าทัพ (ทหารบก / ทหารเรือ / ทหารอากาศ / ตำรวจ):** ทุนเต็มจำนวนพร้อมสวัสดิการ บรรจุเป็นนายทหาร/ตำรวจ
        - **ทุนครูคืนถิ่น / ทุนผลิตครูเพื่อพัฒนาท้องถิ่น:** ทุนการศึกษาพร้อมการันตีบรรจุตำแหน่งครูในภูมิลำเนา
        - **ทุน กยศ. / กรอ.:** สนับสนุนค่าเล่าเรียนสำหรับสถาบันรัฐและเอกชนที่เข้าร่วม
        """)
    elif "ปานกลาง" in budget_ans:
        st.info("""
        **🏛️ แนะนำมหาวิทยาลัยรัฐบาลหลัก (ค่าเทอมตามมาตรฐาน):**
        - **สายสุขภาพ/วิทยาศาสตร์:** มหาวิทยาลัยมหิดล, จุฬาลงกรณ์มหาวิทยาลัย, มหาวิทยาลัยเชียงใหม่
        - **สายเทคโนโลยี/วิศวะ:** กลุ่ม 3 พระจอมเกล้า (สจล., มจธ., มจพ.), มหาวิทยาลัยเกษตรศาสตร์
        - **สายสังคม/บริหาร/ศิลปะ:** มหาวิทยาลัยธรรมศาสตร์, มหาวิทยาลัยศิลปากร, มศว
        """)
    else:
        st.warning("""
        **🌟 แนะนำสถาบันเอกชนชั้นนำ / หลักสูตรนานาชาติ:**
        - **มหาวิทยาลัยเอกชน:** มหาวิทยาลัยกรุงเทพ, มหาวิทยาลัยรังสิต, มหาวิทยาลัยศรีปทุม, มหาวิทยาลัยอัสสัมชัญ (ABAC)
        - **หลักสูตรนานาชาติมหาลัยรัฐ:** SIIT มหาวิทยาลัยธรรมศาสตร์, ICT มหาวิทยาลัยมหิดล, ISE จุฬาลงกรณ์มหาวิทยาลัย
        """)

    st.markdown("---")
    if st.button("🔄 เริ่มทำแบบประเมินใหม่อีกครั้ง"):
        st.session_state.step = 1
        st.session_state.user_preferences = {}
        st.rerun()
