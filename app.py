import streamlit as st
import pandas as pd
import traceback
from streamlit_ace import st_ace

st.set_page_config(page_title="Python Sandbox with Line Numbers", layout="wide")

st.title("🖥️ ห้องปฏิบัติการฝึกเขียน Python (มีเลขบรรทัด)")
st.write("คำชี้แจง: อัปโหลดไฟล์ CSV 1 หรือ 2 ไฟล์ ระบบจะสร้างตัวแปร `df1` และ `df2` ให้นักเรียนนำไปเขียนโค้ดต่อ")

# 💡 แก้ปัญหา TypeError: เช็กและสร้างสถานะเริ่มต้นเพื่อไม่ให้ระบบเออร์เรอร์เวลาหน้าเว็บรีเฟรช
if "editor_code" not in st.session_state:
    st.session_state["editor_code"] = """# ตัวอย่างการใช้งานตัวแปร df1 และ df2
if df1 is not None:
    print("โครงสร้างของ df1 คือ:", df1.shape)
    
if df2 is not None:
    print("โครงสร้างของ df2 คือ:", df2.shape)
"""

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

# 2. พื้นที่เขียนโค้ด Python
st.subheader("📝 พื้นที่เขียนโค้ด Python")

# 🔥 เรียกใช้งาน st_ace โดยดึงค่าจาก session_state ป้องกันอาการ TypeError ทันที
user_code = st_ace(
    value=st.session_state["editor_code"],
    language="python",
    theme="monokai",
    font_size=16,
    tab_size=4,
    wrap=True,
    auto_validate=False,
    height=300,
    key="python_editor_ace"
)

# อัปเดตโค้ดล่าสุดเก็บลงระบบความจำของเพจ
st.session_state["editor_code"] = user_code

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
