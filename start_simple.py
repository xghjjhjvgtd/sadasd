# 文件: start_simple.py
"""
最小化启动脚本 - 绕过环境问题直接启动
"""

import os
import sys
import subprocess
from pathlib import Path

def create_minimal_app():
    """创建一个最小化的应用，避免依赖冲突"""
    
    minimal_app = '''
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64
from datetime import datetime
import json

def create_simple_app():
    """创建简单应用"""
    import streamlit as st
    
    st.set_page_config(
        page_title="飞行数据分析",
        layout="wide"
    )
    
    st.title("✈️ 飞行数据分析工具")
    
    # 文件上传
    uploaded_file = st.file_uploader("上传CSV文件", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # 读取数据
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ 数据加载成功: {len(df)} 行")
            
            # 显示数据
            st.subheader("📋 数据预览")
            st.dataframe(df.head())
            
            # 基本统计
            st.subheader("📊 数据统计")
            st.write(df.describe())
            
            # 简单图表
            st.subheader("📈 可视化")
            
            # 检查是否有数值列
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("X轴", numeric_cols)
                with col2:
                    y_col = st.selectbox("Y轴", numeric_cols)
                
                if st.button("生成图表"):
                    fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                    st.plotly_chart(fig)
            
        except Exception as e:
            st.error(f"❌ 处理数据时出错: {e}")
    
    else:
        st.info("📁 请上传CSV格式的飞行数据文件")
        
        # 示例数据
        if st.button("使用示例数据"):
            sample_data = pd.DataFrame({
                '时间': pd.date_range('2024-01-01', periods=100, freq='1min'),
                '高度_ft': [1000 + i*50 + (i%10)*20 for i in range(100)],
                '空速_kts': [200 + i*2 + (i%5)*10 for i in range(100)],
                '发动机_N1': [80 + i*0.1 + (i%8)*2 for i in range(100)]
            })
            
            st.dataframe(sample_data)
            
            # 创建图表
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=sample_data['时间'], y=sample_data['高度_ft'], 
                                    mode='lines', name='高度'))
            fig.add_trace(go.Scatter(x=sample_data['时间'], y=sample_data['空速_kts'], 
                                    mode='lines', name='空速', yaxis='y2'))
            
            fig.update_layout(
                title='飞行数据示例',
                yaxis=dict(title='高度 (ft)'),
                yaxis2=dict(title='空速 (kts)', overlaying='y', side='right')
            )
            
            st.plotly_chart(fig)

if __name__ == "__main__":
    create_simple_app()
'''
    
    # 保存最小化应用
    with open("flight_app_simple.py", "w", encoding="utf-8") as f:
        f.write(minimal_app)
    
    print("✅ 最小化应用创建完成: flight_app_simple.py")
    return "flight_app_simple.py"

def install_minimal_deps():
    """安装最小化依赖"""
    print("📦 安装最小化依赖...")
    
    # 创建虚拟环境（可选）
    if not Path("venv").exists():
        print("创建虚拟环境...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # 确定Python解释器
    if sys.platform == "win32":
        python_exe = "venv\\Scripts\\python.exe"
        pip_exe = "venv\\Scripts\\pip.exe"
    else:
        python_exe = "venv/bin/python"
        pip_exe = "venv/bin/pip"
    
    # 安装最小依赖
    minimal_deps = [
        "streamlit==1.12.0",
        "pandas==1.5.3",
        "plotly==5.9.0",
        "numpy==1.24.3"
    ]
    
    for dep in minimal_deps:
        print(f"安装 {dep}...")
        subprocess.run([pip_exe, "install", dep])
    
    print("✅ 依赖安装完成")
    return python_exe

def main():
    """主函数"""
    print("🚀 最小化飞行数据分析工具")
    print("=" * 50)
    
    print("请选择启动方式:")
    print("1. 快速修复并启动完整版")
    print("2. 启动最小化版本（推荐）")
    print("3. 创建独立可执行包")
    print("4. 退出")
    
    choice = input("\n请输入选项 (1-4): ").strip()
    
    if choice == "1":
        # 运行修复脚本
        subprocess.run([sys.executable, "fix_environment.py"])
        
    elif choice == "2":
        # 创建并运行最小化应用
        app_file = create_simple_app()
        
        print("\n🌐 启动最小化应用...")
        print("访问地址: http://localhost:8501")
        print("按 Ctrl+C 停止")
        
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run",
                app_file,
                "--server.port", "8501",
                "--server.headless", "false"
            ])
        except KeyboardInterrupt:
            print("\n👋 应用已停止")
            
    elif choice == "3":
        # 创建独立包
        create_standalone_package()
        
    elif choice == "4":
        print("👋 再见")
        
    else:
        print("❌ 无效选项")

def create_standalone_package():
    """创建独立包"""
    print("📦 创建独立包...")
    
    standalone_code = '''
import sys
import os
import io
import pandas as pd
import numpy as np
from datetime import datetime
import json

class FlightAnalyzer:
    """独立飞行分析器"""
    
    def __init__(self):
        pass
    
    def analyze_csv(self, filepath):
        """分析CSV文件"""
        try:
            # 读取CSV
            df = pd.read_csv(filepath)
            
            results = {
                'filename': os.path.basename(filepath),
                'row_count': len(df),
                'column_count': len(df.columns),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'columns': list(df.columns),
                'summary': self._get_summary(df)
            }
            
            return df, results
            
        except Exception as e:
            return None, {'error': str(e)}
    
    def _get_summary(self, df):
        """获取数据摘要"""
        summary = {}
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            summary[col] = {
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'mean': float(df[col].mean()),
                'std': float(df[col].std())
            }
        
        return summary
    
    def generate_report(self, df, analysis):
        """生成报告"""
        report = f"""
飞行数据分析报告
================

文件信息:
--------
文件名: {analysis['filename']}
分析时间: {analysis['timestamp']}
数据规模: {analysis['row_count']} 行 × {analysis['column_count']} 列

数据摘要:
--------
"""
        
        if 'summary' in analysis:
            for col, stats in analysis['summary'].items():
                report += f"\n{col}:\n"
                report += f"  最小值: {stats['min']:.2f}\n"
                report += f"  最大值: {stats['max']:.2f}\n"
                report += f"  平均值: {stats['mean']:.2f}\n"
                report += f"  标准差: {stats['std']:.2f}\n"
        
        # 保存报告
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"flight_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report_file

def main():
    """主函数"""
    print("✈️ 独立飞行数据分析工具")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # 命令行模式
        filepath = sys.argv[1]
        analyzer = FlightAnalyzer()
        
        df, analysis = analyzer.analyze_csv(filepath)
        
        if df is not None:
            print(f"✅ 分析完成: {analysis['filename']}")
            print(f"📊 数据规模: {analysis['row_count']} 行 × {analysis['column_count']} 列")
            
            report_file = analyzer.generate_report(df, analysis)
            print(f"📄 报告已保存: {report_file}")
        else:
            print(f"❌ 分析失败: {analysis['error']}")
    
    else:
        # 交互模式
        print("使用说明:")
        print("1. 将CSV文件拖拽到本程序上")
        print("2. 或运行: python flight_standalone.py 你的文件.csv")
        print("\n支持功能:")
        print("- CSV文件分析")
        print("- 数据统计摘要")
        print("- 报告生成")
        
        input("\n按Enter键退出...")

if __name__ == "__main__":
    main()
'''
    
    # 保存独立包
    with open("flight_standalone.py", "w", encoding="utf-8") as f:
        f.write(standalone_code)
    
    print("✅ 独立包创建完成: flight_standalone.py")
    print("\n使用方法:")
    print("1. 直接拖拽CSV文件到 flight_standalone.py 上")
    print("2. 或运行: python flight_standalone.py 你的文件.csv")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 启动失败: {e}")