# Setup Guide

This repository is currently in the foundation phase. You do not need to install or configure the external systems yet to review the docs, schemas, sample data, or mock Python helper.

When the project moves into later phases, you will need to be guided step by step through creating, downloading, installing, or configuring the items below. Do not assume any of these already exist until confirmed.

## Later Setup Checklist

You will need guidance for:

- Installing Python
- Creating a Python virtual environment
- Installing GnuCash
- Creating a local demo GnuCash file
- Installing or enabling Power Automate Desktop
- Creating a Microsoft Form
- Creating SharePoint Lists
- Creating a Power Automate cloud flow
- Creating a Power Automate Desktop flow
- Creating an OpenAI API key
- Creating a local `.env` file
- Choosing local screenshot and log paths

## Foundation-Only Local Test

Once Python is available, the mock helper can be tested without external systems:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

Mock mode is designed to avoid OpenAI API calls while the PAD and file handoff are being developed.

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
