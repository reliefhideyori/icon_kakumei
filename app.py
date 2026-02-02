"""
Slide Icon Generator - Flask API Server
"""
import os
import base64
from io import BytesIO
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

from styles import STYLES, TRANSLATION_INSTRUCTION, COMMON_CONSTRAINTS

# ==========================================
# 設定
# ==========================================
API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY環境変数が設定されていません")
client = genai.Client(api_key=API_KEY)

# モデル設定
TEXT_MODEL = "gemini-2.0-flash"  # 翻訳用（安定版）
IMAGE_MODEL = "imagen-4.0-generate-001"  # 画像生成用

app = Flask(__name__)

# ==========================================
# ルート
# ==========================================

@app.route("/")
def index():
    """メインページを表示"""
    return render_template("index.html", styles=STYLES)


@app.route("/generate", methods=["POST"])
def generate():
    """アイコンを生成するAPIエンドポイント"""
    try:
        data = request.get_json()
        motif = data.get("motif", "").strip()
        style_id = data.get("style", "comic")
        
        if not motif:
            return jsonify({"error": "モチーフを入力してください"}), 400
        
        if style_id not in STYLES:
            return jsonify({"error": "無効なスタイルです"}), 400
        
        # Step 1: 日本語 → 英語翻訳
        print(f"🔍 翻訳中: '{motif}'")
        try:
            translation_response = client.models.generate_content(
                model=TEXT_MODEL,
                contents=f"{TRANSLATION_INSTRUCTION}\n\nInput: {motif}"
            )
            english_motif = translation_response.text.strip()
            print(f"✨ 翻訳完了: {english_motif}")
        except Exception as e:
            print(f"⚠️ 翻訳エラー（フォールバック）: {e}")
            english_motif = motif  # フォールバック
        
        # Step 2: プロンプト構築（共通制約を追加）
        style = STYLES[style_id]
        style_prompt = style["prompt_template"].format(english_motif=english_motif)
        final_prompt = style_prompt + COMMON_CONSTRAINTS
        print(f"🎨 プロンプト構築完了（共通制約適用）")
        
        # Step 3: 画像生成
        print(f"🚀 {IMAGE_MODEL} で画像生成中...")
        response = client.models.generate_images(
            model=IMAGE_MODEL,
            prompt=final_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/png"
            )
        )
        
        if not response.generated_images:
            return jsonify({"error": "画像が生成されませんでした。別の言葉をお試しください。"}), 500
        
        # 画像をBase64エンコード
        gen_img = response.generated_images[0]
        image = Image.open(BytesIO(gen_img.image.image_bytes))
        
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        print(f"✅ 生成完了!")
        
        return jsonify({
            "success": True,
            "image": f"data:image/png;base64,{img_base64}",
            "motif": motif,
            "english_motif": english_motif,
            "style": style["name"]
        })
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return jsonify({"error": str(e)}), 500


# ==========================================
# 起動
# ==========================================
if __name__ == "__main__":
    print("🎨 Slide Icon Generator 起動中...")
    print("📍 http://localhost:5000 でアクセス")
    app.run(debug=True, port=5000)
