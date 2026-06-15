# Scope

## Business Objective

The project demonstrates controlled AI-assisted supplier onboarding into a desktop finance system where the user interface is the only approved integration path.

The core objective is to show that AI can improve screen validation and audit evidence without being given free control of the finance process.

## V1 Scope

V1 includes:

- Microsoft Forms supplier intake
- SharePoint Lists queue and audit design
- Power Automate cloud flow design
- Power Automate Desktop execution design
- GnuCash vendor creation through the UI
- Python helper scaffold
- OpenAI Vision checkpoint validation pattern
- Mock mode for local development
- JSON schemas and tests
- Fictional sample supplier data
- Local screenshot and JSON log retention

## V1 Exclusions

V1 excludes:

- Bank details
- VAT number
- Payment terms
- Supplier amendments
- Supplier deletion
- AP invoice entry
- AP bill posting
- Payment processing
- Approval workflow
- Duplicate supplier detection
- Retry logic
- Failure emails to finance
- Direct GnuCash API, bindings, or database access
- Real production data

## Success Criteria

The foundation phase is successful when the repository has a clear structure, professional documentation, JSON schemas, sample data, a Python helper scaffold, mock Vision behavior, and tests that can run without external systems.

Later phases will be successful when a fictional supplier can move from a form submission to a confirmed GnuCash vendor record with retained audit evidence.

## Controls

V1 is control-conscious by design:

- PAD remains the scripted executor.
- Vision validates checkpoints only.
- Low confidence stops the process.
- Bank details are excluded.
- Screenshots and logs remain local.
- Real supplier data is not used.

## Assumptions

- The user will be guided through all future downloads and setup.
- GnuCash, Power Automate, SharePoint, Forms, and OpenAI credentials may not exist yet.
- The exact GnuCash menu path must be verified on the installed version before PAD is built.
- V1 is a portfolio-quality proof of concept, not production automation.
