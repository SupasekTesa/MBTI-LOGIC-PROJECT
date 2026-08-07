import streamlit as st

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="ระบบวัดแวว MBTI + ตรรกศาสตร์การศึกษาต่อ",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2rem;
        color: #1E3A8A;
        text-align: center;
        font-weight: bold;
    }
    .sub-title {
        font-size: 1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .logic-box {
        background-color: #EFF6FF;
        border-left: 5px solid #2563EB;
        padding: 1rem;
        border-radius: 6px;
        font-family: monospace;
        color: #1E40AF;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 ระบบวัดแววเลือกคณะและอาชีพด้วยตรรกศาสตร์</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">โครงงานคณิตศาสตร์บูรณาการ: ตรรกศาสตร์ + MBTI + ความสนใจ + เป้าหมายอาชีพ + ทุนการศึกษา</div>', unsafe_allow_html=True)

# Initialize Session State for Multi-step Form
if "step" not in st.session_state:
    st.session_state.step = 1

# Progress Bar
progress = (st.session_state.step - 1) / 3
st.progress(progress)
st.caption(f"ขั้นตอนที่ {st.session_state.step} จาก 4")

# ==========================================
# STEP 1: MBTI ASSESSMENT
# ==========================================
if st.session_state.step == 1:
    st.subheader("🧠 ส่วนที่ 1: แบบประเมินบุคลิกภาพ (MBTI)")
    st.info("💡 สามารถนำคำถาม MBTI ที่คุณคิดเองมาแก้ไขในโค้ดตรงจุดนี้ได้เลยครับ")
    
    with st.form("mbti_form"):
        # --- มิติ E / I ---
        st.markdown("#### 1. การเข้าสังคมและการรับพลังงาน (E vs I)")
        q_ei_1 = st.radio("1.1 คำถาม E/I ข้อที่ 1: [พิมพ์คำถามของคุณตรงนี้]", 
                          ["ตัวเลือก A (แนวทาง E): ชอบทำกิจกรรมกลุ่ม / ออกไปเจอผู้คน", 
                           "ตัวเลือก B (แนวทาง I): ชอบชาร์จพลังคนเดียว / อยู่ในพื้นที่เงียบๆ"], key="q_ei_1")
        
        q_ei_2 = st.radio("1.2 คำถาม E/I ข้อที่ 2: [พิมพ์คำถามของคุณตรงนี้]", 
                          ["ตัวเลือก A (แนวทาง E): ชอบพูดคุยและแสดงความเห็นทันที", 
                           "ตัวเลือก B (แนวทาง I): ชอบคิดทบทวนเงียบๆ ก่อนพูด"], key="q_ei_2")
        
        st.divider()
        # --- มิติ S / N ---
        st.markdown("#### 2. การรับรู้และรับข้อมูล (S vs N)")
        q_sn_1 = st.radio("2.1 คำถาม S/N ข้อที่ 1: [พิมพ์คำถามของคุณตรงนี้]", 
                          ["ตัวเลือก A (แนวทาง S): เน้นรายละเอียด ข้อเท็จจริงที่เห็นชัดเจน", 
                           "ตัวเลือก B (แนวทาง N): เน้นภาพรวม จินตนาการ ความเป็นไปได้"], key="q_sn_1")
        
        st.divider()
        # --- มิติ T / F ---
        st.markdown("#### 3. การตัดสินใจ (T vs F)")
        q_tf_1 = st.radio("3.1 คำถาม T/F ข้อที่ 1: [พิมพ์คำถามของคุณตรงนี้]", 
                          ["ตัวเลือก A (แนวทาง T): ใช้ตรรกะ เหตุผล ความถูกต้องเป็นหลัก", 
                           "ตัวเลือก B (แนวทาง F): ใช้ความรู้สึก ความเข้าใจ ผลกระทบต่อคนเป็นหลัก"], key="q_tf_1")
        
        st.divider()
        # --- มิติ J / P ---
        st.markdown("#### 4. รูปแบบการใช้ชีวิต (J vs P)")
        q_jp_1 = st.radio("4.1 คำถาม J/P ข้อที่ 1: [พิมพ์คำถามของคุณตรงนี้]", 
                          ["ตัวเลือก A (แนวทาง J): ชอบวางแผนล่วงหน้า มีระเบียบแบบแผน", 
                           "ตัวเลือก B (แนวทาง P): ยืดหยุ่น พร้อมปรับเปลี่ยนตามสถานการณ์"], key="q_jp_1")

        next_1 = st.form_submit_button("ถัดไป: ไปยังส่วนความสนใจและความถนัด ➔", use_container_width=True)
        if next_1:
            st.session_state.step = 2
            st.rerun()

# ==========================================
# STEP 2: INTERESTS & HOBBIES
# ==========================================
elif st.session_state.step == 2:
    st.subheader("📚 ส่วนที่ 2: ความสนใจ วิชาที่ชอบ และงานอดิเรก")
    
    with st.form("interests_form"):
        subject = st.selectbox(
            "1. กลุ่มวิชาที่คุณชื่นชอบหรือทำได้ดีที่สุด: [แก้ไขตัวเลือกตรงนี้ได้]",
            [
                "กลุ่มวิชาคำนวณและเทคโนโลยี (คณิตศาสตร์, ฟิสิกส์, คอมพิวเตอร์)",
                "กลุ่มวิชาทดลองและวิทยาศาสตร์สุขภาพ (เคมี, ชีววิทยา)",
                "กลุ่มวิชาภาษา การสื่อสาร และสังคม (ภาษาไทย, อังกฤษ, สังคม)",
                "กลุ่มวิชาสร้างสรรค์และศิลปะ (ศิลปะ, ออกแบบ, ดนตรี, สื่อดิจิทัล)"
            ]
        )
        
        hobby = st.selectbox(
            "2. กิจกรรมหรืองานอดิเรกที่ชอบทำในเวลาว่าง: [แก้ไขตัวเลือกตรงนี้ได้]",
            [
                "วิเคราะห์ วางแผน เล่นเกมกลยุทธ์ แก้โจทย์ซับซ้อน",
                "ช่วยเหลือผู้อื่น ทำงานจิตอาสา รับฟังปัญหาเพื่อน",
                "วาดรูป แต่งเพลง เขียนคอนเทนต์ ออกแบบกราฟิก",
                "ประดิษฐ์สิ่งของ ซ่อมแซม ทดลองสิ่งใหม่ๆ ลงมือทำจริง"
            ]
        )
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            back_2 = st.form_submit_button("⬅ ย้อนกลับ")
        with col_b2:
            next_2 = st.form_submit_button("ถัดไป: ไปยังเป้าหมายและทุนทรัพย์ ➔")
            
        if back_2:
            st.session_state.step = 1
            st.rerun()
        if next_2:
            st.session_state.subject_choice = subject
            st.session_state.hobby_choice = hobby
            st.session_state.step = 3
            st.rerun()

# ==========================================
# STEP 3: GOALS & CAPITAL CONSTRAINTS
# ==========================================
elif st.session_state.step == 3:
    st.subheader("🎯 ส่วนที่ 3: เป้าหมายอาชีพและเงื่อนไขทุนทรัพย์")
    
    with st.form("goals_form"):
        career_goal = st.radio(
            "1. เป้าหมายลักษณะงานที่คุณอยากได้มากที่สุดในอนาคต:",
            [
                "เน้นความมั่นคงสูง มีสวัสดิการดี (เช่น ข้าราชการ, งานสถาบันรัฐ, พยาบาล)",
                "เน้นการสร้างรายได้เร็ว คืนทุนไว คุ้มค่าตอบแทน (เช่น สายเทค, สื่อการตลาด)",
                "เน้นอิสระในการทำงาน มีความยืดหยุ่นสูง (เช่น ฟรีแลนซ์, ครีเอทีฟ, ธุรกิจส่วนตัว)"
            ]
        )
        
        capital_status = st.radio(
            "2. เงื่อนไขและข้อจำกัดด้านทุนทรัพย์ในการศึกษาต่อ:",
            [
                "มีข้อจำกัดสูง (ต้องการทุนเต็มจำนวน / คณะที่มีทุนรองรับ / หรือจบแล้วทำงานได้ทันที)",
                "ไม่มีข้อจำกัด หรือมีทุนทรัพย์ปานกลางถึงสูง (สามารถรับภาระค่าเทอมทั่วไปได้)"
            ]
        )
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            back_3 = st.form_submit_button("⬅ ย้อนกลับ")
        with col_b2:
            submit_all = st.form_submit_button("🚀 ประมวลผลตรรกศาสตร์")
            
        if back_3:
            st.session_state.step = 2
            st.rerun()
        if submit_all:
            st.session_state.career_goal = career_goal
            st.session_state.capital_status = capital_status
            st.session_state.step = 4
            st.rerun()

# ==========================================
# STEP 4: LOGIC PROCESSING & RESULTS
# ==========================================
elif st.session_state.step == 4:
    st.subheader("📊 ส่วนที่ 4: ผลการวิเคราะห์ด้วยตรรกศาสตร์")
    
    # 1. Evaluate MBTI Propositions
    m1_score = 0
    if "แนวทาง E" in st.session_state.get("q_ei_1", ""): m1_score += 1
    if "แนวทาง E" in st.session_state.get("q_ei_2", ""): m1_score += 1
    m1 = True if m1_score >= 1 else False  # T = E, F = I
    
    m2 = False if "แนวทาง N" in st.session_state.get("q_sn_1", "") else True # T = S, F = N
    m3 = True if "แนวทาง T" in st.session_state.get("q_tf_1", "") else False  # T = T, F = F
    m4 = True if "แนวทาง J" in st.session_state.get("q_jp_1", "") else False  # T = J, F = P
    
    mbti_result = f"{'E' if m1 else 'I'}{'S' if m2 else 'N'}{'T' if m3 else 'F'}{'J' if m4 else 'P'}"
    
    # 2. Get Saved Inputs
    subject = st.session_state.get("subject_choice", "")
    hobby = st.session_state.get("hobby_choice", "")
    goal = st.session_state.get("career_goal", "")
    capital = st.session_state.get("capital_status", "")
    
    # 3. Proposition Mapping
    a1 = "คำนวณ" in subject
    a2 = "ชีววิทยา" in subject
    a3 = "ภาษา" in subject
    a4 = "สร้างสรรค์" in subject
    
    g_stable = "ความมั่นคงสูง" in goal
    g_fast_money = "สร้างรายได้เร็ว" in goal
    g_freedom = "เน้นอิสระ" in goal
    
    c1 = "มีข้อจำกัดสูง" in capital  # T = ทุนน้อย
    
    # 4. Rules Evaluation
    rule_tech = (m3 and a1 and g_fast_money) or (a1 and c1)
    rule_health = (a2 or g_stable) and c1
    rule_creative = (a4 or g_freedom) and (not c1)
    
    st.markdown(f"### 👤 ผลการประเมิน MBTI ของคุณ: **{mbti_result}**")
    
    col_r1, col_r2 = st.columns([3, 2])
    
    with col_r1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if rule_tech:
            st.markdown("#### 🎓 คณะและสาขาที่แนะนำ:")
            st.markdown("- **คณะวิทยาการคอมพิวเตอร์ / วิศวกรรมซอฟต์แวร์ / IT**")
            st.markdown("- **คณะครุศาสตร์ (สาขาคณิตศาสตร์ / คอมพิวเตอร์)**")
            st.markdown("#### 💼 อาชีพที่สอดคล้องกับเป้าหมาย:")
            st.markdown("- Software Developer, Data Analyst, ครูทุนรัฐบาล")
            st.markdown("#### 💡 การวิเคราะห์ทุนและเป้าหมาย:")
            st.markdown("ตอบโจทย์กลุ่มที่ต้องการสร้างรายได้เร็ว คืนทุนไว หรือต้องการทุนเรียนฟรีที่มีงานรองรับแน่นอน")
        elif rule_health:
            st.markdown("#### 🎓 คณะและสาขาที่แนะนำ:")
            st.markdown("- **คณะพยาบาลศาสตร์ / คณะสหเวชศาสตร์ / คณะสาธารณสุขศาสตร์**")
            st.markdown("- **คณะครุศาสตร์ (วิชาชีพเฉพาะ)**")
            st.markdown("#### 💼 อาชีพที่สอดคล้องกับเป้าหมาย:")
            st.markdown("- พยาบาลวิชาชีพ, นักเทคนิคการแพทย์, เจ้าหน้าที่สาธารณสุข")
            st.markdown("#### 💡 การวิเคราะห์ทุนและเป้าหมาย:")
            st.markdown("ตอบโจทย์ความมั่นคงสูง และมีทุนผูกพันจากโรงพยาบาลรองรับ เหมาะสำหรับผู้มีข้อจำกัดด้านทุนทรัพย์")
        else:
            st.markdown("#### 🎓 คณะและสาขาที่แนะนำ:")
            st.markdown("- **คณะสถาปัตยกรรมศาสตร์ / คณะนิเทศศาสตร์ / คณะบริหารธุรกิจ**")
            st.markdown("#### 💼 อาชีพที่สอดคล้องกับเป้าหมาย:")
            st.markdown("- UX/UI Designer, ครีเอทีฟดิเรกเตอร์, ผู้ประกอบการ, การตลาดดิจิทัล")
            st.markdown("#### 💡 การวิเคราะห์ทุนและเป้าหมาย:")
            st.markdown("ตอบโจทย์การทำงานที่ยืดหยุ่น มีอิสระสูง และสามารถต่อยอดทักษะเฉพาะทางได้อย่างหลากหลาย")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_r2:
        st.markdown("#### 📐 Proof log (ประพจน์ทางตรรกศาสตร์)")
        st.markdown(f"""
        <div class="logic-box">
        <b>ค่าจริงของประพจน์:</b><br>
        • MBTI = {mbti_result}<br>
        • A1 (วิชาคำนวณ) = {a1}<br>
        • G_stable (มั่นคง) = {g_stable}<br>
        • G_fast (ได้เงินเร็ว) = {g_fast_money}<br>
        • C1 (ทุนน้อย) = {c1}<br><br>
        <b>ประมวลผลกฎตรรกะ:</b><br>
        • Rule Tech = {rule_tech}<br>
        • Rule Health = {rule_health}<br>
        • Rule Creative = {rule_creative}
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("🔄 ทำแบบสอบถามใหม่อีกครั้ง", use_container_width=True):
        st.session_state.step = 1
        st.rerun()
