# GnuCash Setup

GnuCash setup is a later phase. This foundation does not require GnuCash to be installed.

## Intended V1 Use

GnuCash will be treated as a UI-only legacy finance system. The automation must not use GnuCash APIs, Python bindings, direct database writes, or `.gnucash` file manipulation.

## Later Setup Steps

When the time comes, the user will need to be guided through:

1. Downloading and installing GnuCash on Windows 10.
2. Creating a local demo company or book file.
3. Saving the demo file locally.
4. Opening the demo file manually.
5. Confirming the exact menu path for creating a vendor.
6. Confirming display scaling and screen resolution.
7. Practicing the manual supplier/vendor creation flow.

## Example Demo File Path

```text
C:\Users\<YourUser>\Documents\GnuCash\VisionAutomationDemo.gnucash
```

Do not commit `.gnucash` files.

## Manual Workflow To Confirm

The intended workflow is approximately:

```text
Open GnuCash
Open demo company file
Navigate to Business / Vendor / New Vendor
Enter supplier/vendor details
Save
Confirm vendor created
Return to main screen
Close GnuCash
```

The exact labels and menu path must be confirmed against the installed GnuCash version before PAD steps are built.
