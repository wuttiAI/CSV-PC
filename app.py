import streamlit as st
import sys
from io import StringIO
import contextlib

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบกว้าง (Wide Layout)
st.set_page_config(page_title="Python CSV Parser Sandbox", layout="wide")

st.title("🖥️ ห้องปฏิบัติการเขียนฟังก์ชัน Read CSV ด้วยตัวเอง")
st.write("คำชี้แจง: อัปโหลดไฟล์ CSV ระบบจะเก็บเนื้อหาของไฟล์ในรูปแบบข้อความดิบ (String) ไว้ในตัวแปรดิคชันนารีชื่อ `raw_files`")

# 2. แยกหน้าจอเป็น 2 ฝั่ง (ซ้าย: อัปโหลดและดูไฟล์ / ขวา: เขียนโค้ดและดูผลลัพธ์)
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. อัปโหลดและดูไฟล์ข้อความดิบ")
    uploaded_files = st.file_uploader("เลือกไฟล์ CSV (ส่งได้หลายไฟล์พร้อมกัน)", type=["csv"], accept_multiple_files=True)
    
    # ตัวแปรสำหรับเก็บข้อความดิบของไฟล์: {"ชื่อไฟล์.csv": "ข้อความดิบข้างในทั้งหมด"}
    raw_files = {} 
    
    if uploaded_files:
        st.success(f"โหลดไฟล์เข้าสู่ระบบจำนวน {len(uploaded_files)} ไฟล์สำเร็จ!")
        
        for uploaded_file in uploaded_files:
            try:
                # อ่านไฟล์ออกมาเป็น String ดิบๆ โดยตรง
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                file_contents = stringio.read()
                
                # เก็บลงใน Dictionary โดยใช้ชื่อไฟล์เป็น Key
                raw_files[uploaded_file.name] = file_contents
                
                # สร้างกล่องพับเพื่อแสดงหน้าตาของข้อมูลดิบข้างในให้นักเรียนเห็น
                with st.expander(f"📄 เนื้อหาดิบในไฟล์ (Raw Text): {uploaded_file.name}"):
                    st.text(file_contents[:500] + "\n... (มีต่อ) ...") 
                    
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์ {uploaded_file.name}: {e}")
    else:
        st.info("💡 กรุณาอัปโหลดไฟล์ CSV ก่อน ระบบจะสร้างตัวแปรชื่อ `raw_files` ให้ใช้งาน")

with col2:
    st.header("2. พื้นที่เขียนโค้ด Python")
    
    # โจทย์ไกด์ไลน์เริ่มต้นที่แสดงในช่องคำสั่งให้นักเรียน
    default_code = """# โจทย์: เขียนฟังก์ชันเพื่อแปลงข้อความดิบ (CSV String) ให้กลายเป็น List ของ Dictionary
def my_read_csv(csv_string):
    lines = csv_string.strip().split('\\n') # แยกแต่ละบรรทัด
    headers = lines[0].split(',')          # บรรทัดแรกคือหัวคอลัมน์
    
    result = []
    for line in lines[1:]:                 # ลูปตั้งแต่บรรทัดที่สองลงไป
        values = line.split(',')
        # สร้าง dict จับคู่หัวคอลัมน์กับข้อมูล
        row_dict = dict(zip(headers, values)) 
        result.append(row_dict)
        
    return result

# --- ทดสอบเรียกใช้งานฟังก์ชันของนักเรียน ---
file_name = list(raw_files.keys())[0] # ดึงชื่อไฟล์แรกมาทดสอบ
data_string = raw_files[file_name]     # ดึงข้อความดิบออกมา

# รันฟังก์ชัน
parsed_data = my_read_csv(data_string)

print(f"ผลลัพธ์จากการอ่านไฟล์ {file_name}:")
print("ข้อมูล 2 แถวแรกที่แปลงเสร็จแล้ว:")
print(parsed_data[:2])
"""
    
    # ช่องกรอกโค้ดสำหรับนักเรียน
    user_code = st.text_area(
        "เขียนฟังก์ชันและโค้ดของคุณที่นี่ (ใช้ตัวแปร raw_files):", 
        value=default_code, 
        height=380
    )
    
    run_button = st.button("▶️ รันโค้ด (Run Code)")
    
    st.header("3. ผลลัพธ์การประมวลผล (Output)")
    
    if run_button:
        if not raw_files:
            st.warning("⚠️ กรุณาอัปโหลดไฟล์ CSV ก่อนรันโค้ด")
        else:
            # 💡 ฟังก์ชันดักจับคำสั่ง print (แก้ไขส่วนที่เคยบั๊กเรียบร้อยแล้ว)
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

            # ทำการรันโค้ดของนักเรียนในสภาพแวดล้อมจำลอง
            with stdout_io() as s:
                try:
                    # ส่งตัวแปร raw_files เข้าไปในสภาพแวดล้อมให้เด็กเรียกใช้ได้
                    local_env = {"raw_files": raw_files}
                    exec(user_code, globals(), local_env)
                    
                    # แสดงผลลัพธ์ที่ได้จากการสั่ง print
                    result = s.getvalue()
                    if result:
                        st.code(result, language="python")
                    else:
                        st.info("โค้ดทำงานสำเร็จ แต่ไม่มีการสั่ง print ผลลัพธ์ออกมา")
