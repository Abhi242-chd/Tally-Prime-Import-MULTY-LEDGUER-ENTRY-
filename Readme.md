# Excel to Tally Prime XML Converter

This script converts accounting voucher data from an Excel spreadsheet into an XML format compatible with TallyPrime.

It supports multiple ledger–amount pairs per voucher and automatically assigns Debit / Credit logic based on the amount's sign:

- **Negative amount (`-`)** &rarr; Debit (Dr)
- **Positive amount (`+`)** &rarr; Credit (Cr)

---

## Requirements

- **Python**: 3.12 or higher
- **Dependencies**:
  ```sh
  pip install pandas openpyxl
