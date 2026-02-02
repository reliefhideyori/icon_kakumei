# スタイル定義 - プロンプトテンプレート
# 既存のprompt_アメコミ.txt, prompt_モダン.txt を参考に再現性を最大化

# ==========================================
# 共通制約 - すべてのスタイルに適用
# ==========================================
COMMON_CONSTRAINTS = """

=== CRITICAL CONSTRAINTS (STRICTLY ENFORCED) ===
- ABSOLUTELY NO frames, borders, or rounded rectangle containers around the icon.
- ABSOLUTELY NO app icon styling (no rounded squares, no iOS/Android app icon frames).
- ABSOLUTELY NO shadow, drop shadow, or glow effects.
- ABSOLUTELY NO decorative borders or edge elements.
- The object must float freely on pure white background with NO enclosing shape.
- Output must be suitable for direct placement on presentation slides without cropping.
- The icon edges must blend seamlessly into any background."""

STYLES = {
    "comic": {
        "name": "アメコミ (Comic Pop)",
        "description": "派手、原色、ドット絵（ハーフトーン）、太いアウトライン",
        "image": "images/アメコミ.png",
        "prompt_template": """Generate a flat, vector-style icon of a {english_motif}.
Style: Vintage American Pop Art / Retro Comic Book Style (resembling Roy Lichtenstein).
View: Front view, centered on a white background.

Key Visual Elements:
- Outlines: EXTREMELY bold, thick, uniform black outlines defining all shapes. No sketch lines.
- Colors: Strictly limited palette of Cyan, Magenta, Yellow, Red, Black, and Flesh tone.
- Texture: Visible, coarse Ben-Day dots (halftone pattern) on colored areas to simulate vintage printing.
- Shading: Flat shading only. No gradients.
- Composition: The object is completely isolated in the center.
- Background: Pure solid white (#FFFFFF) negative space.

Negative Constraints (Strictly Forbidden):
- NO background elements (ABSOLUTELY NO sunbursts, NO speed lines, NO explosion effects, NO comic panels).
- NO text, speech bubbles, words, or typography.
- NO 3D rendering, realistic textures, or photo-realism.
- NO frames or borders around the edges."""
    },
    "outline": {
        "name": "モダン (Minimal Outline)",
        "description": "シンプル、線画、Apple SF Symbols風",
        "image": "images/モダン.png",
        "prompt_template": """Generate a minimalist line icon of a {english_motif}.
Style: Modern UI Icon / Outline Style (like Apple SF Symbols).
View: Front view, centered on a white background.

Key Visual Elements:
- Lines: Uniform, medium-weight black strokes (#000000).
- Shape: Geometric, clean, and simplified. Rounded corners/caps for a friendly look.
- Fill: No fill (transparent/white).
- Background: Pure solid white (#FFFFFF).
- Composition: The object is isolated in the center. Square aspect ratio.

Negative constraints:
- Do not include text, shadows, or colors.
- Do not use sketch styles or rough lines.
- Do not use complex details."""
    },
    "clay3d": {
        "name": "3Dねんど (Plasticine Clay)",
        "description": "立体的、やわらかい質感、Play-Doh風",
        "image": "images/3Dねんど.png",
        "prompt_template": """Generate a 3D Plasticine Claymation Icon of a {english_motif}.
Style: Stylized 3D Clay Art, Soft Render, Playful.
View: Frontal, Centered, Eye-level.

Key Visual Elements:
- Outlines: No outlines; shapes defined by soft, rounded volume and contact shadows.
- Colors: Saturated, solid "Play-Doh" colors (e.g., Golden Brown, Leafy Green, bright Red, Cheese Yellow). Matte finish.
- Lighting/Shading: Soft, diffuse top-down studio lighting. Gentle gradients, no harsh specular highlights.
- Texture/Surface: Smooth modeling clay texture; slight organic imperfections in shape (hand-sculpted feel) but smooth surface.
- Composition: Isolated subject, centered, icon-style framing.
- Background: Solid white (#FFFFFF).

Negative Constraints (Strictly Forbidden):
- NO outlines, NO sharp edges, NO hyper-realism, NO metallic surfaces, NO complex noise, NO flat 2D vector style."""
    },
    "yurufuwa": {
        "name": "ゆるふわ (Loose Crayon)",
        "description": "手描き風、クレヨン、ゆるい線画、へたうま",
        "image": "images/ゆるふわ.png",
        "prompt_template": """Generate a [Loose Hand-Drawn Crayon/Marker Illustration] of a {english_motif}.
Style: Japanese "Heta-uma" (clumsy-cute) aesthetic, Scribble art, Child-like drawing style, Minimalist Doodle.
View: Front-on, Isolated, Centered.

Key Visual Elements:
- Outlines: Thick, dark brown (#594A3F), rugged, textured strokes. Lines are uneven, wobbly, and occasionally broken or dashed, resembling a worn felt-tip pen or crayon.
- Colors: Soft, warm, desaturated pastels. Pale cream, muted beige, soft grey-blue. Low contrast.
- Lighting/Shading: Flat 2D application. No realistic shadows. "Shading" is represented by crude, loose scribbles or patches of darker color within the shapes (e.g. rough stippling).
- Texture/Surface: Textured brush appearance (crayon or dry marker) on a smooth surface. Imperfect fill.
- Background: Solid, very pale dusty pink/cream (#F8F0EC).

Negative Constraints (Strictly Forbidden):
- NO 3D effects, NO gradients, NO glossy finishes, NO sharp vector lines, NO high saturation, NO realistic lighting, NO complex details, NO fine lines."""
    },
    "business": {
        "name": "ビジネス (Corporate Duotone)",
        "description": "フラット、企業向けピクトグラム、紺×シアン2色",
        "image": "images/ビジネス.png",
        "prompt_template": """Generate a Corporate Duotone Vector Icon of a {english_motif}.
Style: Flat Business Iconography, Glyph Style.
View: Frontal, 2D, Graphic Design.

Key Visual Elements:
- Outlines: Combination of solid silhouette fills and uniform thick lines with rounded ends.
- Colors: Strict Duotone: Deep Navy Blue (#003366) for primary elements, Vibrant Cyan (#3399CC) for accents.
- Lighting/Shading: None. Completely flat color application.
- Texture/Surface: Digital vector smoothness, sharp geometric shapes.
- Composition: Minimalist pictogram, symbolic representation, high contrast.
- Background: Solid white (#FFFFFF).

Negative Constraints (Strictly Forbidden):
- NO gradients, NO drop shadows, NO 3D rendering, NO photorealism, NO texture, NO complex details."""
    }
}

# 翻訳用のシステムプロンプト
TRANSLATION_INSTRUCTION = """You are a visual translator.
Convert the user's Japanese input into a concise, visual English noun or phrase suitable for icon generation.
Output ONLY the English translation, nothing else.
Examples:
- "ロケット" -> "rocket"
- "握手" -> "handshake"
- "アイデア" -> "light bulb representing idea"
- "チームワーク" -> "team of people working together"
"""
