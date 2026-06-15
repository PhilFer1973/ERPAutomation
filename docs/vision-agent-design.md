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
- `NEW_VENDOR_SCREEN`
- `FIELD_VALUE_CHECK`
- `SAVE_CONFIRMATION`
- `FINAL_RECORD_CHECK`
- `ERROR_SCREEN_CHECK`

## Strict JSON Output

Vision responses must contain:

```json
{
  "checkpoint_type": "NEW_VENDOR_SCREEN",
  "status": "continue",
  "screen_state": "new_vendor_screen_visible",
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
