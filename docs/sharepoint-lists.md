# SharePoint Lists

V1 uses SharePoint Lists for the operational queue, audit log, and simple configuration.

## SupplierOnboardingRequests

Purpose: operational queue and high-level status.

| Column | Type | Required | Notes |
|---|---|---:|---|
| Title | Single line text | Yes | Can mirror SupplierLegalName |
| SupplierLegalName | Single line text | Yes | Legal supplier name |
| ContactName | Single line text | Yes | Supplier contact |
| SupplierEmail | Single line text | Yes | Email notification target |
| Address | Multiple lines text | Yes | Street address |
| City | Single line text | Yes | City |
| Postcode | Single line text | Yes | Postcode |
| Country | Single line text | Yes | Country |
| Currency | Choice or text | Yes | Default likely GBP |
| Status | Choice | Yes | New, In Progress, Created, Needs Review, Failed |
| RunId | Single line text | No | Generated per automation run |
| GnuCashVendorId | Single line text | No | If visible or available |
| FailureReason | Multiple lines text | No | Error explanation |
| SubmittedAt | Date/time | Yes | From form/cloud flow |
| ProcessedAt | Date/time | No | Completed or failed timestamp |

Suggested statuses:

```text
New
In Progress
Created
Needs Review
Failed
```

## AutomationRunLog

Purpose: detailed audit log.

| Column | Type | Required | Notes |
|---|---|---:|---|
| RunId | Single line text | Yes | Groups steps for one supplier |
| SupplierRequestId | Number or text | Yes | Source SharePoint item ID |
| StepNumber | Number | Yes | Sequence |
| StepName | Single line text | Yes | Example: Open GnuCash |
| ScreenshotPath | Single line or multiple lines | No | Local path in V1 |
| VisionPromptType | Single line text | No | Example: NEW_VENDOR_SCREEN |
| VisionResponseJson | Multiple lines text | No | Complete model response |
| VisionConfidence | Number | No | Decimal confidence |
| ActionTaken | Multiple lines text | No | What PAD did |
| StepStatus | Choice or text | Yes | Success, Failed, Needs Review |
| ErrorMessage | Multiple lines text | No | Any error |
| CreatedAt | Date/time | Yes | Timestamp |

## AutomationConfig

Purpose: simple configurable values.

| Column | Type | Required | Notes |
|---|---|---:|---|
| ConfigKey | Single line text | Yes | Example: GnuCashFilePath |
| ConfigValue | Multiple lines text | Yes | Value |
| Description | Multiple lines text | No | Explanation |

Suggested config keys:

```text
GnuCashFilePath
ScreenshotRootFolder
ConfidenceThreshold
MockMode
OpenAIModel
```
