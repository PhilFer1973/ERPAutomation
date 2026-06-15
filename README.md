# AI-Guided Legacy ERP Supplier Onboarding Automation

This repository is a proof-of-concept for controlled finance automation in a legacy ERP-style environment. It demonstrates how Microsoft Forms, SharePoint Lists, Power Automate, Power Automate Desktop, Python, OpenAI Vision, and GnuCash can work together to onboard a supplier when the practical integration route is the application user interface.

The central control principle is:

```text
Power Automate Desktop follows the scripted path.
OpenAI Vision validates the screen state, values, and save result.
```

V1 is intentionally not a fully autonomous desktop agent. It keeps execution in Power Automate Desktop and uses AI only as a validation, verification, and audit layer.

## Business Problem

Finance teams often work with ERP or accounting systems where direct integration is blocked by licensing, old versions, missing documentation, operational risk, or lack of IT capacity. In those cases, the approved process may still be the front-end user interface.

This project shows a realistic, controlled pattern for automating that kind of environment:

```text
External supplier form
-> SharePoint operational queue
-> desktop RPA
-> OpenAI Vision screen validation
-> GnuCash vendor creation
-> status update
-> audit trail
```

## Solution Overview

The V1 design uses Microsoft Forms to collect supplier details, SharePoint Lists as the operational queue and audit store, Power Automate Desktop as the executor, GnuCash as the local finance system, and a Python helper as the Vision validation layer.

For this first foundation phase, the repository contains documentation, schemas, sample data, and a runnable Python mock mode. It does not yet automate GnuCash, Power Automate Desktop, SharePoint, or Microsoft Forms.

## Architecture Summary

```text
Microsoft Forms
    -> Power Automate cloud flow
    -> SharePoint SupplierOnboardingRequests
    -> Power Automate Desktop
    -> GnuCash UI
    -> Screenshot checkpoint
    -> Python vision_agent helper
    -> OpenAI Vision or mock response
    -> JSON validation and audit log
    -> PAD continues, stops, or marks for review
```

## V1 Scope

- Supplier legal name
- Contact name
- Email
- Address, city, postcode, and country
- Currency
- Microsoft Forms as the source
- SharePoint Lists as the queue and audit store
- GnuCash as a UI-only finance system
- Power Automate Desktop as the scripted executor
- Python helper for Vision validation
- OpenAI Vision structured JSON responses
- Local screenshot and log retention
- Success email after confirmed creation

## V1 Exclusions

- Bank details
- VAT number
- Payment terms
- Supplier amendments or deletion
- AP invoices, bill posting, or payments
- Approval workflow
- Duplicate supplier detection
- Retry logic
- Finance failure notifications
- Direct GnuCash API access, bindings, or database writes
- Real production supplier data

## Vision Checkpoint Pattern

The automation follows a repeatable checkpoint pattern:

```text
PAD performs a scripted step
PAD captures a screenshot
PAD calls the Python helper
Python sends screenshot context to Vision or mock mode
Vision returns strict JSON
Python validates status and confidence
Python logs the result
PAD continues only when validation passes
```

V1 confidence policy:

```text
confidence >= 0.85: continue
confidence >= 0.70 and < 0.85: stop for review
confidence < 0.70: failed
```

## Why GnuCash

GnuCash is used as a lightweight desktop accounting system that can stand in for a legacy ERP front end. The project deliberately treats it as UI-only so the automation pattern remains relevant to systems where direct integration is not available or not approved.

## Why OpenAI Vision

OpenAI Vision is used to inspect screenshots, confirm screen state, verify entered values, identify visible errors, and produce audit-friendly structured JSON. It does not decide the whole process or control the desktop in V1.

## Why Power Automate Desktop

Power Automate Desktop is the controlled executor. It handles opening applications, navigating screens, entering fields, taking screenshots, and calling the Python helper. That keeps the automation route scripted and easier to audit.

## Developer Quick Start

This foundation can be tested without GnuCash, SharePoint, Forms, Power Automate, or an OpenAI API key.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

Mock mode is enabled by default in `.env.example`.

Example helper call once dependencies are installed:

```powershell
python src\vision_agent\main.py --input-json sample-data\pad-checkpoint-sample.json --output-json logs\sample-output.json
```

The sample PAD checkpoint file uses fictional data and is included only to make mock-mode smoke testing easy.

## Security And Data Warnings

This is a proof of concept. Use fictional data only.

Do not commit:

- `.env` files
- API keys
- real supplier data
- screenshots containing personal data
- generated logs
- `.gnucash` files

The `.gitignore` excludes local logs, screenshot folders, Python cache files, virtual environments, and GnuCash files.

## Roadmap

Planned future phases include the real OpenAI Vision call, guided GnuCash setup, a Power Automate Desktop prototype, Microsoft Forms and SharePoint setup, end-to-end integration, and demo polish.

See [docs/v2-roadmap.md](docs/v2-roadmap.md) for longer-term ideas.
