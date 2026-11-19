# email-signature-compliance-checker

Check email signatures for the required elements: the input file holds one signature block per sender, separated by a line containing only "---", each block starting with a "From: Name <email>" line. Four elements are required — the sender's name in the signature, a job title (a role word such as officer, executive, manager, engineer or support), a phone number of at least 9 digits, and a disclaimer ("confidential" or "disclaimer") — and a signature missing any element is NON-COMPLIANT with the missing elements listed.

Sample input is included (sample.txt with three signatures).

## How to run

```sh
python3 main.py sample.txt
```

## Example output

```
SIG-1 [Ayesha Khan]: COMPLIANT (name, job title, phone number, disclaimer all present)
SIG-2 [Bilal Ahmed]: NON-COMPLIANT - missing: job title, disclaimer
SIG-3 [Sara Malik]: NON-COMPLIANT - missing: phone number
1 compliant, 2 non-compliant out of 3 signature(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
