# 文件: fix_environment.py
"""
环境修复脚本 - 解决NumPy版本冲突问题
"""

import sys
import subprocess
import importlib

def check_and_fix_numpy():
    """检查并修复NumPy版本"""
    print("🔍 检查NumPy版本...")
    
    try:
        import numpy as np
        version = np.__version__
        print(f"当前NumPy版本: {version}")
        
        # 检查是否是2.x版本
        if version.startswith('2.'):
            print("⚠️  检测到NumPy 2.x，与Streamlit 1.12.0不兼容")
            print("正在降级NumPy到1.24.3...")
            
            # 卸载当前NumPy
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "numpy"])
            
            # 安装兼容版本
            subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.24.3"])
            print("✅ NumPy已降级到1.24.3")
            return True
        else:
            print("✅ NumPy版本兼容")
            return True
            
    except ImportError:
        print("❌ NumPy未安装")
        print("正在安装NumPy 1.24.3...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.24.3"])
        return True
    except Exception as e:
        print(f"❌ 检查NumPy失败: {e}")
        return False

def check_and_install_package(package_name, version=None):
    """检查并安装指定包"""
    try:
        importlib.import_module(package_name)
        print(f"✅ {package_name} 已安装")
        return True
    except ImportError:
        print(f"❌ {package_name} 未安装")
        
        install_cmd = [sys.executable, "-m", "pip", "install"]
        if version:
            install_cmd.append(f"{package_name}=={version}")
        else:
            install_cmd.append(package_name)
        
        try:
            subprocess.check_call(install_cmd)
            print(f"✅ {package_name} 安装成功")
            return True
        except Exception as e:
            print(f"❌ 安装 {package_name} 失败: {e}")
            return False

def main():
    """主修复函数"""
    print("=" * 60)
    print("🛠️  飞行数据可视化系统 - 环境修复工具")
    print("=" * 60)
    
    # 修复顺序很重要
    required_packages = [
        ('numpy', '1.24.3'),      # 必须先修复NumPy
        ('chardet', '5.1.0'),     # 然后安装chardet
        ('streamlit', '1.12.0'),  # 最后确保Streamlit
        ('pandas', '1.5.3'),
        ('plotly', '5.9.0'),
        ('geopy', '2.3.0'),
        ('scipy', '1.10.1'),
        ('pyarrow', '12.0.1')
    ]
    
    print("📦 开始修复依赖...")
    
    # 首先修复NumPy
    if not check_and_fix_numpy():
        print("❌ NumPy修复失败，请手动处理")
        return
    
    # 安装其他依赖
    all_success = True
    for package, version in required_packages[1:]:  # 跳过已经处理的NumPy
        if not check_and_install_package(package, version):
            all_success = False
    
    if all_success:
        print("\n✅ 环境修复完成！")
        print("\n现在可以运行系统:")
        print("1. 运行主程序: python main.py")
        print("2. 选择选项1 (Web界面模式)")
        print("3. 浏览器将自动打开 http://localhost:8501")
    else:
        print("\n⚠️  部分依赖安装失败，请手动安装:")
        print("pip install -r requirements_fixed.txt")
    
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 操作取消")
    except Exception as e:
        print(f"❌ 修复过程出错: {e}")