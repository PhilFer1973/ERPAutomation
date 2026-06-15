# Screen Analysis Prompt

Validate the screenshot for the requested checkpoint.

Return strict JSON with:

- checkpoint_type
- status
- screen_state
- confidence
- audit_comment
- visible_errors
- extracted_reference

Allowed statuses are:

- continue
- stop_for_review
- failed
- complete_success

If the expected screen or value is not visible, return `stop_for_review` or `failed`.
