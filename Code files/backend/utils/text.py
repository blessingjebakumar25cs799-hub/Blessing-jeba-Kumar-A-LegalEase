import html
import re


def sanitize_text(text: str) -> str:
    if not text:
        return ""

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2022": "-",
        "\u00b7": "-",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def html_escape(text: str) -> str:
    return html.escape(text, quote=True)


def split_terms(terms: str) -> list[str]:
    return [
        item.strip()
        for item in terms.split(";")
        if item.strip()
    ]