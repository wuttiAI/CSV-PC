import streamlit as st
import pandas as pd
import traceback
import os

st.set_page_config(page_title="Python CSV Sandbox", layout="wide")

st.title("🖥️ ห้องปฏิบัติการฝึกเขียน Python (รันด้วยชื่อไฟล์จริง)")
st.write("คำชี้แจง: อัปโหลดไฟล์ CSV เข้าสู่ระบบ จากนั้นเขียนโค้ดเรียกใช้ไฟล์โดยพิมพ์ชื่อไฟล์ที่คุณอัปโหลดได้เลย")

# 1. ส่วนอัปโหลดไฟล์ (รับได้สูงสุด 2 ไฟล์)
uploaded_files = st.file_uploader("เลือกไฟล์ CSV ของคุณ (สูงสุด 2 ไฟล์)", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files[:2]:
        try:
            # 💡 จุดสำคัญ: แอบเซฟไฟล์ที่เด็กอัปโหลดลงเครื่องเซิร์ฟเวอร์จริงๆ ตามชื่อไฟล์นั้น
            with open(file.name, "wb") as f:
                f.write(file.getbuffer())
                
            st.success(f"💾 อัปโหลดไฟล์ `{file.name}` เข้าสู่ระบบสำเร็จ! (นักเรียนสามารถใช้ชื่อไฟล์นี้ในโค้ดได้เลย)")
            
            # แสดงตัวอย่างข้อมูลให้ดูเพื่อความแน่ใจ
            temp_df = pd.read_csv(file.name)
            st.dataframe(temp_df.head(3))
            
        except Exception as e:
            st.error(f"ไม่สามารถประมวลผลไฟล์ {file.name} ได้: {e}")

st.write("---")

# 2. พื้นที่เขียนโค้ด Python
st.subheader("📝 พื้นที่เขียนโค้ด Python")

# เปลี่ยนโค้ดไกด์ไลน์เริ่มต้นให้ตรงกับสไตล์ที่คุณครูอยากให้เด็กเขียน
default_code = """import pandas as pd

# สมมติว่าอัปโหลดไฟล์ชื่อ studentData.csv เข้ามา
# นักเรียนสามารถใช้คำสั่ง pd.read_csv พิมพ์ชื่อไฟล์ตรงๆ ได้เลยแบบนี้ครับ:
stdData = pd.read_csv('studentData.csv', delimiter=',')
print(stdData)
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
        # ส่ง pandas เข้าไปให้เรียกใช้ได้
        local_scope = {"pd": pd}
        
        # รันโค้ด Python ของนักเรียน
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
