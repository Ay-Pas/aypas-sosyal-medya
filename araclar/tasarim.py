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

SS = 3  # süper örnekleme (yumuşak çizgiler)

def anitkabir(renk=(255, 255, 255), alfa=70, x0=96, x1=984, ust=1040, alt=1135):
    """Anıtkabir Şeref Holü — önden ince çizgi silueti (alt şeritte, ufuk çizgisi gibi)."""
    def ciz():
        k = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        d = ImageDraw.Draw(k)
        c = renk + (alfa,)
        s = lambda v: int(v * SS)
        lw = s(1.6)
        cx = (x0 + x1) / 2
        gen = (x1 - x0) * 0.62           # hol genişliği
        hl, hr = cx - gen / 2, cx + gen / 2
        h = alt - ust
        # zemin çizgisi (tam genişlik)
        d.line([(s(x0), s(alt)), (s(x1), s(alt))], fill=c, width=lw)
        # merdiven: 5 basamak, yukarı doğru daralan
        bas = h * 0.20
        for i in range(5):
            yy = alt - bas * (i + 1) / 5
            pad = gen * 0.10 * (1 - (i + 1) / 5) + gen * 0.02
            d.line([(s(hl - pad), s(yy)), (s(hr + pad), s(yy))], fill=c, width=lw)
        kaide = alt - bas
        # sütunlar (ön cephe: 8 kare sütun)
        tepe = ust + h * 0.26
        n = 8
        sg = gen * 0.028
        for i in range(n):
            xx = hl + gen * 0.04 + (gen * 0.92 - sg) * i / (n - 1)
            d.rectangle([s(xx), s(tepe), s(xx + sg), s(kaide)], outline=c, width=lw)
        # saçaklık / attik
        d.rectangle([s(hl - gen * 0.015), s(ust), s(hr + gen * 0.015), s(tepe)], outline=c, width=lw)
        d.line([(s(hl - gen * 0.015), s(ust + h * 0.09)), (s(hr + gen * 0.015), s(ust + h * 0.09))], fill=c, width=lw)
        # yan revaklar (alçak, iki yana uzanan)
        rv = ust + h * 0.55
        for a, b in [(x0 + 20, hl - gen * 0.06), (hr + gen * 0.06, x1 - 20)]:
            d.line([(s(a), s(rv)), (s(b), s(rv))], fill=c, width=lw)
            for j in range(9):
                xx = a + (b - a) * j / 8
                d.line([(s(xx), s(rv)), (s(xx), s(alt))], fill=c, width=lw)
        return k.resize((W, H), Image.LANCZOS)
    return ciz

def dalgali_bayrak(zemin, alfa=26, x0=330, y0=560, gen=900, yuk=600, genlik=34):
    """Soluk, dalgalanan Türk bayrağı (beyaz yarı saydam alan, ay-yıldız oyuk)."""
    def ciz():
        k = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
        d = ImageDraw.Draw(k)
        s = lambda v: v * SS
        def dy(x):
            t = (x - x0) / gen
            return genlik * math.sin(2 * math.pi * t * 1.3 + 0.6) * (0.25 + t)
        ust = [(s(x), s(y0 + dy(x))) for x in range(int(x0), int(x0 + gen) + 1, 6)]
        alt = [(s(x), s(y0 + yuk + dy(x))) for x in range(int(x0 + gen), int(x0) - 1, -6)]
        d.polygon(ust + alt, fill=(255, 255, 255, alfa))
        # ay-yıldız (bayrak oranları; G = bayrak yüksekliği)
        G = yuk
        cx = x0 + G * 0.5
        cy = y0 + G / 2 + dy(cx)
        r1, r2, kay = G * 0.25, G * 0.20, G * 0.0625
        bos = (0, 0, 0, 0)
        d.ellipse([s(cx - r1), s(cy - r1), s(cx + r1), s(cy + r1)], fill=bos)
        d.ellipse([s(cx + kay - r2), s(cy - r2), s(cx + kay + r2), s(cy + r2)], fill=(255, 255, 255, alfa))
        sr = G * 0.125
        sx = cx + kay + r2 + sr * 0.9
        sy = y0 + G / 2 + dy(sx)
        pts = []
        for i in range(10):
            rr = sr if i % 2 == 0 else sr * 0.382
            a = math.pi + i * math.pi / 5
            pts.append((s(sx + rr * math.cos(a)), s(sy + rr * math.sin(a))))
        d.polygon(pts, fill=bos)
        return k.resize((W, H), Image.LANCZOS)
    return ciz

def kart(dosya, zemin, ust_etiket, baslik, aciklama, ingilizce,
         yazi=BEYAZ, soluk=None, logo_renk=BEYAZ, filigran=None, sembol=None,
         alt_zemin=None, alt_yazi=None, alt_logo=None, gorsel=None):
    soluk = soluk or tuple(int(c * 0.62 + z * 0.38) for c, z in zip(yazi, zemin))
    img = Image.new('RGBA', (W, H), zemin + (255,))
    d = ImageDraw.Draw(img)

    # sembolik çizim katmanı (Anıtkabir, bayrak vb.) — metnin arkasında
    if gorsel:
        kat = gorsel()
        kat_d = ImageDraw.Draw(kat)
        kat_d.rectangle([0, 1140, W, H], fill=(0, 0, 0, 0))
        img.alpha_composite(kat)
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
         gorsel=dalgali_bayrak(KIRMIZI, alfa=38, x0=500, y0=150, gen=680, yuk=230, genlik=32),
         alt_zemin=BEYAZ, alt_yazi=(90, 90, 90), alt_logo=MAVI)
    kart(os.path.join(klasor, '02_10kasim.jpg'), SIYAH,
         '10 Kasım 1938  ·  09:05',
         ['Saygı, minnet', 've özlemle.'],
         ['Cumhuriyetimizin kurucusu Gazi Mustafa', 'Kemal Atatürk\'ü saygıyla anıyoruz.'],
         ['In respectful memory of Mustafa Kemal', 'Atatürk, founder of the Republic of Türkiye.'],
         yazi=(236, 236, 236),
         gorsel=anitkabir(renk=(236, 236, 236), alfa=95, ust=935, alt=1125))
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
