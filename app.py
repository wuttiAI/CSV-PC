import streamlit as st
import pandas as pd
import sys
from io import StringIO
import contextlib

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Python & CSV Sandbox for Students", layout="wide")

st.title("🖥️ ห้องปฏิบัติการฝึกเขียน Python ประมวลผล CSV")
st.write("คำชี้แจง: อัปโหลดไฟล์ CSV ของคุณ จากนั้นเขียนโค้ด Python โดยใช้ตัวแปร `df` เพื่อจัดการข้อมูล")

# แยกหน้าจอเป็น 2 ฝั่ง (ซ้าย: ข้อมูลและโจทย์ / ขวา: พื้นที่เขียนโค้ด)
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. อัปโหลดและดูข้อมูล CSV")
    uploaded_file = st.file_uploader("เลือกไฟล์ CSV", type=["csv"])
    
    # ตัวแปร Global สำหรับเก็บ DataFrame
    df = None
    
    if uploaded_file is not None:
        try:
            # อ่านไฟล์ CSV
            df = pd.read_csv(uploaded_file)
            st.success("อัปโหลดไฟล์สำเร็จ!")
            st.write("📊 **ตัวอย่างข้อมูล 5 แถวแรก:**")
            st.dataframe(df.head())
            
            # แสดงข้อมูลพื้นฐานของไฟล์
            st.write("**โครงสร้างข้อมูล (Columns):**")
            st.write(list(df.columns))
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
    else:
        st.info("💡 กรุณาอัปโหลดไฟล์ CSV ก่อนเพื่อเริ่มใช้งาน (ระบบจะสร้างตัวแปรชื่อ `df` ให้โดยอัตโนมัติ)")

with col2:
    st.header("2. พื้นที่เขียนโค้ด Python")
    
    # โค้ดเริ่มต้นที่แสดงในช่องคำสั่ง
    default_code = """# ตัวอย่าง: แสดงผลข้อมูลตาราง
print("จำนวนแถวและคอลัมน์:", df.shape)
print("\\nข้อมูลสถิติพื้นฐาน:")
print(df.describe())
"""
    
    # ช่องใสโค้ด Python
    user_code = st.text_area(
        "เขียนโค้ดของคุณที่นี่ (ใช้ตัวแปร df แทนข้อมูลของคุณ):", 
        value=default_code, 
        height=300
    )
    
    run_button = st.button("▶️ รันโค้ด (Run Code)")
    
    st.header("3. ผลลัพธ์การประมวลผล (Output)")
    
    if run_button:
        if df is None:
            st.warning("⚠️ กรุณาอัปโหลดไฟล์ CSV ก่อนรันโค้ด")
        else:
            # ฟังก์ชันสำหรับดักจับ stdout (สิ่งที่ print ออกมา)
            @contextlib.contextmanager
            def stdout_io(stdout=None):
                if stdout is None:
                    stdout = StringIO()
                oldout = sys.stdout
                sys.stdout = stdout
                try:
                    yield stdout
                finally:
                    sys.stdout = oldout

            # รันโค้ดของนักเรียน
            with stdout_io() as s:
                try:
                    # สร้าง environment สำหรับรันโค้ด โดยส่ง df เข้าไปด้วย
                    local_env = {"df": df, "pd": pd}
                    exec(user_code, globals(), local_env)
                    
                    # แสดงผลลัพธ์ที่ได้จากการพิมพ์ (print)
                    result = s.getvalue()
                    if result:
                        st.code(result, language="python")
                    else:
                        st.info("โค้ดทำงานสำเร็จ แต่ไม่มีการสั่ง print ผลลัพธ์ออกมา")
                        
                    # หากนักเรียนสร้างตัวแปร df ใหม่ หรืออัปเดตข้อมูล สามารถแสดงผลเป็นตารางได้
                    if isinstance(local_env.get("df"), pd.DataFrame):
                        st.write("📊 **ผลลัพธ์ของตาราง df ล่าสุด:**")
                        st.dataframe(local_env["df"])
                        
                except Exception as e:
                    # แสดง Error หากโค้ดมีปัญหา
                    st.error(f"❌ โค้ดเกิดข้อผิดพลาด:\n{e}")