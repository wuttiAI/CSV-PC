import streamlit as st
import pandas as pd
import traceback

st.set_page_config(page_title="Python Sandbox", layout="wide")

st.title("🖥️ ห้องปฏิบัติการฝึกเขียน Python (เวอร์ชันเสถียร)")
st.write("คำชี้แจง: อัปโหลดไฟล์ CSV 1 หรือ 2 ไฟล์ ระบบจะสร้างตัวแปร `df1` และ `df2` ให้นักเรียนนำไปเขียนโค้ดต่อ")

# กำหนดตัวแปรตั้งต้นให้เป็น None
df1 = None
df2 = None

# 1. ส่วนอัปโหลดไฟล์ (รับได้สูงสุด 2 ไฟล์)
uploaded_files = st.file_uploader("เลือกไฟล์ CSV ของคุณ (สูงสุด 2 ไฟล์)", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    for index, file in enumerate(uploaded_files[:2]):
        try:
            if index == 0:
                df1 = pd.read_csv(file)
                st.success(f"ไฟล์ที่ 1 ({file.name}) โหลดเข้าตัวแปร `df1` เรียบร้อยแล้ว")
                st.dataframe(df1.head(3)) # แสดงตัวอย่างข้อมูล 3 แถวแรก
            elif index == 1:
                df2 = pd.read_csv(file)
                st.success(f"ไฟล์ที่ 2 ({file.name}) โหลดเข้าตัวแปร `df2` เรียบร้อยแล้ว")
                st.dataframe(df2.head(3)) # แสดงตัวอย่างข้อมูล 3 แถวแรก
        except Exception as e:
            st.error(f"ไม่สามารถอ่านไฟล์ {file.name} ได้: {e}")

st.write("---")

# 2. พื้นที่เขียนโค้ด Python (กลับมาใช้กล่องมาตรฐานของ Streamlit ที่เสถียรที่สุด)
st.subheader("📝 พื้นที่เขียนโค้ด Python")

default_code = """# ตัวอย่างการใช้งานตัวแปร df1 และ df2
if df1 is not None:
    print("โครงสร้างของ df1 คือ:", df1.shape)
    
if df2 is not None:
    print("โครงสร้างของ df2 คือ:", df2.shape)
"""

user_code = st.text_area("เขียนโค้ดของคุณที่นี่:", value=default_code, height=250)

# 3. ส่วนประมวลผลและแสดงผลลัพธ์
if st.button("▶️ รันโค้ด (Run Code)"):
    st.subheader("📊 ผลลัพธ์ (Output)")
    
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
    try:
        # ส่งเฉพาะ pandas, df1, df2 เข้าไปในขอบเขตการรันโค้ด
        local_scope = {"df1": df1, "df2": df2, "pd": pd}
        
        # รันโค้ด Python
        exec(user_code, globals(), local_scope)
        
        sys.stdout = old_stdout
        
        # แสดงผลจากการพิมพ์ (print)
        output = redirected_output.getvalue()
        if output:
            st.code(output, language="python")
        else:
            st.info("โค้ดทำงานสำเร็จ (แต่ไม่มีการใช้คำสั่ง print เพื่อแสดงผลลัพธ์)")
            
    except Exception as e:
        sys.stdout = old_stdout
        error_msg = traceback.format_exc()
        st.error(f"❌ โค้ดของนักเรียนมีจุดผิดพลาด:\n{error_msg}")
