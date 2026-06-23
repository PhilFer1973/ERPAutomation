# Microsoft Forms Design

This document defines the recommended V1 Microsoft Forms intake shape for supplier onboarding.

## Purpose

The form should gather only the fields the proven PAD flow can actually use in GnuCash V1.

Do not add extra fields yet for:

- bank details
- VAT
- payment terms
- attachments
- approvals

Those are later-phase concerns.

## Recommended Form Title

```text
New Supplier Onboarding Request
```

## Recommended Questions

| Order | Question | Internal field name | Type | Required | Notes |
|---:|---|---|---|---:|---|
| 1 | Supplier legal name | `SupplierLegalName` | Text | Yes | Maps to GnuCash `Company Name` |
| 2 | Supplier contact name | `ContactName` | Text | Yes | Maps to `Payment Address > Name` |
| 3 | Supplier email | `SupplierEmail` | Text | Yes | Maps to `Email` |
| 4 | Address line 1 | `Address` | Text | Yes | Maps to address line 1 |
| 5 | City | `City` | Text | Yes | Maps to address line 2 |
| 6 | Country | `Country` | Text | Yes | Maps to address line 3 |
| 7 | Postcode | `Postcode` | Text | Yes | Maps to address line 4 |
| 8 | Currency | `Currency` | Choice | Yes | Retained in SharePoint only for V1 |

## Recommended Currency Choices

Start with a narrow list:

```text
GBP
EUR
USD
```

If finance only needs GBP for the demo, a single-choice `GBP` list is acceptable.

## V1 Validation Expectations

The cloud flow should reject or route to review when:

- any required field is blank
- email is clearly malformed
- supplier legal name is missing
- address is incomplete for the local process

## Mapping To SharePoint

The form should map directly into `SupplierOnboardingRequests`:

| Forms field | SharePoint column |
|---|---|
| `SupplierLegalName` | `Title`, `SupplierLegalName` |
| `ContactName` | `ContactName` |
| `SupplierEmail` | `SupplierEmail` |
| `Address` | `Address` |
| `City` | `City` |
| `Country` | `Country` |
| `Postcode` | `Postcode` |
| `Currency` | `Currency` |

## Sample Submission

See:

- `sample-data/supplier-request-sample.json`
- `sample-data/supplier-request-sample.csv`

Those files match the current V1 intake shape.
