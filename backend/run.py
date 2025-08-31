#!/usr/bin/env python3
"""
班级建设网站后端启动脚本
"""

import uvicorn
import os
from app.main import app

if __name__ == "__main__":
    # 获取端口号，Railway会设置PORT环境变量
    port = int(os.environ.get("PORT", 8000))
    
    # 检测运行环境
    is_production = os.environ.get("ENVIRONMENT") == "production"
    
    uvicorn.run(
        "app.main:app" if is_production else app,
        host="0.0.0.0",
        port=port,
        reload=not is_production,
        log_level="info"
    )
