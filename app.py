import streamlit as st
import pandas as pd
import traceback
from streamlit_ace import st_ace  # 🔥 นำเข้ากล่องเขียนโค้ดแบบมีเลขบรรทัด

st.set_page_config(page_title="Python Sandbox with Line Numbers", layout="wide")

st.title("🖥️ ห้องปฏิบัติการฝึกเขียน Python (มีเลขบรรทัด)")
st.write("คำชี้แจง: อัปโหลดไฟล์ CSV 1 หรือ 2 ไฟล์ ระบบจะสร้างตัวแปร `df1` และ `df2` ให้นักเรียนนำไปเขียนโค้ดต่อ")

df1 = None
df2 = None

# 1. ส่วนอัปโหลดไฟล์
uploaded_files = st.file_uploader("เลือกไฟล์ CSV ของคุณ (สูงสุด 2 ไฟล์)", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    for index, file in enumerate(uploaded_files[:2]):
        try:
            if index == 0:
                df1 = pd.read_csv(file)
                st.success(f"ไฟล์ที่ 1 ({file.name}) โหลดเข้าตัวแปร `df1` เรียบร้อยแล้ว")
                st.dataframe(df1.head(3))
            elif index == 1:
                df2 = pd.read_csv(file)
                st.success(f"ไฟล์ที่ 2 ({file.name}) โหลดเข้าตัวแปร `df2` เรียบร้อยแล้ว")
                st.dataframe(df2.head(3))
        except Exception as e:
            st.error(f"ไม่สามารถอ่านไฟล์ {file.name} ได้: {e}")

st.write("---")

# 2. พื้นที่เขียนโค้ด Python (เปลี่ยนเป็นแบบมีเลขบรรทัด)
st.subheader("📝 พื้นที่เขียนโค้ด Python")

default_code = """# ตัวอย่างการใช้งานตัวแปร df1 และ df2
if df1 is not None:
    print("โครงสร้างของ df1 คือ:", df1.shape)
    
if df2 is not None:
    print("โครงสร้างของ df2 คือ:", df2.shape)
"""

# 🔥 เรียกใช้งาน st_ace แทน st.text_area เพื่อเปิดใช้งานเลขบรรทัดและธีมสีโค้ด
user_code = st_ace(
    value=default_code,
    language="python",        # เปิดไฮไลต์สีตามหลักภาษา Python
    theme="monokai",          # สีธีมมืดแบบที่โปรแกรมเมอร์นิยม (เปลี่ยนเป็น "github" ถ้าชอบสีสว่าง)
    font_size=16,             # ขนาดตัวอักษรให้อ่านง่าย
    tab_size=4,               # เคาะ Tab เว้นวรรคทีละ 4 ช่องตามมาตรฐาน Python
    wrap=True,                # ตัดคำอัตโนมัติเมื่อขึ้นบรรทัดใหม่
    auto_validate=False,      # ไม่รันโค้ดอัตโนมัติจนกว่าจะกดปุ่ม
    height=300,
    key="python_editor"
)

# 3. ส่วนประมวลผลและแสดงผลลัพธ์
if st.button("▶️ รันโค้ด (Run Code)"):
    st.subheader("📊 ผลลัพธ์ (Output)")
    
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
    try:
        local_scope = {"df1": df1, "df2": df2, "pd": pd}
        exec(user_code, globals(), local_scope)
        sys.stdout = old_stdout
        
        output = redirected_output.getvalue()
        if output:
            st.code(output, language="python")
        else:
            st.info("โค้ดทำงานสำเร็จ (แต่ไม่มีการใช้คำสั่ง print เพื่อแสดงผลลัพธ์)")
            
    except Exception as e:
        sys.stdout = old_stdout
        error_msg = traceback.format_exc()
        st.error(f"❌ โค้ดของนักเรียนมีจุดผิดพลาด:\n{error_msg}")
