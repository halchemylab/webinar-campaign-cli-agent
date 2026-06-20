from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("webinar-campaign-forge-mcp")

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


@mcp.tool()
def list_generated_assets() -> list[str]:
    """
    Lists generated campaign assets in output/.
    """
    return sorted([p.name for p in OUTPUT_DIR.iterdir() if p.is_file()])


@mcp.tool()
def read_generated_asset(filename: str) -> str:
    """
    Reads a generated text asset from output/.
    """
    normalized = filename.replace("\\", "/")
    safe_name = Path(normalized).name

    if not safe_name or safe_name in {".", ".."}:
        return "Invalid filename."

    path = (OUTPUT_DIR / safe_name).resolve()

    # Ensure the resolved path is inside the output directory
    try:
        path.relative_to(OUTPUT_DIR.resolve())
    except ValueError:
        return "Access denied: Path traversal detected."

    if not path.is_file():
        return f"File not found or is not a file: {safe_name}"

    if path.suffix.lower() not in {".md", ".txt"}:
        return f"Cannot read non-text file: {safe_name}"

    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
