# GnuCash Manual Vendor Creation Steps

This document records the manual GnuCash workflow supplied after the demo file and screenshots were created. It is a design reference for the future Power Automate Desktop flow. It does not implement automation.

Source note kept locally:

```text
C:\Users\Philip\Downloads\ERPAutomation\screenshots\input\gnucash-manual-vendor-creation-steps.txt
```

## Manual Steps

1. Open GnuCash.
2. Open `VisionAutomationDemo.gnucash`.
3. Confirm the main Accounts screen appears.
4. Click `Business`.
5. Click `Vendor`.
6. Click `New Vendor`.
7. Confirm the New Vendor form opens.
8. Enter supplier legal name.
9. Enter contact name.
10. Enter email.
11. Enter address lines using the confirmed V1 order: address, city, country, postcode.
12. Click `OK`.
13. Confirm the vendor is visible/saved.
14. Return to the main screen.
15. Click `File`.
16. Click `Save`.
17. Click `Quit`.

## Confirmed V1 Decisions

- Leave `Vendor Number` blank and allow GnuCash to auto-assign it.
- Enter address lines as `Address`, `City`, `Country`, `Postcode`.
- After confirming the created vendor is visible, return to the main screen, click `File > Save`, then `File > Quit`.
- Keep `Currency` in Microsoft Forms/SharePoint data only for V1 unless a visible GnuCash field is later confirmed.
