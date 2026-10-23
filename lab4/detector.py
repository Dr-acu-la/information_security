#!/usr/bin/env python3
"""
detector.py - a simple phishing indicator scanner (blue-team tool for Lab 4).

It reads an email or a URL from a file or from standard input and reports
the phishing warning signs it finds. It does NOT connect to anything - all
checks are done locally on the text you give it.

Usage:
    python3 detector.py suspicious_email.txt
    echo "http://instagramm.com/login" | python3 detector.py
"""
import sys
import re

# Words that create urgency or fear - a classic social-engineering tactic
URGENCY_WORDS = [
    "urgent", "immediately", "action required", "suspended", "verify",
    "confirm your", "within 24 hours", "account locked", "unusual activity",
    "limited time", "expire", "click here", "update your payment",
]

# Field names that mean a form is asking for secrets or money
SENSITIVE_FIELDS = [
    "password", "passwd", "card", "cardnumber", "card_number", "cvv", "cvc",
    "ssn", "pin", "expiry", "exp_date", "security code",
]

# Brands often impersonated - we flag look-alike spellings of these
BRANDS = ["instagram", "paypal", "apple", "amazon", "google", "microsoft",
          "facebook", "netflix", "bank"]


def check_urls(text):
    findings = []
    # Find href="..." links and bare URLs
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', text, re.I)
    bare = re.findall(r'https?://[^\s"\'<>]+', text, re.I)
    urls = set(hrefs + bare)

    for url in urls:
        host = re.sub(r'^https?://', '', url).split('/')[0].lower()

        if url.lower().startswith("http://"):
            findings.append(f"Insecure link (no HTTPS): {url}")

        if re.match(r'^https?://\d+\.\d+\.\d+\.\d+', url):
            findings.append(f"Link points to a raw IP address: {url}")

        if host in ("localhost", "127.0.0.1"):
            findings.append(f"Link points to localhost (test attack server?): {url}")

        # Look-alike brand domains, e.g. instagramm, paypa1, g00gle
        for brand in BRANDS:
            if brand in host and not re.search(rf'\b{brand}\.(com|net|org)', host):
                findings.append(f"Possible look-alike of '{brand}': {host}")
                break

    # Link text that does not match its destination
    for shown, target in re.findall(r'href=["\']([^"\']+)["\'][^>]*>([^<]+)<', text, re.I):
        if re.search(r'https?://', target) and shown.split('/')[2:3] != target.split('/')[2:3]:
            findings.append(f"Link text says '{target.strip()}' but goes to '{shown}'")
    return findings


def check_language(text):
    low = text.lower()
    return [f"Urgency / pressure phrase: '{w}'" for w in URGENCY_WORDS if w in low]


def check_forms(text):
    findings = []
    if re.search(r'<form', text, re.I):
        for field in SENSITIVE_FIELDS:
            if re.search(rf'name=["\']?[^"\'>]*{field}', text, re.I):
                findings.append(f"Form collects sensitive field: '{field}'")
        # Where does the form send data?
        for action in re.findall(r'(?:action=["\']([^"\']*)["\']|fetch\(\s*["\']([^"\']+)["\'])', text, re.I):
            dest = action[0] or action[1]
            if dest:
                findings.append(f"Form/script sends data to: {dest}")
    return findings


def scan(text):
    findings = []
    findings += check_language(text)
    findings += check_urls(text)
    findings += check_forms(text)
    return findings


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
            text = f.read()
        source = sys.argv[1]
    else:
        text = sys.stdin.read()
        source = "standard input"

    print(f"Phishing scan of: {source}")
    print("=" * 50)
    findings = scan(text)

    if not findings:
        print("No phishing indicators found.")
    else:
        # De-duplicate while keeping order
        seen = set()
        for f in findings:
            if f not in seen:
                seen.add(f)
                print(f"  [!] {f}")
        score = len(seen)
        level = "HIGH" if score >= 4 else "MEDIUM" if score >= 2 else "LOW"
        print("-" * 50)
        print(f"{score} indicator(s) found. Risk level: {level}")


if __name__ == "__main__":
    main()
