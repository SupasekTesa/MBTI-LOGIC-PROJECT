import streamlit as st

# ==========================================
# 1. ตั้งค่าหน้าเว็บ และ CSS ตกแต่งความสวยงาม
# ==========================================
st.set_page_config(
    page_title="ระบบประมวลผลตรรกศาสตร์เพื่อการศึกษาต่อ",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS เพื่อความสวยงาม สไตล์ Modern Dashboard
st.markdown("""
<style>
    /* แบ็กกราวด์และฟอนต์หลัก */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* หัวข้อหลัก */
    .header-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 2.5rem 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.2);
        margin-bottom: 2rem;
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .header-sub {
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* การ์ดคำถามและผลลัพธ์ */
    .custom-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }

    /* กล่องแสดงผลตรรกศาสตร์ */
    .logic-box {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-left: 6px solid #2563EB;
        border-radius: 8px;
        padding: 1.2rem;
        font-family: 'Courier New', monospace;
        color: #1E40AF;
        line-height: 1.6;
    }

    /* ป้ายแสดงประเภท MBTI / Function */
    .badge-mbti {
        background-color: #2563EB;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        display: inline-block;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. คลังคำถาม (แก้ไข/เพิ่มคำถามตรงนี้ได้เลย)
# ==========================================

# 2.1 คำถาม Cognitive Functions (8 ด้าน)
COGNITIVE_QUESTIONS = [
    {"id": "q_te", "func": "Te", "label": "1. ฉันชอบวางแผนที่เป็นระบบ เน้นผลลัพธ์ที่วัดผลได้ และจัดการสิ่งต่างๆ ให้มีประสิทธิภาพสูงสุด"},
    {"id": "q_ti", "func": "Ti", "label": "2. ฉันชอบวิเคราะห์เจาะลึก รื้อดูระบบภายใน เพื่อเข้าใจหลักการทำงานที่แท้จริงอย่างแม่นยำ"},
    {"id": "q_fe", "func": "Fe", "label": "3. ฉันแคร์ความรู้สึกของคนรอบข้าง ไวต่อบรรยากาศกลุ่ม และชอบสร้างความเข้าใจอันดีระหว่างกัน"},
    {"id": "q_fi", "func": "Fi", "label": "4. ฉันยึดมั่นในคุณค่า จริยธรรม และความรู้สึกที่แท้จริงจากภายในของตัวเองเป็นสำคัญ"},
    {"id": "q_ne", "func": "Ne", "label": "5. ฉันชอบคิดนอกกรอบ เชื่อมโยงไอเดียใหม่ๆ และเห็นความเป็นไปได้ที่หลากหลาย"},
    {"id": "q_ni", "func": "Ni", "label": "6. ฉันชอบมองภาพรวมในอนาคต มักมีลางสังหรณ์แม่นยำ และมุ่งสู่เป้าหมายระยะยาว"},
    {"id": "q_se", "func": "Se", "label": "7. ฉันตอบสนองต่อสิ่งแวดล้อมรอบตัวได้ดี ชอบลงมือปฏิบัติจริง และสนุกกับปัจจุบัน"},
    {"id": "q_si", "func": "Si", "label": "8. ฉันให้ความสำคัญกับรายละเอียด ประสบการณ์ในอดีต กฎระเบียบ และความมั่นคง"}
]

# 2.2 คำถามมิติ MBTI เสริม
MBTI_DIMENSIONS = [
    {
        "id": "dim_ei",
        "title": "⚡ มิติการรับพลังงาน (E vs I)",
        "options": ["Extraversion (E): ชอบเข้าสังคม กิจกรรมกลุ่ม ได้พลังงานจากคนรอบข้าง", 
                    "Introversion (I): ชอบความสงบ ชาร์จพลังงานจากการอยู่คนเดียว"]
    },
    {
        "id": "dim_jp",
        "title": "📅 มิติลักษณะการใช้ชีวิต (J vs P)",
        "options": ["Judging (J): ชอบวางแผนล่วงหน้า ทำงานมีระเบียบแบบแผนชัดเจน", 
                    "Perceiving (P): ยืดหยุ่น ปรับเปลี่ยนตามสถานการณ์ ชอบทำงานใกล้เดดไลน์"]
    }
]


# ==========================================
# 3. ส่วนหัวของเว็บไซต์ (Header)
# ==========================================
st.markdown("""
<div class="header-box">
    <div class="header-title">🎓 ระบบวัดแววเลือกคณะและอาชีพด้วยตรรกศาสตร์</div>
    <div class="header-sub">โครงงานคณิตศาสตร์บูรณาการ: ตรรกศาสตร์ + MBTI Cognitive Functions + ปัจจัยทุนการศึกษา</div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 4. จัดการขั้นตอนทำแบบสอบถาม (Step Management)
# ==========================================
if "step" not in st.session_state:
    st.session_state.step = 1

# แสดง Progress Bar
progress_val = (st.session_state.step - 1) / 2
st.progress(progress_val)


# ------------------------------------------
# ขั้นตอนที่ 1: ตอบแบบประเมินบุคลิกภาพ & ความสนใจ
# ------------------------------------------
if st.session_state.step == 1:
    st.subheader("📋 แบบสอบถามวัดแววและความสนใจ")
    
    with st.form("assessment_form"):
        
        # ส่วนที่ 1: Cognitive Functions
        st.markdown("### 🧠 1. ประเมินกระบวนการคิด (Cognitive Functions)")
        st.caption("เลือกสเกล 1 (ไม่จริงเลย) ถึง 5 (ตรงกับฉันมากที่สุด)")
        
        cog_answers = {}
        col_a, col_b = st.columns(2)
        
        for idx, q in enumerate(COGNITIVE_QUESTIONS):
            # สลับลงคอลัมน์ซ้าย-ขวา เพื่อความสวยงาม
            target_col = col_a if idx % 2 == 0 else col_b
            with target_col:
                cog_answers[q["func"]] = st.slider(
                    q["label"], min_value=1, max_value=5, value=3, key=q["id"]
                )

        st.divider()

        # ส่วนที่ 2: MBTI Dimensions
        st.markdown("### 🎭 2. มิติบุคลิกภาพเพิ่มเติม")
        mbti_answers = {}
        for dim in MBTI_DIMENSIONS:
            mbti_answers[dim["id"]] = st.radio(dim["title"], dim["options"], key=dim["id"])

        st.divider()

        # ส่วนที่ 3: วิชาที่ชอบและเงื่อนไขทุน
        st.markdown("### 📚 3. วิชาที่ชอบและเงื่อนไขทุนทรัพย์")
        col_c, col_d = st.columns(2)
        
        with col_c:
            subject = st.selectbox(
                "กลุ่มรายวิชาที่ชอบ/ถนัดที่สุด:",
                [
                    "กลุ่มคำนวณ เทคโนโลยี และตรรกะ (คณิตศาสตร์, ฟิสิกส์, IT)",
                    "กลุ่มวิทยาศาสตร์ชีวภาพ สุขภาพ (เคมี, ชีววิทยา, สุขภาพ)",
                    "กลุ่มภาษา สื่อสาร สังคม และบริหาร (ภาษา, สังคม, การตลาด)",
                    "กลุ่มศิลปะ ออกแบบ และงานสร้างสรรค์ (การออกแบบ, ดนตรี, สื่อ)"
                ]
            )
            
        with col_d:
            capital = st.radio(
                "เงื่อนไขและข้อจำกัดด้านทุนการศึกษา:",
                [
                    "มีข้อจำกัดสูง (ต้องการคณะมีทุนเรียนฟรี / จบแล้วมีงานทำทันที)",
                    "ไม่มีข้อจำกัด หรือมีทุนทรัพย์ปานกลางถึงสูง"
                ]
            )

        submit_btn = st.form_submit_button("🚀 ประมวลผลด้วยตรรกศาสตร์คณิตศาสตร์", use_container_width=True)
        
        if submit_btn:
            # บันทึกค่าลง Session State
            st.session_state.cog_scores = cog_answers
            st.session_state.mbti_answers = mbti_answers
            st.session_state.subject = subject
            st.session_state.capital = capital
            st.session_state.step = 2
            st.rerun()


# ------------------------------------------
# ขั้นตอนที่ 2: ประมวลผลตรรกศาสตร์ & แสดงผลลัพธ์
# ------------------------------------------
elif st.session_state.step == 2:
    
    # 1. ดึงค่าที่บันทึกไว้
    cog_scores = st.session_state.get("cog_scores", {})
    mbti_ans = st.session_state.get("mbti_answers", {})
    subject = st.session_state.get("subject", "")
    capital = st.session_state.get("capital", "")

    # 2. คำนวณฟังก์ชันเด่น (Dominant Cognitive Function)
    dom_func = max(cog_scores, key=cog_scores.get)
    
    # คำนวณ MBTI ย่อ
    e_or_i = "E" if "Extraversion" in mbti_ans.get("dim_ei", "") else "I"
    j_or_p = "J" if "Judging" in mbti_ans.get("dim_jp", "") else "P"
    mbti_summary = f"{e_or_i}-{dom_func}-{j_or_p}"

    # 3. แปลงเป็นตัวแปรประพจน์ทางคณิตศาสตร์ (Boolean Propositions: True/False)
    p_Te = cog_scores.get("Te", 0) >= 4
    p_Ti = cog_scores.get("Ti", 0) >= 4
    p_Fe = cog_scores.get("Fe", 0) >= 4
    p_Ne = cog_scores.get("Ne", 0) >= 4
    
    a_math = "คำนวณ" in subject
    a_bio = "วิทยาศาสตร์ชีวภาพ" in subject
    a_art = "ศิลปะ" in subject
    
    c_low = "มีข้อจำกัดสูง" in capital  # True = ทุนน้อย

    # 4. ประมวลผลด้วยกฎตรรกศาสตร์ (Logical Decision Rules)
    rule_tech = (p_Ti or p_Te) and a_math and c_low
    rule_health = (p_Fe or (cog_scores.get("Si", 0) >= 4)) and a_bio and c_low
    rule_creative = (p_Ne or a_art) and (not c_low)

    # ------------------ แสดงผลลัพธ์หน้าเว็บ ------------------
    st.subheader("🎯 ผลการวิเคราะห์ทางตรรกศาสตร์")
    
    # กล่องสรุปบุคลิกภาพ
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="badge-mbti">{mbti_summary}</span>
        <p style="margin-top: 10px; color: #64748B;">ฟังก์ชันเด่นของคุณคือ <b>{dom_func}</b></p>
    </div>
    """, unsafe_allow_html=True)

    col_res1, col_res2 = st.columns([3, 2])

    with col_res1:
        st.markdown("### 🎓 คณะและอาชีพที่สอดคล้อง")
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        if rule_tech:
            st.markdown("#### 💻 กลุ่มสาขาเทคโนโลยี / คำนวณ / ครูทุน")
            st.markdown("- **คณะที่แนะนำ:** วิทยาการคอมพิวเตอร์, วิศวกรรมซอฟต์แวร์, ครุศาสตร์ (สาขาคอมพิวเตอร์/คณิตศาสตร์)")
            st.markdown("- **อาชีพ:** นักพัฒนาซอฟต์แวร์ (Software Developer), นักวิเคราะห์ข้อมูล (Data Analyst), ครูทุนรัฐบาล")
            st.markdown("- **การวิเคราะห์ทุน:** เป็นสาขาที่คืนทุนไว ตลาดต้องการสูง มีทุนเรียนฟรีจากเอกชนและรัฐบาลจำนวนมาก")
            
        elif rule_health:
            st.markdown("#### 🏥 กลุ่มสาขาการแพทย์ / พยาบาล / สุขภาพ")
            st.markdown("- **คณะที่แนะนำ:** พยาบาลศาสตร์, สหเวชศาสตร์ (กายภาพบำบัด/รังสีเทคนิค), สาธารณสุขศาสตร์")
            st.markdown("- **อาชีพ:** พยาบาลวิชาชีพ, นักเทคนิคการแพทย์, เจ้าหน้าที่สาธารณสุข")
            st.markdown("- **การวิเคราะห์ทุน:** เหมาะกับทุนผูกพันสถาบัน/โรงพยาบาล เรียนฟรี มีเบี้ยเลี้ยง จบแล้วมีงานบรรจุทันที")
            
        elif rule_creative:
            st.markdown("#### 🎨 กลุ่มสาขานวัตกรรม / สื่อ / การบริหาร")
            st.markdown("- **คณะที่แนะนำ:** สถาปัตยกรรมศาสตร์, นิเทศศาสตร์สื่อดิจิทัล, บริหารธุรกิจ (การตลาดดิจิทัล)")
            st.markdown("- **อาชีพ:** UX/UI Designer, ครีเอทีฟ, ผู้ประกอบการยุคใหม่")
            st.markdown("- **การวิเคราะห์ทุน:** ไม่ติดข้อจำกัดทุนทรัพย์ สามารถเลือกสาขาที่ใช้ทักษะเฉพาะทางและความคิดสร้างสรรค์ได้อย่างเต็มที่")
            
        else:
            st.markdown("#### 🏛️ กลุ่มสาขาบริหารธุรกิจ / มนุษยศาสตร์ / สังคมศาสตร์")
            st.markdown("- **คณะที่แนะนำ:** บริหารธุรกิจ, การบัญชี, อักษรศาสตร์, รัฐศาสตร์")
            st.markdown("- **อาชีพ:** นักการตลาด, นักบริหารทรัพยากรบุคคล (HR), เจ้าหน้าที่บริหารงานทั่วไป")
            st.markdown("- **การวิเคราะห์ทุน:** มีความยืดหยุ่นสูง สามารถต่อยอดกู้ยืม กยศ. หรือขอทุนมหาวิทยาลัยเพิ่มเติมได้")
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_res2:
        st.markdown("### 📐 การพิสูจน์ประพจน์ทางคณิตศาสตร์")
        st.markdown(f"""
        <div class="logic-box">
        <b>1. ตัวแปรประพจน์ (Propositions):</b><br>
        • p_Ti (Thinking Logic) = {p_Ti}<br>
        • p_Te (Thinking System) = {p_Te}<br>
        • a_math (วิชาคำนวณ) = {a_math}<br>
        • c_low (ข้อจำกัดทุนสูง) = {c_low}<br><br>
        <b>2. ผลการวิเคราะห์กฎตรรกศาสตร์:</b><br>
        • Rule_Tech = (p_Ti ∨ p_Te) ∧ a_math ∧ c_low<br>
          ➔ ผลลัพธ์: <b>{rule_tech}</b><br><br>
        • Rule_Health = (p_Fe ∨ p_Si) ∧ a_bio ∧ c_low<br>
          ➔ ผลลัพธ์: <b>{rule_health}</b><br><br>
        • Rule_Creative = (p_Ne ∨ a_art) ∧ (¬c_low)<br>
          ➔ ผลลัพธ์: <b>{rule_creative}</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 ทำแบบประเมินใหม่อีกครั้ง", use_container_width=True):
        st.session_state.step = 1
        st.rerun()
