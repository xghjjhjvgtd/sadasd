# 航训评迹-飞行训练数据与品质复盘分析系统
# Streamlit 云端可运行版（修复空白问题）
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="飞行数据可视化系统",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🛫 航训评迹 - 飞行训练数据与品质复盘分析系统")
    st.markdown("---")

    # 上传文件
    uploaded_file = st.file_uploader("上传飞行数据 CSV 文件", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ 数据加载成功！共 {len(df)} 行数据")

        # 显示数据预览
        with st.expander("📋 查看原始数据"):
            st.dataframe(df.head(20), use_container_width=True)

        # 数据分析
        st.subheader("📊 飞行数据概览")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("数据条数", len(df))
        with col2:
            if "altitude" in df.columns:
                st.metric("最大高度", f"{df['altitude'].max():.0f} ft")
            else:
                st.metric("最大高度", "无数据")
        with col3:
            if "speed" in df.columns:
                st.metric("平均速度", f"{df['speed'].mean():.1f} kn")
            else:
                st.metric("平均速度", "无数据")

        # 图表
        st.markdown("---")
        st.subheader("📈 数据趋势图")
        
        if "time" in df.columns and "altitude" in df.columns:
            fig = px.line(df, x="time", y="altitude", title="飞行高度变化")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ 上传标准数据后可查看完整可视化图表")

    else:
        st.info("👆 请上传飞行数据 CSV 文件开始分析")
        
    st.markdown("<br><br><center>系统已正常运行</center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
