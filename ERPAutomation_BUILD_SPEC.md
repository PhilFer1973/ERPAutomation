# ERPAutomation — AI-Guided Legacy ERP Supplier Onboarding Automation

## 1. Project summary

This project builds a proof-of-concept finance automation system that uses Microsoft Forms, SharePoint Lists, Power Automate, Power Automate Desktop, Python, OpenAI Vision, and GnuCash to simulate supplier/vendor onboarding into a legacy ERP system where no practical API integration is available.

The core idea is:

> Power Automate Desktop follows a controlled, scripted path. OpenAI Vision acts as the screen validation, verification, and audit-intelligence layer.

This is not intended to be a fully autonomous agent that freely controls the desktop. It is a controlled finance automation pattern where AI vision is used to confirm screen state, verify fields, detect visible errors, and provide audit commentary.

The repository name is:

```text
ERPAutomation
```

The project-facing title can be:

```text
AI-Guided Legacy ERP Supplier Onboarding Automation
```

or:

```text
AI-Guided ERP Automation Using OpenAI Vision and Power Automate Desktop
```

---

## 2. Business problem

Many finance teams work with older ERP/accounting systems that are difficult to integrate with directly. The blocker is not always that no API technically exists. It may be that:

- the API is unavailable to finance;
- the API is not licensed;
- the API is undocumented;
- the ERP version is too old;
- IT support is unavailable;
- direct database writes are too risky;
- vendor support is slow or costly;
- the only approved operational route is the front-end user interface.

This project demonstrates a realistic pattern for automating such environments:

```text
External supplier onboarding request
→ controlled finance workflow
→ SharePoint operational queue
→ desktop RPA
→ OpenAI Vision screen validation
→ legacy ERP front-end entry
→ status update
→ requester notification
→ retained audit trail
```

---

## 3. V1 objective

Build a V1 prototype that:

1. Receives supplier onboarding data from an external supplier using Microsoft Forms.
2. Creates a SharePoint List item from the form response.
3. Triggers a Power Automate Desktop flow.
4. Opens GnuCash on a Windows 10 machine.
5. Navigates to the GnuCash vendor/supplier creation screen.
6. Uses OpenAI Vision checkpoints to confirm the correct screen and entered values.
7. Creates a new vendor/supplier in GnuCash.
8. Closes GnuCash after processing.
9. Updates SharePoint with the automation result.
10. Sends a simple success email to the supplier email address from the form.
11. Logs every major step, including screenshots and OpenAI Vision JSON responses.

---

## 4. Explicit V1 non-objectives

V1 must not include:

- bank details;
- VAT number capture;
- supplier amendments;
- supplier deletion;
- AP invoice entry;
- AP bill posting;
- payment processing;
- approval workflow;
- duplicate supplier detection;
- retry logic;
- finance failure notifications;
- direct GnuCash API access;
- direct GnuCash database writes;
- GnuCash Python bindings for creating records;
- production supplier data;
- production credentials;
- public storage of real screenshots or logs.

This project intentionally treats GnuCash as a UI-only legacy ERP/accounting system for the purpose of the prototype.

---

## 5. Confirmed V1 technology choices

| Area | Choice |
|---|---|
| Form front end | Microsoft Forms |
| Workflow orchestration | Power Automate cloud flow |
| Operational queue | SharePoint Lists |
| Desktop automation | Power Automate Desktop |
| Local finance system | GnuCash |
| Operating system | Windows 10 |
| AI screen analysis | OpenAI Vision |
| Helper layer | Python |
| OpenAI key storage | `.env` file |
| Screenshots/logs | Stored locally in V1 |
| GitHub repo | `ERPAutomation` |
| Repo visibility | Private initially recommended |
| Supplier data | Fictional/test data only |
| Processing style | One supplier at a time |
| GnuCash access | UI automation only |

---

## 6. System architecture

### 6.1 High-level flow

```text
External supplier
    ↓
Microsoft Forms
    ↓
Power Automate cloud flow
    ↓
SharePoint List: SupplierOnboardingRequests
    ↓
Power Automate Desktop trigger
    ↓
GnuCash opened on Windows 10
    ↓
PAD scripted navigation
    ↓
Screenshot checkpoints
    ↓
Python helper
    ↓
OpenAI Vision screen validation
    ↓
PAD continues or stops
    ↓
Vendor created in GnuCash
    ↓
SharePoint status updated
    ↓
Success email sent
    ↓
Run logs retained
```

### 6.2 Control principle

The key control principle is:

```text
PAD knows the route.
OpenAI Vision confirms the route is safe to continue.
```

OpenAI Vision should not be given unrestricted desktop control.

---

## 7. OpenAI Vision role

OpenAI Vision is the centrepiece of the project, but it should be used in a controlled way.

### 7.1 Vision should do

OpenAI Vision should:

- identify the visible screen;
- confirm whether the expected GnuCash screen is displayed;
- confirm whether expected fields are visible;
- confirm whether specific values appear to have been entered correctly;
- read visible status or error messages;
- confirm whether the vendor appears to have been saved;
- produce structured JSON;
- produce an audit-friendly explanation;
- return confidence scores;
- recommend whether PAD should continue, stop, or mark the item for review.

### 7.2 Vision should not do in V1

OpenAI Vision should not:

- freely browse the desktop;
- decide the entire route without constraints;
- approve suppliers;
- process bank details;
- enter payment information;
- post accounting transactions;
- delete or amend existing records;
- bypass validation;
- write directly to GnuCash data files;
- trigger emails by itself.

---

## 8. PAD and Vision interaction model

V1 should use a checkpoint-based model, not a fully agentic model.

### 8.1 Pattern

```text
PAD performs scripted step
→ PAD takes screenshot
→ PAD calls Python helper
→ Python sends screenshot + checkpoint instruction to OpenAI Vision
→ OpenAI Vision returns strict JSON
→ Python validates JSON
→ Python logs response
→ PAD reads result
→ PAD continues or stops
```

### 8.2 Example checkpoint types

| Checkpoint | Purpose |
|---|---|
| `GN_CASH_MAIN_SCREEN` | Confirm GnuCash is open and main screen visible |
| `NEW_VENDOR_SCREEN` | Confirm New Vendor screen is visible |
| `FIELD_VALUE_CHECK` | Confirm expected field/value appears on screen |
| `SAVE_CONFIRMATION` | Confirm vendor appears to have been saved |
| `FINAL_RECORD_CHECK` | Confirm created vendor appears visible |
| `ERROR_SCREEN_CHECK` | Detect visible error or unexpected screen |

---

## 9. Confidence thresholds

Use the following V1 thresholds:

```text
confidence >= 0.85
    Proceed

confidence >= 0.70 and < 0.85
    Mark checkpoint as uncertain.
    For V1, stop, log, and exit.
    Later V2 may retry screenshot or ask model again.

confidence < 0.70
    Stop, log, and exit.
```

Because this is a finance process, V1 should favour stopping over forcing the automation to continue.

---

## 10. Allowed action/status response types

Even though PAD follows the scripted path, the Vision response should still use a controlled vocabulary.

Recommended allowed response values:

```text
continue
stop_for_review
failed
complete_success
```

Optional future action types if the project later becomes more agentic:

```text
click_text
click_button
click_menu_path
type_into_field
press_key
wait
verify_screen
read_message
stop_for_review
complete_success
```

For V1, Vision does not need to control every click. It should validate screen states and return whether PAD can continue.

---

## 11. Supplier onboarding process

### 11.1 Source

The supplier onboarding request is submitted by an external supplier using Microsoft Forms.

### 11.2 No approval in V1

V1 has no approval workflow.

### 11.3 Processing

The cloud flow creates a SharePoint item. PAD then processes items one at a time.

### 11.4 Required supplier fields

V1 supplier fields:

| Field | Required | Notes |
|---|---:|---|
| Supplier legal name | Yes | Main GnuCash vendor name |
| Contact name | Yes | Contact/person |
| Email | Yes | Used for success notification |
| Address | Yes | Address field |
| City | Yes | Address field |
| Postcode | Yes | Address field |
| Country | Yes | Address field |
| Currency | Yes | Default likely GBP |

Excluded from V1:

- VAT number;
- company number;
- bank details;
- payment terms;
- supplier category;
- tax codes;
- procurement classification.

### 11.5 Validation

Microsoft Forms/Power Automate should validate required fields before the item is processed.

If a record is incomplete or invalid:

```text
Status = Needs Review
FailureReason = clear validation reason
```

No attempt should be made to enter incomplete records into GnuCash.

---

## 12. SharePoint Lists

Use multiple lists for clearer audit and maintainability.

### 12.1 List 1 — SupplierOnboardingRequests

Purpose: operational queue and high-level status.

Suggested columns:

| Column | Type | Required | Notes |
|---|---|---:|---|
| Title | Single line text | Yes | Can mirror SupplierLegalName |
| SupplierLegalName | Single line text | Yes | Legal supplier name |
| ContactName | Single line text | Yes | Supplier contact |
| SupplierEmail | Single line text | Yes | Email notification target |
| Address | Multiple lines text | Yes | Street address |
| City | Single line text | Yes | City |
| Postcode | Single line text | Yes | Postcode |
| Country | Single line text | Yes | Country |
| Currency | Choice/Text | Yes | Default GBP |
| Status | Choice | Yes | See statuses below |
| RunId | Single line text | No | Generated per automation run |
| GnuCashVendorId | Single line text | No | If available/visible |
| FailureReason | Multiple lines text | No | Error explanation |
| SubmittedAt | Date/time | Yes | From form/cloud flow |
| ProcessedAt | Date/time | No | Completed/failed timestamp |

Suggested V1 statuses:

```text
New
In Progress
Created
Needs Review
Failed
```

### 12.2 List 2 — AutomationRunLog

Purpose: detailed audit log.

Suggested columns:

| Column | Type | Required | Notes |
|---|---|---:|---|
| RunId | Single line text | Yes | Groups steps for one supplier |
| SupplierRequestId | Number/Text | Yes | Source SharePoint item ID |
| StepNumber | Number | Yes | Sequence |
| StepName | Single line text | Yes | e.g. Open GnuCash |
| ScreenshotPath | Single line/multiple lines | No | Local path in V1 |
| VisionPromptType | Single line text | No | e.g. NEW_VENDOR_SCREEN |
| VisionResponseJson | Multiple lines text | No | Store complete model response |
| VisionConfidence | Number | No | Decimal confidence |
| ActionTaken | Multiple lines text | No | What PAD did |
| StepStatus | Choice/Text | Yes | Success/Failed/Needs Review |
| ErrorMessage | Multiple lines text | No | Any error |
| CreatedAt | Date/time | Yes | Timestamp |

V1 should log every major action.

### 12.3 List 3 — AutomationConfig

Optional but recommended.

Purpose: store simple configurable values.

Suggested columns:

| Column | Type | Required | Notes |
|---|---|---:|---|
| ConfigKey | Single line text | Yes | e.g. GnuCashFilePath |
| ConfigValue | Multiple lines text | Yes | Value |
| Description | Multiple lines text | No | Explanation |

Possible config keys:

```text
GnuCashFilePath
ScreenshotRootFolder
ConfidenceThreshold
MockMode
OpenAIModel
```

---

## 13. Screenshot and log storage

For V1:

- store screenshots locally;
- store JSON logs locally;
- store screenshot paths in SharePoint;
- exclude screenshots/logs from GitHub;
- retain screenshots for V1;
- use fictional/test supplier data.

Recommended local folders:

```text
screenshots/input/
screenshots/output/
screenshots/archive/
logs/
```

Recommended run-specific folder pattern:

```text
screenshots/archive/{RunId}/
logs/{RunId}/
```

Example:

```text
screenshots/archive/2026-06-15-143000-ABC123/step-001-main-screen.png
logs/2026-06-15-143000-ABC123/step-001-vision-response.json
```

---

## 14. GnuCash setup

### 14.1 Environment

Use:

```text
Windows 10
GnuCash installed locally
Local preconfigured demo company file
Known display scaling
Known screen resolution if possible
```

### 14.2 Simplest setup

The simplest reliable approach is:

1. Install GnuCash locally.
2. Create one demo GnuCash company/book file.
3. Save it locally.
4. Ensure GnuCash can open it directly.
5. Start automation from the GnuCash main screen.
6. End automation by returning to the main screen and closing GnuCash.

### 14.3 Recommended file path

Use a configurable path, with an example like:

```text
C:\Users\<YourUser>\Documents\GnuCash\VisionAutomationDemo.gnucash
```

Do not commit `.gnucash` files to GitHub.

### 14.4 GnuCash workflow

The intended manual workflow is approximately:

```text
Open GnuCash
Open demo company file
Navigate to Business / Vendor / New Vendor
Enter supplier/vendor details
Save
Confirm vendor created
Return to main screen
Close GnuCash
```

Codex should not assume exact GnuCash menu labels without confirming them during setup. The documentation should instruct the user to verify the exact menu path once GnuCash is installed.

---

## 15. Power Automate cloud flow

### 15.1 Purpose

The cloud flow should:

1. Trigger when a Microsoft Forms response is submitted.
2. Get response details.
3. Validate required fields.
4. Create a SharePoint List item in `SupplierOnboardingRequests`.
5. Trigger or enable a Power Automate Desktop flow to process the item.
6. Send success email only after PAD has successfully completed the GnuCash creation process.

### 15.2 V1 email notification

On success:

```text
Subject: Supplier onboarding complete

Body:
{SupplierLegalName} has been successfully added to our system.
```

The email should be sent to the email address submitted on the form.

V1 should not email the supplier on failure. Failure notification to finance is a V2 feature.

---

## 16. Power Automate Desktop responsibilities

PAD should:

- receive or find one SharePoint item to process;
- mark it as `In Progress`;
- generate a `RunId`;
- open GnuCash;
- navigate using menus, UI selectors, keyboard shortcuts, and coordinates where necessary;
- take screenshots at each major step;
- call the Python helper with screenshot path and checkpoint type;
- read Python helper output;
- continue only where Vision validates the expected state;
- enter supplier data into GnuCash;
- save the vendor;
- verify save through Vision;
- update SharePoint status;
- close GnuCash;
- write run logs;
- stop, log, and exit on failure.

### 16.1 Coordinates

Coordinates are allowed in V1 if they work reliably.

However, use this preference order:

```text
1. UI selectors
2. Menus and keyboard shortcuts
3. Image recognition
4. AI-selected or fixed coordinates
```

Coordinates should be documented because they may break if screen scaling or resolution changes.

### 16.2 Attended/unattended

V1 should assume attended automation if licensing or unattended setup is unclear.

Codex should remind the user that Power Automate Desktop licensing and attended/unattended configuration may affect triggering from cloud flows.

---

## 17. Python helper

### 17.1 Purpose

The Python helper should handle:

- OpenAI API calls;
- screenshot encoding;
- prompt construction;
- strict JSON response validation;
- schema validation;
- confidence threshold logic;
- local JSON logging;
- mock mode;
- optional replay mode;
- returning a simple machine-readable result to PAD.

### 17.2 Why Python helper rather than direct PAD/OpenAI call

Power Automate Desktop is good for desktop interaction. Python is better for:

- OpenAI SDK usage;
- structured output validation;
- prompt version control;
- testability;
- mock mode;
- replay mode;
- logging;
- error handling.

### 17.3 Input from PAD to Python

The helper should accept structured inputs from PAD. This can be done through command-line arguments, a JSON file, or a simple local file exchange.

Although the user does not want to operate a CLI manually, PAD can call Python scripts behind the scenes.

Recommended PAD-to-Python input:

```json
{
  "run_id": "2026-06-15-143000-ABC123",
  "supplier_request_id": "42",
  "checkpoint_type": "NEW_VENDOR_SCREEN",
  "screenshot_path": "screenshots/archive/.../step-002-new-vendor.png",
  "expected_screen": "GnuCash New Vendor screen",
  "expected_field": null,
  "expected_value": null,
  "supplier_context": {
    "supplier_legal_name": "Blue Kite Consulting Ltd"
  }
}
```

### 17.4 Output from Python to PAD

Recommended output:

```json
{
  "checkpoint_type": "NEW_VENDOR_SCREEN",
  "status": "continue",
  "screen_state": "new_vendor_screen_visible",
  "confidence": 0.94,
  "audit_comment": "The screenshot appears to show the GnuCash New Vendor form.",
  "visible_errors": [],
  "extracted_reference": null,
  "raw_model_response_path": "logs/2026-06-15-143000-ABC123/step-002-response.json"
}
```

### 17.5 Python modules

Recommended source layout:

```text
src/
└── vision_agent/
    ├── __init__.py
    ├── config.py
    ├── openai_client.py
    ├── screen_analyser.py
    ├── action_schema.py
    ├── audit_logger.py
    └── main.py
```

### 17.6 Python files

#### `config.py`

Should:

- load `.env`;
- load model name;
- load confidence thresholds;
- load log/screenshot roots;
- validate required environment variables.

#### `openai_client.py`

Should:

- create OpenAI client;
- send screenshot and prompt;
- request strict structured JSON;
- return parsed response.

#### `screen_analyser.py`

Should:

- build checkpoint-specific prompts;
- call OpenAI client;
- apply confidence threshold logic;
- produce normalized result.

#### `action_schema.py`

Should:

- define expected JSON schema;
- validate model response;
- define allowed statuses and checkpoint types.

#### `audit_logger.py`

Should:

- write request/response logs;
- write run metadata;
- ensure logs are grouped by `RunId`;
- avoid crashing if log folder does not exist.

#### `main.py`

Should:

- act as the entrypoint for PAD;
- accept input from a JSON file or arguments;
- call the analysis function;
- write output JSON;
- print a simple result path or status for PAD.

---

## 18. Mock mode

Mock mode should be included.

### 18.1 Purpose

Mock mode allows testing without calling OpenAI.

It is useful because:

- PAD can be tested without API calls;
- the project can be demonstrated safely;
- Codex can write tests;
- errors in PAD/script handoff can be debugged separately;
- API cost is avoided during early development.

### 18.2 Example mock response

```json
{
  "checkpoint_type": "NEW_VENDOR_SCREEN",
  "status": "continue",
  "screen_state": "new_vendor_screen_visible",
  "confidence": 0.96,
  "audit_comment": "Mock mode: assuming the New Vendor screen is visible.",
  "visible_errors": [],
  "extracted_reference": null
}
```

Mock mode should be controlled by `.env` or config.

Example:

```text
MOCK_MODE=true
```

---

## 19. Replay mode

Replay mode is optional but recommended if not too complex.

Replay mode means saved screenshots can be re-analysed later without running GnuCash/PAD.

It is useful for:

- improving prompts;
- testing error screenshots;
- comparing model outputs;
- developing the Vision layer independently from desktop automation;
- building a repeatable demo.

Replay mode is not a blocker for V1.

---

## 20. Structured JSON response schema

### 20.1 Required response fields

OpenAI Vision should return strict JSON with at least:

```json
{
  "checkpoint_type": "NEW_VENDOR_SCREEN",
  "status": "continue",
  "screen_state": "new_vendor_screen_visible",
  "confidence": 0.94,
  "audit_comment": "The screenshot appears to show the expected New Vendor screen.",
  "visible_errors": [],
  "extracted_reference": null
}
```

### 20.2 Field definitions

| Field | Type | Required | Notes |
|---|---|---:|---|
| checkpoint_type | string | Yes | Must match input checkpoint |
| status | string | Yes | continue/stop_for_review/failed/complete_success |
| screen_state | string | Yes | Short description |
| confidence | number | Yes | 0 to 1 |
| audit_comment | string | Yes | Human-readable explanation |
| visible_errors | array | Yes | Any visible error/warning messages |
| extracted_reference | string/null | No | Vendor ID/reference if visible |

### 20.3 Allowed statuses

```text
continue
stop_for_review
failed
complete_success
```

---

## 21. Error handling

### 21.1 GnuCash not open

The agent/PAD should open GnuCash.

### 21.2 Wrong company file

Out of scope for V1. Keep setup simple and use a known local demo file.

### 21.3 New Vendor screen not found

```text
Log error
Set request Status = Failed
Set FailureReason
Close GnuCash if safe
Exit current item
Continue to next item if batch mode exists
```

### 21.4 Low Vision confidence

```text
Stop
Log
Set Status = Failed or Needs Review
Exit
```

For V1, use stopping rather than retrying.

### 21.5 Duplicate supplier

Out of scope for V1.

### 21.6 Required fields missing

The form/cloud flow should validate before submission/processing.

If encountered anyway:

```text
Status = Needs Review
FailureReason = Required fields missing
```

### 21.7 Save button does not work

```text
Log error
Set Status = Failed
Exit
```

### 21.8 Save cannot be verified

```text
Log error
Set Status = Failed or Needs Review
Exit
```

### 21.9 Retry logic

Not required in V1.

### 21.10 Failure email to finance

V2 feature.

---

## 22. Security and controls

### 22.1 API key

Use `.env`.

Never commit `.env`.

Provide `.env.example`.

Example `.env.example`:

```text
OPENAI_API_KEY=replace_me
OPENAI_MODEL=gpt-4.1-mini
MOCK_MODE=true
CONFIDENCE_THRESHOLD=0.85
LOG_ROOT=logs
SCREENSHOT_ROOT=screenshots
```

Model names may need updating depending on the current OpenAI account/API availability.

### 22.2 Personal data

V1 may use supplier names and email addresses but should use fictional/test data only.

### 22.3 Screenshots

Screenshots may contain personal data. Retain locally for V1 but exclude from GitHub.

### 22.4 Prompt and response logging

Log prompts and responses locally for audit and debugging.

Do not push real logs to GitHub.

### 22.5 Production warning

This is a proof of concept and should not be used for production supplier onboarding without additional controls, including:

- approval workflow;
- duplicate detection;
- bank detail verification;
- segregation of duties;
- secure credential storage;
- proper audit retention;
- data protection review;
- failure notifications;
- retry handling;
- monitoring.

---

## 23. Email notifications

### 23.1 Success email

To: supplier email from form

Subject:

```text
Supplier onboarding complete
```

Body:

```text
{SupplierLegalName} has been successfully added to our system.
```

If a GnuCash vendor reference is available:

```text
{SupplierLegalName} has been successfully added to our system.

Reference: {GnuCashVendorId}
```

### 23.2 Failure emails

Not required for V1.

V2 should notify finance/admin for:

- Failed;
- Needs Review;
- system exception;
- low confidence;
- duplicate warning.

---

## 24. Demonstration design

V1 should be suitable for a portfolio/demo.

Include:

- README;
- architecture diagram;
- setup guide;
- SharePoint List schema;
- GnuCash setup guide;
- Power Automate cloud flow guide;
- Power Automate Desktop flow guide;
- Vision agent design;
- controls and audit trail explanation;
- V2 roadmap.

The demo should show the robot working on screen.

Optional later deliverables:

- short walkthrough video;
- architecture image;
- dashboard;
- animated GIF;
- sample logs;
- anonymised sample screenshots.

---

## 25. Recommended repository structure

Codex should create or maintain:

```text
ERPAutomation/
├── README.md
├── docs/
│   ├── scope.md
│   ├── architecture.md
│   ├── setup-guide.md
│   ├── gnucash-setup.md
│   ├── power-automate-flow.md
│   ├── power-automate-desktop-flow.md
│   ├── sharepoint-lists.md
│   ├── vision-agent-design.md
│   ├── controls-and-audit.md
│   └── v2-roadmap.md
├── src/
│   └── vision_agent/
│       ├── __init__.py
│       ├── config.py
│       ├── openai_client.py
│       ├── screen_analyser.py
│       ├── action_schema.py
│       ├── audit_logger.py
│       └── main.py
├── tests/
│   ├── test_action_schema.py
│   ├── test_screen_analyser.py
│   └── test_mock_mode.py
├── sample-data/
│   ├── supplier-request-sample.json
│   └── supplier-request-sample.csv
├── screenshots/
│   ├── input/
│   ├── output/
│   └── archive/
├── logs/
├── prompts/
│   ├── system_prompt.md
│   ├── screen_analysis_prompt.md
│   └── save_verification_prompt.md
├── schemas/
│   ├── supplier_request.schema.json
│   └── vision_action.schema.json
├── .env.example
├── .gitignore
└── requirements.txt
```

---

## 26. Recommended `.gitignore`

```gitignore
.env
__pycache__/
*.pyc
.venv/
venv/
logs/
screenshots/input/
screenshots/output/
screenshots/archive/
*.gnucash
*.log
.DS_Store
Thumbs.db
```

---

## 27. Requirements file

Initial `requirements.txt` should likely include:

```text
openai
python-dotenv
pydantic
pytest
```

Optional later:

```text
pillow
jsonschema
rich
```

---

## 28. Sample supplier data

Create `sample-data/supplier-request-sample.json`:

```json
{
  "supplier_legal_name": "Blue Kite Consulting Ltd",
  "contact_name": "Sarah Ahmed",
  "supplier_email": "sarah.ahmed@example.com",
  "address": "10 Market Street",
  "city": "London",
  "postcode": "EC1A 1AA",
  "country": "United Kingdom",
  "currency": "GBP"
}
```

Create `sample-data/supplier-request-sample.csv`:

```csv
SupplierLegalName,ContactName,SupplierEmail,Address,City,Postcode,Country,Currency
Blue Kite Consulting Ltd,Sarah Ahmed,sarah.ahmed@example.com,10 Market Street,London,EC1A 1AA,United Kingdom,GBP
```

---

## 29. Documentation files Codex should create

### 29.1 `README.md`

Should include:

- project title;
- problem statement;
- high-level architecture;
- V1 scope;
- V1 exclusions;
- quick start for developers;
- local setup summary;
- how the Vision checkpoint pattern works;
- why GnuCash is used;
- why OpenAI Vision is used;
- why PAD is used;
- security warning;
- V2 roadmap summary.

### 29.2 `docs/scope.md`

Should include:

- business objective;
- V1 scope;
- V1 exclusions;
- success criteria;
- controls;
- assumptions.

### 29.3 `docs/architecture.md`

Should include:

- text architecture diagram;
- component descriptions;
- data flow;
- control flow;
- error flow.

### 29.4 `docs/setup-guide.md`

Should explain what the user must install/create when the time comes, including:

- Python;
- virtual environment;
- GnuCash;
- Power Automate Desktop;
- Microsoft Forms;
- SharePoint Lists;
- OpenAI API key;
- `.env`;
- test supplier data.

Important instruction for Codex:

> Codex must talk the user through any downloads, installations, accounts, credentials, SharePoint Lists, Microsoft Forms, Power Automate flows, or Power Automate Desktop steps when they become necessary. Do not assume the user has already created these unless confirmed.

### 29.5 `docs/gnucash-setup.md`

Should explain:

- install GnuCash;
- create demo company/book file;
- save locally;
- verify vendor/supplier menu path;
- keep screen resolution/scaling consistent;
- do not use real supplier data.

### 29.6 `docs/power-automate-flow.md`

Should explain planned cloud flow:

```text
When new Microsoft Forms response is submitted
→ get response details
→ validate fields
→ create SharePoint item
→ trigger PAD flow / mark for processing
→ send success email after PAD completion
```

### 29.7 `docs/power-automate-desktop-flow.md`

Should explain planned PAD flow:

```text
Get SharePoint item
Mark In Progress
Generate RunId
Open GnuCash
Screenshot
Vision checkpoint
Navigate to New Vendor
Screenshot
Vision checkpoint
Enter fields
Screenshot
Vision field/value checks
Save
Screenshot
Vision save check
Update SharePoint
Close GnuCash
```

### 29.8 `docs/sharepoint-lists.md`

Should include exact columns for:

- SupplierOnboardingRequests;
- AutomationRunLog;
- AutomationConfig.

### 29.9 `docs/vision-agent-design.md`

Should include:

- checkpoint pattern;
- prompt structure;
- response schema;
- confidence thresholds;
- mock mode;
- replay mode;
- audit logging.

### 29.10 `docs/controls-and-audit.md`

Should include:

- finance control story;
- why AI is constrained;
- screenshot retention;
- JSON logging;
- failure handling;
- V1 exclusions;
- production limitations.

### 29.11 `docs/v2-roadmap.md`

Should include:

- approval workflow;
- bank detail capture with controls;
- duplicate detection;
- finance failure emails;
- retry logic;
- SharePoint document library screenshot storage;
- dashboard;
- vendor amendment process;
- AP invoice entry;
- stronger credential storage;
- unattended automation;
- human-in-the-loop review screen;
- Teams notifications.

---

## 30. First Codex task

The first Codex task should not build the full automation.

The first Codex task should:

1. Create the project skeleton.
2. Create documentation files.
3. Create Python helper scaffold.
4. Create JSON schemas.
5. Create sample supplier data.
6. Create mock mode.
7. Create basic tests.
8. Create `.env.example`, `.gitignore`, and `requirements.txt`.
9. Avoid building the PAD automation until the foundation is reviewed.

Codex should also prepare clear setup instructions for anything the user must later download, install, create, or configure.

---

## 31. Acceptance criteria for first Codex task

The first task is complete when:

- repo structure exists;
- README exists;
- all docs listed above exist;
- `src/vision_agent/` package exists;
- `.env.example` exists;
- `.gitignore` exists;
- `requirements.txt` exists;
- supplier sample JSON and CSV exist;
- supplier request schema exists;
- Vision response schema exists;
- mock mode can return a valid fake response;
- tests can validate schema/mock behaviour;
- no real data, screenshots, logs, API keys, or `.gnucash` files are committed;
- setup guide clearly tells the user what they will need to install/create later;
- Codex has not attempted to automate GnuCash or PAD yet.

---

## 32. Suggested future phases

### Phase 1 — Foundation

Project skeleton, docs, schemas, Python mock mode.

### Phase 2 — OpenAI Vision helper

Real OpenAI Vision call, structured JSON, screenshot analysis.

### Phase 3 — GnuCash setup

Install/configure GnuCash, create demo file, verify manual workflow.

### Phase 4 — PAD prototype

Manual/attended PAD flow that opens GnuCash and executes scripted steps.

### Phase 5 — SharePoint and Forms

Microsoft Form, SharePoint Lists, cloud flow, basic status updates.

### Phase 6 — Integrated run

End-to-end supplier form to GnuCash creation.

### Phase 7 — Demo polish

README, screenshots, architecture diagram, walkthrough, V2 roadmap.

---

## 33. Important reminders for Codex

Codex must:

- keep the user informed before asking them to download/install/create anything;
- talk the user through setup steps clearly when the time comes;
- not assume GnuCash, Power Automate Desktop, SharePoint Lists, Microsoft Forms, or OpenAI credentials already exist unless confirmed;
- avoid committing secrets or real data;
- avoid direct GnuCash database/API integration;
- treat OpenAI Vision as a validation/audit layer in V1;
- keep PAD as the scripted executor;
- keep V1 simple and controlled;
- document assumptions clearly;
- ask before widening scope.

---

## 34. Build philosophy

This project should demonstrate:

```text
Controlled AI in finance automation.
Legacy system automation without direct integration.
OpenAI Vision as screen intelligence.
Power Automate Desktop as controlled execution.
SharePoint as the operational queue and audit layer.
Python as the reliable helper layer.
GnuCash as a lightweight legacy ERP/accounting simulation.
```

The tone of the project should be professional, finance-aware, and control-conscious.

The final project should show that AI can assist with legacy ERP automation, but only inside defined limits, with a clear audit trail and failure handling.
