import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="ระบบวัดแววเลือกคณะและอาชีพด้วยตรรกศาสตร์",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        color: #1E3A8A;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-card {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 6px solid #2563EB;
        margin-top: 1rem;
    }
    .logic-box {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        padding: 1rem;
        border-radius: 8px;
        font-family: monospace;
        color: #1E40AF;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown('<div class="main-title">🎓 ระบบประมวลผลตรรกศาสตร์เพื่อการเลือกคณะและอาชีพ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">โครงงานคณิตศาสตร์บูรณาการ: การประยุกต์ใช้ตรรกศาสตร์ + MBTI + ปัจจัยทุนทรัพย์</div>', unsafe_allow_html=True)

st.divider()

# ==========================================
# FORM SECTION (INPUT)
# ==========================================
with st.form(key="mbti_assessment_form"):
    st.subheader("📋 แบบสอบถามวัดแววและความสนใจ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧠 1. แบบประเมินบุคลิกภาพ (MBTI)")
        
        q1 = st.radio(
            "1.1 การเติมพลังชีวิตและการเข้าสังคม:",
            ["พบปะพูดคุยกับผู้คน ออกไปทำกิจกรรมกลุ่ม (E - Extraversion)",
             "ชอบใช้เวลาอยู่กับตัวเอง ทำกิจกรรมในพื้นที่เงียบๆ (I - Introversion)"]
        )
        
        q2 = st.radio(
            "1.2 วิธีการรับรู้ข้อมูลและการเรียนรู้:",
            ["เน้นข้อมูลข้อเท็จจริง สิ่งที่สัมผัสและจับต้องได้ (S - Sensing)",
             "เน้นการมองภาพรวม จินตนาการ และความเป็นไปได้ใหม่ๆ (N - Intuition)"]
        )
        
        q3 = st.radio(
            "1.3 หลักการในการตัดสินใจ:",
            ["ใช้เหตุผล ตรรกะ ข้อเท็จจริง และความสมเหตุสมผล (T - Thinking)",
             "ใช้ความรู้สึก ค่านิยม ความเข้าอกเข้าใจ และผลกระทบต่อบุคคล (F - Feeling)"]
        )
        
        q4 = st.radio(
            "1.4 รูปแบบการดำเนินชีวิต:",
            ["ชอบความมีระเบียบ วางแผนชัดเจน มีโครงสร้างแน่นอน (J - Judging)",
             "ชอบความยืดหยุ่น ปรับเปลี่ยนตามสถานการณ์ สบายๆ (P - Perceiving)"]
        )

    with col2:
        st.markdown("### 📚 2. วิชา ความสนใจ และกิจกรรม")
        
        subject = st.selectbox(
            "2.1 กลุ่มรายวิชาที่คุณชื่นชอบมากที่สุด:",
            [
                "วิชาคำนวณ ตรรกะ และเทคโนโลยี (คณิตศาสตร์, ฟิสิกส์, คอมพิวเตอร์)",
                "วิชาทดลองและธรรมชาติวิทยา (ชีววิทยา, เคมี, วิทยาศาสตร์สุขภาพ)",
                "วิชาภาษา การสื่อสาร และสังคม (ภาษาไทย, อังกฤษ, สังคมศึกษา)",
                "วิชาสร้างสรรค์และศิลปะ (ศิลปะ, ออกแบบ, ดนตรี, สื่อ)"
            ]
        )
        
        hobby = st.selectbox(
            "2.2 กิจกรรมหรืองานอดิเรกที่ชอบทำ:",
            [
                "วิเคราะห์ วางแผน แก้ปัญหาซับซ้อน หรือเล่นเกมกลยุทธ์",
                "ช่วยเหลือผู้คน งานจิตอาสา รับฟังและปรึกษาปัญหา",
                "สร้างสรรค์งานศิลปะ วาดภาพ ออกแบบ ตัดต่อ ทำคอนเทนต์",
                "ลงมือปฏิบัติจริง งานทดลอง งานช่าง ส่องกล้องประดิษฐ์สิ่งของ"
            ]
        )
        
        st.markdown("### 💰 3. ปัจจัยด้านทุนการศึกษา")
        
        capital = st.radio(
            "3.1 เงื่อนไขและข้อจำกัดด้านทุนทรัพย์ในการศึกษาต่อ:",
            [
                "มีข้อจำกัดสูง (ต้องการคณะที่มีทุนเต็มจำนวน / จบแล้วมีงานรองรับทันที / คืนทุนไว)",
                "ไม่มีข้อจำกัด หรือมีทุนทรัพย์ปานกลางถึงสูง (สามารถรับภาระค่าธรรมเนียมการศึกษาทั่วไปได้)"
            ]
        )

    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="🚀 ประมวลผลตรรกศาสตร์เพื่อหาคณะที่ใช่", use_container_width=True)

# ==========================================
# LOGIC & PROCESSING SECTION
# ==========================================
if submit_button:
    # 1. Convert MBTI Inputs to Logical Propositions (True / False)
    m1 = True if "E - Extraversion" in q1 else False  # T = E, F = I
    m2 = True if "S - Sensing" in q2 else False       # T = S, F = N
    m3 = True if "T - Thinking" in q3 else False      # T = T, F = F
    m4 = True if "J - Judging" in q4 else False       # T = J, F = P
    
    mbti_type = f"{'E' if m1 else 'I'}{'S' if m2 else 'N'}{'T' if m3 else 'F'}{'J' if m4 else 'P'}"
    
    # 2. Convert Subject Inputs
    a1 = "คำนวณ" in subject
    a2 = "ชีววิทยา" in subject
    a3 = "ภาษา" in subject
    a4 = "สร้างสรรค์" in subject
    
    # 3. Convert Hobby Inputs
    h1 = "วิเคราะห์" in hobby
    h2 = "ช่วยเหลือ" in hobby
    h3 = "สร้างสรรค์" in hobby
    h4 = "ลงมือปฏิบัติ" in hobby
    
    # 4. Convert Capital Constraint
    c1 = "มีข้อจำกัดสูง" in capital  # T = ทุนน้อย, F = ทุนพอเพียง
    
    # ==========================================
    # LOGICAL RULES EVALUATION
    # ==========================================
    st.divider()
    st.subheader("🎯 ผลการวิเคราะห์และประมวลผลทางตรรกศาสตร์")
    
    # Logical Rule Formulas
    rule1 = (m3 and a1) and c1                   # Rule 1: Tech / Math + High Capital Constraint
    rule2 = ((not m3) or h2 or a2) and c1        # Rule 2: Healthcare / Caring + High Capital Constraint
    rule3 = (a4 or h3) and (not c1)              # Rule 3: Creative / Design + Sufficient Capital
    rule4 = (m1 or a3) and (not c1)              # Rule 4: Business / Arts + Sufficient Capital
    
    st.markdown(f"### 👤 บุคลิกภาพของคุณ: **{mbti_type}**")
    
    res_col1, res_col2 = st.columns([3, 2])
    
    with res_col1:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        if rule1:
            st.markdown("#### 🎓 คณะและสาขาวิชาที่แนะนำ:")
            st.markdown("- **คณะวิทยาการคอมพิวเตอร์ / เทคโนโลยีสารสนเทศ (IT) / วิศวกรรมซอฟต์แวร์**")
            st.markdown("- **คณะครุศาสตร์ / ศึกษาศาสตร์ (สาขาคณิตศาสตร์ หรือ คอมพิวเตอร์)**")
            st.markdown("#### 💼 แนวทางอาชีพ:")
            st.markdown("- นักพัฒนาซอฟต์แวร์ (Software Developer), นักวิเคราะห์ข้อมูล (Data Analyst), ครูทุนรัฐบาล")
            st.markdown("#### 💡 คำแนะนำด้านทุนการศึกษา:")
            st.markdown("เน้นคณะที่มีโครงการเรียนร่วมกับสถานประกอบการ (Co-op) หรือสมัครทุนครูคืนถิ่น และทุนบริษัทเทคโนโลยี คืนทุนไว โอกาสได้งานทำสูง")
            
        elif rule2:
            st.markdown("#### 🎓 คณะและสาขาวิชาที่แนะนำ:")
            st.markdown("- **คณะพยาบาลศาสตร์ / คณะสหเวชศาสตร์ (กายภาพบำบัด, รังสีเทคนิค)**")
            st.markdown("- **คณะสาธารณสุขศาสตร์ / การแพทย์แผนไทย**")
            st.markdown("#### 💼 แนวทางอาชีพ:")
            st.markdown("- พยาบาลวิชาชีพ, นักเทคนิคการแพทย์, เจ้าหน้าที่สาธารณสุข")
            st.markdown("#### 💡 คำแนะนำด้านทุนการศึกษา:")
            st.markdown("แนะนำยื่นขอทุนผูกพันจากโรงพยาบาลรัฐ/เอกชน หรือทุนสถาบันการศึกษา ซึ่งมักให้ทุนเรียนฟรีพร้อมเบี้ยเลี้ยง และเข้าทำงานได้ทันทีหลังจบ")
            
        elif rule3:
            st.markdown("#### 🎓 คณะและสาขาวิชาที่แนะนำ:")
            st.markdown("- **คณะสถาปัตยกรรมศาสตร์ / คณะมัณฑนศิลป์ / คณะศิลปกรรมศาสตร์**")
            st.markdown("- **คณะนิเทศศาสตร์ / สื่อดิจิทัลและการสื่อสาร**")
            st.markdown("#### 💼 แนวทางอาชีพ:")
            st.markdown("- UX/UI Designer, ครีเอทีฟ (Creative Director), สถาปนิก, นักประดิษฐ์คอนเทนต์")
            st.markdown("#### 💡 คำแนะนำด้านทุนการศึกษา:")
            st.markdown("เนื่องจากไม่มีข้อจำกัดด้านทุนทรัพย์ สามารถเลือกเรียนในหลักสูตรที่เน้นภาคปฏิบัติและอุปกรณ์เฉพาะทางได้อย่างเต็มที่")
            
        else:
            st.markdown("#### 🎓 คณะและสาขาวิชาที่แนะนำ:")
            st.markdown("- **คณะบริหารธุรกิจ / คณะพาณิชยศาสตร์และการบัญชี**")
            st.markdown("- **คณะมนุษยศาสตร์ / อักษรศาสตร์ / รัฐศาสตร์**")
            st.markdown("#### 💼 แนวทางอาชีพ:")
            st.markdown("- นักการตลาดดิจิทัล, นักการทูต, ผู้ประกอบการ, นักบริหารทรัพยากรบุคคล (HR)")
            st.markdown("#### 💡 คำแนะนำด้านทุนการศึกษา:")
            st.markdown("สามารถเลือกต่อยอดในหลักสูตรนานาชาติ หรือคณะสายบริหารเพื่อเพิ่มโอกาสในการทำงานองค์กรข้ามชาติ")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with res_col2:
        st.markdown("#### 📐 สมการตรรกศาสตร์ที่ใช้ประมวลผล (Logical Proof)")
        st.markdown("การแปลงค่าเป็นประพจน์จริง/เท็จ:")
        
        st.markdown(f"""
        <div class="logic-box">
        <b>ตัวแปรประพจน์:</b><br>
        • M3 (Thinking) = {m3}<br>
        • A1 (วิชาคำนวณ) = {a1}<br>
        • A2 (วิชาชีวะ) = {a2}<br>
        • C1 (ทุนน้อย) = {c1}<br><br>
        <b>ผลการคำนวณตามกฎตรรกศาสตร์:</b><br>
        Rule1 = (M3 ∧ A1) ∧ C1 → {rule1}<br>
        Rule2 = ((¬M3) ∨ H2 ∨ A2) ∧ C1 → {rule2}<br>
        Rule3 = (A4 ∨ H3) ∧ (¬C1) → {rule3}<br>
        Rule4 = (M1 ∨ A3) ∧ (¬C1) → {rule4}
        </div>
        """, unsafe_allow_html=True)
