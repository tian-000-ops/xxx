import streamlit as st
import pandas as pd
import os

# ========== 页面基础设置 ==========
st.set_page_config(page_title="学生信息查询系统", layout="wide")

# 蓝紫色自定义样式
custom_css = """
<style>
.stApp {
    background-color: #f8fafc;
}
h1,h2,h3 {
    color:#4338ca;
}
.stButton>button {
    background-color:#4338ca;
    color:white;
    border:none;
}
.stButton>button:hover {
    background-color:#3730a3;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ========== 登录账号密码 ==========
USER_ACCOUNT = "15705181210"
USER_PWD = "1210www"

save_file = "student_save.xlsx"

# 登录状态
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 系统登录")
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        acc = st.text_input("账号")
        pwd = st.text_input("密码",type="password")
        if st.button("登录",use_container_width=True):
            if acc == USER_ACCOUNT and pwd == USER_PWD:
                st.session_state.login = True
                st.rerun()
            else:
                st.error("账号或密码错误")
    st.stop()

# ========== 加载数据 ==========
df = None
if os.path.exists(save_file):
    df = pd.read_excel(save_file, header=1)
else:
    try:
        df = pd.read_excel("student.xlsx", header=1)
    except:
        st.warning("暂无数据，请点击右上角更新上传Excel表格")

# ========== 右上角更新Excel上传按钮 ==========
right_col1, right_col2 = st.columns([8,2])
with right_col2:
    with st.expander("📁 更新Excel数据"):
        up_file = st.file_uploader("上传新版学生Excel", type=["xlsx"])
        if up_file is not None:
            new_df = pd.read_excel(up_file, header=1)
            new_df.to_excel(save_file, index=False)
            st.success("✅ 已上传（⚠️免费云容器重启会丢失，长期更新请把新表上传GitHub覆盖原文件）")
            st.rerun()

st.markdown("---")
st.title("📋 学生信息查询")

# =====调试：显示程序实际读到的表格前5行=====
if df is not None:
    st.write("🔍【调试：程序读到的表格前5行】")
    st.dataframe(df.head(),use_container_width=True)
    st.write("列名列表：", df.columns.tolist())

# ========== 查询模块：填学号 OR 填姓名任意一项即可查询 ==========
col_a,col_b = st.columns(2)
with col_a:
    input_id = st.text_input("输入学号（选填）")
with col_b:
    input_name = st.text_input("输入姓名（选填）")

search_btn = st.button("🔍 查询", type="primary")

if search_btn and df is not None:
    condition = pd.Series([False]*len(df))
    # 学号：第3列；姓名：第2列（根据调试截图修正）
    if input_id.strip():
        c1 = df.iloc[:,3].astype(str).str.contains(input_id.strip(), na=False)
        condition = condition | c1
    if input_name.strip():
        c2 = df.iloc[:,2].astype(str).str.contains(input_name.strip(), na=False)
        condition = condition | c2

    result = df[condition]
    if result.empty:
        st.info("未查询到匹配学生信息")
    else:
        st.subheader("✅ 查询结果")
        st.dataframe(result, use_container_width=True)
elif df is None:
    st.warning("表格数据不存在，请先上传Excel")
