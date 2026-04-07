import docx
from docx.enum.text import WD_COLOR, WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import RGBColor, Pt


FONT_STYLES = {
    "b": "bold",
    "strong": "bold",
    "em": "italic",
    "i": "italic",
    "u": "underline",
    "s": "strike",
    "sup": "superscript",
    "sub": "subscript",
    "th": "bold",
}

FONT_NAMES = {
    "code": "Courier",
    "pre": "Courier",
}


def parse_color(color_str):
    if not color_str:
        return None

    if "rgb" in color_str:
        try:
            color = color_str[color_str.index("(") + 1: color_str.index(")")]
            return tuple(int(x.strip()) for x in color.split(","))
        except Exception:
            return None

    if color_str.startswith("#"):
        color = color_str.lstrip("#")
        try:
            return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        except (ValueError, IndexError):
            return None

    return None


def set_run_font(run, font_name=None, font_size=None, font_color=None):
    if not run:
        return

    if font_name:
        run.font.name = font_name
        r_pr = run._element.get_or_add_rPr()
        r_fonts = r_pr.rFonts
        if r_fonts is None:
            r_fonts = OxmlElement("w:rFonts")
            r_pr.append(r_fonts)

        r_fonts.set(qn("w:ascii"), font_name)
        r_fonts.set(qn("w:hAnsi"), font_name)
        r_fonts.set(qn("w:cs"), font_name)
        r_fonts.set(qn("w:eastAsia"), font_name)

    if font_size:
        run.font.size = Pt(font_size)

    if font_color:
        colors = parse_color(font_color)
        if colors:
            run.font.color.rgb = RGBColor(*colors)


def apply_default_run_font(run, config, in_table=False):
    fonts_cfg = config.get("fonts", {})
    default_font = fonts_cfg.get("default", {})
    table_font = fonts_cfg.get("table", {})

    active_font = table_font if in_table and table_font.get("name") else default_font

    set_run_font(
        run,
        font_name=active_font.get("name"),
        font_size=active_font.get("size"),
        font_color=active_font.get("color"),
    )


def apply_heading_run_style(run, tags, config):
    heading_tag = next((f"h{i}" for i in range(1, 7) if f"h{i}" in tags), None)
    if not heading_tag:
        return

    heading_cfg = config.get("fonts", {}).get("heading", {})
    heading_sizes = heading_cfg.get("sizes", {})

    set_run_font(
        run,
        font_name=heading_cfg.get("name"),
        font_size=heading_sizes.get(heading_tag),
        font_color=heading_cfg.get("color"),
    )
    run.bold = True


def apply_semantic_run_styles(run, tags):
    for tag in tags:
        if tag in FONT_STYLES:
            setattr(run.font, FONT_STYLES[tag], True)

        if tag in FONT_NAMES:
            set_run_font(run, font_name=FONT_NAMES[tag])


def add_styles_to_run(run, style):
    if "color" in style:
        colors = parse_color(style["color"])
        if colors:
            run.font.color.rgb = RGBColor(*colors)

    if "background-color" in style:
        colors = parse_color(style["background-color"])
        if colors:
            run.font.highlight_color = WD_COLOR.GRAY_25


def apply_default_alignment(paragraph, text="", in_table=False):
    clean = " ".join(text.split())

    if in_table:
        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        return

    if len(clean.split()) >= 8:
        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    else:
        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT