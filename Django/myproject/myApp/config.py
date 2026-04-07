from copy import deepcopy

DEFAULT_CONFIG = {
    "fix_html": True,
    "strip_interactive": True,
    "strip_event_handlers": True,
    "normalize_tables": True,
    "decode_html_entities": True,
    "remove_empty_paragraphs": False,
    "remove_empty_spans": False,
    "flatten_nested_spans": False,
    "remove_comments": False,
    "strip_whitespace": False,

    "div_mappings": {},
    "class_styles": {
        "table-dotted": {"border": "1px dotted #999"},
        "table-dashed": {"border": "1px dashed #666"},
        "cell-muted": {"background-color": "#f4f4f2"},
        "cell-strong-border": {"border-left": "2px solid #333"},
    },
    "indent_mapping": {},
    "apply_th_styles": True,

    "fonts": {
        "default": {
            "name": "Verdana",
            "size": 10,
            "color": "#222222",
        },
        "table": {
            "name": "Verdana",
            "size": 9,
        },
        "heading": {
            "name": "Verdana",
            "sizes": {
                "h1": 22,
                "h2": 18,
                "h3": 16,
            },
            "color": "#0d1831",
        },
    },

    "include_images": True,
    "image_placeholder": True,
    "max_image_width": None,

    "table_style": None,
    "flatten_nested_tables": True,
    "table_borders": False,
    "fix_colspan_rowspan": True,

    "default_paragraph_style": None,
    "default_alignment": None,
    "convert_br": True,

    "span_as_stack": True,
    "apply_span_styles": True,
    "color_map": {},

    "allow_existing_document": True,
    "enable_chunk_mode": False,
    "debug": False,

    "respect_inline_table_styles": True,
    "respect_inline_cell_styles": True,

    "default_table_border": {
        "style": "single",
        "size": 4,
        "color": "auto",
    },

    "default_cell_border": None,
    "default_cell_shading": None,
}


def deep_merge(base: dict, override: dict) -> dict:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def build_config(user_config=None) -> dict:
    config = deepcopy(DEFAULT_CONFIG)
    if user_config:
        config = deep_merge(config, user_config)
    return config