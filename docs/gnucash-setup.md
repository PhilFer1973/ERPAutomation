# GnuCash Setup

## Intended V1 Use

GnuCash will be treated as a UI-only legacy finance system. The automation must not use GnuCash APIs, Python bindings, direct database writes, or `.gnucash` file manipulation.

## Confirmed Local Setup

GnuCash is installed and the local demo file has been created outside the repo:

```text
C:\Users\Philip\Documents\VisionAutomationDemo.gnucash
```

Actual screenshots have been captured in:

```text
C:\Users\Philip\Downloads\ERPAutomation\screenshots\input
```

See [gnucash-screenshot-checkpoints.md](gnucash-screenshot-checkpoints.md) for the observed screens, menu paths, field names, and Vision checkpoint catalogue.

See [gnucash-manual-vendor-creation-steps.md](gnucash-manual-vendor-creation-steps.md) for the confirmed manual workflow and close-out sequence.

## Setup Steps Already Completed

The following are complete:

1. GnuCash installed locally.
2. Demo company/book file created.
3. Demo file saved outside the repository.
4. Manual screenshots captured for the V1 path.
5. Vendor creation and verification menu paths captured.

## Example Demo File Path

```text
C:\Users\Philip\Documents\VisionAutomationDemo.gnucash
```

Do not commit `.gnucash` files.

## Manual Workflow To Confirm

The observed workflow is:

```text
Open GnuCash
Open demo company file
Navigate to Business > Vendor > New Vendor...
Enter supplier/vendor details
Click OK
Return to accounts screen
Navigate to Business > Vendor > Vendors Overview
Confirm vendor is visible
Return to main screen
Click File > Save
Click File > Quit
GnuCash closes
```

The exact labels are now captured in screenshots. V1 should leave `Vendor Number` blank, enter address lines as `Address`, `City`, `Country`, `Postcode`, keep `Currency` outside GnuCash UI entry, and explicitly save the GnuCash book before quitting.
