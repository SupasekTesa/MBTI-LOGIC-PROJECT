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
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="ระบบวิเคราะห์อาชีพด้วยตรรกศาสตร์ MBTI & Subject Logic",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------------------------------------
# 2. Session State Management
# ---------------------------------------------------------
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'mbti_result' not in st.session_state:
    st.session_state.mbti_result = "INTJ"
if 'top_subject' not in st.session_state:
    st.session_state.top_subject = None

SCALE_OPTIONS = {
    "1 - ไม่ตรงเลย": 1,
    "2 - ไม่ค่อยตรง": 2,
    "3 - ปานกลาง / ไม่แน่ใจ": 3,
    "4 - ค่อนข้างตรง": 4,
    "5 - ตรงมากที่สุด": 5
}

# ---------------------------------------------------------
# STEP 1: ประเมิน MBTI (Cognitive Functions)
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.title("🧩 ขั้นตอนที่ 1: ประเมินบุคลิกภาพ (MBTI)")
    st.write("เลือกสเกลที่ตรงกับตัวคุณมากที่สุดเพื่อสรุปหาประพจน์ทางบุคลิกภาพ")
    
    with st.form("mbti_form"):
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
            
        submitted = st.form_submit_button("🚀 ประมวลผล MBTI")
        
        if submitted:
            func_scores = {"Ne": 0, "Ni": 0, "Se": 0, "Si": 0, "Te": 0, "Ti": 0, "Fe": 0, "Fi": 0}
            for item in raw_answers.values():
                func_scores[item["func"]] += item["score"]

            dom_func = max(func_scores, key=func_scores.get)
            
            possible_aux = []
            if dom_func in ["Ne", "Se"]: possible_aux = ["Ti", "Fi"]
            elif dom_func in ["Ni", "Si"]: possible_aux = ["Te", "Fe"]
            elif dom_func in ["Te", "Fe"]: possible_aux = ["Ni", "Si"]
            elif dom_func in ["Ti", "Fi"]: possible_aux = ["Ne", "Se"]

            aux_func = max(possible_aux, key=lambda f: func_scores[f])

            type_mapping = {
                ("Ne", "Ti"): "ENTP", ("Ne", "Fi"): "ENFP",
                ("Ni", "Te"): "INTJ", ("Ni", "Fe"): "INFJ",
                ("Se", "Ti"): "ESTP", ("Se", "Fi"): "ESFP",
                ("Si", "Te"): "ISTJ", ("Si", "Fe"): "ISFJ",
                ("Te", "Ni"): "ENTJ", ("Te", "Si"): "ESTJ",
                ("Ti", "Ne"): "INTP", ("Ti", "Se"): "ISTP",
                ("Fe", "Ni"): "ENFJ", ("Fe", "Si"): "ESFJ",
                ("Fi", "Ne"): "INFP", ("Fi", "Se"): "ISFP"
            }
            
            st.session_state.mbti_result = type_mapping.get((dom_func, aux_func), "INTJ")
            st.session_state.step = 2
            st.rerun()

# ---------------------------------------------------------
# STEP 2: สรุปผล MBTI และกำหนดประพจน์ MBTI
# ---------------------------------------------------------
elif st.session_state.step == 2:
    st.title("🌟 ขั้นตอนที่ 2: สรุปประพจน์บุคลิกภาพ (MBTI Proposition)")
    
    mbti = st.session_state.mbti_result
    info = MBTI_DESCRIPTIONS.get(mbti, MBTI_DESCRIPTIONS["INTJ"])
    
    st.success(f"### ผลการวิเคราะห์ MBTI: **{mbti}** ({info['title']})")
    
    st.info(f"""
    **📌 การกำหนดประพจน์หลัก:**
    ให้ประพจน์ **$M_{{{mbti}}}$** แทนความหมาย: *"ผู้เรียนมีบุคลิกภาพแบบ {mbti}"* = **True (จริง)**
    """)
    
    st.markdown("---")
    if st.button("➡️ ไปต่อ: เลือกความชอบวิชาเพื่อสร้างประพจน์ความชอบ (Step 3)"):
        st.session_state.step = 3
        st.rerun()

# ---------------------------------------------------------
# STEP 3: ประเมินวิชาที่ชอบ และกำหนดประพจน์วิชา
# ---------------------------------------------------------
elif st.session_state.step == 3:
    st.title("📚 ขั้นตอนที่ 3: สรุปประพจน์ความชอบวิชา (Subject Propositions)")
    st.write("เลือกสเกลวิชาที่ชอบ เพื่อสรุปวิชาที่เด่นที่สุดมาตั้งเป็นประพจน์ทางตรรกศาสตร์")
    
    with st.form("subject_form"):
        sub_scores = {}
        for q in SUBJECT_QUESTIONS:
            ans = st.radio(
                f"วิชา: {q['text']} ({q['category']}):", 
                options=list(SCALE_OPTIONS.keys()), 
                index=2, 
                key=f"sub_{q['id']}", 
                horizontal=True
            )
            sub_scores[q["category"]] = sub_scores.get(q["category"], 0) + SCALE_OPTIONS[ans]
            
        submitted_step3 = st.form_submit_button("🚀 สรุปประพจน์ความชอบและตรวจสอบเงื่อนไข (Step 4)")
        
        if submitted_step3:
            # หาวิชาที่ชอบมากที่สุดเป็นวิชาหลัก
            sorted_subjects = sorted(sub_scores.items(), key=lambda x: x[1], reverse=True)
            st.session_state.sub_scores = sub_scores
            st.session_state.top_subjects = [s[0] for s in sorted_subjects[:2]] # เลือก 2 อันดับแรก
            st.session_state.step = 4
            st.rerun()

# ---------------------------------------------------------
# STEP 4: เชื่อมประพจน์ (AND) & ตรวจสอบเงื่อนไขคณะ/อาชีพ
# ---------------------------------------------------------
elif st.session_state.step == 4:
    st.title("🎓 ขั้นตอนที่ 4: การประมวลผลตรรกศาสตร์เชื่อมประพจน์ (AND Logic)")
    
    mbti = st.session_state.mbti_result
    top_subs = st.session_state.get("top_subjects", [])

    # กำหนดสถานะความจริงของประพจน์วิชา
    is_math = "Math & Logic" in top_subs or "คณิตศาสตร์/ฟิสิกส์" in top_subs
    is_sci = "Natural Science" in top_subs or "วิทยาศาสตร์/เคมี/ชีวา" in top_subs
    is_art = "Art & Design" in top_subs or "ศิลปะ/ออกแบบ" in top_subs
    is_tech = "Technology" in top_subs or "คอมพิวเตอร์/เทคโนโลยี" in top_subs

    st.markdown("### 1. สรุปประพจน์ทั้งหมด (Propositions Setup)")
    
    st.write(f"- **ประพจน์ $M_{{{mbti}}}$**: ผู้เรียนเป็นคนประเภท {mbti} = `True`")
    st.write(f"- **ประพจน์ $P$ (ชอบคณิตศาสตร์)** = `{is_math}`")
    st.write(f"- **ประพจน์ $Q$ (ชอบวิทยาศาสตร์)** = `{is_sci}`")
    st.write(f"- **ประพจน์ $R$ (ชอบศิลปะ/การออกแบบ)** = `{is_art}`")
    st.write(f"- **ประพจน์ $S$ (ชอบเทคโนโลยี/ไอที)** = `{is_tech}`")

    st.markdown("---")
    st.markdown("### 2. นิยามเงื่อนไขทางตรรกศาสตร์ของแต่ละคณะ (Logical Rules for Faculties)")
    
    # ---------------------------------------------------------
    # ตารางเงื่อนไขการเชื่อมประพจน์ด้วย "และ" (AND Logic)
    # ---------------------------------------------------------
    faculties_rules = [
        {
            "faculty": "คณะวิทยาศาสตร์ / วิทยาศาสตร์ข้อมูล",
            "condition_symbol": r"M_{INTJ} \land P \land Q",
            "eval": (mbti == "INTJ") and is_math and is_sci,
            "rule_desc": "ต้องเป็น INTJ AND ชอบคณิต (P) AND ชอบวิทย์ (Q)"
        },
        {
            "faculty": "คณะวิศวกรรมศาสตร์ / เทคโนโลยีคอมพิวเตอร์",
            "condition_symbol": r"(M_{INTJ} \lor M_{INTP} \lor M_{ENTP}) \land P \land S",
            "eval": (mbti in ["INTJ", "INTP", "ENTP"]) and is_math and is_tech,
            "rule_desc": "ต้องเป็น (INTJ OR INTP OR ENTP) AND ชอบคณิต (P) AND ชอบเทคโนโลยี (S)"
        },
        {
            "faculty": "คณะแพทยศาสตร์ / จิตวิทยาคลินิก",
            "condition_symbol": r"(M_{INFJ} \lor M_{INTJ}) \land Q",
            "eval": (mbti in ["INFJ", "INTJ"]) and is_sci,
            "rule_desc": "ต้องเป็น (INFJ OR INTJ) AND ชอบวิทย์ (Q)"
        },
        {
            "faculty": "คณะศิลปกรรมศาสตร์ / UX-UI Design",
            "condition_symbol": r"(M_{INFP} \lor M_{ISFP} \lor M_{ENTP}) \land R",
            "eval": (mbti in ["INFP", "ISFP", "ENTP"]) and is_art,
            "rule_desc": "ต้องเป็น (INFP OR ISFP OR ENTP) AND ชอบศิลปะ (R)"
        }
    ]

    matched_faculties = []

    for item in faculties_rules:
        st.markdown(f"#### 🏛️ {item['faculty']}")
        st.latex(rf"\text{{เงื่อนไข: }} {item['condition_symbol']}")
        st.write(f"คำอธิบายเงื่อนไข: {item['rule_desc']}")
        
        if item['eval']:
            st.success("ผลลัพธ์ทางตรรกศาสตร์: **TRUE (จริง - ตรงตามเงื่อนไขเข้าคณะนี้ได้)**")
            matched_faculties.append(item['faculty'])
        else:
            st.error("ผลลัพธ์ทางตรรกศาสตร์: **FALSE (เท็จ - ไม่ตรงตามเงื่อนไข)**")
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. สรุปคณะที่สอบผ่านเงื่อนไขตรรกศาสตร์
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("🎯 สรุปผลคณะและอาชีพที่ตรงตามเงื่อนไขตรรกศาสตร์ของคุณ")
    
    if matched_faculties:
        st.balloons()
        for fac in matched_faculties:
            st.markdown(f"- ✅ **{fac}**")
    else:
        st.warning("ยังไม่พบคณะที่ตรงตามเงื่อนไขตรรกศาสตร์แบบสมบูรณ์ (ลองปรับเปลี่ยนการประเมินวิชาที่ชอบใน Step 3)")

    st.markdown("---")
    if st.button("🔄 เริ่มทำแบบประเมินใหม่"):
        st.session_state.step = 1
        st.rerun()
