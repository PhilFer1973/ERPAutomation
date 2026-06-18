# Power Automate Desktop Action Checklist

This checklist expands the PAD build guide into concrete build blocks for the manual Power Automate Desktop implementation that has now been proven locally.

Build this in layers:

1. Local hard-coded fictional supplier data.
2. Mock-mode Python checkpoint calls.
3. Live Vision checkpoint calls.
4. SharePoint/Form integration in a later phase.

Do not add bank details, VAT, payment terms, duplicate detection, retries, or production data in V1.

## 0. Before Opening PAD

Confirm these local files and folders exist:

```text
C:\Users\Philip\Downloads\ERPAutomation
C:\Users\Philip\Downloads\ERPAutomation\.venv\Scripts\python.exe
C:\Users\Philip\Downloads\ERPAutomation\src\vision_agent\main.py
C:\Users\Philip\Documents\VisionAutomationDemo.gnucash
```

For the first PAD handoff test, set `.env` to:

```text
MOCK_MODE=true
```

Use fictional supplier data only. Mock mode does not inspect screenshots, so it tests PAD mechanics and Python handoff only.

## 1. Create PAD Flow

Flow name:

```text
ERPAutomation_GnuCash_Vendor_Onboarding_V1
```

Recommended subflows:

| Subflow | Purpose |
|---|---|
| `Main` | Orchestrates the local supplier onboarding run |
| `InitializeRun` | Sets constants, sample supplier data, RunId, and folders |
| `RunVisionCheckpoint` | Takes screenshot, writes checkpoint request JSON, runs Python, reads output |
| `StopForFailure` | Central stop branch for failed/uncertain checkpoints |

If you prefer a simpler first pass, build everything in `Main` first, then refactor into subflows after the first successful mock run.

The current working build was completed mainly in `Main` with repeated inline checkpoint blocks.

## 2. Main Variables

Create these variables in PAD.

| Variable | Example value |
|---|---|
| `RepoRoot` | `C:\Users\Philip\Downloads\ERPAutomation` |
| `GnuCashFilePath` | `C:\Users\Philip\Documents\VisionAutomationDemo.gnucash` |
| `PythonExe` | `%RepoRoot%\.venv\Scripts\python.exe` |
| `PythonHelper` | `%RepoRoot%\src\vision_agent\main.py` |
| `RunId` | `MANUAL-TEST-001` for the first build |
| `RunScreenshotDir` | `%RepoRoot%\screenshots\archive\%RunId%` |
| `RunInputDir` | `%RepoRoot%\logs\%RunId%\pad-input` |
| `RunOutputDir` | `%RepoRoot%\logs\%RunId%\pad-output` |
| `LastCheckpointType` | blank initially |
| `LastVisionStatus` | blank initially |
| `LastVisionConfidence` | blank initially |
| `LastVisionOutputPath` | blank initially |
| `FailureReason` | blank initially |

## 3. Sample Supplier Variables

For the first local PAD build, hard-code fictional values:

| Variable | Value |
|---|---|
| `SupplierRequestId` | `42` |
| `SupplierLegalName` | `Blue Kite Consulting Ltd` |
| `ContactName` | `Sarah Ahmed` |
| `SupplierEmail` | `sarah.ahmed@example.com` |
| `Address` | `10 Market Street` |
| `City` | `London` |
| `Country` | `United Kingdom` |
| `Postcode` | `EC1A 1AA` |
| `Currency` | `GBP` |

V1 rules:

- Leave `Vendor Number` blank.
- Enter address lines as `Address`, `City`, `Country`, `Postcode`.
- Keep `Currency` in data only; do not enter it into GnuCash unless a visible field is later confirmed.

## 4. InitializeRun Checklist

Build these actions at the start of the flow.

| Step | PAD action intent | Details |
|---:|---|---|
| 1 | Set variable | `RepoRoot = C:\Users\Philip\Downloads\ERPAutomation` |
| 2 | Set variable | `GnuCashFilePath = C:\Users\Philip\Documents\VisionAutomationDemo.gnucash` |
| 3 | Set variable | `PythonExe = %RepoRoot%\.venv\Scripts\python.exe` |
| 4 | Set variable | `PythonHelper = %RepoRoot%\src\vision_agent\main.py` |
| 5 | Set variable | `RunId = MANUAL-TEST-001` for first test |
| 6 | Set variable | `RunScreenshotDir = %RepoRoot%\screenshots\archive\%RunId%` |
| 7 | Set variable | `RunInputDir = %RepoRoot%\logs\%RunId%\pad-input` |
| 8 | Set variable | `RunOutputDir = %RepoRoot%\logs\%RunId%\pad-output` |
| 9 | Create folder | Create `%RunScreenshotDir%` if it does not exist |
| 10 | Create folder | Create `%RunInputDir%` if it does not exist |
| 11 | Create folder | Create `%RunOutputDir%` if it does not exist |
| 12 | Set supplier variables | Use the sample values above |

Later, replace `RunId = MANUAL-TEST-001` with a timestamp plus SharePoint item ID.

## 5. RunVisionCheckpoint Subflow

Create a reusable checkpoint block. If PAD subflow inputs are awkward in your version, copy this block inline for each checkpoint first.

### Inputs

| Input | Example |
|---|---|
| `CheckpointType` | `NEW_VENDOR_FORM_BLANK` |
| `ScreenshotFileName` | `step-004-new-vendor-blank-form.png` |
| `ExpectedScreen` | `GnuCash New Vendor dialog with Vendor tab selected and blank entry fields` |
| `ExpectedField` | `Company Name` or blank |
| `ExpectedValue` | `Blue Kite Consulting Ltd` or blank |
| `AllowedStatus` | `continue` or `complete_success` |

### Actions

| Step | PAD action intent | Details |
|---:|---|---|
| 1 | Set variable | `LastCheckpointType = %CheckpointType%` |
| 2 | Set variable | `ScreenshotPath = %RunScreenshotDir%\%ScreenshotFileName%` |
| 3 | Set variable | `InputJsonPath = %RunInputDir%\%CheckpointType%.json` |
| 4 | Set variable | `OutputJsonPath = %RunOutputDir%\%CheckpointType%-result.json` |
| 5 | Take screenshot | Save active window or full screen to `%ScreenshotPath%` |
| 6 | Compose JSON text | Build PAD checkpoint request JSON using the template below |
| 7 | Write text to file | Write JSON text to `%InputJsonPath%`, overwriting if needed |
| 8 | Run command | Run Python helper with input/output args |
| 9 | Read text from file | Read `%OutputJsonPath%` |
| 10 | Convert JSON to custom object | Parse Python output JSON |
| 11 | Set variable | `LastVisionStatus = ParsedOutput.status` |
| 12 | Set variable | `LastVisionConfidence = ParsedOutput.confidence` |
| 13 | Set variable | `LastVisionOutputPath = %OutputJsonPath%` |
| 14 | If | If `LastVisionStatus` is not `%AllowedStatus%`, call `StopForFailure` |

### JSON Request Template

The actual PAD syntax for variable insertion may differ, but the file content should match this shape:

```json
{
  "run_id": "%RunId%",
  "supplier_request_id": "%SupplierRequestId%",
  "checkpoint_type": "%CheckpointType%",
  "screenshot_path": "%ScreenshotPath%",
  "expected_screen": "%ExpectedScreen%",
  "expected_field": "%ExpectedField%",
  "expected_value": "%ExpectedValue%",
  "supplier_context": {
    "supplier_legal_name": "%SupplierLegalName%",
    "contact_name": "%ContactName%",
    "supplier_email": "%SupplierEmail%",
    "address": "%Address%",
    "city": "%City%",
    "country": "%Country%",
    "postcode": "%Postcode%",
    "currency": "%Currency%"
  }
}
```

For blank `ExpectedField` or `ExpectedValue`, use JSON `null` rather than an empty quoted string if PAD makes that easy. Empty strings are acceptable for the first mock-mode build, but `null` is cleaner.

### Python Command

Use PAD `Run application` for the Python helper. In the current build, this proved more reliable than `Run DOS command`.

Recommended settings:

```text
Application path: %PythonExe%
Command line arguments: "%PythonHelper%" --input-json "%InputJsonPath%" --output-json "%OutputJsonPath%"
Working folder: %RepoRoot%
```

Choose the option that waits for the application to complete before the flow continues.

For the working local build, also set:

```text
Window style: Hidden
```

## 6. StopForFailure Subflow

Use one central branch for any checkpoint that returns `stop_for_review`, `failed`, or an unexpected status.

| Step | PAD action intent | Details |
|---:|---|---|
| 1 | Set variable | `FailureReason = Checkpoint %LastCheckpointType% returned %LastVisionStatus% at confidence %LastVisionConfidence%` |
| 2 | Write text to file | Append failure summary to `%RepoRoot%\logs\%RunId%\pad-failure-summary.txt` |
| 3 | Optional screenshot | Take final error screenshot if useful |
| 4 | Optional cleanup | Close dialogs only if it is safe and no data would be saved accidentally |
| 5 | Stop flow | End current run |

Do not continue entering supplier data after a failed checkpoint.

## 7. Main Flow Action Checklist

Build this sequence after `InitializeRun`.

| Step | PAD action intent | Details |
|---:|---|---|
| 1 | Launch application or open file | Open `VisionAutomationDemo.gnucash` |
| 2 | Wait | Wait until GnuCash Accounts screen is visible |
| 3 | Run checkpoint | `GN_CASH_MAIN_SCREEN`, screenshot `step-001-gnucash-main-screen.png`, allowed `continue` |
| 4 | Click menu | Focus GnuCash and click `Business` using the working local action sequence |
| 5 | Run checkpoint | `BUSINESS_MENU_OPEN`, screenshot `step-002-business-menu-open.png`, allowed `continue` |
| 6 | Click menu item | Open `Vendor` using the working local action sequence |
| 7 | Run checkpoint | `VENDOR_NEW_MENU_PATH`, screenshot `step-003-vendor-new-menu-path.png`, allowed `continue` |
| 8 | Click menu item | Click `New Vendor...` using the working local action sequence |
| 9 | Wait | Wait until the `New Vendor` dialog is visible |
| 10 | Run checkpoint | `NEW_VENDOR_FORM_BLANK`, screenshot `step-004-new-vendor-blank-form.png`, allowed `continue` |
| 11 | Enter text | Leave `Vendor Number` blank |
| 12 | Enter text | Use keyboard entry for `Company Name = %SupplierLegalName%` |
| 13 | Enter text | Use `Tab` and keyboard entry for `Payment Address > Name = %ContactName%` |
| 14 | Enter text | Use `Tab` and keyboard entry for address line 1 = `%Address%` |
| 15 | Enter text | Use `Tab` and keyboard entry for address line 2 = `%City%` |
| 16 | Enter text | Use `Tab` and keyboard entry for address line 3 = `%Country%` |
| 17 | Enter text | Use `Tab` and keyboard entry for address line 4 = `%Postcode%` |
| 18 | Enter text | Use `Tab` and keyboard entry for `Email = %SupplierEmail%` |
| 19 | Run checkpoint | `NEW_VENDOR_FORM_COMPLETED`, screenshot `step-005-new-vendor-completed-before-save.png`, allowed `continue` |
| 20 | Click button | Click `OK` |
| 21 | Wait | Wait until Accounts screen is visible again |
| 22 | Run checkpoint | `POST_SAVE_RETURN_SCREEN`, screenshot `step-006-post-save-return-screen.png`, allowed `continue` |
| 23 | Click menu | Click `Business` |
| 24 | Click menu item | Click or hover `Vendor` |
| 25 | Run checkpoint | `VENDOR_OVERVIEW_MENU_PATH`, screenshot `step-007-vendor-overview-menu-path.png`, allowed `continue` |
| 26 | Click menu item | Click `Vendors Overview` |
| 27 | Wait | Wait until the `Vendors` tab is visible |
| 28 | Run checkpoint | `CREATED_VENDOR_VISIBLE`, screenshot `step-008-created-vendor-visible.png`, allowed `complete_success` |
| 29 | Record success | Store any visible vendor reference if returned in `extracted_reference` |
| 30 | Return to main screen | Click `Accounts` tab or close Vendors tab if needed |
| 31 | Click menu | Click `File` |
| 32 | Click menu item | Click `Save` |
| 33 | Click menu | Click `File` |
| 34 | Click menu item | Click `Quit` |

## 8. First Test Plan

Run the first PAD test with:

```text
MOCK_MODE=true
```

Expected behavior:

- PAD should create the run folders.
- PAD should write checkpoint input JSON files.
- Python should return mock JSON output files.
- PAD should parse `status`.
- PAD should proceed through the full flow.

Because V1 has no duplicate supplier detection, use a fresh fictional supplier name for repeated runs or reset the demo GnuCash file between tests.

If mock mode reaches the end, then test again with:

```text
MOCK_MODE=false
```

Only use fictional supplier data.

First confirmed milestone:

- PAD launched GnuCash successfully.
- PAD created runtime folders.
- PAD captured the first screenshot.
- PAD wrote the first checkpoint request JSON.
- PAD called the Python helper successfully by using `Run application`.
- The helper returned valid mock JSON for `GN_CASH_MAIN_SCREEN`.

Current confirmed build milestone:

- PAD has completed the full V1 demo path through `CREATED_VENDOR_VISIBLE`.
- The local build uses hidden Python helper runs so checkpoints do not visibly break the GnuCash menu state.
- The local build uses a mixed interaction approach because GnuCash did not reliably expose all menu items and text fields as PAD UI elements.

## 9. Known Build Risks

| Risk | Mitigation |
|---|---|
| PAD cannot reliably find a UI element | Use the proven local mix of image clicks, active-window-relative mouse movement, and keyboard entry |
| Window focus changes before screenshot | Add waits and ensure GnuCash window is active |
| JSON string escaping is awkward in PAD | Start with simple fictional values; avoid quote characters in test data |
| PAD writes UTF-8 files with a BOM | Python helper now accepts `utf-8-sig` input |
| `.env` is set to live mode during mock testing | Set `MOCK_MODE=true` before first PAD run |
| Repeated mock tests create duplicate demo vendors | Use unique fictional supplier names or reset the demo file between runs |
| GnuCash prompts on quit | Save through `File > Save` before `File > Quit`; document any prompt if it appears |
| Wrong supplier values entered | Stop at `NEW_VENDOR_FORM_COMPLETED`; do not click `OK` unless Vision confirms |
| GnuCash reopens on the last-used screen in the next run | Treat startup reset or forced clean launch as a V2 hardening task |

## 10. What To Capture During Manual Build

As you build the actual PAD flow, record:

- Exact PAD action names used.
- Any UI selectors that work reliably.
- Any places where keyboard shortcuts are more reliable than clicks.
- Any coordinates used as a fallback.
- Any GnuCash prompt that appears after `File > Save` or `File > Quit`.

Those details should be added back to this document after the first successful PAD mock-mode run.

Known details from the current working build:

- Python helper runs use `Window style = Hidden`.
- Some menu actions required mouse coordinates relative to `Active window`.
- The `New Vendor` form field entry path is keyboard-driven because PAD could not reliably target individual text boxes inside the dialog.
