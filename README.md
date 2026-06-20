# Webinar Campaign Forge Agent

Built as the capstone project for Kaggle's 5-Day AI Agents Intensive with Google.

### Overview

Webinar Campaign Forge Agent is an AI agent that turns rough webinar notes into omnichannel campaign assets: landing page copy, business email drafts, LinkedIn and Facebook posts, UTM tracking links, and QR codes.

### Track

Agents for Business

### Problem

Marketing teams often spend hours converting webinar planning notes into publishable campaign materials. This creates delays, inconsistent messaging, and tracking mistakes.

### Solution

This project uses a Google ADK agent to read the user's requested output mode, extract structured webinar details, draft the requested campaign copy, generate relevant UTM links, create QR codes when needed, and save reusable campaign files into an output folder when the mode calls for it.

## Key Concepts Demonstrated

| Capstone Concept | Where Demonstrated |
|---|---|
| ADK Agent | `webinar_campaign_agent/agent.py` |
| Tool use | `generate_utm_url`, `generate_qr_code`, `save_campaign_file`, `review_webinar_notes` |
| MCP Server | `webinar_campaign_agent/mcp_server.py` |
| Antigravity | Demonstrated in video |
| Security features | Safe filename handling, output directory restriction, no committed secrets |
| Deployability | Local setup instructions and ADK Web demo |
| Agent skills | Campaign generation, structured extraction, validation, tracking links, QR codes, asset export |

## Architecture

The project can run in two modes. ADK mode demonstrates the agent implementation required by the course. CLI mode provides a practical local workflow where users place notes in an input file and generate only the assets they need.

```text
webinar-campaign-cli-agent/
  webinar_campaign_agent/
    __init__.py
    agent.py
    mcp_server.py
    skills/
      __init__.py
      utm_skill.py
      qr_skill.py
      file_skill.py
      validation_skill.py
  input/
    .gitkeep
    raw_webinar_notes.txt
  output/
  samples/
    raw_webinar_notes.txt
  run_from_file.py
  README.md
  requirements.txt
  .env.template
  .gitignore
  LICENSE
```

```mermaid
flowchart LR
    A[ADK prompt] --> B[ADK root_agent]
    C[input/raw_webinar_notes.txt] --> D[CLI runner]
    D --> B

    B --> E[skills/utm_skill.py]
    B --> F[skills/qr_skill.py]
    B --> G[skills/file_skill.py]
    B --> H[skills/validation_skill.py]

    E --> I[Tracked registration links]
    F --> J[Timestamped QR code PNG]
    G --> K[Timestamped campaign copy files]
    H --> L[Missing-info checklist]

    I --> M[output/]
    J --> M
    K --> M

    M --> N[MCP server]
    N --> O[list_generated_assets]
    N --> P[read_generated_asset]
```

| Component | Role |
|---|---|
| `root_agent` | Coordinates mode-aware campaign generation from rough webinar notes |
| `skills/` | Shared tool layer used by ADK mode and CLI mode |
| `run_from_file.py` | Practical local runner that sends `input/raw_webinar_notes.txt` to the same ADK agent |
| `output/` | Local ignored folder for generated campaign assets |
| MCP server | Lets MCP-compatible clients list and inspect generated text assets |

Generated file examples:

```text
output/
  landing_page_YYYYMMDD_HHMMSS.md
  email_draft_YYYYMMDD_HHMMSS.txt
  social_posts_YYYYMMDD_HHMMSS.md
  campaign_qr_YYYYMMDD_HHMMSS.png
```

## Output Modes

The agent reads the user's intent before generating assets.

| User asks | Agent generates |
|---|---|
| Full campaign, everything, or all assets | Landing page, email, LinkedIn post, Facebook post, UTM links, QR code, saved files |
| Just LinkedIn | LinkedIn post, LinkedIn UTM link, LinkedIn share URL |
| Just Facebook | Facebook post, Facebook UTM link, Facebook share URL |
| Email only | Subject lines, preview text, plain-text email draft |
| Landing page only | Landing page copy |
| Social posts only | LinkedIn and Facebook posts, UTM/share links |
| QR code only | QR code from the registration URL |
| Review the campaign | Suggestions only, unless file generation is requested |

## Setup

Clone the repository:

```bash
git clone https://github.com/halchemylab/webinar-campaign-cli-agent.git
cd webinar-campaign-cli-agent
```

Create and activate a virtual environment.

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.template .env
```

Then edit `.env` and replace the placeholder with your Gemini API key:

```env
GOOGLE_API_KEY="YOUR_API_KEY"
```

## Usage

This project supports two execution modes.

### 1. ADK Agent Mode

Use this mode to run the project as an ADK agent.

```bash
adk run webinar_campaign_agent
```

Example prompt:

```text
Generate only a LinkedIn post from these webinar notes:

Topic: Using AI Agents to Improve Omnichannel Marketing Operations
Speaker: Jane Lee
Audience: Marketing managers
Date: July 24, 2026
Registration link: https://example.com/webinar
```

### 2. CLI File Mode

Use this mode to process notes from a local input file.

Create an input file:

macOS/Linux:

```bash
mkdir -p input
cp samples/raw_webinar_notes.txt input/raw_webinar_notes.txt
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force input
Copy-Item samples/raw_webinar_notes.txt input/raw_webinar_notes.txt
```

Then run the agent with a mode:

```bash
python run_from_file.py full
python run_from_file.py linkedin
python run_from_file.py facebook
python run_from_file.py email
python run_from_file.py social
python run_from_file.py landing
python run_from_file.py qr
python run_from_file.py review
```

For example:

```bash
python run_from_file.py linkedin
```

This generates only the LinkedIn post, LinkedIn tracking URL, and LinkedIn share URL.

Generated assets appear in:

```text
output/
```

## What Each Mode Is For

| Mode | Command | Best for |
|---|---|---|
| ADK | `adk run webinar_campaign_agent` | Proving the ADK agent requirement |
| CLI | `python run_from_file.py linkedin` | Fast practical generation |
| CLI review | `python run_from_file.py review` | Missing-info checklist |
| CLI full | `python run_from_file.py full` | Complete campaign package |

## Final Demo Commands

```bash
python run_from_file.py review
python run_from_file.py linkedin
python run_from_file.py full
adk run webinar_campaign_agent
```

Suggested demo positioning:

```text
I kept ADK as the agent interface because it maps directly to the course requirement, but I also added a CLI runner so the workflow is actually useful. Both modes reuse the same campaign tools for validation, UTM generation, QR code creation, and safe file export.
```

## Run the ADK Web Demo

```bash
adk web --port 8000
```

Open the local UI in your browser and select the webinar campaign agent.

ADK Web is used here as a local development and debugging demo interface. It is not a production deployment.

## Run the MCP Server

```bash
python -m webinar_campaign_agent.mcp_server
```

The MCP server exposes generated campaign assets through tools so another MCP-compatible client can list and inspect files in `output/`.

## Security Notes

- `.env` is ignored by Git.
- Generated campaign files are restricted to `output/`.
- Path traversal is blocked with safe filename handling.
- Only `.md`, `.txt`, and `.png` output files are allowed.
- Generated filenames include a timestamp so campaign runs are easier to track.
- The project does not require committing API keys, passwords, or generated client assets.

## Demo Prompt

```text
Generate a full webinar campaign for this event:

Topic: Using AI Agents to Improve Omnichannel Marketing Operations
Speaker: Jane Lee, Director of Growth Marketing at ExampleCo.
Audience: Marketing managers, demand generation teams, and small business owners.
Date: July 24, 2026
Time: 11:00 AM Pacific
Platform: Zoom
Registration link: https://example.com/webinar

Core idea:
Teams waste hours turning event notes into landing pages, emails, social posts, tracking links, and QR codes.
```

## Example Prompts

### Full campaign

```text
Generate the full campaign from these webinar notes:
...
```

### LinkedIn only

```text
Generate only a LinkedIn post from these webinar notes:
...
```

### Facebook only

```text
Generate only a Facebook post from these webinar notes:
...
```

### Email only

```text
Generate an email draft only from these webinar notes:
...
```

### Social posts only

```text
Generate LinkedIn and Facebook posts only from these notes:
...
```

### QR code only

```text
Generate a QR code for this registration URL:
https://example.com/webinar
```

The key agent behavior is that it does not blindly generate every artifact. It reads the user's intent first. If you ask for only LinkedIn, it generates only LinkedIn copy and the LinkedIn tracking link. If you ask for the full campaign, it coordinates multiple tools to generate landing page copy, email, social posts, UTM links, QR code, and saved output files.

## Sample Input

The repository includes a sample notes file:

```text
samples/raw_webinar_notes.txt
```

Use it as the source material for local testing or demo recording.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
