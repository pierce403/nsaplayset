"""Regenerate the checked-in social card with Pillow, DejaVu and URW fonts.

Optional artwork tool; not needed for site builds. Run from any directory.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SCALE = 2
INK = '#34352f'
GREEN = '#51692c'
MUTED = '#66685e'
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
canvas = Image.new('RGB', (1200 * SCALE, 630 * SCALE), 'white')
draw = ImageDraw.Draw(canvas)


def text(position, value, font, size, color=INK):
    draw.text(tuple(v * SCALE for v in position), value,
              font=ImageFont.truetype(str(FONT_DIR / font), size * SCALE),
              fill=color)


def line(points, color, width=1):
    draw.line(tuple(v * SCALE for v in points), fill=color, width=width * SCALE)


logo = Image.open(ROOT / 'static/images/archive/nsa-playset-logo.png').convert('RGBA')
logo = logo.resize((340 * SCALE, 62 * SCALE), Image.Resampling.LANCZOS)
canvas.paste(logo, (64 * SCALE, 48 * SCALE), logo)
text((64, 148), 'SECURITY RESEARCH. OPEN TO EVERYONE.',
     'DejaVuSansMono.ttf', 15, GREEN)
text((60, 196), 'Now you can', 'DejaVuSerif.ttf', 66)
text((60, 275), 'play along!', '/usr/share/fonts/opentype/urw-base35/P052-Italic.otf', 78)
line((64, 364, 514, 364), '#898b7a')
text((64, 400), 'An open catalog of security research', 'DejaVuSans.ttf', 22, MUTED)
text((64, 434), 'hardware and software.', 'DejaVuSans.ttf', 22, MUTED)

# Place the original illustration intact; no generated replacement or retouching.
kid = Image.open(ROOT / 'static/images/archive/hackrf-kid.png').convert('RGBA')
kid = kid.resize((630 * SCALE, 630 * SCALE), Image.Resampling.LANCZOS)
canvas.paste(kid, (570 * SCALE, -8 * SCALE), kid)
line((64, 542, 1136, 542), '#d4d3c9')
text((64, 568), 'nsaplayset.org', 'DejaVuSansMono.ttf', 20)
text((800, 572), 'HARDWARE / SOFTWARE / RESEARCH', 'DejaVuSansMono.ttf', 13, MUTED)
canvas.resize((1200, 630), Image.Resampling.LANCZOS).save(
    ROOT / 'static/images/og-preview.png', optimize=True)
