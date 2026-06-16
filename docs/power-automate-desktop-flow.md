# Power Automate Desktop Flow

This document describes the planned PAD flow. It is not built in this phase.

The current design is based on actual GnuCash screenshots captured from the local demo file. See [gnucash-screenshot-checkpoints.md](gnucash-screenshot-checkpoints.md).

The confirmed manual workflow and close-out sequence are documented in [gnucash-manual-vendor-creation-steps.md](gnucash-manual-vendor-creation-steps.md).

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
Open Business menu
Take screenshot
Run Vision checkpoint: BUSINESS_MENU_OPEN
Open Vendor submenu
Take screenshot
Run Vision checkpoint: VENDOR_NEW_MENU_PATH
Click New Vendor...
Take screenshot
Run Vision checkpoint: NEW_VENDOR_FORM_BLANK
Enter supplier fields
Take screenshot
Run Vision checkpoint: NEW_VENDOR_FORM_COMPLETED
Click OK
Take screenshot
Run Vision checkpoint: POST_SAVE_RETURN_SCREEN
Navigate to Business > Vendor > Vendors Overview
Take screenshot
Run Vision checkpoint: VENDOR_OVERVIEW_MENU_PATH
Open Vendors Overview
Take screenshot
Run Vision checkpoint: CREATED_VENDOR_VISIBLE
Update SharePoint status
Return to main screen
Click File > Save
Click File > Quit
```

## Observed GnuCash Field Mapping

| Supplier request field | GnuCash field |
|---|---|
| SupplierLegalName | Company Name |
| ContactName | Payment Address > Name |
| Address | Payment Address > Address line 1 |
| City | Payment Address > Address line 2 |
| Country | Payment Address > Address line 3 |
| Postcode | Payment Address > Address line 4 |
| SupplierEmail | Email |

The observed screenshots leave `Vendor Number` blank and GnuCash then displays vendor number `000001` in the Vendors tab.

`Currency` is not visible in the captured New Vendor `Vendor` tab and is confirmed to remain in SharePoint/Form data only for V1.

The confirmed close-out behavior is to save the GnuCash book through `File > Save` before quitting.

## PAD To Python Handoff

PAD should pass structured input to Python. A JSON file is recommended:

```json
{
  "run_id": "2026-06-15-143000-ABC123",
  "supplier_request_id": "42",
  "checkpoint_type": "NEW_VENDOR_FORM_BLANK",
  "screenshot_path": "screenshots/archive/2026-06-15-143000-ABC123/step-004-new-vendor-blank.png",
  "expected_screen": "GnuCash New Vendor dialog with the Vendor tab selected",
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
  "checkpoint_type": "NEW_VENDOR_FORM_BLANK",
  "status": "continue",
  "screen_state": "new_vendor_blank_form_visible",
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
