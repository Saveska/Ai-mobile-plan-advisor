import re


def emphasize_offer_names(text: str, offers: list) -> str:
    """
    Highlights offer names in the AI output for better PDF readability.
    """
    for offer in offers:
        name = offer["OfferName"]
        text = re.sub(
            re.escape(name),
            f"<b>{name}</b>",
            text,
            flags=re.IGNORECASE
        )
    return text


def format_sections(text: str) -> str:
    """
    Applies visual emphasis to key sections like Pros, Cons, and Conclusion.
    """
    text = re.sub(r'(\bPros\b|\bCons\b)', r'<u>\1</u>', text)
    text = text.replace("Conclusion", "<b>Conclusion</b>\n")
    return text


def clean_ai_output(text: str, offers: list) -> str:
    """
    Final cleanup pipeline for AI-generated text.
    Ensures consistency before PDF rendering.
    """
    text = re.sub(r'#+\s*', '', text)  # remove accidental markdown
    text = emphasize_offer_names(text, offers)
    text = format_sections(text)
    return re.sub(r'\n\s*\n', '\n\n', text)
