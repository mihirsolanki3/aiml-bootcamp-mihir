# TASK 04
# Email extraction with regex

import re
from collections import Counter

# ---------------------------------------------------------
# 1. Messy text
# ---------------------------------------------------------

text = '''
msofficial12@gmail.com wrote to ravi_k99@gmail.com
aarav.p+work@company.co.in, phone 1234567899
dev@sub.domain.example.org and +91 11111 11111 
not.an.email@ nor @nothing.com -- watch these
'''
# ---------------------------------------------------------
# 2. Extract every email address
# ---------------------------------------------------------

email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

emails = re.findall(email_pattern, text)

print("Email addresses:")
for email in emails:
    print(email)

print("\nNumber of emails:", len(emails))

# ---------------------------------------------------------
# 3. Extract phone numbers
# ---------------------------------------------------------

phone_pattern = r'(?:\+91[\s-]?)?\d{2,5}[-\s]\d{4,5}[-\s]\d{4,5}'

phones = re.findall(phone_pattern, text)

print("\nPhone numbers:")
for phone in phones:
    print(phone)

# ---------------------------------------------------------
# 4. Split each email into username and domain
# ---------------------------------------------------------

email_split_pattern = r'([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})'

email_parts = re.findall(email_split_pattern, text)

print("\nUsername and domain:")

for username, domain in email_parts:
    print("Username:", username)
    print("Domain:", domain)
    print()

# ---------------------------------------------------------
# 5. Count emails by domain
# ---------------------------------------------------------

domains = [domain for username, domain in email_parts]

domain_counts = Counter(domains)

print("Emails by domain:")

for domain, count in domain_counts.items():
    print(domain, ":", count)