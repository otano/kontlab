from django.test import TestCase

from documents.ocr_engine import parse_receipt


class ParseReceiptTests(TestCase):
    def test_parse_full_receipt(self):
        text = "CARREFOUR MARKET\n12 avenue de la Gare\nDate: 24/05/2026\nTOTAL TTC 45,90\nTVA 8,50"
        result = parse_receipt(text)
        self.assertEqual(result["date"], "2026-05-24")
        self.assertEqual(result["amount_ttc"], 45.90)
        self.assertEqual(result["vat"], 8.50)
        self.assertEqual(result["supplier"], "CARREFOUR MARKET")

    def test_parse_date_various_formats(self):
        result = parse_receipt("Date: 01-06-2026 Total 12.50")
        self.assertEqual(result["date"], "2026-06-01")

    def test_parse_no_amount(self):
        result = parse_receipt("No numbers here")
        self.assertIsNone(result["amount_ttc"])

    def test_parse_supplier_first_line(self):
        result = parse_receipt("LIDL\nArticle 1\nTotal 10.00")
        self.assertEqual(result["supplier"], "LIDL")
