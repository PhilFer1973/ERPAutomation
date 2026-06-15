# Power Automate Cloud Flow

This document describes the planned cloud flow. It is not built in the foundation phase.

## Purpose

The cloud flow coordinates form intake, SharePoint queue creation, and final supplier notification after PAD has completed the desktop work.

## Planned V1 Flow

```text
When a Microsoft Forms response is submitted
-> Get response details
-> Validate required supplier fields
-> Create item in SupplierOnboardingRequests
-> Make item available to Power Automate Desktop
-> Wait for or detect PAD completion
-> Send success email only after confirmed creation
```

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
