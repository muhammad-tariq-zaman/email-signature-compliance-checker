"""Check email signatures for the required elements.

Usage: python3 main.py signatures.txt
signatures.txt holds one signature block per sender, separated
by a line containing only "---". Each block starts with a
"From: Name <email>" line, then the signature lines (a "--"
line is ignored). Four elements are required:
- name: the sender's name appears in the signature.
- job title: a line mentions a role word (officer, executive,
  manager, engineer, support, analyst, administrator,
  technician, specialist, coordinator, lead, head).
- phone number: a number of at least 9 digits (spaces, dashes
  and brackets allowed).
- disclaimer: the words "confidential" or "disclaimer" appear.
A signature missing any element is NON-COMPLIANT and the
missing elements are listed.
"""
import argparse, re, sys

TITLE_KEYWORDS = ["officer", "executive", "manager", "engineer",
                  "support", "analyst", "administrator", "technician",
                  "specialist", "coordinator", "lead", "head"]
PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{7,}\d")

def parse_blocks(text):
    blocks = []
    current = []
    for line in text.splitlines():
        if line.strip() == "---":
            if current:
                blocks.append("\n".join(current))
                current = []
        else:
            current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks

def check_block(block):
    sender = ""
    body_lines = []
    for line in block.splitlines():
        if line.startswith("From:"):
            sender = line[5:].strip()
        elif line.strip() == "--":
            continue
        else:
            body_lines.append(line)
    name = sender.split("<")[0].strip()
    body = "\n".join(body_lines)
    body_lower = body.lower()
    missing = []
    if not name or name.lower() not in body_lower:
        missing.append("name")
    if not any(keyword in body_lower for keyword in TITLE_KEYWORDS):
        missing.append("job title")
    if not PHONE_RE.search(body):
        missing.append("phone number")
    if "confidential" not in body_lower and "disclaimer" not in body_lower:
        missing.append("disclaimer")
    return name or sender or "unknown", missing

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as f:
        blocks = parse_blocks(f.read())
    compliant = 0
    for index, block in enumerate(blocks, 1):
        name, missing = check_block(block)
        if not missing:
            compliant += 1
            print(f"SIG-{index} [{name}]: COMPLIANT "
                  "(name, job title, phone number, disclaimer all present)")
        else:
            print(f"SIG-{index} [{name}]: NON-COMPLIANT - missing: {', '.join(missing)}")
    print(f"{compliant} compliant, {len(blocks) - compliant} non-compliant "
          f"out of {len(blocks)} signature(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
