"""
Vercel Serverless Function Entrypoint
"""
import sys
import os

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Flaskアプリをインポート
from app import app

# Vercel用のハンドラー
def handler(request, response):
    return app(request, response)

# Vercel Python runtime用
app = app
