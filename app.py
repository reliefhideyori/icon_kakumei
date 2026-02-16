"""
Slide Icon Generator - Flask API Server
"""
import os
import base64
import time
from io import BytesIO
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

from styles import STYLES, COMMON_CONSTRAINTS

# ==========================================
# 設定
# ==========================================
API_KEY = os.environ.get("GOOGLE_API_KEY")
client = None
if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    print("⚠️ GOOGLE_API_KEY環境変数が設定されていません。画面表示は可能ですが、画像生成は利用できません。")

# モデル設定
IMAGE_MODEL = "gemini-2.0-flash-exp-image-generation"  # 画像生成用（無料利用可能）

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
        if not client:
            return jsonify({"error": "GOOGLE_API_KEYが設定されていません。.envファイルにAPIキーを設定してください。"}), 503

        data = request.get_json()
        motif = data.get("motif", "").strip()
        style_id = data.get("style", "comic")
        
        if not motif:
            return jsonify({"error": "モチーフを入力してください"}), 400
        
        if style_id not in STYLES:
            return jsonify({"error": "無効なスタイルです"}), 400
        
        # Step 1: プロンプト構築（共通制約を追加）
        # 以前は翻訳ステップがありましたが、レート制限対策のため削除し、
        # 日本語(または任意の言語)の入力をそのまま使用します。Geminiは多言語対応しています。
        style = STYLES[style_id]
        style_prompt = style["prompt_template"].format(motif=motif)
        final_prompt = style_prompt + COMMON_CONSTRAINTS
        print(f"🎨 プロンプト構築完了: {final_prompt[:50]}...")
        
        # Step 2: 画像生成（リトライ付き）
        max_retries = 2
        retry_delay = 15  # 秒
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                print(f"🚀 {IMAGE_MODEL} で画像生成中... (試行 {attempt + 1}/{max_retries + 1})")
                response = client.models.generate_content(
                    model=IMAGE_MODEL,
                    contents=final_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE", "TEXT"]
                    )
                )
                
                # レスポンスから画像パートを探す
                image_data = None
                if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                            image_data = part.inline_data.data
                            break
                
                if image_data:
                    break  # 成功
                else:
                    last_error = "画像データが含まれていませんでした"
                    print(f"⚠️ 画像データなし（試行 {attempt + 1}）")
                    
            except Exception as e:
                last_error = str(e)
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    if attempt < max_retries:
                        print(f"⏳ レート制限のため {retry_delay}秒後にリトライします...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        return jsonify({"error": "APIのレート制限に達しました。1分ほど待ってから再度お試しください。"}), 429
                else:
                    raise
        
        if not image_data:
            return jsonify({"error": f"画像が生成されませんでした。別の言葉をお試しください。({last_error})"}), 500
        
        # 画像をBase64エンコード
        image = Image.open(BytesIO(image_data))
        
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        print(f"✅ 生成完了!")
        
        return jsonify({
            "success": True,
            "image": f"data:image/png;base64,{img_base64}",
            "motif": motif,
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
