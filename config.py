# 文件1: config.py - 配置管理（兼容1.12.0）
"""
飞行可视化系统 - 配置文件
Streamlit 1.12.0 兼容版本
"""

import os
from pathlib import Path
import json

class Config:
    """系统配置"""
    
    # 项目路径
    PROJECT_ROOT = Path(__file__).parent
    DATA_DIR = PROJECT_ROOT / "data"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    ASSETS_DIR = PROJECT_ROOT / "assets"
    CACHE_DIR = PROJECT_ROOT / ".cache"
    
    # 默认设置
    DEFAULT_SAMPLE_RATE = 1
    MAX_DATA_POINTS = 10000
    CACHE_SIZE = 100  # 缓存大小（MB）
    
    # 图表设置 - 兼容 Plotly 5.9.0
    CHART_THEME = "plotly"
    CHART_WIDTH = 1000
    CHART_HEIGHT = 500
    
    # 颜色方案
    COLOR_SCHEME = {
        'altitude': '#3498db',
        'airspeed': '#2ecc71',
        'engine': '#e74c3c',
        'trajectory': '#9b59b6',
        'warning': '#f39c12',
        'normal': '#7f8c8d',
        'takeoff': '#e67e22',
        'cruise': '#3498db',
        'landing': '#2ecc71'
    }
    
    # Streamlit 1.12.0 配置
    STREAMLIT_CONFIG = {
        'server.maxUploadSize': 200,  # MB
        'server.enableCORS': False,
        'server.enableXsrfProtection': False,
        'theme.base': 'light'
    }
    
    # 初始化目录
    @staticmethod
    def init_directories():
        """初始化所需目录"""
        directories = [
            Config.DATA_DIR,
            Config.OUTPUT_DIR,
            Config.ASSETS_DIR,
            Config.CACHE_DIR
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
        
        return True

# 初始化配置
config = Config()
