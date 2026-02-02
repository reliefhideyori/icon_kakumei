import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# ==========================================
# 1. あなたの環境専用の設定
# ==========================================
API_KEY = "AIzaSyDL6b8SL3mRjw9_sWwZcxHLVhoYdxZhEU0" # ← 書き換えてください
client = genai.Client(api_key=API_KEY)

# リストから判明した最強のモデルたち
TEXT_MODEL = "nano-banana-pro-preview"  # リストに実在！
IMAGE_MODEL = "imagen-4.0-generate-001" # 次世代モデル

def generate_nanobanana_icon(user_input: str):
    print(f"🚀 NanobananaPro (Experimental Edition) 起動")
    print(f"🎯 モチーフ: '{user_input}'")

    # --- Step 1: プロンプト拡張 (nano-banana-pro-preview 使用) ---
    print(f"🔍 {TEXT_MODEL} が思考中...")
    try:
        instruction = """
        You are NanobananaPro.
        Refine the user input into a complex, high-detail visual prompt for an icon.
        - Describe materials, lighting, and textures (e.g., iridescent metal, frosted glass).
        - Output ONLY the English description.
        """
        response = client.models.generate_content(
            model=TEXT_MODEL,
            contents=f"{instruction}\n\nUser Input: {user_input}"
        )
        detailed_motif = response.text.strip()
        print(f"✨ 拡張完了: {detailed_motif}")
    except Exception as e:
        print(f"⚠️ 拡張エラー（フォールバック）: {e}")
        detailed_motif = user_input

    # --- Step 2: 画像生成 (imagen-4.0-generate-001 使用) ---
    # ここにあなたの「Comic Pop」スタイルを統合
    final_prompt = (
        f"Generate a professional vector icon of {detailed_motif}. "
        "Style: Modern Neo-Comic Art, bold black outlines, vibrant pop-art colors, "
        "subtle halftone dots. Pure white background (#FFFFFF). High contrast, centered."
    )

    print(f"🎨 {IMAGE_MODEL} で画像生成中...")
    try:
        response = client.models.generate_images(
            model=IMAGE_MODEL,
            prompt=final_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/png"
            )
        )
        
        if response.generated_images:
            gen_img = response.generated_images[0]
            # PILで画像を開く
            image = Image.open(BytesIO(gen_img.image.image_bytes))
            
            # 保存
            filename = f"icon_{user_input.replace(' ', '_')}_v4.png"
            image.save(filename)
            print(f"✅ 完了！ファイルを保存しました: {filename}")
            # image.show() # Windowsで自動で画像を開く
        else:
            print("❌ 画像が生成されませんでした。")

    except Exception as e:
        print(f"❌ 画像生成エラー:\n{e}")

# ==========================================
# 実行
# ==========================================
if __name__ == "__main__":
    # ここに作りたいモチーフを入れてください
    generate_nanobanana_icon("Mechanical Owl")