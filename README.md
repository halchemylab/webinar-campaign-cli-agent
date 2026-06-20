# Webinar Campaign Forge Agent

Built as the capstone project for Kaggle's 5-Day AI Agents Intensive with Google.

## Overview

Webinar Campaign Forge Agent is an AI agent that turns rough webinar notes into omnichannel campaign assets: landing page copy, business email drafts, LinkedIn and Facebook posts, UTM tracking links, and QR codes.

## Track

Agents for Business

## Problem

Marketing teams often spend hours converting webinar planning notes into publishable campaign materials. This creates delays, inconsistent messaging, and tracking mistakes.

## Solution

This project uses a Google ADK agent to extract structured webinar details, draft campaign copy, generate UTM links, create a QR code, and save reusable campaign files into an output folder.

## Key Concepts Demonstrated

| Capstone Concept | Where Demonstrated |
|---|---|
| ADK Agent | `webinar_campaign_agent/agent.py` |
| Tool use | `generate_utm_url`, `generate_qr_code`, `save_campaign_file` |
| MCP Server | `webinar_campaign_agent/mcp_server.py` |
| Antigravity | Demonstrated in video |
| Security features | Safe filename handling, output directory restriction, no committed secrets |
| Deployability | Local setup instructions and ADK Web demo |
| Agent skills | Campaign generation, structured extraction, copywriting, asset export |

## Architecture

```text
Raw webinar notes
      |
      v
ADK root_agent
      |
      +--> UTM tool
      +--> QR code tool
      +--> File export tool
      |
      v
output/
  landing_page_YYYYMMDD_HHMMSS.md
  email_draft_YYYYMMDD_HHMMSS.txt
  social_posts_YYYYMMDD_HHMMSS.md
  campaign_qr_YYYYMMDD_HHMMSS.png

MCP server
      |
      +--> list_generated_assets
      +--> read_generated_asset
```

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

## Run the Agent

```bash
adk run webinar_campaign_agent
```

You can also run a one-shot prompt:

```bash
adk run webinar_campaign_agent "Generate a full webinar campaign for the notes in samples/raw_webinar_notes.txt"
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

## Sample Input

The repository includes a sample notes file:

```text
samples/raw_webinar_notes.txt
```

Use it as the source material for local testing or demo recording.
