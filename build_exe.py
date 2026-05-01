# 文件7: build_exe.py - 打包脚本（PyInstaller）
"""
自动打包脚本 - 生成可执行文件
针对 Streamlit 1.12.0 优化
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否安装"""
    try:
        import PyInstaller
        print("✅ PyInstaller 已安装")
        return True
    except ImportError:
        print("❌ PyInstaller 未安装")
        print("正在安装 PyInstaller...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller 安装完成")
            return True
        except Exception as e:
            print(f"❌ 安装失败: {e}")
            return False

def create_spec_file():
    """创建PyInstaller spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# PyInstaller配置
a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        ('config.py', '.'),
        ('requirements.txt', '.'),
        ('core', 'core'),
        ('ui', 'ui'),
        ('data', 'data'),
        ('output', 'output'),
        ('assets', 'assets')
    ],
    hiddenimports=[
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'plotly.graph_objs',
        'plotly.express',
        'geopy',
        'geopy.distance',
        'scipy',
        'scipy.stats',
        'chardet',
        'typing_extensions'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

# 打包选项
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FlightVisualizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)

# 如果需要单文件，取消注释下面这行
# exe = COLLECT(...)
'''
    
    with open("FlightVisualizer.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("✅ Spec文件创建完成")
    return True

def cleanup():
    """清理构建文件"""
    print("🧹 清理构建文件...")
    
    dirs_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['FlightVisualizer.spec']
    
    for dir_name in dirs_to_remove:
        dir_path = Path(dir_name)
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"  删除目录: {dir_name}")
            except Exception as e:
                print(f"  删除目录失败 {dir_name}: {e}")
    
    for file_name in files_to_remove:
        file_path = Path(file_name)
        if file_path.exists():
            try:
                os.remove(file_path)
                print(f"  删除文件: {file_name}")
            except Exception as e:
                print(f"  删除文件失败 {file_name}: {e}")
    
    print("✅ 清理完成")

def build_exe():
    """构建可执行文件"""
    print("🔨 开始构建可执行文件...")
    
    try:
        # 使用PyInstaller打包
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--name=FlightVisualizer",
            "--onefile",
            "--console",
            "--add-data", "config.py;.",
            "--add-data", "requirements.txt;.",
            "--add-data", "core;core",
            "--add-data", "ui;ui",
            "--add-data", "data;data",
            "--add-data", "output;output",
            "--add-data", "assets;assets",
            "--hidden-import=streamlit",
            "--hidden-import=pandas",
            "--hidden-import=numpy",
            "--hidden-import=plotly",
            "--hidden-import=plotly.graph_objs",
            "--hidden-import=plotly.express",
            "--hidden-import=geopy",
            "--hidden-import=geopy.distance",
            "--hidden-import=chardet",
            "--clean",
            "main.py"
        ], check=True, capture_output=True, text=True)
        
        print("✅ 构建成功!")
        
        # 显示输出文件信息
        exe_path = Path("dist") / "FlightVisualizer.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n📦 输出文件: {exe_path}")
            print(f"📏 文件大小: {size_mb:.1f} MB")
            
            # 创建启动脚本
            create_launcher_bat()
            
            return True
        else:
            print("❌ 输出文件不存在")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def create_launcher_bat():
    """创建Windows启动批处理文件"""
    bat_content = '''@echo off
echo ========================================
echo     飞行数据可视化系统
echo ========================================
echo.

REM 检查可执行文件是否存在
if not exist "FlightVisualizer.exe" (
    echo 错误: 找不到 FlightVisualizer.exe
    echo 请确保该文件在当前目录
    pause
    exit /b 1
)

echo 正在启动飞行数据可视化系统...
echo.
echo 请等待程序加载...
echo.
echo 注意:
echo 1. 首次启动可能需要一些时间
echo 2. 程序将在浏览器中打开
echo 3. 按 Ctrl+C 可停止程序
echo.

REM 启动程序
FlightVisualizer.exe

pause
'''
    
    with open("启动飞行可视化系统.bat", "w", encoding="gbk") as f:
        f.write(bat_content)
    
    print("✅ 启动脚本创建完成: 启动飞行可视化系统.bat")

def main():
    """主打包函数"""
    print("=" * 60)
    print("🚀 飞行数据可视化系统 - 打包工具")
    print("=" * 60)
    
    # 检查当前目录
    if not Path("main.py").exists():
        print("❌ 错误: 请在项目根目录运行此脚本")
        print("   当前目录: ", Path.cwd())
        return
    
    print("请选择操作:")
    print("1. 清理构建文件")
    print("2. 构建可执行文件")
    print("3. 创建启动脚本")
    print("4. 一键打包 (清理 + 构建 + 启动脚本)")
    print("5. 退出")
    
    try:
        choice = input("\n请输入选项 (1-5): ").strip()
        
        if choice == "1":
            cleanup()
        
        elif choice == "2":
            if check_pyinstaller():
                build_exe()
        
        elif choice == "3":
            create_launcher_bat()
        
        elif choice == "4":
            print("\n🚀 开始一键打包...")
            cleanup()
            if check_pyinstaller():
                if build_exe():
                    print("\n🎉 打包完成!")
                    print("💡 可执行文件位于 'dist' 目录")
                    print("💡 双击 '启动飞行可视化系统.bat' 运行程序")
        
        elif choice == "5":
            print("👋 再见!")
        
        else:
            print("❌ 无效选项")
    
    except KeyboardInterrupt:
        print("\n👋 操作取消")
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main()