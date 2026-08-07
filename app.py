import streamlit as st

# ==========================================
# 1. ส่วนสำหรับใส่ชุดคำถาม MBTI ของคุณ (ใส่ได้ไม่จำกัดข้อ)
# ==========================================
# คำแนะนำ: อยากเพิ่มคำถามกี่ข้อ แค่ก็อปปี้โครงสร้างใน { } ไปต่อท้ายได้เลยครับ!
MBTI_QUESTIONS = [
    # --- กลุ่มคำถาม E vs I ---
    {
        "id": "q1",
        "dimension": "EI",
        "question": "1.1 เวลาคุณรู้สึกเหนื่อยล้าจากการเรียนหรือการทำงาน คุณเลือกเติมพลังด้วยวิธีไหน?",
        "option_a": "ออกไปเจอเพื่อน พูดคุย หรือทำกิจกรรมร่วมกับกลุ่มคน (แนวทาง E)",
        "option_b": "พักผ่อนเงียบๆ อยู่คนเดียวในพื้นที่ส่วนตัว (แนวทาง I)"
    },
    {
        "id": "q2",
        "dimension": "EI",
        "question": "1.2 ในงานเลี้ยงหรือกิจกรรมโรงเรียน คุณมักจะมีพฤติกรรมอย่างไร?",
        "option_a": "ชอบทำความรู้จักคนใหม่ๆ และเป็นฝ่ายเริ่มทักทายก่อน (แนวทาง E)",
        "option_b": "คุยเฉพาะกับเพื่อนสนิทที่คุ้นเคยอยู่แล้ว (แนวทาง I)"
    },

    # --- กลุ่มคำถาม S vs N ---
    {
        "id": "q3",
        "dimension": "SN",
        "question": "2.1 เวลาคุณฟังบทเรียนหรือรับข้อมูลใหม่ๆ คุณโฟกัสกับสิ่งใดมากกว่า?",
        "option_a": "ข้อเท็จจริง รายละเอียด และสิ่งที่จับต้องใช้ประโยชน์ได้จริง (แนวทาง S)",
        "option_b": "แนวคิด ภาพรวม ความเชื่อมโยง และความเป็นไปได้ใหม่ๆ (แนวทาง N)"
    },

    # --- กลุ่มคำถาม T vs F ---
    {
        "id": "q4",
        "dimension": "TF",
        "question": "3.1 เมื่อต้องแก้ปัญหาหรือตัดสินใจเรื่องสำคัญ คุณใช้อะไรเป็นหลัก?",
        "option_a": "เหตุผล ตรรกะ ข้อเท็จจริง ความถูกต้องที่เป็นธรรม (แนวทาง T)",
        "option_b": "ความรู้สึก ค่านิยม และผลกระทบต่อจิตใจของผู้คน (แนวทาง F)"
    },

    # --- กลุ่มคำถาม J vs P ---
    {
        "id": "q5",
        "dimension": "JP",
        "question": "4.1 สไตล์การทำงานหรือการทำการบ้านของคุณเป็นแบบไหน?",
        "option_a": "วางแผนล่วงหน้า วางตารางเวลาชัดเจน และทำตามแผนเสมอ (แนวทาง J)",
        "option_b": "ยืดหยุ่น ทำตามอารมณ์/ความพร้อม ลุยทำใกล้ๆ กำหนดส่ง (แนวทาง P)"
    }
]


# ==========================================
# PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(page_title="ระบบวัดแววเลือกคณะด้วยตรรกศาสตร์", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    .main-title { font-size: 2rem; color: #1E3A8A; text-align: center; font-weight: bold; }
    .sub-title { font-size: 1rem; color: #4B5563; text-align: center; margin-bottom: 2rem; }
    .mbti-badge { 
        background: linear-gradient(135deg, #2563EB, #1D4ED8); 
        color: white; 
        padding: 1.5rem; 
        border-radius: 12px; 
        text-align: center; 
        font-size: 2.5rem; 
        font-weight: bold;
        letter-spacing: 2px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .card { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; }
    .logic-box { background-color: #EFF6FF; border-left: 5px solid #2563EB; padding: 1rem; border-radius: 6px; font-family: monospace; color: #1E40AF; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 ระบบวัดแววเลือกคณะและอาชีพด้วยตรรกศาสตร์</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">โครงงานคณิตศาสตร์บูรณาการ: ตรรกศาสตร์ + MBTI + ความสนใจ + เป้าหมาย + ทุนการศึกษา</div>', unsafe_allow_html=True)

# Step Session State (1: MBTI คำถาม -> 2: ผล MBTI -> 3: วิชา/งานอดิเรก -> 4: เป้าหมาย/ทุน -> 5: สรุปผลตรรกศาสตร์)
if "step" not in st.session_state:
    st.session_state.step = 1

# Progress Bar
progress = (st.session_state.step - 1) / 4
st.progress(progress)


# ==========================================
# STEP 1: ตอบแบบสอบถาม MBTI (วน Loop อัตโนมัติ)
# ==========================================
if st.session_state.step == 1:
    st.subheader("🧠 ส่วนที่ 1: แบบประเมินบุคลิกภาพ (MBTI)")
    st.write("กรุณาตอบคำถามด้านล่างนี้ตามความเป็นจริงของคุณมากที่สุด:")
    
    with st.form("mbti_dynamic_form"):
        answers = {}
        # วน Loop ดึงคำถามจาก MBTI_QUESTIONS อัตโนมัติ
        for idx, item in enumerate(MBTI_QUESTIONS):
            answers[item["id"]] = st.radio(
                label=item["question"],
                options=[item["option_a"], item["option_b"]],
                key=item["id"]
            )
            st.divider()
            
        submit_mbti = st.form_submit_button("🔍 ประมวลผล MBTI ทันที ➔", use_container_width=True)
        
        if submit_mbti:
            # คำนวณคะแนน MBTI
            scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
            
            for item in MBTI_QUESTIONS:
                ans = answers[item["id"]]
                dim = item["dimension"]
                if ans == item["option_a"]:
                    scores[dim[0]] += 1
                else:
                    scores[dim[1]] += 1
            
            # สรุปผลประเภท MBTI
            mbti_type = ""
            mbti_type += "E" if scores["E"] >= scores["I"] else "I"
            mbti_type += "S" if scores["S"] >= scores["N"] else "N"
            mbti_type += "T" if scores["T"] >= scores["F"] else "F"
            mbti_type += "J" if scores["J"] >= scores["P"] else "P"
            
            # บันทึกลง Session State
            st.session_state.calculated_mbti = mbti_type
            st.session_state.step = 2
            st.rerun()


# ==========================================
# STEP 2: แสดงผลลัพธ์ MBTI ทันที!
# ==========================================
elif st.session_state.step == 2:
    st.subheader("🎉 ผลการประเมินบุคลิกภาพของคุณ")
    
    mbti = st.session_state.get("calculated_mbti", "INTJ")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<div class="mbti-badge">{mbti}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
    st.success(f"ระบบวิเคราะห์ว่าคุณมีบุคลิกภาพแบบ **{mbti}** เรียบร้อยแล้ว! ถัดไป เราจะนำ MBTI นี้ไปวิเคราะห์ร่วมกับวิชาที่ชอบและทุนการศึกษาครับ")
    
    if st.button("ถัดไป: ไปตอบเรื่องวิชาที่ชอบและความสนใจ ➔", use_container_width=True):
        st.session_state.step = 3
        st.rerun()


# ==========================================
# STEP 3: สิ่งที่ชอบ / วิชา / งานอดิเรก
# ==========================================
elif st.session_state.step == 3:
    st.subheader("📚 ส่วนที่ 2: ความสนใจ วิชาที่ชอบ และงานอดิเรก")
    
    with st.form("interests_form"):
        subject = st.selectbox(
            "1. กลุ่มวิชาที่คุณชอบหรือทำได้ดีที่สุด:",
            [
                "กลุ่มวิชาคำนวณและเทคโนโลยี (คณิตศาสตร์, ฟิสิกส์, คอมพิวเตอร์)",
                "กลุ่มวิชาทดลองและวิทยาศาสตร์สุขภาพ (เคมี, ชีววิทยา)",
                "กลุ่มวิชาภาษา การสื่อสาร และสังคม (ภาษาไทย, อังกฤษ, สังคม)",
                "กลุ่มวิชาสร้างสรรค์และศิลปะ (ศิลปะ, ออกแบบ, ดนตรี, สื่อดิจิทัล)"
            ]
        )
        
        hobby = st.selectbox(
            "2. กิจกรรมหรืองานอดิเรกที่ชอบทำ:",
            [
                "วิเคราะห์ วางแผน เล่นเกมกลยุทธ์ แก้โจทย์ซับซ้อน",
                "ช่วยเหลือผู้อื่น ทำงานจิตอาสา รับฟังปัญหาเพื่อน",
                "วาดรูป แต่งเพลง เขียนคอนเทนต์ ออกแบบกราฟิก",
                "ประดิษฐ์สิ่งของ ซ่อมแซม ทดลองสิ่งใหม่ๆ ลงมือทำจริง"
            ]
        )
        
        next_3 = st.form_submit_button("ถัดไป: ไปยังเป้าหมายและทุนทรัพย์ ➔", use_container_width=True)
        if next_3:
            st.session_state.subject_choice = subject
            st.session_state.hobby_choice = hobby
            st.session_state.step = 4
            st.rerun()


# ==========================================
# STEP 4: เป้าหมายอาชีพ & เงื่อนไขทุน
# ==========================================
elif st.session_state.step == 4:
    st.subheader("🎯 ส่วนที่ 3: เป้าหมายอาชีพและเงื่อนไขทุนทรัพย์")
    
    with st.form("goals_form"):
        career_goal = st.radio(
            "1. เป้าหมายลักษณะงานที่อยากได้ในอนาคต:",
            [
                "เน้นความมั่นคงสูง มีสวัสดิการดี (เช่น ข้าราชการ, งานสถาบันรัฐ, พยาบาล)",
                "เน้นการสร้างรายได้เร็ว คืนทุนไว คุ้มค่าตอบแทน (เช่น สายเทค, สื่อการตลาด)",
                "เน้นอิสระในการทำงาน มีความยืดหยุ่นสูง (เช่น ฟรีแลนซ์, ครีเอทีฟ, ธุรกิจส่วนตัว)"
            ]
        )
        
        capital_status = st.radio(
            "2. เงื่อนไขและข้อจำกัดด้านทุนทรัพย์ในการศึกษาต่อ:",
            [
                "มีข้อจำกัดสูง (ต้องการทุนเต็มจำนวน / คณะที่มีทุนรองรับ / จบแล้วทำงานได้ทันที)",
                "ไม่มีข้อจำกัด หรือมีทุนทรัพย์ปานกลางถึงสูง (รับภาระค่าเทอมทั่วไปได้)"
            ]
        )
        
        submit_all = st.form_submit_button("🚀 ประมวลผลตรรกศาสตร์รวมทั้งหมด", use_container_width=True)
        if submit_all:
            st.session_state.career_goal = career_goal
            st.session_state.capital_status = capital_status
            st.session_state.step = 5
            st.rerun()


# ==========================================
# STEP 5: ประมวลผลตรรกศาสตร์รวมทั้งหมด
# ==========================================
elif st.session_state.step == 5:
    st.subheader("📊 สรุปผลการวิเคราะห์ทางตรรกศาสตร์")
    
    mbti = st.session_state.get("calculated_mbti", "")
    subject = st.session_state.get("subject_choice", "")
    goal = st.session_state.get("career_goal", "")
    capital = st.session_state.get("capital_status", "")
    
    # ตัวแปรประพจน์
    m3 = "T" in mbti  # True ถ้าเป็น Thinking
    a1 = "คำนวณ" in subject
    a2 = "ชีววิทยา" in subject
    a4 = "สร้างสรรค์" in subject
    
    g_stable = "ความมั่นคงสูง" in goal
    g_fast = "สร้างรายได้เร็ว" in goal
    g_freedom = "เน้นอิสระ" in goal
    c1 = "มีข้อจำกัดสูง" in capital # T = ทุนน้อย
    
    # กฎทางตรรกศาสตร์
    rule_tech = (m3 and a1 and g_fast) or (a1 and c1)
    rule_health = (a2 or g_stable) and c1
    
    st.markdown(f"### 👤 บุคลิกภาพของคุณ: **{mbti}**")
    
    col_r1, col_r2 = st.columns([3, 2])
    with col_r1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if rule_tech:
            st.markdown("#### 🎓 คณะแนะนำ: **วิทยาการคอมพิวเตอร์ / IT / ครูคณิต-คอม**")
            st.markdown("#### 💼 อาชีพ: **Software Developer / Data Analyst / ครูทุนรัฐบาล**")
            st.markdown("#### 💡 วิเคราะห์ทุน: คืนทุนไว มีโอกาสได้ทุนเอกชน/รัฐบาลสูง")
        elif rule_health:
            st.markdown("#### 🎓 คณะแนะนำ: **พยาบาลศาสตร์ / สหเวชศาสตร์ / สาธารณสุข**")
            st.markdown("#### 💼 อาชีพ: **พยาบาลวิชาชีพ / นักเทคนิคการแพทย์**")
            st.markdown("#### 💡 วิเคราะห์ทุน: ตอบโจทย์ทุนผูกพันโรงพยาบาล มั่นคง เรียนฟรีจบมามีงานทำทันที")
        else:
            st.markdown("#### 🎓 คณะแนะนำ: **สถาปัตยกรรม / นิเทศศาสตร์ / บริหารธุรกิจ**")
            st.markdown("#### 💼 อาชีพ: **UX/UI Designer / ครีเอทีฟ / การตลาดดิจิทัล**")
            st.markdown("#### 💡 วิเคราะห์ทุน: มีความยืดหยุ่นสูง เหมาะกับการเติบโตในสายงานอิสระ")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_r2:
        st.markdown("#### 📐 Proof Log (ตรรกศาสตร์คณิตศาสตร์)")
        st.markdown(f"""
        <div class="logic-box">
        <b>ค่าจริงประพจน์:</b><br>
        • MBTI = {mbti}<br>
        • A1 (คำนวณ) = {a1}<br>
        • C1 (ทุนน้อย) = {c1}<br><br>
        <b>สูตรตรรกะ:</b><br>
        • Rule Tech = (M3 ∧ A1 ∧ G_fast) ∨ (A1 ∧ C1) → {rule_tech}<br>
        • Rule Health = (A2 ∨ G_stable) ∧ C1 → {rule_health}
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("🔄 เริ่มทำแบบสอบถามใหม่", use_container_width=True):
        st.session_state.step = 1
        st.rerun()
