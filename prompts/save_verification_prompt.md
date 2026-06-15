# Save Verification Prompt

Inspect the screenshot and decide whether the supplier/vendor save appears to have completed successfully.

For the current GnuCash V1 design, returning to the Accounts screen after clicking `OK` is not final proof by itself. Final proof comes from the Vendors tab showing the created vendor row.

Return strict JSON only. If a vendor reference is visible, include it in `extracted_reference`. If the save cannot be verified with confidence, return `stop_for_review` or `failed`.
