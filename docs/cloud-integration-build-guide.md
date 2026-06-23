# Cloud Integration Build Guide

This guide turns the existing cloud-side design into a practical V1 build order.

## Goal

Wrap the proven local PAD vendor-creation flow in a lightweight Microsoft cloud layer:

```text
Microsoft Forms
-> SharePoint queue item
-> PAD picks up and processes item
-> PAD writes final status
-> cloud flow sends success email
```

## V1 Build Order

Build in this sequence:

1. Create Microsoft Form
2. Create SharePoint lists
3. Create cloud flow that writes `New` queue items
4. Decide how PAD will pick up `New` items locally
5. Add success notification driven by SharePoint status `Created`

Do not try to solve unattended orchestration, recovery routing, or retries in the same pass.

## Step 1: Create The Form

Use [microsoft-forms-design.md](microsoft-forms-design.md).

Required output:

- one form with the eight V1 fields
- one test response using fictional data

## Step 2: Create SharePoint Lists

Use [sharepoint-lists.md](sharepoint-lists.md).

Minimum V1 lists:

- `SupplierOnboardingRequests`
- `AutomationRunLog`

Optional for later:

- `AutomationConfig`

## Step 3: Build The Intake Cloud Flow

Recommended flow name:

```text
ERPAutomation_Supplier_Intake_V1
```

Recommended actions:

1. trigger: `When a new response is submitted`
2. `Get response details`
3. validate required fields
4. `Create item` in `SupplierOnboardingRequests`
5. set:
   - `Title = SupplierLegalName`
   - `Status = New`
   - `SubmittedAt = utcNow()`

## Step 4: Define PAD Pickup Contract

For V1, keep this simple.

PAD should expect a SharePoint item with:

- supplier core fields
- `Status = New`
- an item ID that can be incorporated into `RunId`

Recommended V1 runtime behavior:

1. PAD selects one `New` item
2. PAD sets `Status = In Progress`
3. PAD runs the proven local GnuCash flow
4. PAD writes back:
   - `Status`
   - `RunId`
   - `ProcessedAt`
   - `FailureReason` when needed
   - `GnuCashVendorId` if visible

## Step 5: Success Notification

Recommended V1 flow name:

```text
ERPAutomation_Supplier_Completion_V1
```

Recommended trigger:

```text
When an item in SupplierOnboardingRequests is modified
```

Condition:

```text
Status = Created
```

Action:

- send success email to `SupplierEmail`

## Suggested V1 Boundaries

Keep these out of the first cloud build:

- unattended desktop triggering
- item locking beyond simple status changes
- duplicate detection
- retry queues
- failure email workflows
- document-library audit storage

## What "Done" Looks Like

Cloud integration is good enough for V1 when:

- a Forms response creates a SharePoint queue item
- PAD can process that queue item using the proven local flow
- the SharePoint item ends in `Created`, `Needs Review`, or `Failed`
- a `Created` item triggers the success email
