import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import parse_blocks, check_block

GOOD = """From: Ayesha Khan <ayesha@company.local>
--
Ayesha Khan
IT Support Executive
Phone: +92 300 1112233
Company Name
This email is confidential and intended only for the recipient."""

class TestSignatureChecker(unittest.TestCase):
    def test_fully_compliant(self):
        name, missing = check_block(GOOD)
        self.assertEqual((name, missing), ("Ayesha Khan", []))

    def test_missing_job_title(self):
        block = """From: Bilal Ahmed <bilal@company.local>
--
Bilal Ahmed
Phone: 0300 1234567"""
        _, missing = check_block(block)
        self.assertEqual(missing, ["job title", "disclaimer"])

    def test_missing_phone(self):
        block = """From: Sara Malik <sara@company.local>
--
Sara Malik
IT Officer
This email is confidential."""
        _, missing = check_block(block)
        self.assertEqual(missing, ["phone number"])

    def test_missing_name(self):
        block = """From: Omar Farooq <omar@company.local>
--
IT Support Executive
Phone: 0300 9998888
This email is confidential."""
        _, missing = check_block(block)
        self.assertEqual(missing, ["name"])

    def test_missing_disclaimer(self):
        block = """From: Sara Malik <sara@company.local>
--
Sara Malik
IT Officer
Phone: 0300 1234567"""
        _, missing = check_block(block)
        self.assertEqual(missing, ["disclaimer"])

    def test_blocks_split_on_separator(self):
        self.assertEqual(len(parse_blocks(GOOD + "\n---\n" + GOOD)), 2)

    def test_empty_text(self):
        self.assertEqual(parse_blocks(""), [])

    def test_phone_with_dashes(self):
        block = """From: Sara Malik <sara@company.local>
--
Sara Malik
IT Officer
Phone: +92-300-1112233
This email is confidential."""
        _, missing = check_block(block)
        self.assertEqual(missing, [])
