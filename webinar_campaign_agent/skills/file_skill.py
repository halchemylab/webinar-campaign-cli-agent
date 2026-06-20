import os
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".md", ".txt", ".png"}


def timestamped_filename(filename: str) -> str:
    """
    Adds a generated timestamp before the file extension.
    """
    path = Path(filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{path.stem}_{timestamp}{path.suffix}"


def safe_filename(filename: str) -> str:
    """
    Prevents path traversal and limits file types.
    This is a visible security feature for the capstone.
    """
    normalized = filename.replace("\\", "/")
    name = os.path.basename(normalized).strip()

    if not name or name in {".", ".."}:
        raise ValueError("Invalid or empty filename.")

    suffix = Path(name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: {suffix}")

    target_path = (OUTPUT_DIR / name).resolve()
    try:
        target_path.relative_to(OUTPUT_DIR.resolve())
    except ValueError as exc:
        raise ValueError("Path traversal detected.") from exc

    return name


def save_campaign_file(filename: str, content: str) -> dict:
    """
    Saves a timestamped text campaign asset to output/.
    """
    safe_name = safe_filename(filename)

    if Path(safe_name).suffix.lower() == ".png":
        return {
            "status": "error",
            "message": "Use generate_qr_code for PNG files.",
        }

    filepath = OUTPUT_DIR / timestamped_filename(safe_name)
    filepath.write_text(content, encoding="utf-8")

    return {
        "status": "success",
        "path": str(filepath),
    }
