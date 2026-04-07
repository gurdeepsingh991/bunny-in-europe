from bs4 import BeautifulSoup


INTERACTIVE_TAGS = ["script", "style", "canvas", "button", "input", "textarea", "select"]


def remove_interactive(soup):
    for tag in soup.find_all(INTERACTIVE_TAGS):
        tag.decompose()

    for tag in soup.find_all():
        for attr in list(tag.attrs.keys()):
            if attr.startswith("on"):
                del tag.attrs[attr]

    return soup


def normalize_tables(soup):
    if isinstance(soup, str):
        soup = BeautifulSoup(soup, "html.parser")

    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if not rows:
            continue

        max_cols = max(
            sum(int(cell.get("colspan", 1)) for cell in row.find_all(["td", "th"], recursive=False))
            for row in rows
        )

        for row in rows:
            cells = row.find_all(["td", "th"], recursive=False)
            current_cols = sum(int(cell.get("colspan", 1)) for cell in cells)
            for _ in range(max_cols - current_cols):
                new_td = soup.new_tag("td")
                new_td.string = ""
                row.append(new_td)

    return soup


def clean_html(html: str, config: dict) -> str:
    soup = BeautifulSoup(html, "html.parser")

    if config.get("strip_interactive", True):
        soup = remove_interactive(soup)

    if config.get("normalize_tables", True):
        soup = normalize_tables(soup)

    return str(soup)


def preprocess_html(html: str, config: dict) -> str:
    soup = BeautifulSoup(html, "html.parser")

    if config.get("fix_html", True):
        soup = BeautifulSoup(clean_html(str(soup), config), "html.parser")

    if config.get("normalize_tables", True):
        soup = normalize_tables(soup)

    if config.get("strip_interactive", True):
        soup = remove_interactive(soup)

    return str(soup)