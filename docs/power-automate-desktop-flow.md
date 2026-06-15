# Power Automate Desktop Flow

This document describes the planned PAD flow. It is not built in the foundation phase.

## PAD Responsibility

PAD is the executor. It opens applications, navigates known screens, enters data, takes screenshots, calls the Python helper, and updates status.

OpenAI Vision does not control the desktop in V1.

## Planned Flow

```text
Get one SharePoint supplier request
Mark request In Progress
Generate RunId
Open GnuCash
Take screenshot
Run Vision checkpoint: GN_CASH_MAIN_SCREEN
Navigate to New Vendor
Take screenshot
Run Vision checkpoint: NEW_VENDOR_SCREEN
Enter supplier fields
Take screenshot
Run Vision checkpoint: FIELD_VALUE_CHECK
Save vendor
Take screenshot
Run Vision checkpoint: SAVE_CONFIRMATION
Update SharePoint status
Close GnuCash
```

## PAD To Python Handoff

PAD should pass structured input to Python. A JSON file is recommended:

```json
{
  "run_id": "2026-06-15-143000-ABC123",
  "supplier_request_id": "42",
  "checkpoint_type": "NEW_VENDOR_SCREEN",
  "screenshot_path": "screenshots/archive/2026-06-15-143000-ABC123/step-002.png",
  "expected_screen": "GnuCash New Vendor screen",
  "expected_field": null,
  "expected_value": null,
  "supplier_context": {
    "supplier_legal_name": "Blue Kite Consulting Ltd"
  }
}
```

## Python To PAD Output

Python should return JSON that PAD can read:

```json
{
  "checkpoint_type": "NEW_VENDOR_SCREEN",
  "status": "continue",
  "screen_state": "new_vendor_screen_visible",
  "confidence": 0.96,
  "audit_comment": "Mock mode: assuming the New Vendor screen is visible.",
  "visible_errors": [],
  "extracted_reference": null,
  "raw_model_response_path": "logs/2026-06-15-143000-ABC123/vision-response.json"
}
```

## Navigation Preference Order

Use this order where possible:

1. UI selectors
2. Menus and keyboard shortcuts
3. Image recognition
4. Fixed coordinates

Coordinates may be used in V1 if needed, but they must be documented because they can break when display scaling or resolution changes.
