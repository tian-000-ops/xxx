import streamlit as st
import pandas as pd
import os

# ========== 页面基础配置 ==========
st.set_page_config(page_title="学生信息查询系统", layout="wide")
# 临时保存上传文件的路径
save_file = "student_save.xlsx"

# ========== 数据读取（固定：第二行作表头，第三行起读数据） ==========
df = None
# 优先读取临时上传的文件
if os.path.exists(save_file):
    try:
        df = pd.read_excel(save_file, header=1)  # 固定header=1，匹配Excel结构
    except Exception:
        # 临时文件损坏则丢弃，回退读取原始表格
        df = None
# 读取github原始表格
if df is None:
    try:
        df = pd.read_excel("student.xlsx", header=1)  # 固定header=1，匹配Excel结构
    except Exception:
        st.warning("暂无有效表格，请右上角上传符合格式的Excel文件")

# ========== 右上角上传更新Excel（同步适配表头规则） ==========
c_left, c_right = st.columns([8, 2])
with c_right:
    with st.expander("📁 更新Excel数据"):
        upload_file = st.file_uploader("上传新Excel", type="xlsx")
        if upload_file is not None:
            # 上传的文件也按第二行作表头读取，保持格式完全一致
            new_df = pd.read_excel(upload_file, header=1)
            new_df.to_excel(save_file, index=False)
            st.success("✅ 上传完成！")
            st.rerun()

# ========== 查询主界面 ==========
st.divider()
st.title("📋 学生信息查询")

# 输入框区域
col_a, col_b = st.columns(2)
with col_a:
    input_xh = st.text_input("输入学号（选填）")
with col_b:
    input_xm = st.text_input("输入姓名（选填）")

# 查询按钮
search_btn = st.button("🔍 查询", type="primary")

# 查询逻辑：学号 OR 姓名匹配
if search_btn and df is not None:
    # 初始化匹配条件
    match_mask = pd.Series([False] * len(df))
    # 列顺序匹配你的表格：姓名=第2列、学号=第3列
    if input_xh.strip() != "":
        id_match = df.iloc[:, 3].astype(str).str.contains(input_xh.strip(), na=False)
        match_mask = match_mask | id_match
    if input_xm.strip() != "":
        name_match = df.iloc[:, 2].astype(str).str.contains(input_xm.strip(), na=False)
        match_mask = match_mask | name_match

    # 执行查询
    result_df = df[match_mask]

    # 结果处理
    if input_xh.strip() == "" and input_xm.strip() == "":
        st.warning("⚠️ 请至少输入学号或者姓名其中一项")
    elif not result_df.empty:
        st.subheader("✅ 查询结果")
        # 自动先显示表头（Excel第二行内容），再展示匹配的数据行
        st.dataframe(result_df, use_container_width=True)
    else:
        st.info("未查询到匹配的学生信息")
# 无数据时的提示
elif df is None and search_btn:
    st.warning("请先上传符合格式的Excel表格")

# ========== 底部说明 ==========
st.markdown("""
<div style='text-align: center; color: #64748b; margin-top: 2rem; font-size: 0.9rem;'>
学生信息查询系统 | 免费云容器重启后临时文件会丢失，永久更新请上传新版Excel到GitHub仓库
</div>
""", unsafe_allow_html=True)
