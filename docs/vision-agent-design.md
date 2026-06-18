# Vision Agent Design

The Python `vision_agent` helper is the boundary between PAD and OpenAI Vision. It validates structured inputs, calls mock mode or Vision, validates the response, applies confidence thresholds, and writes audit logs.

## Checkpoint Pattern

```text
PAD executes known action
PAD captures screenshot
PAD calls Python helper with checkpoint context
Python returns strict JSON
PAD continues only if status and confidence allow it
```

Example checkpoint types:

- `GN_CASH_MAIN_SCREEN`
- `BUSINESS_MENU_OPEN`
- `VENDOR_NEW_MENU_PATH`
- `NEW_VENDOR_FORM_BLANK`
- `NEW_VENDOR_FORM_COMPLETED`
- `FIELD_VALUE_CHECK`
- `SAVE_CONFIRMATION`
- `POST_SAVE_RETURN_SCREEN`
- `VENDOR_OVERVIEW_MENU_PATH`
- `FINAL_RECORD_CHECK`
- `CREATED_VENDOR_VISIBLE`
- `ERROR_SCREEN_CHECK`

## Screenshot-Based V1 Checkpoint Sequence

The current V1 sequence is based on actual GnuCash screenshots captured from:

```text
C:\Users\Philip\Downloads\ERPAutomation\screenshots\input
```

| Step | Screenshot | Checkpoint type | Purpose |
|---:|---|---|---|
| 1 | `01-gnucash-main-screen.PNG` | `GN_CASH_MAIN_SCREEN` | Confirm GnuCash is open on the Accounts screen |
| 2 | `02-business-menu-open.PNG` | `BUSINESS_MENU_OPEN` | Confirm the Business menu is open |
| 3 | `03-vendor-menu-path.PNG` | `VENDOR_NEW_MENU_PATH` | Confirm `Business > Vendor > New Vendor...` is visible |
| 4 | `04-new-vendor-blank-form.PNG` | `NEW_VENDOR_FORM_BLANK` | Confirm the blank New Vendor form is ready |
| 5 | `05-new-vendor-completed-before-save.PNG` | `NEW_VENDOR_FORM_COMPLETED` | Confirm values are visible before save |
| 6 | `06-after-save-confirmation-or-return-screen.PNG` | `POST_SAVE_RETURN_SCREEN` | Confirm GnuCash returned to the accounts screen after OK |
| 7 | `07-created-vendor-path.PNG` | `VENDOR_OVERVIEW_MENU_PATH` | Confirm `Business > Vendor > Vendors Overview` is visible |
| 8 | `08-created-vendor-visible.PNG` | `CREATED_VENDOR_VISIBLE` | Confirm the created vendor row is visible |

See [gnucash-screenshot-checkpoints.md](gnucash-screenshot-checkpoints.md) for the detailed evidence and field mapping.

The working PAD flow should not treat `POST_SAVE_RETURN_SCREEN` as final success. It should verify `CREATED_VENDOR_VISIBLE`, update status, return to the main screen, save the GnuCash book through `File > Save`, and then quit GnuCash.

The PAD-facing checkpoint request examples live in `sample-data/pad-checkpoints/`, and the full sequence is defined in `pad/checkpoint-manifest.json`.

## Strict JSON Output

Vision responses must contain:

```json
{
  "checkpoint_type": "NEW_VENDOR_FORM_BLANK",
  "status": "continue",
  "screen_state": "new_vendor_blank_form_visible",
  "confidence": 0.96,
  "audit_comment": "The expected screen appears to be visible.",
  "visible_errors": [],
  "extracted_reference": null
}
```

Allowed statuses:

```text
continue
stop_for_review
failed
complete_success
```

## Confidence Threshold

The default threshold is `0.85`.

```text
confidence >= 0.85: continue
confidence >= 0.70 and < 0.85: stop_for_review
confidence < 0.70: failed
```

For a finance process, uncertain results stop the workflow rather than forcing progress.

## Mock Mode

Mock mode returns a valid fake Vision response without calling OpenAI. It is controlled by:

```text
MOCK_MODE=true
```

Mock mode supports:

- local tests
- early PAD handoff testing
- demos without API calls
- development without OpenAI cost

## Real OpenAI Vision Mode

When `MOCK_MODE=false`, the helper calls OpenAI through the Responses API. The request includes:

- system-level instructions that constrain the model to validation only
- `input_text` containing the checkpoint prompt
- `input_image` containing the screenshot as a base64 data URL
- a strict JSON schema response format matching `schemas/vision_action.schema.json`

After the API call, the helper still validates the JSON locally and applies the confidence policy before returning anything to PAD.

Real mode requires:

- `OPENAI_API_KEY` in `.env`
- a supported screenshot file type: `.png`, `.jpg`, `.jpeg`, or `.webp`
- a checkpoint request whose `screenshot_path` points to an existing file

If the API returns malformed JSON, an unsupported status, a mismatched checkpoint, or a low-confidence result, the helper stops or marks the checkpoint for review according to the V1 policy.

## Replay Mode Idea

Replay mode is a future option where saved screenshots can be analyzed again without running PAD or GnuCash. This would help improve prompts, compare model output, and build repeatable demos.

Replay mode is not required for the foundation phase.

## Audit Logging

Each Vision result should be logged under the run ID:

```text
logs/{RunId}/vision-response-{checkpoint}.json
```

In V1, logs and screenshots remain local and are excluded from GitHub.
