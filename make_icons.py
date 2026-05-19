# 生成喝水时间 PWA 图标：蓝底白水滴
from PIL import Image, ImageDraw
import os, math

OUT = os.path.join(os.path.dirname(__file__), "www", "icons")
os.makedirs(OUT, exist_ok=True)

BLUE_TOP = (92, 198, 247)    # #5cc6f7
BLUE_BOT = (21, 146, 207)    # #1592cf

def vgrad(size, top, bot):
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        t = y / (size - 1)
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        for x in range(size):
            px[x, y] = (r, g, b)
    return img

def draw_drop(size, scale=1.0):
    """蓝底 + 白色水滴；scale<1 给可遮罩图标留安全边距"""
    SS = size * 4  # 超采样抗锯齿
    img = vgrad(SS, BLUE_TOP, BLUE_BOT).convert("RGBA")
    d = ImageDraw.Draw(img)
    cx = SS / 2
    s = SS * scale
    top_y = SS * 0.5 - s * 0.40   # 水滴尖
    cyc = SS * 0.5 + s * 0.16     # 底圆圆心
    r = s * 0.30                  # 底圆半径
    # 底部圆
    d.ellipse([cx - r, cyc - r, cx + r, cyc + r], fill=(255, 255, 255, 255))
    # 顶部尖：三角形覆盖圆上半，平滑连成水滴
    d.polygon([(cx, top_y), (cx + r, cyc), (cx - r, cyc)],
              fill=(255, 255, 255, 255))
    # 高光
    hr = r * 0.42
    d.ellipse([cx - r * 0.45 - hr, cyc - r * 0.25 - hr,
               cx - r * 0.45 + hr, cyc - r * 0.25 + hr],
              fill=(255, 255, 255, 70))
    return img.resize((size, size), Image.LANCZOS)

# 标准图标（全幅）
for sz in (192, 512):
    draw_drop(sz, 1.0).save(os.path.join(OUT, f"icon-{sz}.png"))

# 可遮罩图标（留安全区，约 78% 内容）
draw_drop(512, 0.62).save(os.path.join(OUT, "icon-512-maskable.png"))

# iOS 主屏图标 180（iOS 会自动圆角，做满幅）
draw_drop(180, 1.0).save(os.path.join(OUT, "apple-touch-icon.png"))

print("icons written to", OUT)
print(os.listdir(OUT))
