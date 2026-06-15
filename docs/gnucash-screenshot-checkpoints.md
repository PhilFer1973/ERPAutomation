# GnuCash Screenshot Checkpoints

This document records the actual GnuCash screens captured for the V1 supplier onboarding prototype. It is documentation and Vision design only. It does not build the Power Automate Desktop flow.

## Confirmed Local Demo Setup

Demo file:

```text
C:\Users\Philip\Documents\GnuCash\VisionAutomationDemo.gnucash
```

Screenshot folder:

```text
C:\Users\Philip\Downloads\ERPAutomation\screenshots\input
```

Screenshots are intentionally ignored by Git because they may contain local or personal data in later runs.

## Observed Menu Paths

New vendor creation path:

```text
Business > Vendor > New Vendor...
```

Created vendor verification path:

```text
Business > Vendor > Vendors Overview
```

## Observed New Vendor Form

The `New Vendor` dialog has two visible tabs:

- `Vendor`
- `Payment Information`

The `Vendor` tab contains:

- `Vendor Number`
- `Company Name`
- `Active`
- `Payment Address > Name`
- `Payment Address > Address`
- `Phone`
- `Fax`
- `Email`
- `Notes`
- `Help`
- `Cancel`
- `OK`

## Observed Field Mapping

| Supplier request field | GnuCash field observed in screenshots | Notes |
|---|---|---|
| Supplier legal name | `Company Name` | Required V1 target field |
| Contact name | `Payment Address > Name` | Observed sample uses `John Doe` |
| Address | `Payment Address > Address` line 1 | Observed sample uses `1 New Street` |
| City | `Payment Address > Address` line 2 | Observed sample uses `London` |
| Country | `Payment Address > Address` line 3 | Observed sample uses `UK` |
| Postcode | `Payment Address > Address` line 4 | Observed sample uses `SW1 2AY` |
| Email | `Email` | Observed sample uses `john.doe@testco.com` |
| Currency | Not visible on the `Vendor` tab | May remain a SharePoint/form value unless later GnuCash setup reveals a visible field |
| Vendor number | `Vendor Number` | Left blank in the observed New Vendor screenshot and auto-assigned as `000001` after save |

## Screenshot Checkpoint Catalogue

| Screenshot | Checkpoint type | Expected visual evidence | PAD decision when valid |
|---|---|---|---|
| `01-gnucash-main-screen.PNG` | `GN_CASH_MAIN_SCREEN` | Window title includes `VisionAutomationDemo.gnucash - Accounts - GnuCash`; accounts tab visible; top menu includes `Business` | Continue |
| `02-business-menu-open.PNG` | `BUSINESS_MENU_OPEN` | `Business` menu is open; menu shows `Customer`, `Vendor`, `Employee`, `Business Linked Documents`, `Sales Tax Table`, `Billing Terms Editor` | Continue |
| `03-vendor-menu-path.PNG` | `VENDOR_NEW_MENU_PATH` | `Business > Vendor` submenu is open; `New Vendor...` is visible | Continue |
| `04-new-vendor-blank-form.PNG` | `NEW_VENDOR_FORM_BLANK` | `New Vendor` dialog is visible; `Vendor` tab selected; `Company Name`, address, and email fields are blank | Continue |
| `05-new-vendor-completed-before-save.PNG` | `NEW_VENDOR_FORM_COMPLETED` | `New Vendor - Test Co Limited` dialog is visible; entered field values are visible; `OK` button is visible | Continue |
| `06-after-save-confirmation-or-return-screen.PNG` | `POST_SAVE_RETURN_SCREEN` | Accounts screen is visible again after `OK`; title begins with `*VisionAutomationDemo.gnucash`, indicating unsaved book changes | Continue to final record verification |
| `07-created-vendor-path.PNG` | `VENDOR_OVERVIEW_MENU_PATH` | `Business > Vendor` submenu is open; `Vendors Overview` is visible | Continue |
| `08-created-vendor-visible.PNG` | `CREATED_VENDOR_VISIBLE` | `Vendors` tab is visible; row shows `Test Co Limited`, vendor number `000001`, address `1 New Street`, and `London` | Complete success |

## Important Design Notes

The `POST_SAVE_RETURN_SCREEN` checkpoint is not enough by itself to prove the vendor was created. It only proves GnuCash returned to the accounts screen after the `OK` action. The final proof is the `CREATED_VENDOR_VISIBLE` checkpoint on the Vendors tab.

The asterisk in the GnuCash window title after saving the vendor suggests the GnuCash book has unsaved changes. Later PAD design should handle this deliberately, most likely by saving the book before closing. That behavior is not implemented yet.

## Questions To Confirm Before PAD Build

Before building the PAD flow, confirm:

- Whether `Vendor Number` should always be left blank for GnuCash to auto-assign.
- Whether the address line order should remain `Address`, `City`, `Country`, `Postcode`.
- Whether the final PAD flow should click toolbar `Save` after vendor creation before closing GnuCash.
- Whether `Currency` should remain outside GnuCash V1 entry because no visible field appeared in the captured `Vendor` tab.
