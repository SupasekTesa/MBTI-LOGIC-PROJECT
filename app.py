import streamlit as st

st.set_page_config(page_title="Career Logic Matcher", layout="wide")

st.title("🏛️ ระบบแนะนำคณะและอาชีพด้วยตรรกศาสตร์")
st.caption("ประมวลผลด้วยตัวเชื่อมทางตรรกศาสตร์ (MBTI ∧ ความชอบ)")

# ==========================================
# STEP 1: รับค่า MBTI (กำหนดประพจน์บุคลิกภาพ)
# ==========================================
st.header("1. เลือกบุคลิกภาพ MBTI")

all_mbti = [
    "INTJ", "INTP", "ENTJ", "ENTP", 
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ", 
    "ISTP", "ISFP", "ESTP", "ESFP"
]

user_mbti = st.selectbox("ผลลัพธ์ MBTI ของคุณ:", all_mbti)

# สร้าง Dictionary เก็บค่าความจริงของประพจน์ MBTI (ตัวที่เลือกจะเป็น True ตัวอื่นเป็น False)
mbti_prop = {m: (m == user_mbti) for m in all_mbti}

st.divider()

# ==========================================
# STEP 2: ประพจน์ความชอบ 5 หมวดวิชา/สายงาน
# ==========================================
st.header("2. เลือกความชอบ (5 หมวดหลัก)")

col1, col2 = st.columns(2)

with col1:
    p_sci = st.checkbox("🔬 p1: วิทยาศาสตร์และเทคโนโลยี (Science & Tech)")
    p_math = st.checkbox("📐 p2: คณิตศาสตร์และตรรกะ (Math & Logic)")
    p_art = st.checkbox("🎨 p3: ศิลปะและการออกแบบ (Art & Design)")

with col2:
    p_lang = st.checkbox("🗣️ p4: ภาษาและมนุษยศาสตร์ (Language & Humanities)")
    p_social = st.checkbox("💼 p5: สังคมศาสตร์และการบริหาร (Social & Management)")

# กำหนดประพจน์เดี่ยวของความชอบ (Atomic Propositions)
P_sci = p_sci
P_math = p_math
P_art = p_art
P_lang = p_lang
P_social = p_social

st.divider()

# ==========================================
# STEP 3 & 4: ประมวลผลและแสดงตรรกศาสตร์
# ==========================================
if st.button("🚀 ประมวลผลเงื่อนไขทางตรรกศาสตร์", type="primary"):
    st.header("3. ผลลัพธ์และการวิเคราะห์เงื่อนไข")
    
    # กำหนดเงื่อนไขของแต่ละคณะและอาชีพตามตรรกศาสตร์
    # รูปแบบ: (ประพจน์ MBTI) ∧ (ประพจน์ความชอบ)
    career_rules = [
        {
            "faculty": "คณะวิทยาศาสตร์ / คณะวิศวกรรมศาสตร์",
            "careers": "นักวิจัย, วิศวกร, นักวิทยาศาสตร์ข้อมูล (Data Scientist)",
            "condition": (mbti_prop["INTJ"] or mbti_prop["INTP"] or mbti_prop["ENTJ"] or mbti_prop["ISTP"]) and (P_math and P_sci),
            "logic_symbol": "(INTJ \\lor INTP \\lor ENTJ \\lor ISTP) \\land (p_2 \\land p_1)"
        },
        {
            "faculty": "คณะเทคโนโลยีสารสนเทศ (IT / Computer Science)",
            "careers": "นักพัฒนาระบบ (Developer), นักวิเคราะห์ระบบ, UX/UI Engineer",
            "condition": (mbti_prop["INTJ"] or mbti_prop["INTP"] or mbti_prop["ENTP"] or mbti_prop["ISTP"]) and P_math,
            "logic_symbol": "(INTJ \\lor INTP \\lor ENTP \\lor ISTP) \\land p_2"
        },
        {
            "faculty": "คณะจิตวิทยา / คณะมนุษยศาสตร์",
            "careers": "นักจิตวิทยาปรึกษา, นักวิจัยพฤติกรรม, ที่ปรึกษาองค์กร",
            "condition": (mbti_prop["INFJ"] or mbti_prop["INFP"] or mbti_prop["ENFJ"] or mbti_prop["ISFJ"]) and (P_sci or P_social),
            "logic_symbol": "(INFJ \\lor INFP \\lor ENFJ \\lor ISFJ) \\land (p_1 \\lor p_5)"
        },
        {
            "faculty": "คณะสถาปัตยกรรมศาสตร์ / การออกแบบดิจิทัล",
            "careers": "สถาปนิก, นักออกแบบผลิตภัณฑ์, UX/UI Designer",
            "condition": (mbti_prop["INTJ"] or mbti_prop["INFP"] or mbti_prop["ISFP"] or mbti_prop["ENTP"]) and P_art,
            "logic_symbol": "(INTJ \\lor INFP \\lor ISFP \\lor ENTP) \\land p_3"
        },
        {
            "faculty": "คณะอักษรศาสตร์ / ศิลปศาสตร์",
            "careers": "นักแปล, นักเขียน, Content Creator, นักการทูต",
            "condition": (mbti_prop["INFJ"] or mbti_prop["INFP"] or mbti_prop["ENFP"] or mbti_prop["ISFJ"]) and P_lang,
            "logic_symbol": "(INFJ \\lor INFP \\lor ENFP \\lor ISFJ) \\land p_4"
        },
        {
            "faculty": "คณะบริหารธุรกิจ / พาณิชยศาสตร์และการบัญชี",
            "careers": "นักบริหารโครงการ, นักการตลาด, ผู้ประกอบการ, นักวิเคราะห์การเงิน",
            "condition": (mbti_prop["ENTJ"] or mbti_prop["ESTJ"] or mbti_prop["ENFJ"] or mbti_prop["ENTP"]) and P_social,
            "logic_symbol": "(ENTJ \\lor ESTJ \\lor ENFJ \\lor ENTP) \\land p_5"
        },
        {
            "faculty": "คณะนิเทศศาสตร์ / สื่อมวลชน",
            "careers": "ผู้กำกับ, นักประชาสัมพันธ์, นักจัดกิจกรรม (Event Planner)",
            "condition": (mbti_prop["ENFP"] or mbti_prop["ESFP"] or mbti_prop["ENTP"] or mbti_prop["ESTP"]) and (P_art or P_lang),
            "logic_symbol": "(ENFP \\lor ESFP \\lor ENTP \\lor ESTP) \\land (p_3 \\lor p_4)"
        }
    ]

    # กรองเฉพาะคณะที่ผลลัพธ์ประพจน์เป็น จริง (True)
    matched_results = [rule for rule in career_rules if rule["condition"]]

    if matched_results:
        st.subheader(f"พบ {len(matched_results)} คณะ/สายงานที่ตรงตามเงื่อนไขตรรกศาสตร์ของคุณ:")
        
        for index, item in enumerate(matched_results, start=1):
            with st.expander(f"📌 {index}. {item['faculty']}", expanded=True):
                st.write(f"**อาชีพที่แนะนำ:** {item['careers']}")
                st.info(f"**สูตรตรรกศาสตร์ที่ตรงเงื่อนไข:** ${item['logic_symbol']} \\equiv \\text{{True}}$")
    else:
        st.error("❌ ไม่พบคณะที่ตรงตามเงื่อนไขตรรกศาสตร์ที่กำหนด ลองปรับเลือกความชอบเพิ่มเติม")
