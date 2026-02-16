"""
Vercel Serverless Function Entrypoint
"""
import sys
import os

# プロジェクトルートと現在のディレクトリをパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, current_dir)

try:
    # Flaskアプリをインポート
    from app import app
    print("Successfully imported app")
except ImportError as e:
    print(f"Error importing app: {e}")
    # 依存関係の確認用ログ
    import pkg_resources
    installed_packages = [d.project_name for d in pkg_resources.working_set]
    print(f"Installed packages: {installed_packages}")
    raise e

# Vercelは自動的に 'app' 変数を探し、WSGIアプリケーションとして扱います。
# 独自の handler 関数は不要であり、場合によってはVercelのランタイムエラーを引き起こす可能性があります。
app = app
