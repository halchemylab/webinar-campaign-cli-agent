import sys
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from webinar_campaign_agent.agent import root_agent


APP_NAME = "webinar_campaign_forge"
USER_ID = "local_user"
SESSION_ID = "local_session"

INPUT_FILE = Path("input/raw_webinar_notes.txt")


MODE_PROMPTS = {
    "full": "Generate the full campaign package.",
    "linkedin": "Generate only a LinkedIn post with a LinkedIn UTM tracking link and LinkedIn share URL.",
    "facebook": "Generate only a Facebook post with a Facebook UTM tracking link and Facebook share URL.",
    "email": "Generate only a plain-text business email draft with 3 subject lines and preview text.",
    "social": "Generate only LinkedIn and Facebook posts with their UTM tracking links.",
    "landing": "Generate only landing page copy.",
    "qr": "Generate only a QR code for the registration URL.",
    "review": "Review these webinar campaign notes, produce a missing-information checklist, and suggest improvements. Do not generate files.",
}


def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "full"

    if mode not in MODE_PROMPTS:
        valid_modes = ", ".join(MODE_PROMPTS.keys())
        raise ValueError(f"Invalid mode '{mode}'. Use one of: {valid_modes}")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_FILE}. "
            "Create input/raw_webinar_notes.txt first."
        )

    notes = INPUT_FILE.read_text(encoding="utf-8")

    prompt = f"""
{MODE_PROMPTS[mode]}

Use the webinar notes below.

If a registration URL exists in the notes, use it as the destination URL.
If details are missing, use visible placeholders instead of inventing facts.
For review mode, use the review_webinar_notes tool before giving recommendations.

NOTES:
{notes}
"""

    session_service = InMemorySessionService()
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    )

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content,
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)


if __name__ == "__main__":
    main()
