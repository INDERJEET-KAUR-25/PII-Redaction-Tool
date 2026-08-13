import re

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"""
    (?:
        \+?\d{1,3}[-.\s]?
    )?
    (?:
        \(?\d{2,5}\)?[-.\s]?
    )?
    \d{3,5}
    [-.\s]?
    \d{4,6}
    """,
    re.VERBOSE,
)

IP_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)

SSN_PATTERN = re.compile(
    r"\b\d{3}-\d{2}-\d{4}\b"
)

CREDIT_CARD_PATTERN = re.compile(
    r"\b(?:\d[ -]?){13,19}\b"
)

DOB_PATTERN = re.compile(
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
)

COMPANY_PATTERN = re.compile(
    r"\b[A-Z][A-Za-z0-9&., ]{1,60}"
    r"(?:Limited|Ltd\.?|Private Limited|Pvt\. Ltd\.?|LLP|Inc\.?|Corporation|Corp\.?|Bank|Technologies|Industries)\b"
)

ADDRESS_PATTERN = re.compile(
    r"""
    (
        (?:House\s?No\.?|H\.?No\.?|Flat|Apartment|Building|Tower|Floor|Block)
        [^.,;\n]{0,80}
    )
    |
    (
        \d{1,4}
        \s+
        [A-Za-z0-9\s]+
        \s+
        (?:Road|Rd\.?|Street|St\.?|Lane|Sector|Avenue|Ave\.?)
        [^.,;\n]{0,60}
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)