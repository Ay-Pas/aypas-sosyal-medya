import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = 'araclar/logo.jpg'
F = '/usr/share/fonts/truetype/google-fonts/'
def font(w, s): return ImageFont.truetype(F + f'Poppins-{w}.ttf', s)

BLUE = (15, 70, 126)
NAVY = (8, 30, 60)
RED = (227, 10, 23)
W, H = 1080, 1350

# --- logo as alpha mask (bg 247 -> 0, blue -> 255), cropped
src = Image.open(SRC).convert('L')
mask = src.point(lambda v: max(0, min(255, int((247 - v) / (247 - 70) * 255))))
mask = mask.crop(mask.getbbox())

def logo(color, width):
    m = mask.resize((width, int(mask.height * width / mask.width)), Image.LANCZOS)
    img = Image.new('RGBA', m.size, color + (0,))
    img.putalpha(m)
    return img

def ctext(d, y, txt, f, fill, spacing=0):
    w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=fill)

def footer(img, color, line_color):
    d = ImageDraw.Draw(img)
    d.line([(W/2 - 60, 1150), (W/2 + 60, 1150)], fill=line_color, width=2)
    lg = logo(color, 230)
    img.alpha_composite(lg, ((W - lg.width)//2, 1175))

def crescent_star(d, cx, cy, r, fill, bg):
    # Turkish flag proportions (relative to outer crescent radius r)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill)
    ri = r * 0.8; ox = cx + r * 0.25 * 2
    ox = cx + r * 0.5 * (1/1)*0.5 + r*0.0
    ox = cx + r * 0.25
    d.ellipse([ox-ri, cy-ri, ox+ri, cy+ri], fill=bg)
    # star
    sx = cx + r * 0.25 + ri + r * 0.0 - r*0.05 + r*0.3333*0.5
    sx = ox + ri - r*0.05 + r*0.25
    sr = r * 0.5
    pts = []
    for i in range(10):
        a = math.pi/2 * 0 + i * math.pi/5 - math.pi/2 + math.pi/2*0
        rr = sr if i % 2 == 0 else sr * 0.382
        ang = math.radians(180) + i * math.pi / 5  # one point to the left (toward crescent)
        pts.append((sx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)

# ===== 1) 29 Ekim
def ekim29():
    img = Image.new('RGBA', (W, H), RED + (255,))
    d = ImageDraw.Draw(img)
    # subtle big "103"
    crescent_star(d, 485, 300, 120, (255,255,255), RED)
    ctext(d, 500, '29 EKİM 1923', font('Medium', 34), (255,255,255))
    ctext(d, 560, 'Cumhuriyetimizin', font('Light', 64), (255,255,255))
    ctext(d, 640, '103. Yılı Kutlu Olsun', font('Bold', 76), (255,255,255))
    d.line([(W/2-40, 770), (W/2+40, 770)], fill=(255,255,255), width=3)
    ctext(d, 800, 'Happy 103rd Anniversary', font('Medium', 40), (255,235,235))
    ctext(d, 852, 'of the Republic of Türkiye', font('Light', 40), (255,235,235))
    # white footer band
    d.rectangle([0, 1100, W, H], fill=(255,255,255))
    lg = logo(BLUE, 210)
    img.alpha_composite(lg, ((W - lg.width)//2, 1100 + (250 - lg.height)//2))
    return img

# ===== 2) 10 Kasım
def kasim10():
    img = Image.new('RGBA', (W, H), (14, 14, 16, 255))
    d = ImageDraw.Draw(img)
    ctext(d, 250, '09:05', font('Light', 150), (235,235,235))
    d.line([(W/2-50, 470), (W/2+50, 470)], fill=(200,200,200), width=2)
    ctext(d, 510, '10 KASIM 1938', font('Medium', 36), (180,180,180))
    ctext(d, 580, 'Cumhuriyetimizin kurucusu', font('Light', 44), (235,235,235))
    ctext(d, 640, 'Gazi Mustafa Kemal Atatürk\'ü', font('Bold', 52), (255,255,255))
    ctext(d, 710, 'saygı, minnet ve özlemle anıyoruz.', font('Light', 44), (235,235,235))
    ctext(d, 840, 'In loving memory of Mustafa Kemal Atatürk,', font('Light', 32), (160,160,160))
    ctext(d, 884, 'founder of the Republic of Türkiye.', font('Light', 32), (160,160,160))
    d.line([(W/2-60, 1080), (W/2+60, 1080)], fill=(90,90,90), width=2)
    lg = logo((255,255,255), 200)
    img.alpha_composite(lg, ((W - lg.width)//2, 1120))
    return img

# ===== 3) 24 Kasım
def kasim24():
    img = Image.new('RGBA', (W, H), (247, 247, 247, 255))
    d = ImageDraw.Draw(img)
    # chalkboard-ish blue block
    d.rounded_rectangle([90, 150, W-90, 960], radius=36, fill=BLUE)
    d.rounded_rectangle([110, 170, W-110, 940], radius=26, outline=(255,255,255,), width=2)
    # simple pencil icon
    px, py = W/2, 290
    d.polygon([(px-110, py+18), (px+70, py+18), (px+110, py), (px+70, py-18), (px-110, py-18)], fill=(255,196,0))
    d.polygon([(px+70, py+18), (px+110, py), (px+70, py-18)], fill=(240,214,170))
    d.polygon([(px+98, py+6), (px+110, py), (px+98, py-6)], fill=(40,40,40))
    d.rectangle([px-130, py-18, px-110, py+18], fill=(230,120,140))
    ctext(d, 380, '24 KASIM', font('Medium', 38), (190,215,240))
    ctext(d, 440, 'Öğretmenler Günü', font('Bold', 82), (255,255,255))
    ctext(d, 545, 'Kutlu Olsun', font('Light', 64), (255,255,255))
    ctext(d, 680, 'Bilgiyle geleceği inşa eden', font('Light', 36), (225,235,245))
    ctext(d, 728, 'tüm öğretmenlerimize teşekkürler.', font('Light', 36), (225,235,245))
    ctext(d, 830, 'Happy Teachers\' Day', font('Medium', 38), (190,215,240))
    lg = logo(BLUE, 220)
    img.alpha_composite(lg, ((W - lg.width)//2, 1060))
    return img

# ===== 4) Yılbaşı
def yilbasi():
    img = Image.new('RGBA', (W, H), NAVY + (255,))
    # vertical gradient
    g = Image.new('RGBA', (W, H))
    gd = ImageDraw.Draw(g)
    for y in range(H):
        t = y / H
        c = tuple(int(a + (b - a) * t) for a, b in zip((20, 72, 130), (6, 22, 48)))
        gd.line([(0, y), (W, y)], fill=c + (255,))
    img = g
    d = ImageDraw.Draw(img)
    random.seed(7)
    snow = Image.new('RGBA', (W, H), (0,0,0,0)); sd = ImageDraw.Draw(snow)
    for _ in range(140):
        x, y, r = random.randint(0, W), random.randint(0, 1100), random.choice([2,2,3,4,5])
        sd.ellipse([x-r, y-r, x+r, y+r], fill=(255,255,255, random.randint(70,200)))
    img.alpha_composite(snow.filter(ImageFilter.GaussianBlur(0.8)))
    # snowflake glyph
    cx, cy, R = W/2, 270, 95
    for k in range(6):
        a = k * math.pi / 3
        x2, y2 = cx + R*math.cos(a), cy + R*math.sin(a)
        d.line([(cx, cy), (x2, y2)], fill=(255,255,255), width=6)
        for f_ in (0.55, 0.8):
            bx, by = cx + R*f_*math.cos(a), cy + R*f_*math.sin(a)
            for s in (-1, 1):
                b = a + s * math.pi/4
                d.line([(bx, by), (bx + 26*math.cos(b), by + 26*math.sin(b))], fill=(255,255,255), width=5)
    ctext(d, 410, '2027', font('Bold', 210), (255,255,255))
    ctext(d, 660, 'Mutlu Yıllar', font('Light', 76), (255,255,255))
    ctext(d, 760, 'Happy New Year', font('Medium', 44), (175,205,240))
    ctext(d, 880, 'Yeni yılda da soğuk zincirin güvenilir ortağı.', font('Light', 32), (200,215,235))
    ctext(d, 922, 'Your trusted partner in the cold chain.', font('Light', 32), (150,175,210))
    d.line([(W/2-60, 1080), (W/2+60, 1080)], fill=(120,150,190), width=2)
    lg = logo((255,255,255), 200)
    img.alpha_composite(lg, ((W - lg.width)//2, 1120))
    return img

for name, fn in [('01_29ekim', ekim29), ('02_10kasim', kasim10), ('03_24kasim', kasim24), ('04_yilbasi', yilbasi)]:
    fn().convert('RGB').save(f'2026/{name}.jpg', quality=93)
print('ok', mask.size)
