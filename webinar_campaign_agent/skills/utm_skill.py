import re
import urllib.parse


def safe_campaign_slug(campaign: str) -> str:
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

    campaign_slug = safe_campaign_slug(campaign)

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
