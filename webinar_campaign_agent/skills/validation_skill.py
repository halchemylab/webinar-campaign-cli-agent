import re


REQUIRED_FIELDS = {
    "topic": [r"\btopic\s*:", r"\btitle\s*:", r"\bwebinar\b"],
    "speaker": [r"\bspeaker\s*:", r"\bpresenter\s*:", r"\bhost\s*:"],
    "audience": [r"\baudience\s*:", r"\bfor\s+(marketing|sales|business|teams|managers)"],
    "date": [r"\bdate\s*:", r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\b", r"\b\d{1,2}/\d{1,2}/\d{2,4}\b"],
    "registration_link": [r"\bregistration\s+link\s*:", r"https?://"],
}


def review_webinar_notes(notes: str) -> dict:
    """
    Checks rough webinar notes for details needed to generate campaign assets.
    """
    normalized = notes.lower()
    missing = []

    for field, patterns in REQUIRED_FIELDS.items():
        if not any(re.search(pattern, normalized) for pattern in patterns):
            missing.append(field)

    if missing:
        checklist = [field.replace("_", " ") for field in missing]
        return {
            "status": "needs_info",
            "missing_fields": checklist,
            "message": "Missing recommended campaign details: "
            + ", ".join(checklist)
            + ". Use placeholders if generating assets now.",
        }

    return {
        "status": "ready",
        "missing_fields": [],
        "message": "The notes include the core details needed for campaign generation.",
    }
