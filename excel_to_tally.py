# excel_to_tally.py
# Converts Excel -> tally_import.xml for Tally Prime import
# Works with ANY number of ledger pairs (Ledger, Amount)
# Debit/Credit logic:
#   Negative amount = Debit
#   Positive amount = Credit

import re
from datetime import datetime
from pathlib import Path
import pandas as pd
from xml.etree.ElementTree import Element, SubElement, ElementTree

# -------- Helpers --------

def to_tally_date(val) -> str:
    """Return YYYYMMDD or empty string if invalid."""
    if pd.isna(val):
        return ""
    try:
        dt = pd.to_datetime(val, errors="coerce", dayfirst=True)
        if pd.isna(dt):
            return ""
        return dt.strftime("%Y%m%d")
    except Exception:
        return ""


def clean_headers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.replace("\n", " ", regex=True)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    return df


def detect_indices(columns) -> list[int]:
    """Find all N from headers like 'LEDGER NAME - N' and 'LEDGER AMOUNT - N'."""
    idxs = set()
    for col in columns:
        m1 = re.match(r"^LEDGER.*?(-\s*(\d+))$", col, flags=re.IGNORECASE)
        m2 = re.match(r"^.*AMOUNT.*?(-\s*(\d+))$", col, flags=re.IGNORECASE)
        if m1 and m1.group(2):
            idxs.add(int(m1.group(2)))
        if m2 and m2.group(2):
            idxs.add(int(m2.group(2)))
    return sorted(idxs)


def build_xml(df: pd.DataFrame, out_path: Path, company_name: str | None = None) -> dict:
    env = Element("ENVELOPE")
    header = SubElement(env, "HEADER")
    SubElement(header, "TALLYREQUEST").text = "Import Data"

    body = SubElement(env, "BODY")
    importdata = SubElement(body, "IMPORTDATA")

    reqdesc = SubElement(importdata, "REQUESTDESC")
    SubElement(reqdesc, "REPORTNAME").text = "Vouchers"
    if company_name:
        staticvars = SubElement(reqdesc, "STATICVARIABLES")
        SubElement(staticvars, "SVCURRENTCOMPANY").text = company_name

    reqdata = SubElement(importdata, "REQUESTDATA")

    rows_in_excel = 0
    vouchers_built = 0
    skipped = []

    indices = detect_indices(df.columns)

    auto_vno = 1  # For auto Voucher Numbers

    for ridx, row in df.iterrows():
        rows_in_excel += 1
        vtype = str(row.get("VOUCHER TYPE", "Journal") or "Journal")
        vdate = to_tally_date(row.get("DATE", ""))

        # Voucher Number: take from Excel or auto-generate
        vnum  = str(row.get("VOUCHER NO", "") or f"VCH-{auto_vno:03d}")
        ref   = str(row.get("REFERENCE NUMBER", "") or "")
        narr  = str(row.get("STANDARD NARRATION", "") or "")
        effdt = to_tally_date(row.get("EFFECTIVE DATE", row.get("DATE", ""))) or vdate

        if not vdate:
            skipped.append((ridx + 1, "Missing/invalid DATE"))
            continue

        tmsg = SubElement(reqdata, "TALLYMESSAGE", attrib={"xmlns:UDF": "TallyUDF"})
        v = SubElement(tmsg, "VOUCHER", ACTION="Create", VCHTYPE=vtype)
        SubElement(v, "VOUCHERTYPENAME").text = vtype
        SubElement(v, "DATE").text = vdate
        SubElement(v, "VOUCHERNUMBER").text = vnum
        if ref:
            SubElement(v, "REFERENCE").text = ref
        SubElement(v, "EFFECTIVEDATE").text = effdt
        if narr:
            SubElement(v, "NARRATION").text = narr

        lines_added = 0
        dr_total, cr_total = 0, 0

        for i in indices:
            # Match name/amount columns
            name_col = next((c for c in df.columns if re.fullmatch(fr".*LEDGER.*- {i}", c, flags=re.IGNORECASE)), None)
            amt_col  = next((c for c in df.columns if re.fullmatch(fr".*AMOUNT.*- {i}", c, flags=re.IGNORECASE)), None)
            if not name_col or not amt_col:
                continue

            lname = row.get(name_col)
            amt_val = row.get(amt_col)
            if pd.isna(lname) or pd.isna(amt_val):
                continue

            try:
                amount = float(str(amt_val).replace(",", ""))
            except Exception:
                continue

            if round(amount, 2) == 0.0:
                continue

            le = SubElement(v, "ALLLEDGERENTRIES.LIST")
            SubElement(le, "LEDGERNAME").text = str(lname).strip()
            SubElement(le, "ISDEEMEDPOSITIVE").text = "YES" if amount < 0 else "NO"
            SubElement(le, "AMOUNT").text = f"{amount:.2f}"

            if amount < 0:
                dr_total += abs(amount)
            else:
                cr_total += abs(amount)

            lines_added += 1

        # Check balancing
        if lines_added == 0:
            reqdata.remove(tmsg)
            skipped.append((ridx + 1, "No valid ledger lines"))
            continue

        if round(dr_total, 2) != round(cr_total, 2):
            reqdata.remove(tmsg)
            skipped.append((ridx + 1, f"Dr/Cr mismatch (DR={dr_total}, CR={cr_total})"))
            continue

        vouchers_built += 1
        auto_vno += 1

    # Write XML file
    out_path = Path(out_path)
    ElementTree(env).write(out_path, encoding="utf-8", xml_declaration=True)

    return {
        "rows_in_excel": rows_in_excel,
        "vouchers_built": vouchers_built,
        "rows_skipped": len(skipped),
        "skipped_details": skipped[:10],
        "output": str(out_path.resolve()),
    }


if __name__ == "__main__":
    # Ask for Excel path
    src_file = input("Enter path to Excel file (default: vouchers.xlsx): ").strip() or "vouchers.xlsx"
    src = Path(src_file)
    dst = Path("tally_import.xml")

    # Load and clean
    df = pd.read_excel(src)
    df = clean_headers(df)

    # Build XML
    summary = build_xml(df, dst, company_name=None)

    print(summary)
    print(f"✅ Wrote {summary['vouchers_built']} vouchers to {dst}")
