import streamlit as st
import pandas as pd
import os

# ==========页面配置==========
st.set_page_config(page_title="学生信息查询系统", layout="wide")

# 登录账号密码
USER_ACCOUNT = "15705181210"
USER_PWD = "1210www"
save_file = "student_save.xlsx"

if "login" not in st.session_state:
    st.session_state.login = False

# 登录页面
if not st.session_state.login:
    st.title("🔐 系统登录")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("账号")
        password = st.text_input("密码", type="password")
        if st.button("登录", use_container_width=True):
            if username == USER_ACCOUNT and password == USER_PWD:
                st.session_state.login = True
                st.rerun()
            else:
                st.error("账号或密码错误")
    st.stop()

# 读取Excel
df = None
if os.path.exists(save_file):
    df = pd.read_excel(save_file, header=1)
else:
    try:
        df = pd.read_excel("student.xlsx", header=1)
    except Exception:
        st.warning("暂无表格，请右上角上传Excel文件")

# 右上角上传更新Excel
c_left, c_right = st.columns([8, 2])
with c_right:
    with st.expander("📁 更新Excel数据"):
        upload_file = st.file_uploader("上传新Excel", type="xlsx")
        if upload_file is not None:
            new_df = pd.read_excel(upload_file, header=1)
            new_df.to_excel(save_file, index=False)
            st.success("上传完成！")
            st.rerun()

st.divider()
st.title("📋 学生信息查询")

# 查询输入区
col_a, col_b = st.columns(2)
with col_a:
    input_xh = st.text_input("输入学号（选填）")
with col_b:
    input_xm = st.text_input("输入姓名（选填）")

search_btn = st.button("🔍 查询", type="primary")

if search_btn and df is not None:
    mask = pd.Series([False] * len(df))
    # 学号：第3列，姓名：第2列
    if input_xh.strip() != "":
        mask = mask | df.iloc[:,3].astype(str).str.contains(input_xh.strip(), na=False)
    if input_xm.strip() != "":
        mask = mask | df.iloc[:,2].astype(str).str.contains(input_xm.strip(), na=False)

    result = df[mask]
    if input_xh.strip() == "" and input_xm.strip() == "":
        st.warning("请至少输入学号或者姓名其中一项")
    elif not result.empty:
        st.subheader("✅ 查询结果")
        st.dataframe(result, use_container_width=True)
    else:
        st.info("未查询到匹配学生信息")
elif df is None and search_btn:
    st.warning("请先上传Excel表格")
