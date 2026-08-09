import streamlit as st
from questions import COGNITIVE_QUESTIONS  # ดึงคลังคำถามมาจากไฟล์ questions.py

# ==========================================
# 1. PAGE CONFIG & STYLING (ปรับแต่งความสวยงาม)
# ==========================================
st.set_page_config(
    page_title="ระบบวัดแววด้วย Cognitive Functions & ตรรกศาสตร์",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    .header-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(37, 99, 235, 0.2);
        margin-bottom: 2rem;
    }
    .header-title { font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem; }
    .header-sub { font-size: 1.1rem; opacity: 0.9; }
    .custom-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
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
    .badge-func {
        background-color: #2563EB;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border-radius: 50px;
        display: inline-block;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ส่วนหัวเว็บไซต์
st.markdown("""
<div class="header-box">
    <div class="header-title">🎓 ระบบประมวลผลตรรกศาสตร์เพื่อการศึกษาต่อ</div>
    <div class="header-sub">โครงงานคณิตศาสตร์บูรณาการ: Cognitive Functions 8 ด้าน + วิชาที่ชอบ + เงื่อนไขทุนทรัพย์</div>
</div>
""", unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1

# ==========================================
# 2. STEP 1: ทำแบบสอบถาม
# ==========================================
if st.session_state.step == 1:
    st.subheader("📋 แบบสอบถามประเมินตนเอง")
    
    with st.form("main_form"):
        # 1. Cognitive Functions Questions
        st.markdown("### 🧠 1. แบบประเมิน Cognitive Functions")
        st.caption("โปรดเลือก 'ใช่' หากตรงกับความเป็นจริงของคุณ หรือ 'ไม่ใช่' หากไม่ตรง")
        
        user_cog_responses = {}
        for q in COGNITIVE_QUESTIONS:
            user_cog_responses[q["id"]] = {
                "func": q["func"],
                "ans": st.radio(
                    q["text"],
                    options=["ใช่", "ไม่ใช่"],
                    index=1,
                    horizontal=True,
                    key=q["id"]
                )
            }
            st.divider()

        # 2. Subject & Capital Input
        st.markdown("### 📚 2. ความสนใจรายวิชาและทุนทรัพย์")
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox(
                "กลุ่มรายวิชาที่ชอบ/ถนัดที่สุด:",
                [
                    "กลุ่มคำนวณ เทคโนโลยี และตรรกะ (คณิตศาสตร์, ฟิสิกส์, IT)",
                    "กลุ่มวิทยาศาสตร์ชีวภาพ สุขภาพ (เคมี, ชีววิทยา, พยาบาล)",
                    "กลุ่มภาษา สื่อสาร สังคม และบริหาร (ภาษา, สังคม, การตลาด)",
                    "กลุ่มศิลปะ ออกแบบ และงานสร้างสรรค์ (ศิลปะ, ดนตรี, สื่อดิจิทัล)"
                ]
            )
            
        with col2:
            capital = st.radio(
                "เงื่อนไขและข้อจำกัดด้านทุนการศึกษา:",
                [
                    "มีข้อจำกัดสูง (ต้องการคณะมีทุนเรียนฟรี / จบแล้วมีงานทำทันที / คืนทุนไว)",
                    "ไม่มีข้อจำกัด หรือมีทุนทรัพย์ปานกลางถึงสูง"
                ]
            )

        submit_btn = st.form_submit_button("🚀 ประมวลผลด้วยตรรกศาสตร์คณิตศาสตร์", use_container_width=True)
        
        if submit_btn:
            st.session_state.user_cog_responses = user_cog_responses
            st.session_state.subject = subject
            st.session_state.capital = capital
            st.session_state.step = 2
            st.rerun()

# ==========================================
# 3. STEP 2: ประมวลผลและแสดงผลลัพธ์
# ==========================================
elif st.session_state.step == 2:
    responses = st.session_state.get("user_cog_responses", {})
    subject = st.session_state.get("subject", "")
    capital = st.session_state.get("capital", "")

    # 1. คำนวณคะแนน Cognitive Functions (ตอบ 'ใช่' ได้ 1 คะแนน)
    func_scores = {"Te": 0, "Ti": 0, "Fe": 0, "Fi": 0, "Ne": 0, "Ni": 0, "Se": 0, "Si": 0}
    for q_id, val in responses.items():
        if val["ans"] == "ใช่":
            func_scores[val["func"]] += 1

    # หา Dominant Function (ฟังก์ชันที่คะแนนสูงสุด)
    dom_func = max(func_scores, key=func_scores.get)

    # 2. แปลงข้อมูลเป็นประพจน์ทางคณิตศาสตร์ (Propositions)
    p_Ti = func_scores["Ti"] >= 3
    p_Te = func_scores["Te"] >= 3
    p_Fe = func_scores["Fe"] >= 3
    p_Ne = func_scores["Ne"] >= 3
    
    a_math = "คำนวณ" in subject
    a_bio = "วิทยาศาสตร์ชีวภาพ" in subject
    a_art = "ศิลปะ" in subject
    
    c_low = "มีข้อจำกัดสูง" in capital  # True = ทุนน้อย

    # 3. ประมวลผลด้วยสูตรตรรกศาสตร์ (Rules)
    rule_tech = (p_Ti or p_Te) and a_math and c_low
    rule_health = (p_Fe or (func_scores["Si"] >= 3)) and a_bio and c_low
    rule_creative = (p_Ne or a_art) and (not c_low)

    # แสดงผล
    st.subheader("🎯 ผลการวิเคราะห์ด้วยตรรกศาสตร์")
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="badge-func">Dominant Function: {dom_func}</span>
        <p style="margin-top: 10px; color: #64748B;">กระบวนการทางความคิดหลักของคุณคือ <b>{dom_func}</b></p>
    </div>
    """, unsafe_allow_html=True)

    col_res1, col_res2 = st.columns([3, 2])

    with col_res1:
        st.markdown("### 🎓 คณะและอาชีพที่สอดคล้อง")
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        if rule_tech:
            st.markdown("#### 💻 กลุ่มสาขาเทคโนโลยี / คำนวณ / ครูทุน")
            st.markdown("- **คณะที่แนะนำ:** วิทยาการคอมพิวเตอร์, วิศวกรรมซอฟต์แวร์, ครุศาสตร์ (คอมพิวเตอร์/คณิตศาสตร์)")
            st.markdown("- **แนวทางอาชีพ:** Software Developer, Data Analyst, ครูทุนรัฐบาล")
            st.markdown("- **คำแนะนำด้านทุน:** คืนทุนไว ตลาดมีความต้องการสูง มีทุนเรียนฟรีจากเอกชนและรัฐบาล")
        elif rule_health:
            st.markdown("#### 🏥 กลุ่มสาขาการแพทย์ / พยาบาล / สุขภาพ")
            st.markdown("- **คณะที่แนะนำ:** พยาบาลศาสตร์, สหเวชศาสตร์, สาธารณสุขศาสตร์")
            st.markdown("- **แนวทางอาชีพ:** พยาบาลวิชาชีพ, นักเทคนิคการแพทย์, เจ้าหน้าที่สาธารณสุข")
            st.markdown("- **คำแนะนำด้านทุน:** เหมาะกับทุนผูกพันโรงพยาบาล เรียนฟรี มีเบี้ยเลี้ยง จบแล้วบรรจุทันที")
        elif rule_creative:
            st.markdown("#### 🎨 กลุ่มสาขานวัตกรรม / สื่อ / งานสร้างสรรค์")
            st.markdown("- **คณะที่แนะนำ:** สถาปัตยกรรมศาสตร์, นิเทศศาสตร์สื่อดิจิทัล, บริหารธุรกิจ")
            st.markdown("- **แนวทางอาชีพ:** UX/UI Designer, ครีเอทีฟดิเรกเตอร์, ผู้ประกอบการ")
            st.markdown("- **คำแนะนำด้านทุน:** ยืดหยุ่นสูง สามารถพัฒนาทักษะเฉพาะทางได้เต็มที่")
        else:
            st.markdown("#### 🏛️ กลุ่มสาขาบริหารธุรกิจ / มนุษยศาสตร์ / สังคมศาสตร์")
            st.markdown("- **คณะที่แนะนำ:** บริหารธุรกิจ, บัญชี, อักษรศาสตร์, รัฐศาสตร์")
            st.markdown("- **แนวทางอาชีพ:** นักการตลาด, นักทรัพยากรมนุษย์ (HR), งานบริหารทั่วไป")
            st.markdown("- **คำแนะนำด้านทุน:** สามารถกู้ยืม กยศ. หรือยื่นขอทุนการศึกษาของมหาวิทยาลัยเพิ่มเติมได้")
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_res2:
        st.markdown("### 📐 การพิสูจน์ทางตรรกศาสตร์ (Logic Proof)")
        st.markdown(f"""
        <div class="logic-box">
        <b>1. สรุปคะแนน Cognitive Functions:</b><br>
        • Ne={func_scores['Ne']} | Ni={func_scores['Ni']}<br>
        • Se={func_scores['Se']} | Si={func_scores['Si']}<br>
        • Te={func_scores['Te']} | Ti={func_scores['Ti']}<br>
        • Fe={func_scores['Fe']} | Fi={func_scores['Fi']}<br><br>
        <b>2. ตัวแปรประพจน์จริง/เท็จ:</b><br>
        • p_Ti = {p_Ti} | p_Te = {p_Te}<br>
        • a_math = {a_math} | c_low = {c_low}<br><br>
        <b>3. ผลการคำนวณตามกฎ:</b><br>
        • Rule_Tech = (p_Ti ∨ p_Te) ∧ a_math ∧ c_low → <b>{rule_tech}</b><br>
        • Rule_Health = (p_Fe ∨ p_Si) ∧ a_bio ∧ c_low → <b>{rule_health}</b><br>
        • Rule_Creative = (p_Ne ∨ a_art) ∧ (¬c_low) → <b>{rule_creative}</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 ทำแบบประเมินใหม่อีกครั้ง", use_container_width=True):
        st.session_state.step = 1
        st.rerun()
