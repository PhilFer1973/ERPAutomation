# Power Automate Cloud Flow

This document describes the V1 cloud-flow design that should sit around the now-proven PAD vendor onboarding flow.

## Purpose

The cloud flow coordinates form intake, SharePoint queue creation, and final supplier notification after PAD has completed the desktop work.

## V1 Flow

```text
When a Microsoft Forms response is submitted
-> Get response details
-> Validate required supplier fields
-> Create item in SupplierOnboardingRequests
-> Make item available to Power Automate Desktop
-> Wait for or detect PAD completion
-> Send success email only after confirmed creation
```

## Recommended V1 Orchestration Pattern

The safest V1 cloud pattern is:

1. Microsoft Forms captures supplier data.
2. Cloud flow validates the response and creates one SharePoint queue item.
3. PAD reads from `SupplierOnboardingRequests` and performs the local GnuCash work.
4. PAD writes the final status and any visible vendor reference back to SharePoint.
5. Cloud flow sends a success email only when the SharePoint item reaches `Created`.

This keeps the cloud flow simple and avoids fragile real-time orchestration between cloud and desktop while the desktop process is still being hardened.

## Supplier Request Status Lifecycle

Recommended V1 states:

```text
New
In Progress
Created
Needs Review
Failed
```

Suggested ownership:

- cloud flow sets `New`
- PAD sets `In Progress` when it begins work
- PAD sets `Created`, `Needs Review`, or `Failed` at the end
- cloud flow reacts to the final state for notifications

## Required Field Validation

The form/cloud flow should require:

- Supplier legal name
- Contact name
- Supplier email
- Address
- City
- Postcode
- Country
- Currency

Incomplete records should not be sent to GnuCash. They should be marked `Needs Review` with a clear failure reason.

See [sharepoint-lists.md](sharepoint-lists.md) for the queue schema and [microsoft-forms-design.md](microsoft-forms-design.md) for the intake field design.

## Minimal V1 Cloud Actions

Recommended first cloud flow actions:

1. `When a new response is submitted`
2. `Get response details`
3. validate required fields
4. `Create item` in `SupplierOnboardingRequests`
5. set `Status = New`
6. copy the Forms timestamp into `SubmittedAt`
7. optionally send an internal acknowledgement to the finance/admin owner

The success email should be built as a separate state-change flow or as a later branch that reacts only when SharePoint status becomes `Created`.

## Success Email

To: supplier email from the form

Subject:

```text
Supplier onboarding complete
```

Body:

```text
{SupplierLegalName} has been successfully added to our system.
```

If a visible GnuCash vendor reference is available, it may be included later.

## Failure Email

Failure emails are excluded from V1. Finance/admin failure notification is a V2 feature.

## Licensing Note

Power Automate Desktop licensing and attended/unattended configuration may affect how cloud flows trigger desktop flows. This must be checked during the setup phase.

## V1 Build Boundary

The repo now contains:

- the proven local PAD flow design
- the SharePoint queue shape
- the expected request fields

The missing tenant-side build work is:

- creating the Microsoft Form
- creating the SharePoint lists
- creating the cloud flow in Power Automate
- deciding how PAD will pick up `New` items in your environment
