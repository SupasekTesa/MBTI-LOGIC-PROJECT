import streamlit as st
from questions import (
    COGNITIVE_QUESTIONS, 
    SUBJECT_QUESTIONS, 
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
if 'top_subjects' not in st.session_state:
    st.session_state.top_subjects = []

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
                key=f"cog_{q.get('id', idx)}",
                horizontal=True
            )
            raw_answers[q.get('id', idx)] = {"func": q["func"], "score": SCALE_OPTIONS[ans]}
            st.markdown("<hr style='margin: 0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)
            
        submitted = st.form_submit_button("🚀 ประมวลผล MBTI")
        
        if submitted:
            func_scores = {"Ne": 0, "Ni": 0, "Se": 0, "Si": 0, "Te": 0, "Ti": 0, "Fe": 0, "Fi": 0}
            for item in raw_answers.values():
                func_scores[item["func"]] += item["score"]

            func_percentages = {func: round((score / 50) * 100, 1) for func, score in func_scores.items()}
            sorted_funcs = sorted(func_scores.items(), key=lambda x: x[1], reverse=True)

            dom_func = max(func_scores, key=func_scores.get)
            
            aux_candidates_map = {
                "Ne": ["Ti", "Fi"], "Se": ["Ti", "Fi"],
                "Ni": ["Te", "Fe"], "Si": ["Te", "Fe"],
                "Te": ["Ni", "Si"], "Fe": ["Ni", "Si"],
                "Ti": ["Ne", "Se"], "Fi": ["Ne", "Se"]
            }
            possible_aux = aux_candidates_map.get(dom_func, ["Te", "Fe"])
            aux_func = max(possible_aux, key=lambda f: func_scores[f])

            opposite_map = {
                "Ne": "Si", "Si": "Ne",
                "Ni": "Se", "Se": "Ni",
                "Te": "Fi", "Fi": "Te",
                "Ti": "Fe", "Fe": "Ti"
            }
            tertiary_func = opposite_map[aux_func]
            inferior_func = opposite_map[dom_func]

            st.session_state.func_scores = func_scores
            st.session_state.func_percentages = func_percentages
            st.session_state.sorted_funcs = sorted_funcs
            st.session_state.possible_aux = possible_aux
            st.session_state.mbti_stack = {
                "Dom": dom_func,
                "Aux": aux_func,
                "Tert": tertiary_func,
                "Inf": inferior_func
            }

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
# STEP 2: สรุปผล MBTI และแสดงสมการตรรกศาสตร์
# ---------------------------------------------------------
elif st.session_state.step == 2:
    st.title("🌟 ขั้นตอนที่ 2: สรุปผลลัพธ์และแบบจำลองตรรกศาสตร์ MBTI")
    
    mbti = st.session_state.mbti_result
    info = MBTI_DESCRIPTIONS.get(mbti, MBTI_DESCRIPTIONS["INTJ"])
    sorted_funcs = st.session_state.get("sorted_funcs", [])
    func_pct = st.session_state.get("func_percentages", {})
    stack = st.session_state.get("mbti_stack", {})
    possible_aux = st.session_state.get("possible_aux", [])
    
    st.success(f"### ผลการวิเคราะห์ MBTI: **{mbti}** ({info['title']})")
    st.info(f"**ลักษณะตัวตน:** {info['desc']}")

    st.subheader("📊 ลำดับคะแนนและ Cognitive Stack")
    col_chart, col_rank = st.columns([3, 2])
    
    with col_chart:
        st.markdown("**ระดับความเข้มข้นของฟังก์ชัน (%):**")
        for func_code, score in sorted_funcs:
            pct = func_pct.get(func_code, 0)
            st.write(f"**{func_code}**: {score}/50 คะแนน ({pct}%)")
            st.progress(pct / 100)
            
    with col_rank:
        st.markdown("**ฟังก์ชันการทำงานหลัก:**")
        if stack:
            st.write(f"🥇 **Dominant:** `{stack['Dom']}` ({func_pct.get(stack['Dom'], 0)}%)")
            st.write(f"🥈 **Auxiliary:** `{stack['Aux']}` ({func_pct.get(stack['Aux'], 0)}%)")
            st.write(f"🥉 **Tertiary:** `{stack['Tert']}` ({func_pct.get(stack['Tert'], 0)}%)")
            st.write(f"⚓ **Inferior:** `{stack['Inf']}` ({func_pct.get(stack['Inf'], 0)}%)")
            
    st.markdown("---")

    if stack:
        dom = stack['Dom']
        aux = stack['Aux']
        tert = stack['Tert']
        inf = stack['Inf']
        aux_str = ", ".join(possible_aux)
        aux_set_display = "{" + aux_str + "}"

        with st.expander("📚 คลิกเพื่อดูตรรกศาสตร์การคำนวณ (ระดับ ม.4: เรื่องประพจน์และเงื่อนไข)", expanded=True):
            st.markdown("### 1. การกำหนดประพจน์พื้นฐาน (Propositions Setup)")
            st.write(f"* **ประพจน์ $A$**: {dom} เป็นฟังก์ชันที่มีคะแนนสูงที่สุดในทุกฟังก์ชัน `(True)`")
            st.write(f"* **ประพจน์ $B$**: {aux} เป็นฟังก์ชันที่มีคะแนนสูงที่สุดในกลุ่ม {aux_set_display} `(True)`")
            st.write(f"* **ประพจน์ $M_{{{mbti}}}$**: ผู้เรียนมีบุคลิกภาพแบบ {mbti} `(True)`")
            
            st.markdown("---")
            st.markdown("### 2. เงื่อนไขทางตรรกศาสตร์ในการตัดสิน Dominant (ฟังก์ชันหลัก)")
            st.latex(rf"A \iff (\text{{Dom}} = \text{{{dom}}})")
            st.caption(f"อธิบาย: ประพจน์ A เป็นจริง ก็ต่อเมื่อ กำหนดให้ Dominant Function คือ {dom}")

            st.markdown("---")
            st.markdown("### 3. ตรรกศาสตร์การเลือก Auxiliary (ฟังก์ชันรอง) และการตัดสินประเภท")
            st.latex(rf"B \iff (\text{{Aux}} = \text{{{aux}}})")
            st.caption(f"อธิบาย: ประพจน์ B เป็นจริง ก็ต่อเมื่อ กำหนดให้ Auxiliary Function คือ {aux}")

            st.markdown(f"**เงื่อนไขประพจน์สรุปประเภท {mbti}:**")
            st.latex(rf"(A \land B) \implies M_{{{mbti}}}")
            st.write(f"* **สรุปตรรกศาสตร์:** (ประพจน์ $A$ เป็นจริง) $\\land$ (ประพจน์ $B$ เป็นจริง) $\\implies$ สรุปว่าเป็นประพจน์ **$M_{{{mbti}}}$**")

            st.markdown("---")
            st.markdown("### 4. กฎคู่สมดุลตรงข้าม (สมมูลทางตรรกศาสตร์ $\iff$)")
            st.latex(rf"(\text{{Dom}} = \text{{{dom}}}) \iff (\text{{Inferior}} = \text{{{inf}}})")
            st.latex(rf"(\text{{Aux}} = \text{{{aux}}}) \iff (\text{{Tertiary}} = \text{{{tert}}})")

    st.markdown("---")
    if st.button("➡️ ไปต่อ: เลือกความชอบวิชาเพื่อสร้างประพจน์ความชอบ (Step 3)"):
        st.session_state.step = 3
        st.rerun()

# ---------------------------------------------------------
# STEP 3: ประเมินวิชาที่ชอบ และกำหนดประพจน์วิชา (ปรับปรุงให้อัปเดตตาม questions.py เสมอ)
# ---------------------------------------------------------
elif st.session_state.step == 3:
    st.title("📚 ขั้นตอนที่ 3: สรุปประพจน์ความชอบวิชา (Subject Propositions)")
    st.write("เลือกสเกลวิชาที่ชอบ เพื่อสรุปวิชาที่เด่นที่สุดมาตั้งเป็นประพจน์ทางตรรกศาสตร์")
    
    with st.form("subject_form"):
        sub_scores = {}
        for idx, q in enumerate(SUBJECT_QUESTIONS, 1):
            q_id = q.get('id', idx)
            st.markdown(f"**ข้อที่ {idx}:** {q['text']} *(หมวด: {q['category']})*")
            ans = st.radio(
                f"ระดับความตรง ({q_id}):", 
                options=list(SCALE_OPTIONS.keys()), 
                index=2, 
                key=f"sub_{q_id}", 
                horizontal=True
            )
            sub_scores[q["category"]] = sub_scores.get(q["category"], 0) + SCALE_OPTIONS[ans]
            st.markdown("<hr style='margin: 0.3rem 0 1rem 0;'>", unsafe_allow_html=True)
            
        submitted_step3 = st.form_submit_button("🚀 สรุปประพจน์ความชอบและตรวจสอบเงื่อนไข (Step 4)")
        
        if submitted_step3:
            sorted_subjects = sorted(sub_scores.items(), key=lambda x: x[1], reverse=True)
            st.session_state.sub_scores = sub_scores
            # เก็บหมวดวิชาที่ได้คะแนนสูงสุด 2 อันดับแรก
            st.session_state.top_subjects = [s[0] for s in sorted_subjects[:2]]
            st.session_state.step = 4
            st.rerun()

# ---------------------------------------------------------
# STEP 4: เชื่อมประพจน์ (AND) & ตรวจสอบเงื่อนไขคณะ/อาชีพ
# ---------------------------------------------------------
elif st.session_state.step == 4:
    st.title("🎓 ขั้นตอนที่ 4: การประมวลผลตรรกศาสตร์เชื่อมประพจน์ (AND Logic)")
    
    mbti = st.session_state.mbti_result
    top_subs = st.session_state.get("top_subjects", [])

    # ฟังก์ชันช่วยตรวจเช็กหมวดวิชาแบบรองรับทั้งคำไทยและคำอังกฤษ
    def check_subject(keywords, target_list):
        return any(any(kw.lower() in sub.lower() for kw in keywords) for sub in target_list)

    is_math = check_subject(["math", "คณิต"], top_subs)
    is_sci = check_subject(["science", "วิทย์", "ชีว", "เคมี"], top_subs)
    is_art = check_subject(["art", "ศิลปะ", "ออกแบบ", "design"], top_subs)
    is_tech = check_subject(["tech", "คอมพิวเตอร์", "เทคโนโลยี", "it"], top_subs)

    st.markdown("### 1. สรุปประพจน์ทั้งหมด (Propositions Setup)")
    st.write(f"- **ประพจน์ $M_{{{mbti}}}$**: ผู้เรียนเป็นคนประเภท {mbti} = `True`")
    st.write(f"- **ประพจน์ $P$ (ชอบคณิตศาสตร์)** = `{is_math}`")
    st.write(f"- **ประพจน์ $Q$ (ชอบวิทยาศาสตร์)** = `{is_sci}`")
    st.write(f"- **ประพจน์ $R$ (ชอบศิลปะ/การออกแบบ)** = `{is_art}`")
    st.write(f"- **ประพจน์ $S$ (ชอบเทคโนโลยี/ไอที)** = `{is_tech}`")

    st.markdown("---")
    st.markdown("### 2. นิยามเงื่อนไขทางตรรกศาสตร์ของแต่ละคณะ (Logical Rules for Faculties)")
    
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
        st.session_state.clear()
        st.rerun()
