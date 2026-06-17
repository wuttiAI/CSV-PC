import streamlit as st
import pandas as pd
import traceback
import os

st.set_page_config(page_title="Python CSV Sandbox", layout="wide")

st.title("🖥️ ฝึกเขียน Python กับไฟล์ CSV) : by UPR Wuttichai")
st.write("คำชี้แจง: ระบบได้เตรียมไฟล์ข้อมูลสำหรับฝึกหัดไว้ให้เรียบร้อยแล้ว นักเรียนสามารถเขียนโค้ดเรียกใช้ไฟล์ตามชื่อด้านล่างได้ทันที")

# --- 🟢 ส่วนที่ 1: รายชื่อไฟล์จริงที่คุณครูกำหนด ---
preset_files = ["sciScore.csv", "studentData.csv", "studentData-noHeader.csv"]

st.subheader("📊 ไฟล์ข้อมูลที่มีอยู่ในระบบ (พร้อมใช้เรียน)")
cols = st.columns(len(preset_files))

for index, file_name in enumerate(preset_files):
    with cols[index]:
        # ตรวจสอบว่าคุณครูอัปโหลดไฟล์นี้ขึ้น GitHub หรือยัง
        if os.path.exists(file_name):
            st.info(f"📄 ไฟล์: `{file_name}`")
            try:
                # ถ้าเป็นไฟล์แบบไม่มี Header ให้ลองจำลองเปิดแบบไม่มีหัวคอลัมน์เพื่อความสวยงามบนหน้าเว็บ
                if "noHeader" in file_name:
                    temp_df = pd.read_csv(file_name, header=None)
                else:
                    temp_df = pd.read_csv(file_name)
                st.dataframe(temp_df.head(3))
            except Exception as e:
                st.error(f"อ่านไฟล์ล้มเหลว: {e}")
        else:
            st.warning(f"⚠️ ไม่พบไฟล์ `{file_name}`\n(กรุณาอัปโหลดไฟล์นี้ขึ้นหน้าแรกของ GitHub)")

st.write("---")

# --- 📝 ส่วนที่ 2: พื้นที่เขียนโค้ด Python ---
st.subheader("📝 พื้นที่เขียนโค้ด Python")

# ไกด์ไลน์คำสั่งสอนนักเรียนเกี่ยวกับความแตกต่างของไฟล์แต่ละประเภท
default_code = """import pandas as pd

# 💡 ตัวอย่างที่ 1: อ่านไฟล์ธรรมดาที่มีหัวคอลัมน์
df_std = pd.read_csv('studentData.csv')
print("--- ข้อมูลใน studentData.csv ---")
print(df_std.head(2))

# 💡 ตัวอย่างที่ 2: อ่านไฟล์ที่ไม่มีหัวคอลัมน์ (ต้องระบุ header=None และตั้งชื่อคอลัมน์เอง)
# df_no_header = pd.read_csv('studentData-noHeader.csv', header=None, names=['id', 'name', 'age'])
# print("\\n--- ข้อมูลใน studentData-noHeader.csv ---")
# print(df_no_header.head(2))

# 💡 ลองเขียนโค้ดวิเคราะห์ข้อมูลของคุณต่อตรงนี้ได้เลยครับ:
"""

user_code = st.text_area("เขียนโค้ดของคุณที่นี่:", value=default_code, height=320)

# --- 📊 ส่วนที่ 3: ประมวลผลเมื่อกดปุ่ม ---
if st.button("▶️ รันโค้ด (Run Code)"):
    st.subheader("📊 ผลลัพธ์ (Output)")
    
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
    try:
        # ส่งพารามิเตอร์ pandas เข้าไปให้นักเรียนเรียกใช้
        local_scope = {"pd": pd}
        
        # รันโค้ด
        exec(user_code, globals(), local_scope)
        
        sys.stdout = old_stdout
        
        # ดึงข้อความจากการสั่ง print ออกมาแสดง
        output = redirected_output.getvalue()
        if output:
            st.code(output, language="python")
        else:
            st.info("โค้ดทำงานสำเร็จ (แต่ไม่มีการใช้คำสั่ง print เพื่อแสดงผลลัพธ์)")
            
    except Exception as e:
        sys.stdout = old_stdout
        error_msg = traceback.format_exc()
        st.error(f"❌ โค้ดของนักเรียนมีจุดผิดพลาด:\n{error_msg}")
