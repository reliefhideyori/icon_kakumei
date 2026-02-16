from rembg import remove
from PIL import Image
import os
import glob

# 設定
INPUT_DIR = r"C:\Users\hide0\OneDrive\デスクトップ\★AI\★Antigravity\Webアプリ_アイコン生成\ヒーローページ"
OUTPUT_DIR = r"C:\Users\hide0\OneDrive\デスクトップ\★AI\★Antigravity\Webアプリ_アイコン生成\static\images\hero"

# 出力ディレクトリ作成
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 画像処理
image_files = glob.glob(os.path.join(INPUT_DIR, "*.png"))
print(f"発見した画像ファイル数: {len(image_files)}")

for img_path in image_files:
    try:
        filename = os.path.basename(img_path)
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        print(f"処理中: {filename}...")
        
        input_image = Image.open(img_path)
        output_image = remove(input_image)
        output_image.save(output_path)
        
        print(f"完了: {output_path}")
    except Exception as e:
        print(f"エラー ({filename}): {e}")

print("すべての処理が完了しました。")
