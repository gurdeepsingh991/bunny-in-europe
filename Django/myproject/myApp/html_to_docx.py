from io import BytesIO
from .parser import HtmlToDocx


def convert_html_to_docx(html_string, config=None):
    parser = HtmlToDocx(config=config)
    document = parser.parse_html_string(html_string)
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    return buffer