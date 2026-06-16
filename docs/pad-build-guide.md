# Power Automate Desktop Build Guide

This guide describes how to build the V1 Power Automate Desktop flow from the confirmed GnuCash screenshots and Python helper contract. It is a controlled build guide, not an exported PAD flow file.

The future PAD flow should be built manually in Power Automate Desktop using this guide, then tested first in mock mode and only later with live OpenAI Vision.

For a more granular step-by-step build list, use [pad-action-checklist.md](pad-action-checklist.md).

## Key Files

| File | Purpose |
|---|---|
| `pad/checkpoint-manifest.json` | PAD checkpoint sequence and runtime path conventions |
| `schemas/pad_checkpoint_request.schema.json` | JSON contract for PAD-to-Python input |
| `schemas/vision_action.schema.json` | JSON contract for Python-to-PAD output |
| `sample-data/pad-checkpoints/` | Example checkpoint request JSON files |
| `src/vision_agent/main.py` | Python entrypoint PAD should call |
| `docs/gnucash-screenshot-checkpoints.md` | Visual checkpoint evidence from actual screenshots |
| `docs/gnucash-manual-vendor-creation-steps.md` | Confirmed manual workflow |

## PAD Flow Name

Recommended name:

```text
ERPAutomation_GnuCash_Vendor_Onboarding_V1
```

## V1 Runtime Assumptions

- GnuCash is installed locally.
- Demo file is stored outside the repo:

```text
C:\Users\Philip\Documents\GnuCash\VisionAutomationDemo.gnucash
```

- Repo root is:

```text
C:\Users\Philip\Downloads\ERPAutomation
```

- Python helper is called through:

```text
C:\Users\Philip\Downloads\ERPAutomation\.venv\Scripts\python.exe
```

- Python script path is:

```text
C:\Users\Philip\Downloads\ERPAutomation\src\vision_agent\main.py
```

## Flow Variables

Create PAD variables equivalent to:

| Variable | Example | Notes |
|---|---|---|
| `RepoRoot` | `C:\Users\Philip\Downloads\ERPAutomation` | Base path for helper and runtime files |
| `GnuCashFilePath` | `C:\Users\Philip\Documents\GnuCash\VisionAutomationDemo.gnucash` | Demo book file |
| `PythonExe` | `%RepoRoot%\.venv\Scripts\python.exe` | Local venv Python |
| `PythonHelper` | `%RepoRoot%\src\vision_agent\main.py` | Helper entrypoint |
| `RunId` | `yyyyMMdd-HHmmss-{SharePointItemId}` | Unique per supplier |
| `RunScreenshotDir` | `%RepoRoot%\screenshots\archive\%RunId%` | Runtime screenshot folder |
| `RunInputDir` | `%RepoRoot%\logs\%RunId%\pad-input` | PAD checkpoint request JSON folder |
| `RunOutputDir` | `%RepoRoot%\logs\%RunId%\pad-output` | Python result JSON folder |

## Supplier Field Variables

Map SharePoint/form data to these PAD variables:

| PAD variable | Source field | GnuCash target |
|---|---|---|
| `SupplierLegalName` | `SupplierLegalName` | `Company Name` |
| `ContactName` | `ContactName` | `Payment Address > Name` |
| `SupplierEmail` | `SupplierEmail` | `Email` |
| `Address` | `Address` | `Payment Address > Address` line 1 |
| `City` | `City` | `Payment Address > Address` line 2 |
| `Country` | `Country` | `Payment Address > Address` line 3 |
| `Postcode` | `Postcode` | `Payment Address > Address` line 4 |
| `Currency` | `Currency` | SharePoint/Form only in V1 |

V1 should leave `Vendor Number` blank.

## Checkpoint Helper Pattern

For each checkpoint:

1. PAD takes a screenshot and saves it to `%RunScreenshotDir%`.
2. PAD writes a checkpoint request JSON file to `%RunInputDir%`.
3. PAD runs Python:

```powershell
%PythonExe% %PythonHelper% --input-json "%InputJsonPath%" --output-json "%OutputJsonPath%"
```

4. PAD reads `%OutputJsonPath%`.
5. PAD parses `status` and `confidence`.
6. PAD continues only when the returned `status` is allowed for that checkpoint.
7. PAD stops and logs when `status` is `stop_for_review` or `failed`.

## Checkpoint Sequence

Use `pad/checkpoint-manifest.json` as the machine-readable reference.

| Step | PAD action | Checkpoint |
|---:|---|---|
| 1 | Open GnuCash and demo file; capture accounts screen | `GN_CASH_MAIN_SCREEN` |
| 2 | Open `Business` menu; capture menu | `BUSINESS_MENU_OPEN` |
| 3 | Open `Vendor` submenu; capture `New Vendor...` path | `VENDOR_NEW_MENU_PATH` |
| 4 | Click `New Vendor...`; capture blank form | `NEW_VENDOR_FORM_BLANK` |
| 5 | Enter supplier fields; capture completed form | `NEW_VENDOR_FORM_COMPLETED` |
| 6 | Click `OK`; capture returned accounts screen | `POST_SAVE_RETURN_SCREEN` |
| 7 | Open `Business > Vendor`; capture `Vendors Overview` path | `VENDOR_OVERVIEW_MENU_PATH` |
| 8 | Open `Vendors Overview`; capture created vendor row | `CREATED_VENDOR_VISIBLE` |
| 9 | Return to main screen, use `File > Save`, then `File > Quit` | No Vision checkpoint required in V1 unless close prompts appear |

## Failure Handling

If Python returns:

```text
stop_for_review
failed
```

PAD should:

1. Stop the current supplier run.
2. Save the Python output JSON path to the run log.
3. Record the failed checkpoint type.
4. Update SharePoint status to `Failed` or `Needs Review`.
5. Do not click `OK`, save, or continue entering data after a failed validation.

For V1, do not retry automatically.

## Mock-Mode First Test

Before using live OpenAI Vision:

1. Set `.env` to:

```text
MOCK_MODE=true
```

2. Build the PAD flow to call the helper and parse the output.
3. Confirm PAD can move through the skeleton using mock responses.
4. Only then switch to:

```text
MOCK_MODE=false
```

Live mode should be tested on fictional data only.

## Not In This Phase

This guide does not yet build:

- Microsoft Forms integration
- SharePoint polling or trigger logic
- Cloud flow trigger
- Supplier success email
- Failure email to finance
- Retry handling
- Duplicate detection
- Bank details
- Production supplier processing

Those remain later phases.
