import os
import re
import urllib.parse
from pathlib import Path

import qrcode
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent

load_dotenv()

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".md", ".txt", ".png"}


def _safe_filename(filename: str) -> str:
    """
    Prevents path traversal and limits file types.
    This is a visible security feature for the capstone.
    """
    name = os.path.basename(filename).strip()

    if not name:
        raise ValueError("Filename cannot be empty.")

    suffix = Path(name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: {suffix}")

    return name


def _safe_campaign_slug(campaign: str) -> str:
    """
    Converts a campaign name into a safe UTM slug.
    """
    slug = campaign.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = slug.strip("_")
    return slug or "webinar_campaign"


def generate_utm_url(
    base_url: str,
    source: str,
    medium: str,
    campaign: str,
) -> dict:
    """
    Generates a safe UTM tracking URL and optional social share URL.
    """
    parsed = urllib.parse.urlparse(base_url)

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return {
            "status": "error",
            "message": "base_url must be a valid http or https URL.",
        }

    campaign_slug = _safe_campaign_slug(campaign)

    query = dict(urllib.parse.parse_qsl(parsed.query))
    query.update(
        {
            "utm_source": source.lower().strip(),
            "utm_medium": medium.lower().strip(),
            "utm_campaign": campaign_slug,
        }
    )

    final_url = urllib.parse.urlunparse(
        parsed._replace(query=urllib.parse.urlencode(query))
    )

    encoded_url = urllib.parse.quote(final_url, safe="")

    share_url = None
    if source.lower() == "linkedin":
        share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}"
    elif source.lower() == "facebook":
        share_url = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"

    return {
        "status": "success",
        "tracking_url": final_url,
        "share_url": share_url,
    }


def generate_qr_code(url: str, filename: str = "campaign_qr.png") -> dict:
    """
    Creates a QR code PNG in output/.
    """
    safe_name = _safe_filename(filename)

    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return {
            "status": "error",
            "message": "QR code URL must be a valid http or https URL.",
        }

    filepath = OUTPUT_DIR / safe_name

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)

    return {
        "status": "success",
        "path": str(filepath),
    }


def save_campaign_file(filename: str, content: str) -> dict:
    """
    Saves a text campaign asset to output/.
    """
    safe_name = _safe_filename(filename)

    if Path(safe_name).suffix.lower() == ".png":
        return {
            "status": "error",
            "message": "Use generate_qr_code for PNG files.",
        }

    filepath = OUTPUT_DIR / safe_name
    filepath.write_text(content, encoding="utf-8")

    return {
        "status": "success",
        "path": str(filepath),
    }


SYSTEM_INSTRUCTION = """
You are Webinar Campaign Forge, an omnichannel campaign agent for business webinar promotion.

Your job:
Turn rough webinar notes, transcripts, or planning bullets into campaign-ready assets.

Always produce:
1. Webinar overview table with topic, speaker, audience, date/time, platform, and registration URL.
2. Landing page copy with:
   - Hero headline
   - Subheadline
   - Audience pain points
   - Key takeaways
   - Speaker section
   - CTA section
3. Plain-text business email draft with:
   - 3 subject lines
   - Preview text
   - Email body
4. LinkedIn and Facebook posts.
5. UTM links for linkedin, facebook, and email.
6. QR code for the primary registration link.
7. Saved output files:
   - landing_page.md
   - email_draft.txt
   - social_posts.md

If information is missing, do not stop.
Use clear placeholders like [INSERT SPEAKER NAME] or [INSERT WEBINAR DATE].

Security rules:
- Never ask for or expose API keys.
- Never save files outside output/.
- Never create executable files.
- Never include private credentials in generated content.
"""

root_agent = Agent(
    model="gemini-flash-latest",
    name="webinar_campaign_forge_agent",
    description="Creates webinar campaign assets, UTM links, QR codes, and export files from raw notes.",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        generate_utm_url,
        generate_qr_code,
        save_campaign_file,
    ],
)
