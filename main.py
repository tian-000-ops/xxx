import streamlit as st
import pandas as pd

# 基础数据加载
def load_base_data():
    return pd.read_excel("student.xlsx", header=1)
df = load_base_data()

# 查询区域
with st.container(border=True):
    st.subheader("🔍 学生信息检索")
    col1, col2 = st.columns(2)
    with col1:
        input_id = st.text_input("请输入学号", placeholder="输入完整学号")
    with col2:
        input_name = st.text_input("请输入姓名", placeholder="输入学生姓名")

    search_btn = st.button("开始查询", type="primary")

    # 核心修改：按「或」逻辑查询，兼容单输入/双输入场景
    if search_btn:
        # 初始化匹配条件：全不匹配
        match_condition = pd.Series([False] * len(df))
        
        # 学号不为空时，追加学号匹配条件
        if input_id.strip() != "":
            id_match = df["学号"].astype(str) == input_id.strip()
            match_condition = match_condition | id_match
        
        # 姓名不为空时，追加姓名匹配条件
        if input_name.strip() != "":
            name_match = df["姓名"] == input_name.strip()
            match_condition = match_condition | name_match

        # 执行查询
        res_df = df[match_condition]

        # 结果处理
        if input_id.strip() == "" and input_name.strip() == "":
            st.warning("⚠️ 请至少输入学号或姓名其中一项")
        elif not res_df.empty:
            st.success("✅ 查询成功，匹配信息如下：")
            st.dataframe(res_df, height=350, use_container_width=True)
        else:
            st.warning("⚠️ 未找到对应学生，请核对学号和姓名")

# 底部说明
st.markdown("""
<div style='text-align: center; color: #64748b; margin-top: 2rem; font-size: 0.9rem;'>
学生信息查询系统 | 上传表格自动永久保存，退出重登无需重新上传
</div>
""", unsafe_allow_html=True)
