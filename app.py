import streamlit as st
import pandas as pd
import plotly.express as px
from questions import (
    COGNITIVE_QUESTIONS, 
    SUBJECT_QUESTIONS, 
    HOBBY_QUESTIONS, 
    GOAL_QUESTIONS,
    FINANCIAL_QUESTIONS
)

# ==========================================
# 1. PAGE CONFIG & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="ระบบวิเคราะห์ MBTI & Cognitive Functions",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    
    /* การ์ดคำถามแบบสอบถาม Step 1 */
    .question-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .question-badge {
        display: inline-block;
        background-color: #EFF6FF;
        color: #2563EB;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    .question-text {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }

    /* การ์ดคำถาม Step 2-4 */
    .category-badge {
        display: inline-block;
        background-color: #F1F5F9;
        color: #475569;
        font-weight: 700;
        font-size: 0.8rem;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        margin-bottom: 0.4rem;
        border: 1px solid #CBD5E1;
    }
    .sub-question-card {
        background-color: #FFFFFF;
        border-left: 5px solid #3B82F6;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }

    /* การ์ดสรุปผล MBTI */
    .mbti-hero-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 2.5rem 1.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        margin-bottom: 2rem;
    }
    .mbti-type-text {
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .func-card {
        background-color: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }
    .func-badge {
        font-size: 0.85rem;
        font-weight: bold;
        color: #64748B;
        text-transform: uppercase;
    }
    .func-title {
        font-size: 2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin: 0.3rem 0;
    }
    .func-desc {
        font-size: 0.85rem;
        color: #475569;
    }

    /* การ์ดอาชีพแนะนำ */
    .career-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .career-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #0F172A;
        margin: 0.4rem 0;
    }

    .logic-box {
        background-color: #0F172A;
        color: #38BDF8;
        border-radius: 12px;
        padding: 1.5rem;
        font-family: 'Courier New', monospace;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# ฐานข้อมูลจับคู่ MBTI & ลำดับฟังก์ชัน
MBTI_STACKS = {
    "ENTP": {"Dom": "Ne", "Aux": "Ti", "Tert": "Fe", "Inf": "Si", "Title": "นักประดิษฐ์และนักโต้วิเคราะห์"},
    "INTP": {"Dom": "Ti", "Aux": "Ne", "Tert": "Si", "Inf": "Fe", "Title": "นักคิดเชิงตรรกะและนักสืบค้น"},
    "ENTJ": {"Dom": "Te", "Aux": "Ni", "Tert": "Se", "Inf": "Fi", "Title": "ผู้บังคับบัญชาและนักวางกลยุทธ์"},
    "INTJ": {"Dom": "Ni", "Aux": "Te", "Tert": "Fi", "Inf": "Se", "Title": "นักวางแผนและนักคิดเชิงวิสัยทัศน์"},
    "ENFP": {"Dom": "Ne", "Aux": "Fi", "Tert": "Te", "Inf": "Si", "Title": "ผู้สร้างแรงบันดาลใจและนักจุดประกาย"},
    "INFP": {"Dom": "Fi", "Aux": "Ne", "Tert": "Si", "Inf": "Te", "Title": "นักอุดมคติและผู้แสวงหาความจริงแท้"},
    "ENFJ": {"Dom": "Fe", "Aux": "Ni", "Tert": "Se", "Inf": "Ti", "Title": "ตัวแทนผู้สร้างความเปลี่ยนแปลง"},
    "INFJ": {"Dom": "Ni", "Aux": "Fe", "Tert": "Ti", "Inf": "Se", "Title": "ผู้แนะนำและนักหยั่งรู้จิตใจ"},
    "ESTP": {"Dom": "Se", "Aux": "Ti", "Tert": "Fe", "Inf": "Ni", "Title": "ผู้ลุยแก้ปัญหาและนักปรับตัว"},
    "ISTP": {"Dom": "Ti", "Aux": "Se", "Tert": "Ni", "Inf": "Fe", "Title": "ช่างฝีมือและนักวิเคราะห์เครื่องกล"},
    "ESTJ": {"Dom": "Te", "Aux": "Si", "Tert": "Ne", "Inf": "Fi", "Title": "ผู้บริหารและนักจัดการระบบ"},
    "ISTJ": {"Dom": "Si", "Aux": "Te", "Tert": "Fi", "Inf": "Ne", "Title": "ผู้ตรวจสอบและนักลงมือทำตามหน้าที่"},
    "ESFP": {"Dom": "Se", "Aux": "Fi", "Tert": "Te", "Inf": "Ni", "Title": "ผู้สร้างความบันเทิงและมีชีวิตชีวา"},
    "ISFP": {"Dom": "Fi", "Aux": "Se", "Tert": "Ni", "Inf": "Te", "Title": "ศิลปินและผู้หลงใหลในสุนทรียภาพ"},
    "ESFJ": {"Dom": "Fe", "Aux": "Si", "Tert": "Ne", "Inf": "Ti", "Title": "ผู้ดูแลความสงบและผู้ประสานงาน"},
    "ISFJ": {"Dom": "Si", "Aux": "Fe", "Tert": "Ti", "Inf": "Ne", "Title": "ผู้ปกป้องและผู้เอื้ออารี"},
}

FUNC_DESCRIPTIONS = {
    "Ne": "คิดนอกกรอบ หาไอเดียใหม่ๆ เชื่อมโยงสิ่งรอบตัว",
    "Ni": "มองเห็นวิสัยทัศน์ ภาพรวมในอนาคต มีลางสังหรณ์แม่นยำ",
    "Se": "อยู่กับปัจจุบัน รับรู้ประสาทสัมผัส ปรับตัวไว",
    "Si": "ละเอียดยอดเยี่ยม ทำตามขั้นตอน จดจำประสบการณ์อดีต",
    "Te": "เน้นผลลัพธ์ จัดระบบ วางแผนเด็ดขาด บริหารงานเก่ง",
    "Ti": "วิเคราะห์ตรรกะภายใน ตั้งคำถาม หาเหตุผลลึกซึ้ง",
    "Fe": "แคร์ความรู้สึกกลุ่ม สร้างบรรยากาศ มารยาทสังคม",
    "Fi": "ยึดมั่นค่านิยมส่วนตัว ความจริงแท้ จริงใจกับความรู้สึก"
}

# ==========================================
# ฐานข้อมูลวิเคราะห์อาชีพเชิงลึกตาม MBTI
# ==========================================
MBTI_CAREER_ANALYSIS = {
    "ENTP": {
        "cognitive_style": "ใช้ Extraverted Intuition (Ne) สำรวจความเป็นไปได้ใหม่ๆ ร่วมกับ Introverted Thinking (Ti) ที่วิเคราะห์โครงสร้างตรรกะอย่างเฉียบแหลม",
        "why_fit": "คุณมีธรรมชาติของนักคิดนอกกรอบ สามารถมองเห็นรอยรั่วหรือโอกาสในระบบที่คนอื่นมองไม่เห็น กล้าตั้งคำถามกับกฎเดิมๆ และสนุกกับการแก้ปัญหาที่ไม่ซ้ำซาก",
        "work_environment": "เหมาะกับงานที่ยืดหยุ่น ให้อิสระในการทดลองความคิดใหม่ๆ มีความท้าทาย และไม่ต้องทำงานประจำที่เป็นพิธีการซ้ำๆ ทุกวัน",
        "careers": [
            {"title": "นักพัฒนานวัตกรรม / Startup Founder", "desc": "ใช้ Ne มองเห็นโอกาสทางธุรกิจใหม่ๆ และใช้ Ti ออกแบบโมเดลธุรกิจเชิงตรรกะ"},
            {"title": "Software Architect / Tech Consultant", "desc": "ออกแบบสถาปัตยกรรมระบบที่ซับซ้อนและให้คำปรึกษาการแก้ปัญหาเทคโนโลยี"},
            {"title": "นักวางกลยุทธ์การตลาด (Marketing Strategist)", "desc": "คิดค้นแคมเปญสร้างสรรค์ที่ฉีกแนวและวิเคราะห์อินไซต์ผู้บริโภค"}
        ]
    },
    "INTP": {
        "cognitive_style": "ใช้ Introverted Thinking (Ti) ในการจำลองโครงสร้างตรรกะในหัวอย่างลึกซึ้ง และเสริมด้วย Extraverted Intuition (Ne) เพื่อเชื่อมโยงทฤษฎี",
        "why_fit": "คุณเด่นในการถอดรหัสความซับซ้อน ค้นหาความถูกต้องแม่นยำเชิงทฤษฎี ชอบอยู่กับโจทย์ยากๆ ที่ต้องใช้การคิดเชิงวิเคราะห์ลึกซึ้งโดยไม่มีใครมารบกวน",
        "work_environment": "เหมาะกับงานที่ได้ใช้สมาธิสูง งานวิจัย งานเชิงทฤษฎีและเทคโนโลยีที่มีอิสระทางความคิด ไม่เน้นงานการเมืองในองค์กร",
        "careers": [
            {"title": "Data Scientist / AI Engineer", "desc": "วิเคราะห์อัลกอริทึมและสร้างโมเดลคณิตศาสตร์ประมวลผลข้อมูลขนาดใหญ่"},
            {"title": "นักวิจัยเชิงทฤษฎี / นักวิทยาศาสตร์", "desc": "ค้นคว้า ค้นหาหลักการใหม่ๆ และแก้โจทย์เชิงลึกทางวิทยาศาสตร์"},
            {"title": "Backend Systems Developer", "desc": "ออกแบบและเขียนโค้ดโครงสร้างพื้นฐานเบื้องหลังระบบคอมพิวเตอร์ให้มีความเสถียรสูงสุด"}
        ]
    },
    "ENTJ": {
        "cognitive_style": "ใช้ Extraverted Thinking (Te) ในการวางโครงสร้างและเร่งรัดผลลัพธ์ ผสานกับ Introverted Ni ที่วางวิสัยทัศน์ระยะยาว",
        "why_fit": "คุณมีสัญชาตญาณความเป็นผู้นำ มองเห็นเป้าหมายชัดเจน ตัดสินใจเด็ดขาดโดยอิงข้อมูลจริง และสามารถบริหารจัดการคนและทรัพยากรให้บรรลุเป้าหมายได้อย่างมีประสิทธิภาพสูงสุด",
        "work_environment": "เหมาะกับสภาพแวดล้อมที่เน้นผลงาน (Performance-driven) องค์กรที่มีการเติบโตสูง หรือตำแหน่งบริหารที่ได้ใช้อำนาจในการตัดสินใจ",
        "careers": [
            {"title": "ผู้บริหารองค์กร / Management Consultant", "desc": "ปรับปรุงประสิทธิภาพองค์กร วางโครงสร้างกลยุทธ์ และขับเคลื่อนเป้าหมายใหญ่"},
            {"title": "วิศวกรระบบและผู้จัดการโครงการ (Project Director)", "desc": "ควบคุมโครงการขนาดใหญ่ให้เสร็จทันเวลาและอยู่ในงบประมาณ"},
            {"title": "นักลงทุน / Investment Banker", "desc": "ประเมินมูลค่าธุรกิจ วิเคราะห์ความเสี่ยง และตัดสินใจทางการเงินเชิงกลยุทธ์"}
        ]
    },
    "INTJ": {
        "cognitive_style": "ใช้ Introverted Intuition (Ni) สร้างแบบจำลองวิสัยทัศน์ในอนาคต แล้วใช้ Extraverted Thinking (Te) แปลงให้เป็นแผนงานจริงที่จับต้องได้",
        "why_fit": "คุณเป็นสถาปนิกทางความคิด สามารถมองเห็นภาพรวมในอีก 5-10 ปีข้างหน้า และสร้างระบบที่เป็นลำดับขั้นตอนเพื่อไปถึงจุดนั้นอย่างเป็นวิทยาศาสตร์และไร้อารมณ์ปะปน",
        "work_environment": "เหมาะกับงานวางแผนระยะยาว งานวิเคราะห์เชิงกลยุทธ์ที่ต้องการความอิสระสูง และเน้นมาตรฐานผลงานที่สมบูรณ์แบบ",
        "careers": [
            {"title": "Enterprise Architect / System Planner", "desc": "วางโครงสร้างระบบเทคโนโลยีสารสนเทศขององค์กรให้รองรับการเติบโตในอนาคต"},
            {"title": "นักวิเคราะห์นโยบายและกลยุทธ์ (Strategic Planner)", "desc": "คาดการณ์ทิศทางตลาดและวางแผนการดำเนินงานระยะยาว"},
            {"title": "นักวิจัยทางเทคโนโลยี / R&D Specialist", "desc": "คิดค้นพัฒนาเทคโนโลยีและผลิตภัณฑ์ต้นแบบเพื่อสร้างความได้เปรียบแข่งขัน"}
        ]
    },
    "ENFP": {
        "cognitive_style": "ใช้ Extraverted Intuition (Ne) มองหาโอกาสใหม่ๆ และแรงบันดาลใจ ผสานกับ Introverted Feeling (Fi) ที่ยึดมั่นในค่านิยมและความหมายของชีวิต",
        "why_fit": "คุณเปี่ยมด้วยพลังสร้างสรรค์ สื่อสารและสร้างแรงบันดาลใจให้คนอื่นได้ยอดเยี่ยม สัมผัสได้ถึงศักยภาพที่ซ่อนอยู่ในตัวผู้คนและโปรเจกต์ต่างๆ",
        "work_environment": "เหมาะกับงานที่ได้ปฏิสัมพันธ์กับคน มีบรรยากาศเปิดกว้าง อบอุ่น มีอิสระทางความคิด และได้สร้างอิมแพกต์เชิงบวกให้สังคม",
        "careers": [
            {"title": "Creative Director / Content Creator", "desc": "คิดค้นคอนเซปต์และสื่อสารเรื่องราวที่มีพลังผ่านสื่อหลากหลายรูปแบบ"},
            {"title": "นักพัฒนาศักยภาพมนุษย์ (People & Culture Specialist)", "desc": "สร้างบรรยากาศองค์กรและออกแบบโปรแกรมพัฒนาบุคลากร"},
            {"title": "นักทำการตลาดเชิงสังคม / UX Researcher", "desc": "ศึกษาพฤติกรรมและความต้องการที่แท้จริงของผู้ใช้เพื่อสร้างประสบการณ์ที่ดี"}
        ]
    },
    "INFP": {
        "cognitive_style": "ใช้ Introverted Feeling (Fi) ประเมินสิ่งต่างๆ จากค่านิยมและความถูกต้องภายใน ร่วมกับ Extraverted Intuition (Ne) ที่มองหาความเป็นไปได้ด้านศิลปะและความหมาย",
        "why_fit": "คุณมีความเข้าใจความรู้สึกมนุษย์อย่างลึกซึ้ง ยึดมั่นในอุดมการณ์ และมีพรสวรรค์ในการถ่ายทอดความรู้สึกหรือไอเดียผ่านงานศิลปะ ภาษา และการเยียวยาจิตใจ",
        "work_environment": "เหมาะกับงานที่สงบ ไม่มีการแข่งขันที่ก้าวร้าว ได้ทำงานที่ตรงกับความเชื่อส่วนตัว และมีอิสระในการถ่ายทอดความเป็นตัวเอง",
        "careers": [
            {"title": "นักเขียน / ผู้กำกับศิลป์ / นักสื่อสารมวลชน", "desc": "ถ่ายทอดเรื่องราวลึกซึ้ง สะท้อนสังคม และสร้างแรงบันดาลใจผ่านตัวหนังสือ"},
            {"title": "นักจิตวิทยาปรึกษา / นักบำบัด", "desc": "รับฟังและช่วยเหลือผู้คนให้ก้าวผ่านปัญหาทางจิตใจด้วยความเข้าใจลึกซึ้ง"},
            {"title": "นักออกแบบประสบการณ์ (UX Designer)", "desc": "ออกแบบระบบและอินเทอร์เฟซที่คำนึงถึงความรู้สึกและความสะดวกของผู้ใช้อย่างแท้จริง"}
        ]
    },
    "ENFJ": {
        "cognitive_style": "ใช้ Extraverted Feeling (Fe) รับรู้และดึงศักยภาพของผู้คน ร่วมกับ Introverted Intuition (Ni) ที่มองเห็นเส้นทางการเติบโตในอนาคต",
        "why_fit": "คุณเป็นผู้นำโดยธรรมชาติที่สร้างแรงบันดาลใจผ่านความเห็นอกเห็นใจ โน้มน้าวใจเก่ง และสามารถประสานความร่วมมือให้ทุกคนมุ่งสู่เป้าหมายเดียวกันได้อย่างกลมกลืน",
        "work_environment": "เหมาะกับองค์กรที่เน้นการพัฒนาคน การศึกษา การดูแลสังคม หรือการบริหารทีมที่ต้องสร้างความร่วมมือสูง",
        "careers": [
            {"title": "นักบริหารทรัพยากรบุคคล (HR Director)", "desc": "วางแผนและพัฒนาบุคลากร สร้างวัฒนธรรมองค์กรที่เข้มแข็งและมีความสุข"},
            {"title": "ผู้เชี่ยวชาญด้านการสื่อสารองค์กร / PR Manager", "desc": "สร้างภาพลักษณ์และบริหารความสัมพันธ์กับสาธารณชน"},
            {"title": "นักการศึกษา / โค้ชผู้บริหาร (Executive Coach)", "desc": "ถ่ายทอดความรู้และดึงศักยภาพสูงสุดของบุคคลและองค์กร"}
        ]
    },
    "INFJ": {
        "cognitive_style": "ใช้ Introverted Intuition (Ni) หยั่งรู้แรงจูงใจและความเป็นไปในอนาคต ผสานกับ Extraverted Feeling (Fe) ที่ใส่ใจสวัสดิภาพและความรู้สึกของผู้คน",
        "why_fit": "คุณมองเห็นมิติที่ซ่อนอยู่หลังพฤติกรรมมนุษย์ มีความตั้งใจจริงที่จะช่วยเหลือผู้อื่น และสามารถวางแผนเชิงกลยุทธ์เพื่อแก้ไขปัญหาสังคมระยะยาวได้อย่างมีทิศทาง",
        "work_environment": "เหมาะกับงานที่มีคุณค่าเชิงอุดมคติ เงียบสงบ เน้นการวิเคราะห์และช่วยเหลือผู้คนอย่างมีระบบ ไม่วุ่นวายฉาบฉวย",
        "careers": [
            {"title": "นักจิตวิทยาคลินิก / นักวิจัยพฤติกรรมมนุษย์", "desc": "วิเคราะห์และทำความเข้าใจโครงสร้างทางจิตวิทยาเพื่อการรักษาและพัฒนา"},
            {"title": "นักวางแผนพัฒนาสังคม / NGO Director", "desc": "วางกลยุทธ์แก้ไขปัญหาสังคม ยกระดับคุณภาพชีวิตผู้ด้อยโอกาส"},
            {"title": "Organizational Development Consultant", "desc": "ให้คำปรึกษาการปรับโครงสร้างองค์กรโดยคำนึงถึงมิติมนุษย์และระบบ"}
        ]
    },
    "ESTP": {
        "cognitive_style": "ใช้ Extraverted Sensing (Se) สังเกตสิ่งรอบตัวรวดเร็ว แม่นยำ ร่วมกับ Introverted Thinking (Ti) ที่ประเมินตรรกะและแก้ปัญหาหน้างานทันที",
        "why_fit": "คุณเป็นนักลุยแก้ปัญหาในสถานการณ์จริง ตัดสินใจได้เด็ดเดี่ยวใต้ความกดดัน สังเกตเห็นโอกาสตรงหน้าและลงมือทำทันทีโดยไม่ลังเล",
        "work_environment": "เหมาะกับงานที่ตื่นเต้น มีการเคลื่อนไหว ได้เจอผู้คนหรือเจรจา มีการแข่งขัน และเห็นผลลัพธ์ทันตา",
        "careers": [
            {"title": "นักบริหารวิกฤต (Crisis Manager) / ผู้จัดการฝ่ายปฏิบัติการ", "desc": "เข้าควบคุมสถานการณ์ฉุกเฉินและแก้ไขปัญหาหน้างานอย่างทันท่วงที"},
            {"title": "นักขายเชิงรุก / Business Development", "desc": "อ่านเกมผู้ซื้อ เจรจาต่อรอง และปิดดีลธุรกิจในสถานการณ์การแข่งขันสูง"},
            {"title": "วิศวกรสนาม (Field Engineer) / ผู้เชี่ยวชาญไอทีหน้างาน", "desc": "ติดตั้ง ตรวจสอบ และแก้ไขปัญหาระบบอุปกรณ์ในสถานที่จริง"}
        ]
    },
    "ISTP": {
        "cognitive_style": "ใช้ Introverted Thinking (Ti) วิเคราะห์กลไกตรรกะของระบบ ร่วมกับ Extraverted Sensing (Se) ที่ตอบสนองต่อเครื่องมือและข้อเท็จจริงตรงหน้า",
        "why_fit": "คุณมีทักษะทางวิศวกรรมและการแก้ปัญหาเฉพาะหน้าชั้นยอด ชอบถอดแกะเรียนรู้ว่าสิ่งต่างๆ ทำงานอย่างไร และใช้เครื่องมือวิเคราะห์แก้ไขจุดบกพร่องได้อย่างแม่นยำ",
        "work_environment": "เหมาะกับงานที่ได้ลงมือปฏิบัติจริง มีโจทย์ทางเทคนิคให้แก้ ไม่เน้นงานเอกสารหรือการประชุมที่ยาวนานไร้จุดหมาย",
        "careers": [
            {"title": "Cybersecurity Analyst / Penetration Tester", "desc": "ค้นหารอยรั่ว เจาะระบบทดสอบความปลอดภัย และแก้ไขบั๊กทางเทคนิค"},
            {"title": "วิศวกรซ่อมบำรุงและระบบกลไก (Mechanical Engineer)", "desc": "วิเคราะห์ วินิจฉัย และดูแลรักษาระบบเครื่องจักรและอุปกรณ์ซับซ้อน"},
            {"title": "DevOps Engineer / Data Infrastructure Analyst", "desc": "ดูแลและปรับปรุงประสิทธิภาพการทำงานของระบบเซิร์ฟเวอร์และไปป์ไลน์ข้อมูล"}
        ]
    },
    "ESTJ": {
        "cognitive_style": "ใช้ Extraverted Thinking (Te) จัดระเบียบการทำงานให้มีประสิทธิภาพสูงสุด ร่วมกับ Introverted Sensing (Si) ที่ยึดมั่นในมาตรฐานและข้อมูลที่ถูกต้อง",
        "why_fit": "คุณเป็นนักบริหารจัดการที่ยอดเยี่ยม สร้างกฎเกณฑ์ กำหนดมาตรฐาน และควบคุมให้ทุกคนทำตามแผนงานได้อย่างเป็นระเบียบ เรียบร้อย และตรงเวลา",
        "work_environment": "เหมาะกับองค์กรที่มีโครงสร้างชัดเจน เช่น หน่วยงานรัฐ ราชการ โรงงานอุตสาหกรรม หรือบริษัทชั้นนำที่เน้นระบบมาตรฐาน",
        "careers": [
            {"title": "ผู้จัดการฝ่ายปฏิบัติการ (Operations Manager)", "desc": "ควบคุมกระบวนการผลิตและการทำงานขององค์กรให้เป็นไปตามมาตรฐาน"},
            {"title": "ผู้ตรวจสอบบัญชีและระบบ (Auditor)", "desc": "ตรวจสอบความถูกต้องของกฎระเบียบ การเงิน และกระบวนการทำงาน"},
            {"title": "ผู้บริหารงานราชการ / รัฐวิสาหกิจ", "desc": "บังคับใช้ นโยบาย ควบคุมกำกับดูแลให้ระบบงานของรัฐดำเนินไปอย่างมั่นคง"}
        ]
    },
    "ISTJ": {
        "cognitive_style": "ใช้ Introverted Sensing (Si) เก็บรวบรวมข้อมูลและรายละเอียดอย่างแม่นยำ ผสานกับ Extraverted Thinking (Te) ในการประมวลผลตามกฎระเบียบ",
        "why_fit": "คุณเป็นเสาหลักแห่งความน่าเชื่อถือ ทำงานด้วยความละเอียดรอบคอบสูงมาก รักษาสัญญา เคารพกฎเกณฑ์ และไม่ยอมปล่อยให้มีข้อผิดพลาดในงาน",
        "work_environment": "เหมาะกับงานที่ต้องการความถูกต้อง 100% มีระเบียบปฏิบัติชัดเจน มั่นคง และมีขั้นตอนประเมินผลที่เป็นสัดส่วน",
        "careers": [
            {"title": "นักวิเคราะห์การเงินและระบบบัญชี (Financial Analyst)", "desc": "ตรวจสอบตัวเลข งบการเงิน และวิเคราะห์ความเสี่ยงอย่างละเอียดรอบคอบ"},
            {"title": "ผู้เชี่ยวชาญด้านกฎหมาย / Compliance Officer", "desc": "ดูแลการปฏิบัติตามกฎหมายและข้อบังคับทางธุรกิจเพื่อป้องกันความผิดพลาด"},
            {"title": "Database Administrator / Quality Assurance (QA)", "desc": "ดูแลความถูกต้องและทดสอบระบบซอฟต์แวร์ให้ตรงตามสเปกอย่างเคร่งครัด"}
        ]
    },
    "ESFP": {
        "cognitive_style": "ใช้ Extraverted Sensing (Se) ดื่มด่ำและตอบสนองกับสิ่งแวดล้อมปัจจุบัน ร่วมกับ Introverted Feeling (Fi) ที่ถ่ายทอดความรู้สึกอย่างเป็นธรรมชาติ",
        "why_fit": "คุณมีเสน่ห์ เข้าถึงง่าย เข้าใจความต้องการของคนตรงหน้าได้ทันที สื่อสารสนุกสนาน และสร้างพลังบวกให้ทุกพื้นที่ที่คุณอยู่",
        "work_environment": "เหมาะกับงานที่ได้เจอผู้คน ไม่นั่งโต๊ะจำเจ มีสีสัน บันเทิง หรือได้เดินทางและจัดกิจกรรมตื่นเต้น",
        "careers": [
            {"title": "Event Organizer / Public Relations Specialist", "desc": "เนรมิตงานอีเวนต์และบริหารประสบการณ์ตรงของผู้เข้าร่วมงาน"},
            {"title": "พิธีกร / นักแสดง / นักสร้างความบันเทิงดิจิทัล", "desc": "ใช้เสน่ห์และการตอบสนองต่อผู้ชมในการสร้างความสนุกสนาน"},
            {"title": "ผู้เชี่ยวชาญการบริการลูกค้า VIP (Customer Experience Manager)", "desc": "ดูแลและสร้างความประทับใจเฉพาะบุคคลให้กับลูกค้าสำคัญ"}
        ]
    },
    "ISFP": {
        "cognitive_style": "ใช้ Introverted Feeling (Fi) เข้าถึงอารมณ์สุนทรีย์ลึกซึ้ง ร่วมกับ Extraverted Sensing (Se) ที่สังเกตและถ่ายทอดผ่านประสาทสัมผัสและชิ้นงาน",
        "why_fit": "คุณมีความโดดเด่นด้านศิลปะ รสชาติ และสุนทรียภาพ สามารถถ่ายทอดอารมณ์ความรู้สึกออกมาเป็นผลงานรูปธรรมที่สวยงามและมีเอกลักษณ์เฉพาะตัว",
        "work_environment": "เหมาะกับสตูดิโอ งานสร้างสรรค์ หัตถศิลป์ บรรยากาศที่เป็นอิสระ ไม่มีความกดดันทางการเมืองในองค์กร",
        "careers": [
            {"title": "Graphic Designer / Visual Artist", "desc": "สร้างสรรค์งานทัศนศิลป์ กราฟิก และองค์ประกอบความสวยงามของแบรนด์"},
            {"title": "นักออกแบบผลิตภัณฑ์ / Fashion Designer", "desc": "ออกแบบสิ่งของเครื่องใช้และเสื้อผ้าที่ผสมผสานประโยชน์ใช้สอยและความงาม"},
            {"title": "เชฟนักปรุงอาหาร (Culinary Artist) / ช่างภาพ", "desc": "รังสรรค์ประสบการณ์ทางประสาทสัมผัสผ่านอาหารและภาพถ่าย"}
        ]
    },
    "ESFJ": {
        "cognitive_style": "ใช้ Extraverted Feeling (Fe) สัมผัสและดูแลความต้องการของกลุ่ม ผสานกับ Introverted Sensing (Si) ที่ใส่ใจในรายละเอียดและขนบปฏิบัติ",
        "why_fit": "คุณเป็นผู้ดูแลและสนับสนุนที่ยอดเยี่ยม คอยอำนวยความสะดวก สร้างบรรยากาศที่อบอุ่น และทำให้ทุกคนรู้สึกได้รับการยอมรับและเป็นส่วนหนึ่งของกลุ่ม",
        "work_environment": "เหมาะกับงานบริการ สุขภาพ การประสานงานชุมชน หรือองค์กรที่เน้นช่วยเหลือดูแลผู้คนอย่างเป็นระบบ",
        "careers": [
            {"title": "ผู้ดูแลสุขภาพ / พยาบาลวิชาการ / นักกายภาพบำบัด", "desc": "ดูแลเอาใจใส่ผู้ป่วยด้วยความนุ่มนวลและปฏิบัติตามมาตรฐานการรักษา"},
            {"title": "ผู้ประสานงานโครงการ / ฝ่ายบริหารงานลูกค้า (Account Executive)", "desc": "ดูแลความสัมพันธ์และประสานความต้องการระหว่างลูกค้าและทีมงาน"},
            {"title": "นักสังคมสงเคราะห์ / ผู้บริหารงานบริการชุมชน", "desc": "จัดกิจกรรมช่วยเหลือและสร้างสวัสดิภาพให้กับคนในสังคม"}
        ]
    },
    "ISFJ": {
        "cognitive_style": "ใช้ Introverted Sensing (Si) จดจำรายละเอียดและความต้องการเฉพาะบุคคล ร่วมกับ Extraverted Feeling (Fe) ที่คอยช่วยเหลือผู้อื่นเงียบๆ",
        "why_fit": "คุณเป็นผู้ปิดทองหลังพระที่มีความรอบคอบและใส่ใจรายละเอียดสูงมาก ทำงานด้วยความอดทน ละเอียดอ่อน และคอยปกป้องดูแลให้ระบบและผู้คนปลอดภัย",
        "work_environment": "เหมาะกับงานที่ได้ช่วยเหลือผู้อื่น มีความมั่นคง สภาพแวดล้อมสงบ เป็นระเบียบเรียบร้อย และไม่ต้องแข่งขันเอาหน้า",
        "careers": [
            {"title": "บุคลากรทางการแพทย์ / เภสัชกร / พยาบาล", "desc": "จ่ายยาและดูแลสุขภาพของผู้ป่วยด้วยความถูกต้อง แม่นยำ และรอบคอบสูงสุด"},
            {"title": "เจ้าหน้าที่บริหารงานเอกสาร / ผู้ช่วยผู้บริหาร", "desc": "จัดเก็บข้อมูล ดูแลตารางงาน และสนับสนุนการทำงานเบื้องหลังให้เป็นระบบ"},
            {"title": "บรรณารักษ์ / นักจัดเก็บและอนุรักษ์ข้อมูล", "desc": "ดูแลจัดหมวดหมู่ข้อมูลและทรัพยากรให้เป็นระเบียบเพื่อการสืบค้นที่สะดวก"}
        ]
    }
}

# ตัวแปรจัดการขั้นตอนหลัก
TOTAL_STEPS = 5
if "step" not in st.session_state:
    st.session_state.step = 1

# ตัวแปรสำหรับแบ่งคำถามใน Step 1 (Pagination)
QUESTIONS_PER_PAGE = 10
TOTAL_COG_QUESTIONS = len(COGNITIVE_QUESTIONS)
TOTAL_COG_PAGES = (TOTAL_COG_QUESTIONS + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE

if "cog_page" not in st.session_state:
    st.session_state.cog_page = 0

if "user_cog_responses" not in st.session_state:
    st.session_state.user_cog_responses = {}

progress_val = min((st.session_state.step - 1) / (TOTAL_STEPS - 1), 1.0)
st.progress(progress_val)


# ==========================================
# STEP 1: แบบประเมิน Cognitive Functions
# ==========================================
if st.session_state.step == 1:
    current_page = st.session_state.cog_page
    start_idx = current_page * QUESTIONS_PER_PAGE
    end_idx = min(start_idx + QUESTIONS_PER_PAGE, TOTAL_COG_QUESTIONS)
    current_questions = COGNITIVE_QUESTIONS[start_idx:end_idx]

    st.subheader("🧠 ส่วนที่ 1: แบบประเมิน Cognitive Functions")
    
    col_p1, col_p2 = st.columns([3, 1])
    with col_p1:
        st.caption(f"📌 **หน้า {current_page + 1} จาก {TOTAL_COG_PAGES}** (คำถามข้อที่ {start_idx + 1} - {end_idx} จากทั้งหมด {TOTAL_COG_QUESTIONS} ข้อ)")
    with col_p2:
        sub_progress = (current_page + 1) / TOTAL_COG_PAGES
        st.progress(sub_progress)

    st.info("💡 **ระดับการให้คะแนน:** 1 = ไม่ตรงเลย | 2 = ไม่ค่อยตรง | 3 = ปานกลาง | 4 = ค่อนข้างตรง | 5 = ตรงมากที่สุด")

    with st.form(key=f"form_step1_page_{current_page}"):
        page_responses = {}
        
        for idx, q in enumerate(current_questions, start=start_idx + 1):
            st.markdown(f"""
            <div class="question-card">
                <div class="question-badge">คำถามข้อที่ {idx} / {TOTAL_COG_QUESTIONS}</div>
                <div class="question-text">{q['text']}</div>
            </div>
            """, unsafe_allow_html=True)

            saved_score = st.session_state.user_cog_responses.get(q["id"], {}).get("score", 3)

            selected_score = st.radio(
                label=f"เลือกคะแนนสำหรับข้อ {idx}",
                options=[1, 2, 3, 4, 5],
                index=saved_score - 1,
                horizontal=True,
                key=f"q_{q['id']}",
                label_visibility="collapsed"
            )

            page_responses[q["id"]] = {
                "func": q["func"],
                "score": selected_score
            }
            st.markdown("<br>", unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if current_page > 0:
                submit_prev = st.form_submit_button("⬅ หน้าก่อนหน้า", use_container_width=True)
            else:
                submit_prev = False

        with col_btn2:
            if current_page < TOTAL_COG_PAGES - 1:
                submit_next = st.form_submit_button("หน้าถัดไป ➔", use_container_width=True)
            else:
                submit_next = st.form_submit_button("ถัดไป: เลือกวิชาความถนัด ➔", use_container_width=True)

        if submit_prev:
            st.session_state.user_cog_responses.update(page_responses)
            st.session_state.cog_page -= 1
            st.rerun()

        if submit_next:
            st.session_state.user_cog_responses.update(page_responses)
            if current_page < TOTAL_COG_PAGES - 1:
                st.session_state.cog_page += 1
                st.rerun()
            else:
                st.session_state.step = 2
                st.rerun()

# ==========================================
# STEP 2: วิชาที่ชอบ
# ==========================================
elif st.session_state.step == 2:
    st.subheader("📚 ส่วนที่ 2: ความสนใจและความถนัดรายวิชา")
    st.caption("โปรดเลือกการประเมินตามความเป็นจริง เพื่อความแม่นยำในการวิเคราะห์")

    with st.form("form_step2"):
        user_sub_responses = {}
        for idx, q in enumerate(SUBJECT_QUESTIONS, 1):
            st.markdown(f"""
            <div class="sub-question-card">
                <span class="category-badge">🏷️ {q['category']}</span>
                <div style="font-weight: 600; color: #1E293B; font-size: 1.05rem;">ข้อ {idx}. {q['text']}</div>
            </div>
            """, unsafe_allow_html=True)

            col_ans, _ = st.columns([1, 2])
            with col_ans:
                ans = st.radio(
                    f"ตอบข้อ {idx}:", 
                    ["ใช่", "ไม่ใช่"], 
                    index=1, 
                    horizontal=True, 
                    key=q["id"],
                    label_visibility="collapsed"
                )

            user_sub_responses[q["id"]] = {
                "category": q["category"],
                "ans": ans
            }
            st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("⬅ ย้อนกลับ"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.form_submit_button("ถัดไป: งานอดิเรก ➔", use_container_width=True):
                st.session_state.user_sub_responses = user_sub_responses
                st.session_state.step = 3
                st.rerun()

# ==========================================
# STEP 3: งานอดิเรก
# ==========================================
elif st.session_state.step == 3:
    st.subheader("🎨 ส่วนที่ 3: งานอดิเรกและสไตล์กิจกรรมในเวลาว่าง")
    st.caption("เลือกกิจกรรมที่คุณทำแล้วรู้สึกสนุก มีพลัง หรือทำเป็นประจำ")

    with st.form("form_step3"):
        user_hob_responses = {}
        for idx, q in enumerate(HOBBY_QUESTIONS, 1):
            st.markdown(f"""
            <div class="sub-question-card" style="border-left-color: #8B5CF6;">
                <span class="category-badge">🎯 {q['category']}</span>
                <div style="font-weight: 600; color: #1E293B; font-size: 1.05rem;">ข้อ {idx}. {q['text']}</div>
            </div>
            """, unsafe_allow_html=True)

            col_ans, _ = st.columns([1, 2])
            with col_ans:
                ans = st.radio(
                    f"ตอบข้อ {idx}:", 
                    ["ใช่", "ไม่ใช่"], 
                    index=1, 
                    horizontal=True, 
                    key=q["id"],
                    label_visibility="collapsed"
                )

            user_hob_responses[q["id"]] = {
                "category": q["category"],
                "ans": ans
            }
            st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("⬅ ย้อนกลับ"):
                st.session_state.step = 2
                st.rerun()
        with col2:
            if st.form_submit_button("ถัดไป: การเงิน/ทุนทรัพย์ ➔", use_container_width=True):
                st.session_state.user_hob_responses = user_hob_responses
                st.session_state.step = 4
                st.rerun()

# ==========================================
# STEP 4: การเงิน/เป้าหมายอาชีพ
# ==========================================
elif st.session_state.step == 4:
    st.subheader("💼 ส่วนที่ 4: เป้าหมายอาชีพ และ ปัจจัยทุนการศึกษา")
    st.caption("โปรดระบุเงื่อนไขตามความเป็นจริง เพื่อให้ระบบวิเคราะห์เส้นทางศึกษาต่อและทุนที่เหมาะสมที่สุด")

    with st.form("form_step4"):
        user_goal_responses = {}
        
        # 1. คำถามเป้าหมายอาชีพ
        st.markdown("#### 🎯 1. สไตล์เป้าหมายการทำงานในอนาคต")
        for idx, q in enumerate(GOAL_QUESTIONS, 1):
            st.markdown(f"""
            <div class="sub-question-card" style="border-left-color: #10B981;">
                <span class="category-badge">🚀 {q['category']}</span>
                <div style="font-weight: 600; color: #1E293B; font-size: 1.05rem;">ข้อ {idx}. {q['text']}</div>
            </div>
            """, unsafe_allow_html=True)

            col_ans, _ = st.columns([1, 2])
            with col_ans:
                ans = st.radio(
                    f"ตอบข้อ {idx}:", 
                    ["ใช่", "ไม่ใช่"], 
                    index=1, 
                    horizontal=True, 
                    key=q["id"],
                    label_visibility="collapsed"
                )
            user_goal_responses[q["id"]] = {"category": q["category"], "ans": ans}
            st.markdown("<br>", unsafe_allow_html=True)

        st.divider()

        # 2. คำถามเจาะลึกการเงินและทุนทรัพย์ 5 ข้อ
        st.markdown("#### 💰 2. เงื่อนไขด้านทุนทรัพย์และภาระทางการเงิน (5 ข้อ)")
        
        user_fin_responses = {}
        for f_q in FINANCIAL_QUESTIONS:
            st.markdown(f"""
            <div class="sub-question-card" style="border-left-color: #F59E0B;">
                <span class="category-badge">💳 {f_q['category']}</span>
                <div style="font-weight: 600; color: #1E293B; font-size: 1.05rem;">{f_q['label']}</div>
            </div>
            """, unsafe_allow_html=True)

            selected_opt = st.radio(
                f_q['label'],
                options=f_q['options'],
                index=0,
                key=f_q['id'],
                label_visibility="collapsed"
            )
            user_fin_responses[f_q['id']] = selected_opt
            st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("⬅ ย้อนกลับ"):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.form_submit_button("🚀 ประมวลผลและดูผลลัพธ์", use_container_width=True):
                st.session_state.user_goal_responses = user_goal_responses
                st.session_state.user_fin_responses = user_fin_responses
                st.session_state.capital = user_fin_responses.get("fin_budget", "")
                st.session_state.step = 5
                st.rerun()

# ==========================================
# STEP 5: หน้าสรุปผลลัพธ์
# ==========================================
elif st.session_state.step == 5:
    st.balloons()

    cog_resp = st.session_state.get("user_cog_responses", {})
    sub_resp = st.session_state.get("user_sub_responses", {})
    goal_resp = st.session_state.get("user_goal_responses", {})
    fin_resp = st.session_state.get("user_fin_responses", {})
    capital = st.session_state.get("capital", "")

    # ดึงค่าตอบคำถามการเงินเพื่อใช้ประมวลผล
    budget_choice = str(fin_resp.get("fin_budget", capital))
    scholarship_need = str(fin_resp.get("fin_scholarship", ""))
    debt_burden = str(fin_resp.get("fin_debt", ""))
    job_goal = " ".join([str(v) for v in goal_resp.values()]) + " " + " ".join([str(v) for v in fin_resp.values()])

    # 1. คำนวณคะแนน Cognitive Functions
    func_scores = {"Ne": 0, "Ni": 0, "Se": 0, "Si": 0, "Te": 0, "Ti": 0, "Fe": 0, "Fi": 0}
    for q_id, val in cog_resp.items():
        if isinstance(val, dict) and "func" in val and "score" in val:
            func_scores[val["func"]] += val["score"]

    # 2. ค้นหา Type MBTI
    sorted_funcs = sorted(func_scores.items(), key=lambda x: x[1], reverse=True)
    top_func = sorted_funcs[0][0]
    second_func = sorted_funcs[1][0]

    predicted_type = "ENTP"
    for mbti_name, stack in MBTI_STACKS.items():
        if stack["Dom"] == top_func and stack["Aux"] == second_func:
            predicted_type = mbti_name
            break
        elif stack["Dom"] == top_func:
            predicted_type = mbti_name

    stack_info = MBTI_STACKS.get(predicted_type, MBTI_STACKS["ENTP"])

    # 3. ตรวจสอบเงื่อนไขจากคำถามย่อยหมวดวิชา
    a_math = any(sub_resp.get(f"sub_math_{i}", {}).get("ans") == "ใช่" for i in range(1, 4))
    a_sci = any(sub_resp.get(f"sub_sci_{i}", {}).get("ans") == "ใช่" for i in range(1, 4))
    a_art = any(sub_resp.get(f"sub_art_{i}", {}).get("ans") == "ใช่" for i in range(1, 4))
    c_low = "จำกัดสูง" in capital if capital else False

    rule_tech = (func_scores["Ti"] >= 12 or func_scores["Te"] >= 12) and a_math
    rule_health = (func_scores["Fe"] >= 12 or func_scores["Si"] >= 12) and a_sci
    rule_creative = (func_scores["Ne"] >= 12 or a_art)

    # Header MBTI Hero Card
    st.markdown(f"""
    <div class="mbti-hero-card">
        <div style="font-size: 1.2rem; opacity: 0.9;">ผลการประมวลผลบุคลิกภาพของคุณคือ</div>
        <div class="mbti-type-text">{predicted_type}</div>
        <div style="font-size: 1.3rem; font-weight: 500;">"{stack_info['Title']}"</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "✨ สรุป MBTI & Cognitive Functions", 
        "🎓 คณะ/อาชีพ & แนะนำมหาวิทยาลัยตามงบ", 
        "📐 การพิสูจน์ตรรกศาสตร์"
    ])

    with tab1:
        st.subheader("🧩 ลำดับกระบวนการทางความคิด (Cognitive Function Hierarchy)")
        st.caption("สมองของคุณประมวลผลข้อมูลและตัดสินใจผ่านฟังก์ชันหลัก 4 ลำดับนี้:")

        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        funcs_to_show = [
            ("Dominant (ฟังก์ชันหลัก)", stack_info["Dom"]),
            ("Auxiliary (ฟังก์ชันรอง)", stack_info["Aux"]),
            ("Tertiary (ฟังก์ชันสำรอง)", stack_info["Tert"]),
            ("Inferior (จุดอ่อน)", stack_info["Inf"])
        ]
        
        cols = [col_f1, col_f2, col_f3, col_f4]
        for idx, (label, f_code) in enumerate(funcs_to_show):
            with cols[idx]:
                st.markdown(f"""
                <div class="func-card">
                    <div class="func-badge">{label}</div>
                    <div class="func-title">{f_code}</div>
                    <div class="func-desc">{FUNC_DESCRIPTIONS.get(f_code, '')}</div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        st.subheader("📊 กราฟเปรียบเทียบคะแนน Cognitive Functions ทั้ง 8 ด้าน")
        df_scores = pd.DataFrame(list(func_scores.items()), columns=['Function', 'Score'])
        df_scores = df_scores.sort_values(by='Score', ascending=True)

        fig = px.bar(
            df_scores, 
            x='Score', 
            y='Function', 
            orientation='h',
            text='Score',
            color='Score',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            height=400,
            xaxis_title="คะแนนที่ได้",
            yaxis_title="ฟังก์ชัน",
            coloraxis_showscale=False
        )
        fig.update_traces(textposition='inside', textfont_size=14)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("🎓 วิเคราะห์เส้นทางอาชีพและสถาบันการศึกษาตามโปรไฟล์ของคุณ")

        # ดึงข้อมูล MBTI ที่ประมวลผลได้
        mbti_career_info = MBTI_CAREER_ANALYSIS.get(predicted_type, MBTI_CAREER_ANALYSIS["ENTP"])

        # --------------------------------------------------------
        # 1. กล่องวิเคราะห์เจาะลึกทำไม MBTI ของผู้ใช้จึงเหมาะกับสายงานนี้
        # --------------------------------------------------------
        st.markdown(f"""
        <div style="background-color: #EFF6FF; border-left: 6px solid #2563EB; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.8rem;">
            <h3 style="color: #1E3A8A; margin-top:0;">🧠 ทำไมบุคลิกภาพ {predicted_type} ({stack_info['Title']}) ถึงเหมาะกับสายงานนี้?</h3>
            <p style="color: #1E293B; font-size: 1.05rem;"><b>⚙️ กระบวนการคิดทางสมอง (Cognitive Mechanism):</b><br>{mbti_career_info['cognitive_style']}</p>
            <p style="color: #1E293B; font-size: 1.05rem;"><b>💡 จุดเด่นทางบุคลิกภาพที่สอดคล้อง (Why You Fit):</b><br>{mbti_career_info['why_fit']}</p>
            <p style="color: #1E293B; font-size: 1.05rem; margin-bottom:0;"><b>🏢 สภาพแวดล้อมการทำงานที่ดึงศักยภาพสูงสุด (Ideal Work Environment):</b><br>{mbti_career_info['work_environment']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💼 อาชีพเด่นที่ตอบโจทย์รูปแบบการคิดของคุณ")
        col_c1, col_c2, col_c3 = st.columns(3)
        career_cols = [col_c1, col_c2, col_c3]
        for idx, car in enumerate(mbti_career_info['careers']):
            with career_cols[idx % 3]:
                st.markdown(f"""
                <div class="career-card">
                    <div style="color: #2563EB; font-weight: 700; font-size: 0.85rem; text-transform: uppercase;">RECOMMENDED CAREER {idx+1}</div>
                    <div class="career-title">{car['title']}</div>
                    <div style="color: #475569; font-size: 0.95rem; line-height: 1.5;">{car['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        st.markdown("### 🏫 มหาวิทยาลัยและเส้นทางศึกษาต่อที่ 'ตรงกับทุนของคุณ'")

        if "จำกัดสูง" in budget_choice or "สนใจมาก" in scholarship_need:
            st.info("💡 **ระบบคัดกรองเฉพาะ:** สถาบันที่มีทุนเรียนฟรี ทุนผูกพันมีงานรองรับ หรือค่าเทอมประหยัดตอบโจทย์งบประมาณของคุณ")

            col_uni1, col_uni2 = st.columns(2)
            with col_uni1:
                st.markdown("""
                <div style="background-color: #FFFFFF; border: 2px solid #3B82F6; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                    <h4 style="color: #1E3A8A; margin-top:0;">🎓 สถาบันทุนผูกพัน (จบแล้วมีงานทำทันที)</h4>
                    <ul>
                        <li><b>วิทยาลัยพยาบาลบรมราชชนนี / สถาบันพระบรมราชชนก:</b> มีทุนเรียนฟรี มีเบี้ยเลี้ยง จบแล้วบรรจุเป็นพยาบาลรัฐทันที</li>
                        <li><b>วิทยาลัยพยาบาลเหล่าทัพ / ตำรวจ:</b> ทุนการศึกษาพร้อมสวัสดิการ บรรจุรับราชการทันทีหลังจบ</li>
                        <li><b>โครงการทุนครูคืนถิ่น (คณะศึกษาศาสตร์/ครุศาสตร์):</b> เรียนฟรีพร้อมการันตีตำแหน่งบรรจุครูในภูมิลำเนา</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with col_uni2:
                st.markdown("""
                <div style="background-color: #FFFFFF; border: 2px solid #10B981; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                    <h4 style="color: #065F46; margin-top:0;">🏛️ มหาวิทยาลัยค่าเทอมประหยัด & ยืดหยุ่น</h4>
                    <ul>
                        <li><b>มหาวิทยาลัยรามคำแหง / มสธ.:</b> ค่าเทอมเริ่มต้นหลักพัน สามารถเรียนไปทำงานไปได้ ตอบโจทย์การคืนทุนไว</li>
                        <li><b>มหาวิทยาลัยเทคโนโลยีราชมงคล (RMUT) ทั่วประเทศ:</b> ค่าเทอมประหยัด เน้นทักษะปฏิบัติจริง กู้ กยศ. ได้ 100%</li>
                        <li><b>มหาวิทยาลัยราชภัฏในภูมิลำเนา:</b> ช่วยประหยัดค่าหอพักและค่าครองชีพได้อย่างมาก</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        elif "ปานกลาง" in budget_choice:
            st.info("💡 **ระบบคัดกรองเฉพาะ:** มหาวิทยาลัยรัฐบาลชั้นนำที่ค่าเทอมอยู่ในระดับปานกลาง (15,000 - 40,000 บาท/เทอม)")

            st.markdown("""
            <div style="background-color: #FFFFFF; border: 2px solid #3B82F6; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                <h4 style="color: #1E3A8A; margin-top:0;">🏛️ มหาวิทยาลัยรัฐบาลหลักที่แนะนำ</h4>
                <ul>
                    <li><b>สายเทค/วิศวะ:</b> กลุ่ม 3 พระจอมเกล้า (สจล., มจธ., มจพ.), มหาวิทยาลัยเกษตรศาสตร์, มหาวิทยาลัยเชียงใหม่</li>
                    <li><b>สายการแพทย์/สุขภาพ:</b> มหาวิทยาลัยมหิดล, จุฬาลงกรณ์มหาวิทยาลัย, มหาวิทยาลัยขอนแก่น, มหาวิทยาลัยสงขลานครินทร์</li>
                    <li><b>สายบริหาร/สังคม/ศิลปะ:</b> มหาวิทยาลัยธรรมศาสตร์, มหาวิทยาลัยศิลปากร, มหาวิทยาลัยศรีนครินทรวิโรฒ (มศว)</li>
                </ul>
                <p style="font-size: 0.85rem; color: #64748B; margin-bottom:0;">* ทุกสถาบันมีทุนจ้างงานในมหาลัย และทุนกู้ยืม กยศ./กอศ. รองรับ</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.info("💡 **ระบบคัดกรองเฉพาะ:** หลักสูตรนานาชาติ มหาวิทยาลัยเอกชนอุปกรณ์ทันสมัย หรือสถาบันที่มีคอนเนกชันธุรกิจสูง")

            st.markdown("""
            <div style="background-color: #FFFFFF; border: 2px solid #8B5CF6; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
                <h4 style="color: #5B21B6; margin-top:0;">🌟 สถาบันเอกชนชั้นนำ & หลักสูตรนานาชาติ</h4>
                <ul>
                    <li><b>มหาวิทยาลัยกรุงเทพ / มหาวิทยาลัยรังสิต / มหาวิทยาลัยศรีปทุม:</b> โดดเด่นด้านอุปกรณ์ระดับมืออาชีพ คอนเนกชันสายงานตรง</li>
                    <li><b>มหาวิทยาลัยอัสสัมชัญ (ABAC):</b> เด่นหลักสูตรนานาชาติและการสร้างเครือข่ายธุรกิจระดับสากล</li>
                    <li><b>หลักสูตรนานาชาติมหาลัยรัฐ (เช่น SIIT มธ. / ICT มหิดล / ISE จุฬาฯ):</b> เรียนเป็นภาษาอังกฤษพร้อมโอกาสฝึกงานต่างประเทศ</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        if "ส่งเสียครอบครัว" in debt_burden or "คืนทุนไว" in job_goal:
            st.warning("⚠️ **คำแนะนำพิเศษสำหรับเป้าหมายรายได้เร็ว/ภาระครอบครัว:** แนะนำให้เลือกเรียนสายที่มีการฝึกงานตรงกับบริษัทตั้งแต่ปี 3-4 หรือเลือกสายงานเทค/ดิจิทัล ซึ่งสามารถรับงาน Freelance สร้างรายได้ระหว่างเรียนได้ทันที")

    with tab3:
        st.subheader("📐 โครงสร้างการพิสูจน์ทางตรรกศาสตร์ (Logic Proof)")
        st.caption("อธิบายกระบวนการคำนวณเบื้องหลังด้วยทฤษฎีประพจน์ทางคณิตศาสตร์")

        st.markdown(f"""
        <div class="logic-box">
        <b>1. สรุปคะแนน Cognitive Functions (รวมจากแบบสอบถาม 80 ข้อ):</b><br>
        • Ne = {func_scores['Ne']} | Ni = {func_scores['Ni']}<br>
        • Se = {func_scores['Se']} | Si = {func_scores['Si']}<br>
        • Te = {func_scores['Te']} | Ti = {func_scores['Ti']}<br>
        • Fe = {func_scores['Fe']} | Fi = {func_scores['Fi']}<br><br>
        
        <b>2. กำหนดตัวแปรประพจน์ (Propositions):</b><br>
        • p_Dom = {top_func} (ฟังก์ชันหลักที่ได้คะแนนสูงสุด)<br>
        • a_math (ชอบสายคำนวณ) = {a_math}<br>
        • a_sci (ชอบสายวิทย์) = {a_sci}<br>
        • c_low (เงื่อนไขข้อจำกัดทุนสูง) = {c_low}<br><br>
        
        <b>3. การสรุปผลตามกฎเงื่อนไข (Rule Inference):</b><br>
        • Rule_Tech = (Ti ∨ Te) ∧ a_math ∧ c_low → <b>{rule_tech}</b><br>
        • Rule_Health = (Fe ∨ Si) ∧ a_sci ∧ c_low → <b>{rule_health}</b><br>
        • Rule_Creative = (Ne ∨ a_art) → <b>{rule_creative}</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 ทำแบบประเมินใหม่อีกครั้ง", use_container_width=True):
        st.session_state.step = 1
        st.session_state.cog_page = 0
        st.session_state.user_cog_responses = {}
        st.rerun()
