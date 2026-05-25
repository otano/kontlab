import re
from datetime import datetime


def parse_receipt(text):
    fields = {
        "date": None,
        "amount_ttc": None,
        "vat": None,
        "supplier": None,
    }

    date_match = re.search(
        r"(\d{2}[/-]\d{2}[/-]\d{4})", text
    )
    if date_match:
        try:
            fields["date"] = datetime.strptime(
                date_match.group(1).replace("-", "/"), "%d/%m/%Y"
            ).date().isoformat()
        except ValueError:
            pass

    amount_match = re.search(
        r"(?:total|ttc|net\s*[\s:])\s*[:\s]*(\d+[.,]\d{2})",
        text,
        re.IGNORECASE,
    )
    if not amount_match:
        amount_match = re.search(r"(\d+[.,]\d{2})\s*[€€]", text)
    if not amount_match:
        amount_match = re.search(r"(\d+[.,]\d{2})\s*$", text, re.MULTILINE)
    if amount_match:
        fields["amount_ttc"] = float(
            amount_match.group(1).replace(",", ".")
        )

    vat_match = re.search(
        r"(?:tva|t.v.a)\s*[:\s]*(\d+[.,]\d{2})",
        text,
        re.IGNORECASE,
    )
    if vat_match:
        fields["vat"] = float(vat_match.group(1).replace(",", "."))

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if lines:
        fields["supplier"] = lines[0]

    return fields
