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
if 'category_scores' not in st.session_state:
    st.session_state.category_scores = {}

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
            q_id = q.get('id', idx)
            st.markdown(f"**ข้อที่ {idx}:** {q['text']}")
            ans = st.radio(
                f"ระดับความตรง (ข้อ {idx}):", 
                options=list(SCALE_OPTIONS.keys()), 
                index=2, 
                key=f"cog_{q_id}",
                horizontal=True
            )
            raw_answers[q_id] = {"func": q["func"], "score": SCALE_OPTIONS[ans]}
            st.markdown("<hr style='margin: 0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)
            
        submitted = st.form_submit_button("🚀 ประมวลผล MBTI (ไปขั้นตอนที่ 2)")
        
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
        aux_str = ", ".join(possible_aux)

        with st.expander("📚 คลิกเพื่อดูตรรกศาสตร์การคำนวณ", expanded=True):
            st.markdown("### 1. การกำหนดประพจน์พื้นฐาน")
            st.write(f"* **ประพจน์ $A$**: {dom} เป็นฟังก์ชันที่มีคะแนนสูงที่สุด `(True)`")
            st.write(f"* **ประพจน์ $B$**: {aux} เป็นฟังก์ชันรองที่มีคะแนนสูงสุดในกลุ่ม {{{aux_str}}} `(True)`")
            st.write(f"* **ประพจน์ $M_{{{mbti}}}$**: สรุปว่าเป็นบุคลิกภาพ {mbti} `(True)`")
            st.latex(rf"(A \land B) \implies M_{{{mbti}}}")

    st.markdown("---")
    if st.button("➡️ ไปต่อ: ประเมินความชอบ 5 หมวดหมู่ (Step 3)"):
        st.session_state.step = 3
        st.rerun()

# ---------------------------------------------------------
# STEP 3: ประเมินความชอบ 5 หมวดหมู่ (วิชา, งานอดิเรก, เป้าหมาย, การเงิน)
# ---------------------------------------------------------
elif st.session_state.step == 3:
    st.title("📚 ขั้นตอนที่ 3: ประเมินความชอบและศักยภาพ 5 หมวดหมู่")
    st.write("กรุณาทำแบบประเมินให้ครบทั้ง 5 หมวด เพื่อนำไปสรุปเป็นประพจน์ทางตรรกศาสตร์")
    
    all_question_sets = [
        ("📖 1. วิชาความรู้ (Subject Knowledge)", SUBJECT_QUESTIONS, "sub"),
        ("🎨 2. งานอดิเรกและความสนใจ (Hobbies & Interests)", HOBBY_QUESTIONS, "hobby"),
        ("🎯 3. เป้าหมายอาชีพและค่านิยม (Career Goals)", GOAL_QUESTIONS, "goal"),
        ("💰 4. การบริหารและการเงิน (Financial & Management)", FINANCIAL_QUESTIONS, "fin")
    ]
    
    with st.form("all_categories_form"):
        category_scores = {}
        
        for tab_name, questions_list, prefix in all_question_sets:
            st.subheader(tab_name)
            for idx, q in enumerate(questions_list, 1):
                # ดึงข้อมูลแบบปลอดภัย ป้องกัน KeyError
                if isinstance(q, dict):
                    q_text = q.get('text') or q.get('question') or str(q)
                    category = q.get('category', 'ทั่วไป')
                    q_id = q.get('id', f"{prefix}_{idx}")
                else:
                    q_text = str(q)
                    category = 'ทั่วไป'
                    q_id = f"{prefix}_{idx}"
                
                st.markdown(f"**ข้อที่ {idx}:** {q_text} *(หมวด: {category})*")
                ans = st.radio(
                    f"ระดับความตรง ({q_id}):", 
                    options=list(SCALE_OPTIONS.keys()), 
                    index=2, 
                    key=f"{prefix}_{q_id}", 
                    horizontal=True
                )
                category_scores[category] = category_scores.get(category, 0) + SCALE_OPTIONS[ans]
                st.markdown("<hr style='margin: 0.2rem 0 0.8rem 0;'>", unsafe_allow_html=True)
            st.markdown("---")

        submitted_step3 = st.form_submit_button("🚀 สรุปประพจน์และประมวลผลหาคณะ/อาชีพ (Step 4)")
        
        if submitted_step3:
            st.session_state.category_scores = category_scores
            st.session_state.step = 4
            st.rerun()
# ---------------------------------------------------------
# STEP 4: เชื่อมประพจน์ (AND/OR Logic) & ตรวจสอบเงื่อนไขคณะ/อาชีพ
# ---------------------------------------------------------
elif st.session_state.step == 4:
    st.title("🎓 ขั้นตอนที่ 4: ประมวลผลตรรกศาสตร์เชื่อมประพจน์และสรุปคณะ/อาชีพ")
    
    mbti = st.session_state.mbti_result
    cat_scores = st.session_state.get("category_scores", {})

    # ฟังก์ชันช่วยเช็กคะแนนในแต่ละหมวดว่าสูงกว่าเกณฑ์ปานกลางไหม (คะแนนเฉลี่ย >= 3 ต่อข้อ)
    def is_category_high(keywords):
        for cat, score in cat_scores.items():
            if any(kw.lower() in cat.lower() for kw in keywords):
                if score >= 6: # มีความสนใจในระดับปานกลางขึ้นไป
                    return True
        return False

    # กำหนดประพจน์หลักตามหมวดหมู่
    is_math_sci = is_category_high(["math", "คณิต", "science", "วิทย์", "ฟิสิกส์", "เคมี", "ชีว"])
    is_tech = is_category_high(["tech", "คอมพิวเตอร์", "เทคโนโลยี", "it", "coding", "นวัตกรรม"])
    is_art_design = is_category_high(["art", "ศิลปะ", "ออกแบบ", "design", "สร้างสรรค์", "บันเทิง"])
    is_biz_finance = is_category_high(["finance", "การเงิน", "ธุรกิจ", "การบริหาร", "การลงทุน", "การตลาด", "การค้า"])
    is_social_people = is_category_high(["social", "สังคม", "ภาษา", "จิตวิทยา", "การบริการ", "การสื่อสาร", "บริหารคน"])

    st.markdown("### 1. สรุปประพจน์ความสนใจและศักยภาพ (Propositions Setup)")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.write(f"- **ประพจน์ $M_{{{mbti}}}$**: บุคลิกภาพแบบ {mbti} = `True`")
        st.write(f"- **ประพจน์ $P$ (สนใจสายวิทยาศาสตร์/คณิตศาสตร์)** = `{is_math_sci}`")
        st.write(f"- **ประพจน์ $Q$ (สนใจเทคโนโลยี/ไอที/นวัตกรรม)** = `{is_tech}`")
    with col_p2:
        st.write(f"- **ประพจน์ $R$ (สนใจศิลปะ/การออกแบบ/งานสร้างสรรค์)** = `{is_art_design}`")
        st.write(f"- **ประพจน์ $S$ (สนใจบริหาร/การเงิน/ธุรกิจ)** = `{is_biz_finance}`")
        st.write(f"- **ประพจน์ $T$ (สนใจมนุษยศาสตร์/สังคม/จิตวิทยา/ภาษา)** = `{is_social_people}`")

    st.markdown("---")
    st.markdown("### 2. ตรวจสอบเงื่อนไขทางตรรกศาสตร์ของแต่ละสายคณะและอาชีพ")
    
    # นิยามเงื่อนไขตรรกศาสตร์ครอบคลุมทุกสายอาชีพ
    faculties_rules = [
        {
            "faculty": "🏛️ คณะวิศวกรรมศาสตร์ / เทคโนโลยีสารสนเทศ (Engineers & Developers)",
            "condition_symbol": r"(M_{INTJ} \lor M_{INTP} \lor M_{ENTP} \lor M_{ISTP}) \land Q \land (P \lor S)",
            "eval": (mbti in ["INTJ", "INTP", "ENTP", "ISTP"]) and is_tech and (is_math_sci or is_biz_finance),
            "rule_desc": "ต้องเป็น (INTJ, INTP, ENTP, ISTP) AND สนใจเทคโนโลยี (Q) AND (สนใจวิทย์/คณิต หรือ การเงิน)",
            "careers": "วิศวกรซอฟต์แวร์, นักพัฒนาระบบ, Data Scientist, วิศวกรเครือข่าย"
        },
        {
            "faculty": "🏛️ คณะแพทยศาสตร์ / เภสัชศาสตร์ / จิตวิทยาคลินิก (Healthcare & Medical Sciences)",
            "condition_symbol": r"(M_{INFJ} \lor M_{INTJ} \lor M_{ISFJ} \lor M_{ENFJ}) \land P \land T",
            "eval": (mbti in ["INFJ", "INTJ", "ISFJ", "ENFJ"]) and is_math_sci and is_social_people,
            "rule_desc": "ต้องเป็น (INFJ, INTJ, ISFJ, ENFJ) AND สนใจวิทย์ (P) AND สนใจสังคม/ช่วยเหลือคน (T)",
            "careers": "แพทย์, เภสัชกร, นักจิตวิทยาคลินิก, นักวิจัยทางแพทย์"
        },
        {
            "faculty": "🏛️ คณะบริหารธุรกิจ / เศรษฐศาสตร์ / การบัญชีและการเงิน (Business & Finance)",
            "condition_symbol": r"(M_{ENTJ} \lor M_{ESTJ} \lor M_{ESTP} \lor M_{ENTP}) \land S",
            "eval": (mbti in ["ENTJ", "ESTJ", "ESTP", "ENTP"]) and is_biz_finance,
            "rule_desc": "ต้องเป็น (ENTJ, ESTJ, ESTP, ENTP) AND สนใจธุรกิจและการเงิน (S)",
            "careers": "นักลงทุน, ผู้ประกอบการ, นักวิเคราะห์การเงิน, ผู้จัดการฝ่ายกลยุทธ์"
        },
        {
            "faculty": "🏛️ คณะศิลปกรรมศาสตร์ / UX-UI Design / สื่อดิจิทัล (Arts & Creative Design)",
            "condition_symbol": r"(M_{INFP} \lor M_{ISFP} \lor M_{ENFP} \lor M_{ENTP}) \land R",
            "eval": (mbti in ["INFP", "ISFP", "ENFP", "ENTP"]) and is_art_design,
            "rule_desc": "ต้องเป็น (INFP, ISFP, ENFP, ENTP) AND สนใจงานศิลป์/สร้างสรรค์ (R)",
            "careers": "UX/UI Designer, กราฟิกดีไซเนอร์, ครีเอทีฟ, แอนิเมเตอร์"
        },
        {
            "faculty": "🏛️ คณะนิเทศศาสตร์ / อักษรศาสตร์ / การตลาดและสื่อสาร (Communications & Media)",
            "condition_symbol": r"(M_{ENFP} \lor M_{ESFP} \lor M_{ENFJ} \lor M_{ENTP}) \land (R \lor S \lor T)",
            "eval": (mbti in ["ENFP", "ESFP", "ENFJ", "ENTP"]) and (is_art_design or is_biz_finance or is_social_people),
            "rule_desc": "ต้องเป็น (ENFP, ESFP, ENFJ, ENTP) AND (สนใจศิลป์ หรือ ธุรกิจ หรือ สื่อสารสังคม)",
            "careers": "นักการตลาดดิจิทัล, PR Manager, นักเขียน/นักคอนเทนต์, ผู้จัดรายการ"
        },
        {
            "faculty": "🏛️ คณะนิติศาสตร์ / รัฐศาสตร์ / สังคมสงเคราะห์ (Law & Public Administration)",
            "condition_symbol": r"(M_{ISTJ} \lor M_{ESTJ} \lor M_{INTJ} \lor M_{ENFJ}) \land T",
            "eval": (mbti in ["ISTJ", "ESTJ", "INTJ", "ENFJ"]) and is_social_people,
            "rule_desc": "ต้องเป็น (ISTJ, ESTJ, INTJ, ENFJ) AND สนใจสังคม/กฎหมาย/การเมือง (T)",
            "careers": "ทนายความ, ผู้พิพากษา, นักการเมือง, นักการทูต, ข้าราชการบริหาร"
        }
    ]

    matched_faculties = []

    for item in faculties_rules:
        st.markdown(f"#### {item['faculty']}")
        st.latex(rf"\text{{เงื่อนไข: }} {item['condition_symbol']}")
        st.write(f"**คำอธิบายเงื่อนไข:** {item['rule_desc']}")
        st.write(f"**อาชีพที่แนะนำ:** {item['careers']}")
        
        if item['eval']:
            st.success("ผลลัพธ์ทางตรรกศาสตร์: **TRUE (จริง - ตรงตามเงื่อนไขสายนี้)**")
            matched_faculties.append((item['faculty'], item['careers']))
        else:
            st.error("ผลลัพธ์ทางตรรกศาสตร์: **FALSE (เท็จ - ไม่ตรงตามเงื่อนไข)**")
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🎯 สรุปคณะและอาชีพที่ตรงตามเงื่อนไขตรรกศาสตร์ของคุณ")
    
    if matched_faculties:
        st.balloons()
        for fac_title, careers in matched_faculties:
            st.markdown(f"- ✅ **{fac_title}**")
            st.caption(f"  └ อาชีพที่เหมาะสม: {careers}")
    else:
        st.warning("ยังไม่พบคณะที่ตรงตามเงื่อนไขตรรกศาสตร์แบบสมบูรณ์ (ลองปรับเปลี่ยนการประเมินความชอบใน Step 3)")

    st.markdown("---")
    if st.button("🔄 เริ่มทำแบบประเมินใหม่ทั้งหมด"):
        st.session_state.clear()
        st.rerun()
