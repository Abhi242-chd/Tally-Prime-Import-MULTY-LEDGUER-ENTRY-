# Excel to Tally Voucher Converter

Converts vouchers entered in an Excel template into an XML file that Tally can import, with checks that stop the errors Tally would otherwise reject.

**Why it exists:** Tally refuses to import entries with more than 2 decimal places, or entries that don't balance, and writes an error log instead. This tool catches both problems in Excel, before the import.

<!-- TODO: add a screenshot of the template and of the balance error message -->

## What it does

- Reads vouchers from an Excel template (`.xlsm`)
- Blocks saving when a voucher does not balance, and points to the row
- Rounds amounts to 2 decimal places
- Builds `tally_import.xml` ready for import into Tally
- Skips any voucher that does not balance, so it never reaches Tally

## Requirements

- Microsoft Excel with **macros enabled** (the balance check is a macro; if macros are off, the check does not run)
- Python 3 and `pandas` (only if running from source; the `.exe` needs neither)
- Tested on TallyPrime 5.1 and TallyPrime 6 (imports worked without issues). Other versions are untested.

## Step 1: Enter accounting data

Open `tally_voucher_template_10_ledgers.xlsm` and enter your vouchers.

The template supports:

- Date
- Voucher Type
- Narration
- Voucher Number
- Reference Number
- Effective Date
- Up to 10 pairs of Ledger Name and Amount per voucher

**Amount rules**

| Entry | Meaning |
|---|---|
| Negative amount | Debit (Dr.) |
| Positive amount | Credit (Cr.) |

- Each voucher must add up to **zero** (total debit = total credit).
- Amounts are rounded to 2 decimals when typed. If you paste values, check the result.
- Ledger names must match the names in Tally **exactly**, including spelling and spaces.

**Example: Sales voucher**

| DATE | VOUCHER TYPE | NARRATION | VOUCHER NO | LEDGER NAME - 1 | AMOUNT - 1 | LEDGER NAME - 2 | AMOUNT - 2 | LEDGER NAME - 3 | AMOUNT - 3 | LEDGER NAME - 4 | AMOUNT - 4 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 28-05-2024 | Sales | invoice no.1068 | invoice no.1068 | buyer | -1224.00 | SALE | 1037.10 | IGST | 186.68 | ROUNDING OFF | 0.22 |

Check: -1224.00 + 1037.10 + 186.68 + 0.22 = 0.00

**What the template checks when you save**

- If a voucher does not add up to zero, an error is shown with the row number, and the file will not save until it is fixed.

## Step 2: Convert to XML

**Option A: Executable**

1. Put the `.exe` in the same folder as the Excel file.
2. Double-click it.
3. Enter the Excel file path, or press Enter to use the default (`tally_voucher_template_10_ledgers.xlsm`).
4. The tool writes `tally_import.xml` in the same folder and prints a summary.

**Option B: From source**

```bash
pip install pandas openpyxl
python main.py
```

<!-- TODO: replace main.py with your script's real filename -->

The converter reads the first sheet of the workbook. Vouchers that do not balance are skipped and are not written to the XML.

## Step 3: Import into Tally

1. **Back up your company data first**, or test on a copy of the company.
2. Open the company in Tally.
3. Go to the Import option and choose Vouchers/Transactions, then select `tally_import.xml`.
   <!-- TODO: add exact menu path for your Tally version -->
4. Check the import result. Tally writes an error log for any entry it rejects.

## Troubleshooting

| Problem | Likely cause |
|---|---|
| Tally rejects an entry | Ledger name does not match Tally exactly, or an amount has more than 2 decimals |
| Fewer vouchers than expected in Tally | Some vouchers were skipped as unbalanced; check the summary printed by the converter |
| No balance error when saving | Macros are disabled in Excel |
| Antivirus warns about the `.exe` | Common with Python-built executables; run from source instead, or ask IT |

## Known limitations

- Works only when macros are enabled.
- Pasted values may bypass the 2-decimal rounding in the template. Paste as typed values and check them.
- Rounding each line can leave a voucher off by a small amount. Check balances after rounding.
- Does not check ledger names against your Tally ledger list.

## Notes

- The sample data above is fictional. Do not commit real company data to this repository.
- This tool prepares data for import. Always review the imported vouchers in Tally.
