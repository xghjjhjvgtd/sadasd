# 文件6: main.py - 程序入口（Streamlit 1.12.0兼容）
"""
飞行数据可视化系统 - 主程序入口
Streamlit 1.12.0 兼容版本
"""

import sys
import os
from pathlib import Path
import subprocess
import webbrowser
import threading
import time

def setup_environment():
    """设置运行环境"""
    print("=" * 60)
    print("航训评迹-飞行训练数据与品质复盘分析系统")
    print("=" * 60)
    
    # 检查Python版本
    if sys.version_info < (3, 9):
        print("⚠️  警告: 建议使用 Python 3.9 或更高版本")
        print(f"当前版本: {sys.version}")
    
    # 项目路径
    project_root = Path(__file__).parent
    
    # 检查依赖
    print("\n📦 检查依赖库...")
    
    required_packages = [
        'streamlit==1.12.0',
        'pandas==1.4.4',
        'numpy==1.21.6',
        'plotly==5.9.0',
        'geopy==2.2.0'
    ]
    
    missing_packages = []
    
    for package_spec in required_packages:
        package_name = package_spec.split('==')[0]
        try:
            __import__(package_name)
            print(f"✅ {package_name}")
        except ImportError:
            missing_packages.append(package_spec)
            print(f"❌ {package_name}")
    
    # 安装缺失的依赖
    if missing_packages:
        print(f"\n❌ 缺少 {len(missing_packages)} 个依赖库")
        
        try:
            import pip
            print("正在安装缺失的依赖...")
            
            for package in missing_packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ 已安装: {package}")
            
            print("\n✅ 所有依赖已安装完成!")
            
        except Exception as e:
            print(f"❌ 安装依赖失败: {e}")
            print("\n💡 请手动安装依赖:")
            print("pip install -r requirements.txt")
            return False
    
    print("\n✅ 环境检查完成!")
    return True

def run_streamlit():
    """运行Streamlit应用"""
    print("\n🌐 启动Web应用...")
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    dashboard_file = current_dir / "ui" / "dashboard.py"
    
    if not dashboard_file.exists():
        print(f"❌ 找不到仪表板文件: {dashboard_file}")
        return False
    
    print("💡 请稍等，系统正在启动...")
    print("📡 本地访问地址: http://localhost:8501")
    print("=" * 60)
    print("\n🚀 启动完成后，浏览器将自动打开")
    print("🔄 按 Ctrl+C 停止应用")
    print("=" * 60)
    
    try:
        # 延迟打开浏览器
        def open_browser():
            time.sleep(3)
            webbrowser.open("http://localhost:8501")
        
        # 启动浏览器线程
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # 运行Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(dashboard_file),
            "--server.port", "8501",
            "--server.headless", "false",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false",
            "--browser.serverAddress", "localhost"
        ])
        
        return True
        
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
        return True
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

def run_cli_mode():
    """运行命令行模式（备用）"""
    print("\n📟 命令行模式")
    print("=" * 60)
    
    # 添加项目路径
    project_root = Path(__file__).parent
    sys.path.append(str(project_root))
    
    from core.data_loader import FlightDataLoader
    from core.analyzer import SimpleFlightAnalyzer
    
    data_loader = FlightDataLoader()
    analyzer = SimpleFlightAnalyzer()
    
    current_data = None
    
    while True:
        print("\n请选择操作:")
        print("1. 加载CSV文件")
        print("2. 使用示例数据")
        print("3. 分析数据")
        print("4. 查看数据摘要")
        print("5. 导出数据")
        print("6. 返回主菜单")
        print("7. 退出")
        
        try:
            choice = input("\n请输入选项 (1-7): ").strip()
            
            if choice == '1':
                file_path = input("请输入CSV文件路径: ").strip()
                if Path(file_path).exists():
                    try:
                        current_data = data_loader.load_csv(Path(file_path))
                        print(f"✅ 加载成功: {len(current_data)} 行数据")
                    except Exception as e:
                        print(f"❌ 加载失败: {e}")
                else:
                    print("❌ 文件不存在")
            
            elif choice == '2':
                try:
                    current_data = data_loader.generate_sample_data()
                    print(f"✅ 示例数据生成成功: {len(current_data)} 行数据")
                except Exception as e:
                    print(f"❌ 生成失败: {e}")
            
            elif choice == '3':
                if current_data is None:
                    print("❌ 请先加载数据")
                    continue
                
                try:
                    analysis = analyzer.analyze(current_data)
                    print(f"✅ 分析完成!")
                    print(f"   发现 {len(analysis['anomalies'])} 个异常")
                    
                    if 'flight_summary' in analysis:
                        summary = analysis['flight_summary']
                        if 'duration_minutes' in summary:
                            print(f"   飞行时长: {summary['duration_minutes']:.1f} 分钟")
                        if 'max_altitude' in summary:
                            print(f"   最大高度: {summary['max_altitude']:.0f} ft")
                except Exception as e:
                    print(f"❌ 分析失败: {e}")
            
            elif choice == '4':
                if current_data is None:
                    print("❌ 请先加载数据")
                    continue
                
                try:
                    summary = data_loader.get_data_summary(current_data)
                    print("\n📋 数据摘要:")
                    for category, info in summary.items():
                        print(f"\n{category}:")
                        if isinstance(info, dict):
                            for key, value in info.items():
                                print(f"  {key}: {value}")
                        else:
                            print(f"  {info}")
                except Exception as e:
                    print(f"❌ 获取摘要失败: {e}")
            
            elif choice == '5':
                if current_data is None:
                    print("❌ 请先加载数据")
                    continue
                
                try:
                    from config import config
                    config.init_directories()
                    
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    csv_file = config.OUTPUT_DIR / f"flight_data_{timestamp}.csv"
                    
                    current_data.to_csv(csv_file, index=False)
                    print(f"✅ 数据已导出: {csv_file}")
                except Exception as e:
                    print(f"❌ 导出失败: {e}")
            
            elif choice == '6':
                return True  # 返回主菜单
            
            elif choice == '7':
                print("👋 再见!")
                return False  # 退出程序
            
            else:
                print("❌ 无效选项")
        
        except KeyboardInterrupt:
            print("\n🔙 返回主菜单")
            return True
        except Exception as e:
            print(f"❌ 发生错误: {e}")

def main():
    """主函数"""
    try:
        # 设置环境
        if not setup_environment():
            print("❌ 环境设置失败")
            return
        
        while True:
            
            try:
                choice = input("\n按回车进入系统: ").strip()
                if choice =="test":
                    print("\n请选择运行模式:")
                    print("1. Web界面模式 (推荐)")
                    print("2. 命令行模式")
                    print("3. 退出程序")
                    choice = input("\n请输入选项 (1-3): ").strip()
                    if choice == '1':
                        success = run_streamlit()
                        if not success:
                            print("⚠️  Web模式启动失败")
                            input("按Enter键继续...")
                
                    elif choice == '2':
                        should_continue = run_cli_mode()
                        if not should_continue:
                            break
                
                    elif choice == '3':
                        print("👋 再见!")
                        break
                
                    else:
                        print("❌ 无效选项")
                else:
                    success = run_streamlit()
                    if not success:
                        print("⚠️  Web模式启动失败")
                        input("按Enter键继续...")
            except KeyboardInterrupt:
                print("\n👋 程序已停止")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")
    
    except Exception as e:
        print(f"❌ 程序运行错误: {e}")
        print("\n💡 建议:")
        print("1. 检查Python版本 (需要3.9+)")
        print("2. 确保依赖库已安装")
        print("3. 查看错误详情")

if __name__ == "__main__":
    main()
