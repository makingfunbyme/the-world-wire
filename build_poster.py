"""Draw the World Wire front page from the supplied editorial copy."""

from math import cos, radians, sin, sqrt
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

SIZE = 1024
LEFT, RIGHT = 26, 998
WIDTH = RIGHT - LEFT
PAPER = (247, 244, 237)
INK = (20, 18, 16)
RED = (176, 22, 24)
GRAY = (104, 99, 92)
BODY_INK = (82, 78, 72)
LIGHT = (196, 190, 181)
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
FONTS = {}
MEASURE = ImageDraw.Draw(Image.new("L", (1, 1)))

DEK = (
    "Trump, Xi and Putin sit at one table in Shenzhen — the first three-way summit of the world's "
    "three largest nuclear powers; arms control tops an agenda none of them has agreed to."
)
STATS = (
    ("$115.8B", "NVIDIA Q3"), ("$81.3B", "ANTHROPIC IPO"),
    ("15.9M", "GTA VI ORDERS"), ("200,000", "FLEE AKVAN"),
    ("730,000", "ICJ CASE"), ("19", "SIBERIA CRASH"),
)
PAGE_NUMBERS = (
    ("3 leaders", "Shenzhen"), ("48 hrs", "COP31 left"),
    ("$1.5B", "GTA VI pre-orders"), ("11 districts", "on red alert"),
    ("$87B", "India renewables"), ("6 deaths", "Java bridge collapse"),
)
STORIES = (
    ("SHENZHEN", "Three leaders, one table",
     "Trump presses nuclear arms control; Xi calls for open trade; Putin arrives with Ukraine unresolved. "
     "Most of the agenda is unresolved before it begins."),
    ("THE HAGUE", "ICJ rules on the Rohingya",
     "The World Court delivers its genocide judgment against Myanmar seven years after 730,000 fled. "
     "No state has been found to have committed genocide before."),
    ("THE GULF", "Iran widens the war",
     "Strikes hit air bases in Kuwait and Bahrain; a gas tanker burns in the Strait of Hormuz; "
     "US aircraft hit Qeshm island. Oil markets open jittery."),
    ("SAN FRANCISCO", "Nvidia: a $115.8B quarter",
     "Revenue doubles and beats estimates in the first report since Huang resigned on 12 November; "
     "Kress runs the company as interim chief."),
    ("NEW YORK", "Anthropic's record IPO",
     "The largest listing on record raises $81.3B at $83 a share and trades to a near $1.5T valuation. "
     "The first-day pop is now the story."),
    ("NEW YORK", "GTA VI lands, 13 years on",
     "15.9M pre-orders worth $1.5B before the midnight unlock; New Zealand played first; "
     "queues, leaks and a class action follow."),
    ("ODISHA", "Cyclone Akvan nears",
     "200,000 evacuated along India's east coast before Friday landfall; red alerts in 11 districts; "
     "schools and ports shut."),
    ("ANTALYA", "COP31's last 48 hours",
     "Ministers take over the text; the $120B adaptation finance line and a fossil-fuel phase-out remain open."),
    ("KYIV", "Ukraine hits refineries",
     "Ukraine says it struck storage tanks at Russia's Ilsky refinery and a processing unit at Afipsky."),
    ("SIBERIA", "19 dead in a crash",
     "A Russian military transport aircraft goes down in the east; the cause is under investigation."),
    ("WASHINGTON", "A flaw in Java",
     "US, British, German, South Korean and Chinese authorities urge a patch for remote code execution "
     "in Java's memory functions."),
    ("DHAKA", "Arson before Hasina",
     "A spate of attacks is linked to the former prime minister's proposed return; hundreds of arrests reported."),
    ("CARACAS", "Washington's thaw",
     "Military ties restored, with training and intelligence sharing agreed between the US and "
     "Venezuela's interim government."),
    ("JERUSALEM", "Knesset defies Netanyahu",
     "The parliament elects a Gadi Eisenkot ally as speaker — a blow to the prime minister's coalition arithmetic."),
    ("BEIJING", "A gene-trial death",
     "China sacks a scientist after a six-year-old dies in a gene-editing trial, reviving the He Jiankui question."),
    ("NAIROBI", "Kenya's third term",
     "A court weighs a constitutional change; protests build as the government presses its case."),
    ("MELBOURNE", "Allies pull out of a Qatari fund",
     "Australia and the Netherlands withdraw from a Qatar-backed fund after revelations about a former prime minister."),
    ("FRANKFURT", "Deutsche Bank raided",
     "A search targets an Epi-pent-linked deal. The FT reports $82M in payments."),
    ("BANGALORE", "India's renewables pledge",
     "Prime Minister Modi commits $87B to renewables in India by 2030."),
    ("WASHINGTON", "Senators warn on AI",
     "A bipartisan group warns that AI cyber threats are outpacing defences."),
    ("SYDNEY", "Bonds in a dead heat",
     "England and Australia draw in the women's rugby tournament opener."),
    ("DOHA", "Japan-China defence talks",
     "Taki and Japan's defence minister meet Chinese counterparts for a 2x2 dialogue."),
    ("TOKYO", "A soft-power farewell",
     "Japan's popular defence minister steps down, shifting the cabinet's centre of gravity."),
    ("JAKARTA", "A bridge collapses",
     "Six die when a bridge on Java gives way days after a cement plant flood."),
    ("CANBERRA", "Sanctions on settlers",
     "Australia sanctions three people and four groups over West Bank settlements."),
    ("GAMBIA", "A genocide case shifts",
     "Ministers take over the ICJ's Rohingya text after The Gambia brought the 2017 case."),
    ("ABUJA", "Nigeria's flood relief",
     "Twelve die in a landslide as flood relief reaches the state."),
    ("SANTA CLARA", "Chip halts stop",
     "Nvidia's stop for a chip line upends the supply calendar a second time."),
    ("HONG KONG", "US index futures rise",
     "US stock futures climb ahead of Anthropic's Nasdaq debut as global shares trade mixed."),
    ("LOS ANGELES", "Jazz end Lakers' streak",
     "Utah beats Los Angeles 109–97, ending the Lakers' nine-game winning streak."),
)
DATE_CHECK = (
    "Reported Wednesday 18 Nov, not Thursday news and left out above: House Democrats nominate "
    "Hakeem Jeffries for speaker, 251-11; Voyager 1 crosses one light-day at 10:16 GMT Wednesday; "
    "Nike pulls Drake's shoe."
)

# Coastlines are drawn in globe-local coordinates. Eurasia's outline includes India.
LAND = (
    # Africa
    ((-105, -10), (-99, -25), (-89, -30), (-81, -38), (-67, -36), (-53, -29),
     (-39, -27), (-32, -15), (-22, 1), (-11, 4), (-23, 19), (-31, 23),
     (-33, 43), (-47, 68), (-57, 73), (-65, 59), (-70, 39), (-82, 23),
     (-95, 22), (-107, 9)),
    # Europe, Asia and the Indian subcontinent
    ((-106, -45), (-108, -58), (-96, -65), (-101, -72), (-86, -77), (-80, -72),
     (-67, -82), (-58, -99), (-46, -116), (-28, -128), (-10, -137), (26, -129),
     (48, -112), (68, -105), (77, -94), (99, -86), (117, -72), (126, -61),
     (112, -57), (104, -45), (94, -47), (84, -32), (78, -30), (85, -18),
     (75, -6), (66, -2), (59, 10), (60, 23), (54, 19), (47, 4),
     (35, 6), (28, 24), (20, 34), (11, 20), (5, 4), (-5, -7),
     (-13, -5), (-15, 9), (-24, 0), (-34, -16), (-43, -28), (-54, -34),
     (-61, -44), (-70, -39), (-79, -45), (-90, -39), (-97, -48)),
    # Britain, Madagascar, Japan, Indonesia and Australia
    ((-108, -70), (-111, -83), (-103, -89), (-98, -78), (-102, -70)),
    ((-25, 49), (-20, 44), (-21, 60), (-28, 69), (-30, 63)),
    ((93, -25), (100, -38), (104, -39), (101, -27), (94, -19), (88, -19)),
    ((52, 25), (61, 29), (68, 41), (64, 43), (54, 34)),
    ((69, 36), (76, 26), (83, 27), (81, 38), (75, 42)),
    ((70, 45), (85, 46), (94, 50), (84, 51), (72, 49)),
    ((93, 39), (104, 41), (112, 47), (105, 48), (96, 45)),
    ((70, 68), (82, 57), (94, 61), (100, 55), (111, 61), (113, 74),
     (103, 84), (91, 93), (81, 90), (74, 82), (63, 80)),
)


def font(face, size):
    key = (face, size)
    if key not in FONTS:
        FONTS[key] = ImageFont.truetype(str(FONT_DIR / f"DejaVu{face}.ttf"), size)
    return FONTS[key]


def wrap(text, typeface, width):
    lines = []
    line = ""
    for word in text.split():
        candidate = f"{line} {word}" if line else word
        if line and MEASURE.textlength(candidate, font=typeface) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    if any(MEASURE.textlength(part, font=typeface) > width for part in lines):
        raise ValueError(f"A word is wider than its text block: {text}")
    return lines


def block(draw, x, y, text, typeface, width, leading, color, limit=None):
    lines = wrap(text, typeface, width)
    for row, line in enumerate(lines[:limit]):
        draw.text((x, y + row * leading), line, font=typeface, fill=color, anchor="lt")
    return len(lines)


def ellipse(x, y, rx, ry=None):
    ry = rx if ry is None else ry
    return (x - rx, y - ry, x + rx, y + ry)


def header(draw):
    draw.text((LEFT, 16), "THE WORLD WIRE", font=font("Serif-Bold", 54), fill=INK, anchor="lt")
    for y, label in ((27, "No. 119"), (45, "ONE PAGE · ONE DAY")):
        draw.text((RIGHT, y), label, font=font("SansMono", 10), fill=GRAY, anchor="rt")
    draw.text((LEFT, 80), "THURSDAY, 19 NOVEMBER 2026",
              font=font("SansMono-Bold", 11), fill=INK, anchor="lt")
    draw.text((RIGHT, 80), "MIDNIGHT EDITION",
              font=font("SansMono-Bold", 11), fill=RED, anchor="rt")
    draw.line((LEFT, 101, RIGHT, 101), fill=INK, width=3)
    draw.line((LEFT, 107, RIGHT, 107), fill=INK)
    draw.text((LEFT, 121), "THE DAY THE THREE MET",
              font=font("Serif-Bold", 40), fill=INK, anchor="lt")
    if block(draw, LEFT, 161, DEK, font("Serif", 15), WIDTH, 18, INK) != 2:
        raise ValueError("The lead dek must fill two lines")
    draw.rectangle((LEFT, 196, RIGHT, 197), fill=RED)

    draw.rectangle((LEFT, 204, RIGHT, 253), fill=INK)
    for index, (number, caption) in enumerate(STATS):
        x = LEFT + (index + 0.5) * WIDTH / len(STATS)
        if index:
            divider = round(LEFT + index * WIDTH / len(STATS))
            draw.line((divider, 214, divider, 243), fill=GRAY)
        draw.text((x, 212), number, font=font("Serif-Bold", 21), fill=PAPER, anchor="mt")
        draw.text((x, 239), caption, font=font("SansMono", 8), fill=LIGHT, anchor="mt")


def globe(img):
    illustration = Image.new("RGB", (304, 314), PAPER)
    cx, cy, radius = 152, 181, 126
    diameter = 2 * radius + 1
    layer = Image.new("RGBA", (diameter, diameter), PAPER + (255,))
    poles = (0, 0, diameter - 1, diameter - 1)
    grid = ImageDraw.Draw(layer)
    for scale in (0.34, 0.68, 0.95):
        grid.ellipse(ellipse(radius, radius, round(radius * scale), radius), outline=LIGHT)
    for latitude in range(-80, 81, 20):
        offset = radius * sin(radians(latitude))
        half_width = sqrt(radius ** 2 - offset ** 2)
        points = [
            (round(radius + x), round(radius + offset + 11 * (1 - (x / half_width) ** 2)))
            for x in range(-int(half_width), int(half_width) + 1)
        ]
        grid.line(points, fill=LIGHT)

    shorelines = [[(radius + x, radius + y) for x, y in coast] for coast in LAND]
    land_mask = Image.new("L", layer.size)
    land_draw = ImageDraw.Draw(land_mask)
    for coast in shorelines:
        land_draw.polygon(coast, fill=255)
    layer.paste(PAPER + (255,), (0, 0, diameter, diameter), land_mask)

    hatch = Image.new("L", layer.size)
    engraving = ImageDraw.Draw(hatch)
    for x in range(-diameter, diameter, 6):
        engraving.line((x, diameter, x + diameter, 0), fill=255)
    layer.paste(LIGHT + (255,), (0, 0, diameter, diameter), ImageChops.multiply(hatch, land_mask))
    for coast in shorelines:
        grid.line(coast + [coast[0]], fill=INK)

    circular = Image.new("L", layer.size)
    ImageDraw.Draw(circular).ellipse(poles, fill=255)
    illustration.paste(layer, (cx - radius, cy - radius), circular)
    draw = ImageDraw.Draw(illustration)
    draw.ellipse(ellipse(cx, cy, radius + 4), outline=INK)
    draw.ellipse(ellipse(cx, cy, radius), outline=INK, width=2)

    table_y = 37
    beacons = ((19, 121), (75, 120), (100, 137), (121, 163),
               (173, 191), (213, 165), (242, 108), (289, 155))
    for x, y in beacons:
        draw.line((cx, table_y, x, y), fill=RED)
    for number, (x, y) in enumerate(beacons, start=1):
        draw.ellipse(ellipse(x, y, 4), fill=PAPER, outline=RED)
        draw.ellipse(ellipse(x, y, 2), fill=RED)
        draw.text((x + 8, y), str(number), font=font("SansMono-Bold", 9), fill=RED,
                  anchor="lm", stroke_width=1, stroke_fill=PAPER)

    draw.ellipse(ellipse(cx, table_y, 63, 16), fill=PAPER, outline=INK, width=3)
    draw.ellipse(ellipse(cx, table_y, 56, 10), outline=GRAY)
    for angle, label in ((-90, "US"), (30, "CN"), (150, "RU")):
        x = round(cx + 74 * cos(radians(angle)))
        y = round(table_y + 30 * sin(radians(angle)))
        draw.ellipse(ellipse(x, y, 3), fill=INK)
        dx, dy = {"US": (15, 0), "CN": (16, 0), "RU": (-16, 0)}[label]
        draw.text((x + dx, y + dy), label, font=font("SansMono-Bold", 10),
                  fill=RED, anchor="mm")
    illustration = illustration.resize((204, 211), Image.Resampling.LANCZOS)
    img.paste(illustration, ((SIZE - illustration.width) // 2, 255))
    ImageDraw.Draw(img).text(
        (SIZE // 2, 469),
        "SHENZHEN, 8 P.M. — three chairs, one table. Red marks trace the day's other fronts.",
        font=font("SansMono", 9), fill=GRAY, anchor="mt",
    )


def numbers_strip(draw):
    top, bottom = 481, 504
    draw.line((LEFT, top, RIGHT, top), fill=INK)
    draw.line((LEFT, bottom, RIGHT, bottom), fill=INK)
    draw.text((LEFT, top + 9), "THE PAGE IN NUMBERS",
              font=font("SansMono-Bold", 9), fill=INK, anchor="lt")
    facts_left = LEFT + 126
    cell_width = (RIGHT - facts_left) / len(PAGE_NUMBERS)
    for index, (number, label) in enumerate(PAGE_NUMBERS):
        x = round(facts_left + index * cell_width)
        draw.line((x, top + 4, x, bottom - 4), fill=LIGHT)
        center = x + cell_width / 2
        draw.text((center, top + 3), number, font=font("SansMono-Bold", 9), fill=INK, anchor="mt")
        draw.text((center, top + 13), label, font=font("SansMono", 9), fill=INK, anchor="mt")


def story_grid(draw):
    top, bottom = 505, 961
    gutter = 14
    columns = 4
    rows = (len(STORIES) + columns - 1) // columns
    column_width = (WIDTH - (columns - 1) * gutter) / columns
    row_height = (bottom - top) / rows
    headline_font = font("Serif-Bold", 13)
    body_font = font("Sans", 9)
    highlights = {1, 2, 3, 7, 9}
    for column in range(columns):
        x = round(LEFT + column * (column_width + gutter))
        edge = round(LEFT + column * (column_width + gutter) + column_width)
        if column:
            draw.line((x - gutter // 2, top + 1, x - gutter // 2, bottom), fill=LIGHT)
        for row in range(rows):
            index = columns * row + column
            if index >= len(STORIES):
                break
            number = index + 1
            dateline, headline, body = STORIES[index]
            y = round(top + row * row_height) + 2
            accent = RED if number in highlights else INK
            draw.rectangle((x, y, x + 17, y + 8), fill=accent)
            draw.text((x + 8.5, y + 4), f"{number:02}",
                      font=font("SansMono-Bold", 8), fill=PAPER, anchor="mm")
            draw.text((x + 22, y + 1), dateline, font=font("SansMono", 8),
                      fill=RED if number in highlights else GRAY, anchor="lt")
            if block(draw, x, y + 11, headline, headline_font, edge - x, 14, INK) != 1:
                raise ValueError(f"Headline exceeds its column: {headline}")
            body_width = edge - x
            max_lines = 4 if number <= 16 else 3
            leading = 8 if len(wrap(body, body_font, body_width)) == 4 else 10
            if block(draw, x, y + 24, body, body_font, body_width, leading, BODY_INK, max_lines) > max_lines:
                raise ValueError(f"Body exceeds its allotted lines: {headline}")
            if row < rows - 1:
                rule_y = round(top + (row + 1) * row_height)
                draw.line((x, rule_y, edge, rule_y), fill=LIGHT)


def footer(draw):
    top = 964
    padding = 10
    draw.rectangle((LEFT, top, RIGHT, 1004), outline=RED, width=2)
    draw.text((LEFT + padding, top + padding), "DATE CHECK",
              font=font("SansMono-Bold", 10), fill=RED, anchor="lt")
    copy_x = LEFT + 79
    if block(draw, copy_x, top + padding, DATE_CHECK, font("SansMono", 10),
             RIGHT - copy_x - padding, 11, INK) != 2:
        raise ValueError("The date check must fill two lines")
    draw.text((SIZE // 2, 1014),
              "Every line here happened, or was first reported, on Thursday 19 November 2026. "
              "Drawn, set and written by an agent.",
              font=font("SansMono", 9), fill=GRAY, anchor="mm")


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)
    header(draw)
    globe(img)
    numbers_strip(draw)
    story_grid(draw)
    footer(draw)
    path = Path(__file__).with_name("entry.png")
    img.save(path, optimize=True)
    print(f"{path.name}: {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
