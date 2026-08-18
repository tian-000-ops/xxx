import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="学生信息查询系统", layout="wide")
save_file = "student_save.xlsx"

df = None
# 读取文件 header=1：Excel第二行为表头
if os.path.exists(save_file):
    try:
        df = pd.read_excel(save_file, header=1)
    except Exception:
        df = None
if df is None:
    try:
        df = pd.read_excel("student.xlsx", header=1)
    except Exception:
        st.warning("暂无有效表格，请右上角上传符合格式的Excel文件")


c_left, c_right = st.columns([8, 2])
with c_right:
    with st.expander("📁 更新Excel数据"):
        upload_file = st.file_uploader("上传新Excel", type="xlsx")
        if upload_file is not None:
            # 直接保存原始上传字节，不经过pandas！完整保留Excel全部行
            with open(save_file, "wb") as f:
                f.write(upload_file.getbuffer())
            st.success("✅ 上传完成！")
            st.rerun()


st.divider()
st.title("📋 学生信息查询")

col_a, col_b = st.columns(2)
with col_a:
    input_xh = st.text_input("输入学号（选填）")
with col_b:
    input_xm = st.text_input("输入姓名（选填）")

search_btn = st.button("🔍 查询", type="primary")

if search_btn and df is not None:
    match_mask = pd.Series([False] * len(df))
    if input_xh.strip() != "":
        id_match = df.iloc[:, 3].astype(str).str.contains(input_xh.strip(), na=False)
        match_mask = match_mask | id_match
    if input_xm.strip() != "":
        name_match = df.iloc[:, 2].astype(str).str.contains(input_xm.strip(), na=False)
        match_mask = match_mask | name_match

    result_df = df[match_mask]

    if input_xh.strip() == "" and input_xm.strip() == "":
        st.warning("⚠️ 请至少输入学号或者姓名其中一项")
    elif not result_df.empty:
        st.subheader("✅ 查询结果")
        st.dataframe(result_df, use_container_width=True)
    else:
        st.info("未查询到匹配的学生信息")
elif df is None and search_btn:
    st.warning("请先上传符合格式的Excel表格")


st.markdown("""
<div style='text-align: center; color: #64748b; margin-top: 2rem; font-size: 0.9rem;'>
学生信息查询系统 | 免费云容器重启后临时文件会丢失，永久更新请上传新版Excel到GitHub仓库
</div>
""", unsafe_allow_html=True)
