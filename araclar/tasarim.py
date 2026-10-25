"""Ay-Pas kurumsal özel gün şablonu (1080x1350, Instagram dikey).

Kullanım:  python3 araclar/tasarim.py            -> 2026 görsellerini üretir
Yeni gün eklemek için: kart(...) çağrısı yaz, aynı ızgara ve tipografiyi koru.

Tasarım sistemi
- Izgara: 96 px kenar boşluğu, sola hizalı metin.
- Üst: küçük harf aralıklı "üst etiket" (tarih / gün adı) + ince çizgi.
- Orta: büyük başlık (Inter Display SemiBold), altında Türkçe açıklama (Inter Light).
- Alt orta: İngilizce satır(lar), daha soluk renk.
- Alt: tam genişlik ince çizgi, solda logo, sağda ay-pas.com / @aypasrefrigeration.
- Süs yok; en fazla bir sembol (ör. ay-yıldız) ve büyük, çok soluk bir sayı/yıl.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

KOK = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(KOK, 'fonts')
LOGO = os.path.join(KOK, 'logo.jpg')

W, H, M = 1080, 1350, 96
MAVI = (15, 70, 126)
LACIVERT = (10, 32, 64)
KIRMIZI = (200, 16, 46)
SIYAH = (18, 18, 20)
BEYAZ = (255, 255, 255)

def f(ad, s):
    return ImageFont.truetype(os.path.join(FONT, ad + '.otf'), s)

# --- logo: açık zemin -> alfa maskesi
_src = Image.open(LOGO).convert('L')
_mask = _src.point(lambda v: max(0, min(255, int((247 - v) / (247 - 70) * 255))))
_mask = _mask.crop(_mask.getbbox())

def logo(renk, yukseklik):
    gen = int(_mask.width * yukseklik / _mask.height)
    m = _mask.resize((gen, yukseklik), Image.LANCZOS)
    img = Image.new('RGBA', m.size, renk + (0,))
    img.putalpha(m)
    return img

def izli(d, xy, metin, font, renk, aralik=0.0):
    """Harf aralıklı metin (tracking)."""
    x, y = xy
    for ch in metin:
        d.text((x, y), ch, font=font, fill=renk)
        x += d.textlength(ch, font=font) + font.size * aralik

def ay_yildiz(d, cx, cy, r, renk, zemin):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=renk)
    ri, ox = r * 0.8, cx + r * 0.25
    d.ellipse([ox - ri, cy - ri, ox + ri, cy + ri], fill=zemin)
    sx, sr = ox + ri * 0.62, r * 0.5
    pts = []
    for i in range(10):
        rr = sr if i % 2 == 0 else sr * 0.382
        a = math.pi + i * math.pi / 5
        pts.append((sx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=renk)

def kart(dosya, zemin, ust_etiket, baslik, aciklama, ingilizce,
         yazi=BEYAZ, soluk=None, logo_renk=BEYAZ, filigran=None, sembol=None,
         alt_zemin=None, alt_yazi=None, alt_logo=None):
    soluk = soluk or tuple(int(c * 0.62 + z * 0.38) for c, z in zip(yazi, zemin))
    img = Image.new('RGBA', (W, H), zemin + (255,))
    d = ImageDraw.Draw(img)

    # çok soluk büyük sayı (filigran)
    if filigran:
        kat = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        kd = ImageDraw.Draw(kat)
        ff = f('InterDisplay-Bold', 560)
        tw = kd.textlength(filigran, font=ff)
        kd.text((W - tw + 30, 640), filigran, font=ff, fill=yazi + (14,))
        kd.rectangle([0, 1140, W, H], fill=(0, 0, 0, 0))  # alt banda taşmasın
        img.alpha_composite(kat)
        d = ImageDraw.Draw(img)

    # üst etiket + çizgi
    izli(d, (M, M + 4), ust_etiket.upper(), f('Inter-Medium', 24), yazi, 0.18)
    d.line([(M, M + 56), (M + 72, M + 56)], fill=yazi, width=3)

    y = 430
    if sembol:
        sembol(d, M + 70, 330)
    # başlık
    fb = f('InterDisplay-SemiBold', 84)
    for satir in baslik:
        d.text((M, y), satir, font=fb, fill=yazi)
        y += 100
    y += 28
    fa = f('Inter-Light', 34)
    for satir in aciklama:
        d.text((M, y), satir, font=fa, fill=yazi)
        y += 48
    y += 40
    fe = f('Inter-Regular', 28)
    for satir in ingilizce:
        d.text((M, y), satir, font=fe, fill=soluk)
        y += 42

    # alt bant
    ab = 1160
    if alt_zemin:
        d.rectangle([0, ab, W, H], fill=alt_zemin)
        ay, ly, lr = alt_yazi, alt_logo, alt_yazi
    else:
        d.line([(M, ab), (W - M, ab)], fill=soluk, width=1)
        ay, ly, lr = soluk, logo_renk, soluk
    lg = logo(ly, 120)
    img.alpha_composite(lg, (M, ab + (H - ab - lg.height) // 2))
    d = ImageDraw.Draw(img)
    fs = f('Inter-Regular', 24)
    for i, t in enumerate(['ay-pas.com', '@aypasrefrigeration']):
        tw = d.textlength(t, font=fs)
        d.text((W - M - tw, ab + 62 + i * 38), t, font=fs, fill=ay)

    img.convert('RGB').save(dosya, quality=94)

def uret_2026(klasor):
    os.makedirs(klasor, exist_ok=True)
    kart(os.path.join(klasor, '01_29ekim.jpg'), KIRMIZI,
         '29 Ekim 1923 – 2026',
         ['Cumhuriyetimizin', '103. yılı kutlu olsun.'],
         ['Cumhuriyetimizin kuruluş yıldönümünü', 'gururla kutluyoruz.'],
         ['Happy 103rd Anniversary of the', 'Republic of Türkiye.'],
         filigran='103',
         sembol=lambda d, x, y: ay_yildiz(d, x, y, 62, BEYAZ, KIRMIZI),
         alt_zemin=BEYAZ, alt_yazi=(90, 90, 90), alt_logo=MAVI)
    kart(os.path.join(klasor, '02_10kasim.jpg'), SIYAH,
         '10 Kasım 1938  ·  09:05',
         ['Saygı, minnet', 've özlemle.'],
         ['Cumhuriyetimizin kurucusu Gazi Mustafa', 'Kemal Atatürk\'ü saygıyla anıyoruz.'],
         ['In respectful memory of Mustafa Kemal', 'Atatürk, founder of the Republic of Türkiye.'],
         yazi=(236, 236, 236))
    kart(os.path.join(klasor, '03_24kasim.jpg'), MAVI,
         '24 Kasım  ·  Öğretmenler Günü',
         ['Öğretmenler Günü', 'kutlu olsun.'],
         ['Bilgiyle geleceği inşa eden tüm', 'öğretmenlerimize teşekkür ederiz.'],
         ['Happy Teachers\' Day to everyone who', 'builds the future through knowledge.'])
    kart(os.path.join(klasor, '04_yilbasi.jpg'), LACIVERT,
         '1 Ocak 2027',
         ['Mutlu yıllar.'],
         ['Yeni yılda da iş ortaklarımızın yanında,', 'soğuk zincirin güvenilir çözüm ortağıyız.'],
         ['Happy New Year. Your trusted partner', 'in commercial refrigeration.'],
         filigran='2027')

if __name__ == '__main__':
    uret_2026(os.path.join(os.path.dirname(KOK), '2026'))
