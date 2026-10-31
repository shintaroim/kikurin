"""
Refined Image Generation Suite for Kikurin's Official Website.
Produces 7 studio-quality assets with clean backgrounds and professional typography.
"""

import os
from collections import deque
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

IMG_DIR = r"C:\AI Workspace\1_Projects\きくりん\image"
SRC_FACE = os.path.join(IMG_DIR, "2026-10-31_08-36.png")
SRC_BODY = os.path.join(IMG_DIR, "スクリーンショット 2026-10-18 151209.png")

def make_avatars():
    """Generates 600x600 square avatar and circular transparent avatar."""
    im = Image.open(SRC_FACE).convert("RGB")
    # Face crop region centered on Kikurin
    crop = im.crop((180, 50, 560, 430))
    w, h = crop.size
    pixels = crop.load()

    # Clean top-left background (remove faint blue text stroke)
    for y in range(h):
        for x in range(w // 3):
            r, g, b = pixels[x, y]
            if x < 75 and y < 140:
                pixels[x, y] = (255, 255, 255)

    # Web image enhancements
    crop = ImageEnhance.Color(crop).enhance(1.05)
    crop = ImageEnhance.Contrast(crop).enhance(1.03)
    crop = ImageEnhance.Sharpness(crop).enhance(1.12)

    # 1. kikurin_avatar_square.png (600x600)
    square_avatar = crop.resize((600, 600), Image.Resampling.LANCZOS)
    square_path = os.path.join(IMG_DIR, "kikurin_avatar_square.png")
    square_avatar.save(square_path, "PNG", quality=95)
    print("Saved:", square_path)

    # 2. kikurin_avatar_circle.png (600x600 transparent)
    circle_avatar = square_avatar.convert("RGBA")
    mask = Image.new("L", (600, 600), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((8, 8, 592, 592), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    circle_avatar.putalpha(mask)

    # Border in warm amber brand color
    border_img = Image.new("RGBA", (600, 600), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(border_img)
    bdraw.ellipse((8, 8, 592, 592), outline=(217, 119, 6, 240), width=6)
    circle_avatar = Image.alpha_composite(circle_avatar, border_img)

    circle_path = os.path.join(IMG_DIR, "kikurin_avatar_circle.png")
    circle_avatar.save(circle_path, "PNG")
    print("Saved:", circle_path)

    # 3. kikurin_bust_transparent.png (600x750 transparent)
    # Bust crop with shoulders and chest
    bust_crop = im.crop((165, 45, 575, 540))
    bw, bh = bust_crop.size
    bp = bust_crop.load()
    for y in range(bh):
        for x in range(bw // 3):
            if x < 85 and y < 150:
                bp[x, y] = (255, 255, 255)

    bust_crop = ImageEnhance.Color(bust_crop).enhance(1.05)
    bust_crop = ImageEnhance.Contrast(bust_crop).enhance(1.03)
    bust_crop = ImageEnhance.Sharpness(bust_crop).enhance(1.12)
    bust_scaled = bust_crop.resize((600, 750), Image.Resampling.LANCZOS).convert("RGBA")

    # Create flood-fill transparency mask
    sw, sh = bust_scaled.size
    sp = bust_scaled.load()
    t_mask = Image.new("L", (sw, sh), 255)
    visited = [[False]*sh for _ in range(sw)]
    q = deque([(0, 0), (sw-1, 0), (0, 300), (sw-1, 300)])
    for sx, sy in q:
        visited[sx][sy] = True

    while q:
        cx, cy = q.popleft()
        r, g, b, _ = sp[cx, cy]
        if r > 240 and g > 240 and b > 240:
            t_mask.putpixel((cx, cy), 0)
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < sw and 0 <= ny < sh and not visited[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny))

    t_mask = t_mask.filter(ImageFilter.GaussianBlur(1.2))
    bust_scaled.putalpha(t_mask)
    bust_path = os.path.join(IMG_DIR, "kikurin_bust_transparent.png")
    bust_scaled.save(bust_path, "PNG")
    print("Saved:", bust_path)

def extract_upperbody():
    """Extracts Kikurin's clean upper body with transparent background."""
    im = Image.open(SRC_BODY).convert("RGBA")
    # Exact bounding crop: x: 622 to 945, y: 120 to 512
    crop = im.crop((622, 120, 945, 512))
    w, h = crop.size
    pixels = crop.load()

    # Left boundary profile to eliminate any watermark text
    edge_profile = {
        0: 154, 40: 154, 60: 146, 80: 145, 100: 145, 120: 144,
        140: 151, 160: 166, 180: 174, 200: 128, 220: 106, 240: 97,
        260: 86, 280: 73, 300: 49, 320: 31, 340: 13, 360: 10, 396: 0
    }

    def get_left_boundary(y):
        keys = sorted(edge_profile.keys())
        for i in range(len(keys)-1):
            if keys[i] <= y <= keys[i+1]:
                ratio = (y - keys[i]) / (keys[i+1] - keys[i])
                return int(edge_profile[keys[i]] * (1 - ratio) + edge_profile[keys[i+1]] * ratio)
        return 0

    mask = Image.new("L", (w, h), 255)
    visited = [[False]*h for _ in range(w)]
    q = deque()

    for x in range(w):
        q.append((x, 0))
        visited[x][0] = True
    for y in range(h):
        if y < h - 40:
            q.append((0, y))
            visited[0][y] = True
            q.append((w - 1, y))
            visited[w - 1][y] = True

    while q:
        cx, cy = q.popleft()
        r, g, b, _ = pixels[cx, cy]
        left_bound = get_left_boundary(cy)

        is_bg = (cx < left_bound - 2) or (r > 218 and g > 218 and b > 218)
        if is_bg:
            mask.putpixel((cx, cy), 0)
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny))

    mask_soft = mask.filter(ImageFilter.GaussianBlur(1.0))
    result = crop.copy()
    result.putalpha(mask_soft)
    return result

def make_cards_and_banner(transparent_person):
    """Generates Hero card, Profile card, Upperbody cutout, and OGP banner."""
    pw, ph = transparent_person.size

    # 4. kikurin_upperbody_transparent.png (800x1000)
    trans_canvas = Image.new("RGBA", (800, 1000), (0, 0, 0, 0))
    scale = 2.45
    scaled_w, scaled_h = int(pw * scale), int(ph * scale)
    scaled_person = transparent_person.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
    pos_x = (800 - scaled_w) // 2 + 10
    pos_y = 1000 - scaled_h
    trans_canvas.paste(scaled_person, (pos_x, pos_y), scaled_person)

    trans_path = os.path.join(IMG_DIR, "kikurin_upperbody_transparent.png")
    trans_canvas.save(trans_path, "PNG")
    print("Saved:", trans_path)

    # 5. kikurin_hero_card.png (800x1000) - Clean elegant studio look
    # Background: clean subtle warm ivory studio
    bg_hero = Image.new("RGB", (800, 1000), (252, 250, 247))
    h_draw = ImageDraw.Draw(bg_hero)
    for y in range(1000):
        ratio = y / 1000.0
        r = int(255 * (1 - ratio) + 248 * ratio)
        g = int(253 * (1 - ratio) + 245 * ratio)
        b = int(250 * (1 - ratio) + 238 * ratio)
        h_draw.line([(0, y), (800, y)], fill=(r, g, b))

    # Paste scaled person
    bg_hero.paste(scaled_person, (pos_x, pos_y), scaled_person)
    bg_hero = ImageEnhance.Color(bg_hero).enhance(1.05)
    bg_hero = ImageEnhance.Contrast(bg_hero).enhance(1.03)

    hero_path = os.path.join(IMG_DIR, "kikurin_hero_card.png")
    bg_hero.save(hero_path, "PNG", quality=95)
    print("Saved:", hero_path)

    # 6. kikurin_profile_portrait.png (800x1000) - Warm neutral paper tone
    bg_profile = Image.new("RGB", (800, 1000), (250, 248, 245))
    p_draw = ImageDraw.Draw(bg_profile)
    for y in range(1000):
        ratio = y / 1000.0
        r = int(252 * (1 - ratio) + 245 * ratio)
        g = int(250 * (1 - ratio) + 242 * ratio)
        b = int(246 * (1 - ratio) + 235 * ratio)
        p_draw.line([(0, y), (800, y)], fill=(r, g, b))

    bg_profile.paste(scaled_person, (pos_x, pos_y), scaled_person)
    bg_profile = ImageEnhance.Color(bg_profile).enhance(1.04)
    bg_profile = ImageEnhance.Contrast(bg_profile).enhance(1.02)

    profile_path = os.path.join(IMG_DIR, "kikurin_profile_portrait.png")
    bg_profile.save(profile_path, "PNG", quality=95)
    print("Saved:", profile_path)

    # 7. kikurin_ogp_banner.png (1200x630)
    banner = Image.new("RGB", (1200, 630), (252, 250, 247))
    b_draw = ImageDraw.Draw(banner)

    # Warm gradient
    for x in range(1200):
        ratio = x / 1200.0
        r = int(248 * (1 - ratio) + 255 * ratio)
        g = int(245 * (1 - ratio) + 253 * ratio)
        b = int(240 * (1 - ratio) + 250 * ratio)
        b_draw.line([(x, 0), (x, 630)], fill=(r, g, b))

    # Amber brand top line
    b_draw.rectangle([(0, 0), (1200, 8)], fill=(217, 119, 6))

    # Kikurin person on right side
    b_scale = 1.62
    bw, bh = int(pw * b_scale), int(ph * b_scale)
    b_person = transparent_person.resize((bw, bh), Image.Resampling.LANCZOS)
    banner.paste(b_person, (1200 - bw - 30, 630 - bh), b_person)

    # Fonts
    font_mincho = ImageFont.truetype("C:/Windows/Fonts/yumin.ttf", 44)
    font_mincho_sm = ImageFont.truetype("C:/Windows/Fonts/yumin.ttf", 36)
    font_gothic_bold = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
    font_gothic_text = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 19)
    font_badge = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 16)

    # Pill badge
    b_draw.rounded_rectangle([(70, 65), (420, 105)], radius=20, fill=(254, 243, 199), outline=(245, 158, 11), width=1)
    b_draw.text((92, 74), "ライフ＆キャリアシェルパ 公式サイト", fill=(180, 83, 9), font=font_badge)

    # Catchphrase in Yu Mincho
    b_draw.text((70, 135), "五感をととのえ、心をひらく。", fill=(41, 37, 36), font=font_mincho)
    b_draw.text((70, 198), "答えはすべて、あなたの中にある。", fill=(41, 37, 36), font=font_mincho)

    # Name
    b_draw.text((70, 290), "菊池 伸哉", fill=(28, 25, 23), font=font_mincho_sm)
    b_draw.text((250, 302), "（きくりん）", fill=(217, 119, 6), font=font_gothic_bold)

    # Horizontal divider
    b_draw.line([(70, 355), (620, 355)], fill=(214, 211, 209), width=2)

    # Qualifications & Role
    b_draw.text((70, 380), "国家資格 キャリアコンサルタント / 産業カウンセラー", fill=(87, 83, 78), font=font_gothic_text)
    b_draw.text((70, 418), "元蕎麦職人 × 「在り方をととのえる」深層対話伴走", fill=(87, 83, 78), font=font_gothic_text)

    # URL Button
    b_draw.rounded_rectangle([(70, 480), (370, 532)], radius=12, fill=(41, 37, 36))
    b_draw.text((100, 492), "🌐  lifesherpasin.com", fill=(255, 255, 255), font=font_gothic_bold)

    ogp_path = os.path.join(IMG_DIR, "kikurin_ogp_banner.png")
    banner.save(ogp_path, "PNG", quality=95)
    print("Saved:", ogp_path)

if __name__ == "__main__":
    print("Executing updated image generator...")
    make_avatars()
    tp = extract_upperbody()
    make_cards_and_banner(tp)
    print("All refreshed assets ready!")
