# Controls And Audit

This project is designed around controlled AI use in a finance process.

## Why AI Is Constrained

OpenAI Vision validates what appears on screen. It does not decide the whole route, control the desktop freely, approve suppliers, create bank records, or post accounting entries.

PAD remains responsible for the scripted route. The Python helper validates whether each checkpoint is safe enough to continue.

## Why PAD Remains The Executor

Power Automate Desktop is better suited for deterministic desktop execution:

- opening applications
- navigating menus
- typing values
- taking screenshots
- calling local scripts
- updating workflow status

This separation keeps the AI role understandable and auditable.

## Why Bank Details Are Excluded

Bank details are excluded from V1 because supplier bank data carries higher fraud, privacy, and control risk. A production version would need approval workflow, bank verification, segregation of duties, stronger access control, and audit retention.

## Screenshot Retention

Screenshots are useful audit evidence, but they may contain personal data. V1 stores them locally and excludes them from GitHub.

Recommended folders:

```text
screenshots/input/
screenshots/output/
screenshots/archive/
```

## JSON Logging

Each checkpoint should retain structured JSON showing:

- checkpoint type
- status
- confidence
- screen state
- visible errors
- audit comment
- extracted reference if visible

## Failure Handling

V1 favors stopping over continuing when there is uncertainty.

Failure examples:

- wrong screen
- required field missing
- visible error message
- save not verified
- confidence below threshold
- invalid JSON

The request should be marked `Failed` or `Needs Review`, with a clear failure reason.

## Production Limitations

This proof of concept is not production-ready. Production use would require:

- approval workflow
- duplicate detection
- bank detail controls
- secure credential storage
- monitoring and alerting
- retry strategy
- incident handling
- privacy and retention review
- access control
- segregation of duties
