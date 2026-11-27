### Step 1: Enter Accounting Data

Open `tally_voucher_template_10_ledgers.xlsm` and enter your voucher details.

The template supports:

- Date
- Voucher Type
- Standard Narration
- Voucher Number
- Reference Number
- Effective Date
- Up to 7 Ledger Name and Amount pairs

**Example: Sales Voucher**

| DATE | VOUCHER TYPE | NARRATION | VOUCHER NO | LEDGER NAME - 1 | AMOUNT - 1 | LEDGER NAME - 2 | AMOUNT - 2 | LEDGER NAME - 3 | AMOUNT - 3 |
|---|---|---|---|---|---:|---|---:|---|---:|
| 28-05-2024 | Sales | invoice no.1068 | invoice no.1068 | buyer | -1224.00 | SALE | 1037.10 | IGST | 186.68 |

You can enter up to seven ledger–amount pairs in each voucher.

**Entering amounts:**
- Negative amount = Debit (Dr.)
- Positive amount = Credit (Cr.)
- Amounts are automatically rounded to two decimal places.
- Each voucher must balance: total Debit must equal total Credit.

The template checks the balance when you save. If the amounts do not match, it displays an error and asks you to correct the entry before saving.