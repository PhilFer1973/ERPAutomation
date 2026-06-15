# Architecture

## High-Level Flow

```text
External supplier
    -> Microsoft Forms
    -> Power Automate cloud flow
    -> SharePoint List: SupplierOnboardingRequests
    -> Power Automate Desktop
    -> GnuCash desktop UI
    -> Screenshot checkpoint
    -> Python vision_agent helper
    -> OpenAI Vision or mock mode
    -> JSON validation and audit log
    -> SharePoint status update
    -> Success email
```

## Components

| Component | Role |
|---|---|
| Microsoft Forms | Collect supplier details from the external supplier |
| Power Automate cloud flow | Validate form data and create SharePoint queue items |
| SharePoint Lists | Store requests, run logs, and configuration |
| Power Automate Desktop | Execute the controlled desktop steps |
| GnuCash | Simulated legacy finance system |
| Python helper | Validate Vision JSON, apply confidence rules, and write logs |
| OpenAI Vision | Inspect screenshots and return structured validation results |

## Data Flow

Supplier data begins in Microsoft Forms and becomes a SharePoint item. PAD reads or receives the item, enters the supplier into GnuCash, and writes back status. Screenshots and Vision responses are retained as local audit artifacts in V1.

## Control Flow

PAD performs a known step, captures a screenshot, and asks the Python helper to validate that checkpoint. The helper returns a simple status such as `continue`, `stop_for_review`, `failed`, or `complete_success`.

PAD only continues when the checkpoint response is valid and confidence meets the configured threshold.

## Error Flow

Typical stop conditions include:

- GnuCash not visible
- Expected screen not found
- Required value not visible
- Save not confirmed
- Visible error detected
- Vision confidence below threshold
- Invalid JSON response

In V1, the process stops, logs the issue, and marks the request as `Failed` or `Needs Review`. Retry behavior is intentionally deferred.
