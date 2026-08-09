import streamlit as st

# ==========================================
# 1. คลังคำถาม Cognitive Functions ทั้ง 8 ตัว
# ==========================================
# แต่ละข้อจะให้ผู้ใช้เลือกระดับความตรงกับตัวเอง (1 ถึง 5)
COGNITIVE_QUESTIONS = [
    {"id": "te_1", "func": "Te", "text": "ฉันชอบเน้นผลลัพธ์ จัดระบบ วางแผนขั้นตอนการทำงานให้มีประสิทธิภาพสูงสุด"},
    {"id": "ti_1", "func": "Ti", "text": "ฉันชอบวิเคราะห์เจาะลึก รื้อดูระบบภายใน เพื่อเข้าใจหลักการทำงานที่แท้จริงอย่างแม่นยำ"},
    {"id": "fe_1", "func": "Fe", "text": "ฉันแคร์ความรู้สึกของคนรอบข้าง ไวต่อบรรยากาศกลุ่ม และชอบสร้างความสมานฉันท์"},
    {"id": "fi_1", "func": "Fi", "text": "ฉันยึดมั่นในคุณค่า จริยธรรม และความรู้สึกที่แท้จริงภายในของตัวเองอย่างแรงกล้า"},
    {"id": "ne_1", "func": "Ne", "text": "ฉันชอบคิดนอกกรอบ เชื่อมโยงไอเดียใหม่ๆ และมองเห็นความเป็นไปได้หลากหลายช่องทาง"},
    {"id": "ni_1", "func": "Ni", "text": "ฉันชอบมองภาพรวมในอนาคต มีลางสังหรณ์แม่นยำ และมุ่งสู่เป้าหมายระยะยาวเพียงหนึ่งเดียว"},
    {"id": "se_1", "func": "Se", "text": "ฉันตอบสนองต่อสิ่งแวดล้อมรอบตัวได้ดี ชอบการลงมือทำจริง และอยู่กับปัจจุบันขณะ"},
    {"id": "si_1", "func": "Si", "text": "ฉันให้ความสำคัญกับประสบการณ์ในอดีต กฎระเบียบ รายละเอียด และความมั่นคงปลอดภัย"}
]

# Page Configuration
st.set_page_config(page_title="ระบบประมวลผล Cognitive Functions + ตรรกศาสตร์", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    .main-title { font-size: 2rem; color: #1E3A8A; text-align: center; font-weight: bold; }
    .badge { background: #1E40AF; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; }
    .logic-box { background-color: #EFF6FF; border-left: 5px solid #2563EB; padding: 1rem; border-radius: 6px; font-family: monospace; color: #1E40AF; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 ระบบวัดแวว Cognitive Functions & ตรรกศาสตร์เพื่อการศึกษาต่อ</div>', unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1

# ==========================================
# STEP 1: ประเมิน Cognitive Functions 8 ตัว
# ==========================================
if st.session_state.step == 1:
    st.subheader("🧠 ส่วนที่ 1: ประเมินกระบวนการทางความคิด (Cognitive Functions)")
    st.write("ให้คะแนนข้อความต่อไปนี้ตามความเป็นจริง (1 = ไม่จริงเลย, 5 = ตรงกับฉันมากที่สุด)")
    
    with st.form("cog_form"):
        scores = {}
        for q in COGNITIVE_QUESTIONS:
            scores[q["id"]] = st.slider(q["text"], 1, 5, 3, key=q["id"])
            st.divider()
            
        btn_1 = st.form_submit_button("ถัดไป: เลือกความสนใจและทุนทรัพย์ ➔", use_container_width=True)
        if btn_1:
            st.session_state.cog_scores = scores
            st.session_state.step = 2
            st.rerun()

# ==========================================
# STEP 2: ความสนใจ & ทุนการศึกษา
# ==========================================
elif st.session_state.step == 2:
    st.subheader("📚 ส่วนที่ 2: ความสนใจ และ ปัจจัยทางเศรษฐกิจ")
    
    with st.form("info_form"):
        subject = st.selectbox("กลุ่มวิชาที่ชื่นชอบที่สุด:", [
            "คำนวณ เทคโนโลยี และตรรกศาสตร์ (คณิต, ฟิสิกส์, IT)",
            "วิทยาศาสตร์ชีวภาพ สุขภาพ และการทดลอง (เคมี, ชีวะ)",
            "ภาษา ศิลปะ สื่อ และงานสร้างสรรค์",
            "บริหาร การจัดการ สังคม และกฎหมาย"
        ])
        
        capital = st.radio("ข้อจำกัดด้านทุนทรัพย์ในการศึกษาต่อ:", [
            "มีข้อจำกัดสูง (ต้องการคณะที่มีทุนเรียนฟรี / จบแล้วมีงานทำทันที)",
            "ไม่มีข้อจำกัด หรือมีทุนทรัพย์ปานกลางถึงสูง"
        ])
        
        btn_2 = st.form_submit_button("🚀 ประมวลผลตรรกศาสตร์คณิตศาสตร์ ➔", use_container_width=True)
        if btn_2:
            st.session_state.subject = subject
            st.session_state.capital = capital
            st.session_state.step = 3
            st.rerun()

# ==========================================
# STEP 3: ประมวลผลตรรกศาสตร์ (Mathematical Logic Evaluation)
# ==========================================
elif st.session_state.step == 3:
    st.subheader("📊 ผลการวิเคราะห์ Cognitive Functions และตรรกศาสตร์")
    
    raw_scores = st.session_state.get("cog_scores", {})
    
    # 1. รวมคะแนนแต่ละ Function
    func_totals = {"Te": 0, "Ti": 0, "Fe": 0, "Fi": 0, "Ne": 0, "Ni": 0, "Se": 0, "Si": 0}
    for q in COGNITIVE_QUESTIONS:
        f = q["func"]
        func_totals[f] += raw_scores.get(q["id"], 3)
        
    # หา Dominant Function (ฟังก์ชันที่ได้คะแนนสูงสุด)
    dom_func = max(func_totals, key=func_totals.get)
    
    # 2. แปลงเป็นตัวแปรประพจน์ทางคณิตศาสตร์ (True / False)
    # ให้ประพจน์เป็น True เมื่อคะแนนฟังก์ชันนั้นสูงกว่าหรือเท่ากับ 4
    p_Te = func_totals["Te"] >= 4
    p_Ti = func_totals["Ti"] >= 4
    p_Fe = func_totals["Fe"] >= 4
    p_Fi = func_totals["Fi"] >= 4
    p_Ne = func_totals["Ne"] >= 4
    p_Ni = func_totals["Ni"] >= 4
    
    subject = st.session_state.get("subject", "")
    capital = st.session_state.get("capital", "")
    
    a_math = "คำนวณ" in subject
    a_bio = "วิทยาศาสตร์ชีวภาพ" in subject
    c_low = "มีข้อจำกัดสูง" in capital # T = ทุนน้อย
    
    # 3. ประมวลผลด้วยกฎตรรกศาสตร์ (Logical Rules)
    # Rule 1: สาย Tech / วิศวะ / คอมพิวเตอร์
    rule_tech = (p_Ti or p_Te) and a_math and c_low
    # Rule 2: สาย การแพทย์ / พยาบาล / สุขภาพ
    rule_health = (p_Fe or p_Si) and a_bio and c_low
    # Rule 3: สาย นวัตกรรม / ครีเอทีฟ / การบริหาร
    rule_creative = (p_Ne or p_Ni) and (not c_low)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"### 🧬 ฟังก์ชันเด่นของคุณ: **{dom_func}**")
        st.write("คะแนน Cognitive Functions ทั้ง 8 ตัว:")
        st.json(func_totals)
        
    with col2:
        st.markdown("### 🎓 คำแนะนำคณะและอาชีพ")
        if rule_tech:
            st.success("**แนะนำ:** คณะวิทยาการคอมพิวเตอร์ / วิศวกรรมซอฟต์แวร์ / ครุศาสตร์คอมพิวเตอร์")
            st.info("**แนวทางทุน:** มีทุนเรียนฟรีจากบริษัทเทคโนโลยี / จบแล้วคืนทุนไว มีงานรองรับ 100%")
        elif rule_health:
            st.success("**แนะนำ:** คณะพยาบาลศาสตร์ / สหเวชศาสตร์ / สาธารณสุขศาสตร์")
            st.info("**แนวทางทุน:** มีทุนผูกพันจากโรงพยาบาลรัฐบาล เรียนฟรี มีเบี้ยเลี้ยง จบแล้วบรรจุทันที")
        else:
            st.success("**แนะนำ:** คณะสถาปัตยกรรม / นิเทศศาสตร์ / บริหารธุรกิจ / เทคโนโลยีสารสนเทศ")
            st.info("**แนวทางทุน:** สามารถเลือกสายงานยืดหยุ่น สร้างนวัตกรรมใหม่ๆ หรือทำธุรกิจส่วนตัวได้")
            
        st.markdown("#### 📐 สมการตรรกศาสตร์ที่ใช้พิสูจน์ (Logic Expression)")
        st.markdown(f"""
        <div class="logic-box">
        • p_Ti (Thinking Inside) = {p_Ti}<br>
        • p_Te (Thinking Outside) = {p_Te}<br>
        • c_low (ข้อจำกัดทุนสูง) = {c_low}<br><br>
        <b>สูตรตรรกะที่รันจริง:</b><br>
        Rule_Tech = (p_Ti ∨ p_Te) ∧ a_math ∧ c_low → <b>{rule_tech}</b>
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("🔄 ทำแบบสอบถามใหม่"):
        st.session_state.step = 1
        st.rerun()
