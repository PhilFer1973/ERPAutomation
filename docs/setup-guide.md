# Setup Guide

This repository can be reviewed and tested in mock mode without external systems. The real OpenAI Vision helper is scaffolded, but it should only be turned on when an API key and real screenshot are available.

When the project moves into later phases, you will need to be guided step by step through creating, downloading, installing, or configuring the items below. Do not assume any of these already exist until confirmed.

## Later Setup Checklist

You will need guidance for:

- Installing Python
- Creating a Python virtual environment
- Installing GnuCash: completed
- Creating a local demo GnuCash file: completed
- Installing or enabling Power Automate Desktop
- Creating a Microsoft Form
- Creating SharePoint Lists
- Creating a Power Automate cloud flow
- Creating a Power Automate Desktop flow
- Creating an OpenAI API key
- Creating a local `.env` file
- Choosing local screenshot and log paths

Current GnuCash demo file:

```text
C:\Users\Philip\Documents\GnuCash\VisionAutomationDemo.gnucash
```

Current GnuCash screenshot input folder:

```text
C:\Users\Philip\Downloads\ERPAutomation\screenshots\input
```

Confirmed manual GnuCash workflow:

```text
Business > Vendor > New Vendor...
Enter V1 supplier fields
OK
Business > Vendor > Vendors Overview
Confirm created vendor visible
Return to main screen
File > Save
File > Quit
```

## Foundation-Only Local Test

Once Python is available, the mock helper can be tested without external systems:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

Mock mode is designed to avoid OpenAI API calls while the PAD and file handoff are being developed.

## Real Vision Helper Setup

When you are ready to test the real OpenAI Vision path, you will need to be guided through:

1. Installing dependencies from `requirements.txt`.
2. Creating an OpenAI API key.
3. Copying `.env.example` to `.env`.
4. Setting `OPENAI_API_KEY` in `.env`.
5. Setting `MOCK_MODE=false`.
6. Supplying a checkpoint JSON file that points to a real screenshot.

The sample checkpoint file is safe for mock mode, but it does not point to a real screenshot yet.

## Environment File

Create `.env` later by copying `.env.example`.

Never commit `.env`.

Example values:

```text
OPENAI_API_KEY=replace_me
OPENAI_MODEL=gpt-4.1-mini
MOCK_MODE=true
CONFIDENCE_THRESHOLD=0.85
LOG_ROOT=logs
SCREENSHOT_ROOT=screenshots
```

## Important Project Rule

Before any future phase requires external setup, the user should be walked through the exact download, installation, account, credential, SharePoint, Forms, Power Automate, or GnuCash steps needed.

The foundation phase must not depend on those systems.
