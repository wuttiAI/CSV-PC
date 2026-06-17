import streamlit as st
import pandas as pd
import traceback
import os

st.set_page_config(page_title="Python CSV Sandbox (3 Files)", layout="wide")

st.title("🖥️ ห้องปฏิบัติการฝึกเขียน Python (รองรับสูงสุด 3 ไฟล์)")
st.write("คำชี้แจง: อัปโหลดไฟล์ CSV ได้สูงสุด 3 ไฟล์ จากนั้นเขียนโค้ดเรียกใช้ไฟล์โดยพิมพ์ชื่อไฟล์ให้ตรงกับที่คุณอัปโหลด")

# 1. ส่วนอัปโหลดไฟล์ (ปรับเปลี่ยนตรงคลิปหนีบไฟล์ให้รับสูงสุด 3 ไฟล์)
uploaded_files = st.file_uploader("เลือกไฟล์ CSV ของคุณ (สูงสุด 3 ไฟล์)", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    # จำกัดการทำงานไว้ที่ไม่เกิน 3 ไฟล์แรกที่อัปโหลดเข้ามา
    for file in uploaded_files[:3]:
        try:
            # บันทึกไฟล์ลงเซิร์ฟเวอร์ตามชื่อไฟล์จริง
            with open(file.name, "wb") as f:
                f.write(file.getbuffer())
                
            st.success(f"💾 อัปโหลดไฟล์ `{file.name}` สำเร็จ! (นำชื่อนี้ไปใส่ในโค้ดได้เลย)")
            
            # แสดงตารางตัวอย่างข้อมูล 3 แถวแรกให้นักเรียนเช็กคอลลัมน์
            temp_df = pd.read_csv(file.name)
            st.dataframe(temp_df.head(3))
            
        except Exception as e:
            st.error(f"ไม่สามารถประมวลผลไฟล์ {file.name} ได้: {e}")

st.write("---")

# 2. พื้นที่เขียนโค้ด Python
st.subheader("📝 พื้นที่เขียนโค้ด Python")

# ปรับตัวอย่างโค้ดไกด์ไลน์ให้นักเรียนเห็นภาพการดึงข้อมูล 3 ไฟล์มาใช้งานพร้อมกัน
default_code = """import pandas as pd

# ตัวอย่าง: หากนักเรียนอัปโหลดไฟล์มา 3 ไฟล์ สามารถเขียนอ่านไฟล์ตรงๆ ได้แบบนี้เลยครับ
# df1 = pd.read_csv('student_info.csv')
# df2 = pd.read_csv('student_score.csv')
# df3 = pd.read_csv('student_attendance.csv')

# ทดลองพิมพ์โค้ดของคุณด้านล่างนี้ได้เลย:
"""

user_code = st.text_area("เขียนโค้ดของคุณที่นี่:", value=default_code, height=280)

# 3. ส่วนประมวลผลและแสดงผลลัพธ์เมื่อกดปุ่ม
if st.button("▶️ รันโค้ด (Run Code)"):
    st.subheader("📊 ผลลัพธ์ (Output)")
    
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
    try:
        # ส่ง Library Pandas เข้าไปในระบบรันโค้ดของนักเรียน
        local_scope = {"pd": pd}
        
        # รันโค้ด Python
        exec(user_code, globals(), local_scope)
        
        sys.stdout = old_stdout
        
        # ดึงค่าที่นักเรียนสั่ง print ออกมาแสดงผล
        output = redirected_output.getvalue()
        if output:
            st.code(output, language="python")
        else:
            st.info("โค้ดทำงานสำเร็จ (แต่ไม่มีการใช้คำสั่ง print เพื่อแสดงผลลัพธ์)")
            
    except Exception as e:
        sys.stdout = old_stdout
        error_msg = traceback.format_exc()
        st.error(f"❌ โค้ดของนักเรียนมีจุดผิดพลาด:\n{error_msg}")
