#!/usr/bin/env python3
"""
测试文件上传功能
"""

import requests
import json
from PIL import Image
import io
import os

def test_upload():
    """测试文件上传"""
    
    # 1. 登录获取token
    login_data = {'username': 'admin', 'password': '123456'}
    login_response = requests.post('http://localhost:8000/api/auth/login', json=login_data)
    
    if login_response.status_code != 200:
        print(f"登录失败: {login_response.text}")
        return
        
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # 2. 创建一个测试图片
    img = Image.new('RGB', (300, 200), color='red')
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='JPEG')
    img_buffer.seek(0)
    
    # 3. 准备上传数据
    files = {
        'file': ('test_image.jpg', img_buffer, 'image/jpeg')
    }
    data = {
        'activity_id': '1',  # 使用第一个活动
        'title': '测试图片',
        'description': '这是一个测试上传的图片'
    }
    
    # 4. 上传文件
    upload_response = requests.post(
        'http://localhost:8000/api/media/upload',
        headers=headers,
        files=files,
        data=data
    )
    
    if upload_response.status_code == 200:
        result = upload_response.json()
        print("✅ 文件上传成功!")
        print(f"文件ID: {result['id']}")
        print(f"文件路径: {result['file_path']}")
        print(f"完整URL: http://localhost:8000/uploads/{result['file_path']}")
        
        # 5. 测试访问上传的文件
        file_url = f"http://localhost:8000/uploads/{result['file_path']}"
        file_response = requests.get(file_url)
        
        if file_response.status_code == 200:
            print("✅ 文件可以正常访问!")
        else:
            print(f"❌ 文件访问失败: {file_response.status_code}")
            
    else:
        print(f"❌ 文件上传失败: {upload_response.status_code}")
        print(f"错误信息: {upload_response.text}")

if __name__ == "__main__":
    test_upload()
