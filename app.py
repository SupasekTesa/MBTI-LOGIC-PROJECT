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
# STEP 1: ประเมิน Cognitive Functions (80 ข้อ + คำนวณละเอียด)
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.title("🧩 ขั้นตอนที่ 1: ประเมินบุคลิกภาพ (Cognitive Functions 80 ข้อ)")
    st.write("โปรดเลือกสเกลที่ตรงกับความเป็นจริงของคุณมากที่สุด (1 = ไม่ตรงเลย, 5 = ตรงมากที่สุด)")
    
    with st.form("mbti_form"):
        # เก็บคำตอบแยกตาม ID ข้อสอบเพื่อป้องกันข้อมูลตีกัน
        raw_answers = {}
        for idx, q in enumerate(COGNITIVE_QUESTIONS, 1):
            st.markdown(f"**ข้อที่ {idx}:** {q['text']}")
            ans = st.radio(
                f"ระดับความตรง (ข้อ {idx}):", 
                options=list(SCALE_OPTIONS.keys()), 
                index=2, 
                key=f"cog_{q['id']}",
                horizontal=True
            )
            raw_answers[q['id']] = {"func": q["func"], "score": SCALE_OPTIONS[ans]}
            st.markdown("<hr style='margin: 0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)
            
        submitted = st.form_submit_button("🚀 ประมวลผลและคำนวณตรรกศาสตร์ MBTI (Step 1)")
        
        if submitted:
            # 1. รวมคะแนนแยกตามฟังก์ชัน (เต็ม 50 คะแนนต่อฟังก์ชัน)
            func_scores = {"Ne": 0, "Ni": 0, "Se": 0, "Si": 0, "Te": 0, "Ti": 0, "Fe": 0, "Fi": 0}
            for item in raw_answers.values():
                func_scores[item["func"]] += item["score"]

            # 2. คำนวณเปอร์เซ็นต์ความเด่นของแต่ละฟังก์ชัน
            func_percentages = {func: round((score / 50) * 100, 1) for func, score in func_scores.items()}

            # 3. จัดลำดับฟังก์ชันจากมากไปน้อย
            sorted_funcs = sorted(func_scores.items(), key=lambda x: x[1], reverse=True)
            
            # บันทึกค่าลง session_state สำหรับนำไปแสดงผลละเอียด
            st.session_state.func_scores = func_scores
            st.session_state.func_percentages = func_percentages
            st.session_state.sorted_funcs = sorted_funcs
            st.session_state.top_functions = [f[0] for f in sorted_funcs[:4]]

            # 4. คำนวณแกน MBTI ทั้ง 4 มิติเชิงปริมาณ
            extroversion = func_scores["Ne"] + func_scores["Se"] + func_scores["Te"] + func_scores["Fe"]
            introversion = func_scores["Ni"] + func_scores["Si"] + func_scores["Ti"] + func_scores["Fi"]
            
            intuition = func_scores["Ne"] + func_scores["Ni"]
            sensing = func_scores["Se"] + func_scores["Si"]
            
            thinking = func_scores["Te"] + func_scores["Ti"]
            feeling = func_scores["Fe"] + func_scores["Fi"]

            perceiving = func_scores["Ne"] + func_scores["Se"]
            judging = func_scores["Ni"] + func_scores["Si"]

            dim_e_i = "E" if extroversion >= introversion else "I"
            dim_n_s = "N" if intuition >= sensing else "S"
            dim_t_f = "T" if thinking >= feeling else "F"
            dim_p_j = "P" if perceiving >= judging else "J"

            mbti_code = f"{dim_e_i}{dim_n_s}{dim_t_f}{dim_p_j}"
            if mbti_code not in MBTI_DESCRIPTIONS:
                mbti_code = "ENFP"
                
            st.session_state.mbti_result = mbti_code
            st.session_state.step = 2
            st.rerun()

# ---------------------------------------------------------
# STEP 2: สรุปผลลัพธ์การคำนวณละเอียด
# ---------------------------------------------------------
elif st.session_state.step == 2:
    st.title("🌟 ขั้นตอนที่ 2: สรุปผลลัพธ์และรายงานการคำนวณตรรกศาสตร์")
    
    mbti = st.session_state.mbti_result
    info = MBTI_DESCRIPTIONS.get(mbti, MBTI_DESCRIPTIONS["ENTP"])
    sorted_funcs = st.session_state.get("sorted_funcs", [])
    func_pct = st.session_state.get("func_percentages", {})
    func_raw = st.session_state.get("func_scores", {})
    
    st.success(f"### ผลการวิเคราะห์: บุคลิกภาพของคุณคือ **{mbti}** ({info['title']})")
    st.info(f"**ลักษณะตัวตน:** {info['desc']}")
    
    # แสดงตารางวิเคราะห์ Cognitive Function Stack แบบละเอียด
    st.subheader("📊 ตรรกศาสตร์การคำนวณ Cognitive Functions (คะแนนเต็ม 50 คะแนน)")
    
    col_chart, col_rank = st.columns([3, 2])
    
    with col_chart:
        st.markdown("**ระดับความเข้มข้นของแต่ละฟังก์ชัน (%):**")
        for func_code, score in sorted_funcs:
            pct = func_pct.get(func_code, 0)
            st.write(f"**{func_code}**: {score}/50 คะแนน ({pct}%)")
            st.progress(pct / 100)
            
    with col_rank:
        st.markdown("**การจัดลำดับตามทฤษฎี (Cognitive Stack):**")
        if len(sorted_funcs) >= 8:
            st.write(f"🥇 **Dominant (ฟังก์ชันหลัก):** `{sorted_funcs[0][0]}` ({func_pct[sorted_funcs[0][0]]}%)")
            st.write(f"🥈 **Auxiliary (ฟังก์ชันรอง):** `{sorted_funcs[1][0]}` ({func_pct[sorted_funcs[1][0]]}%)")
            st.write(f"🥉 **Tertiary (ฟังก์ชันลำดับสาม):** `{sorted_funcs[2][0]}` ({func_pct[sorted_funcs[2][0]]}%)")
            st.write(f"⚓ **Inferior (จุดที่ต้องพัฒนา):** `{sorted_funcs[-1][0]}` ({func_pct[sorted_funcs[-1][0]]}%)")

    st.markdown("---")
    
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
