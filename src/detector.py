from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

from constants import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    IP_PATTERN,
    SSN_PATTERN,
    CREDIT_CARD_PATTERN,
    DOB_PATTERN,
    COMPANY_PATTERN,
    ADDRESS_PATTERN,
)

from utils import PIIEntity


class HybridDetector:

    def __init__(self):

        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {
                    "lang_code": "en",
                    "model_name": "en_core_web_sm",
                }
            ],
        }

        provider = NlpEngineProvider(
            nlp_configuration=configuration
        )

        self.analyzer = AnalyzerEngine(
            nlp_engine=provider.create_engine()
        )

    # ----------------------------------------------------
    # Regex Detection
    # ----------------------------------------------------

    def regex_detect(self, text):

        entities = []

        patterns = {
            "EMAIL": EMAIL_PATTERN,
            "PHONE": PHONE_PATTERN,
            "IP_ADDRESS": IP_PATTERN,
            "SSN": SSN_PATTERN,
            "CREDIT_CARD": CREDIT_CARD_PATTERN,
            "DATE_TIME": DOB_PATTERN,
            "ORGANIZATION": COMPANY_PATTERN,
            "ADDRESS": ADDRESS_PATTERN,
        }

        for entity_type, pattern in patterns.items():

            for match in pattern.finditer(text):

                entities.append(
                    PIIEntity(
                        entity_type=entity_type,
                        value=match.group(),
                        start=match.start(),
                        end=match.end(),
                    )
                )

        return entities

    # ----------------------------------------------------
    # PERSON Detection using Presidio
    # ----------------------------------------------------

    def person_detect(self, text):

        entities = []

        if not text.strip():
            return entities

        if text.isupper():
            return entities

        blacklist = {
            "prospectus",
            "offer",
            "equity",
            "shares",
            "issue",
            "investor",
            "investors",
            "company",
            "companies",
            "chapter",
            "table",
            "contents",
            "section",
            "schedule",
            "board",
            "financial",
            "capital",
            "book",
            "running",
            "lead",
            "manager",
            "sebi",
            "ipo",
        }

        results = self.analyzer.analyze(
            text=text,
            language="en",
            entities=["PERSON"],
        )

        for result in results:

            if result.score < 0.80:
                continue

            value = text[result.start:result.end].strip()

            if len(value.split()) > 4:
                continue

            if any(ch.isdigit() for ch in value):
                continue

            lower = value.lower()

            if any(word in lower for word in blacklist):
                continue

            entities.append(
                PIIEntity(
                    entity_type="PERSON",
                    value=value,
                    start=result.start,
                    end=result.end,
                )
            )

        return entities

    # ----------------------------------------------------
    # Remove Duplicate Entities
    # ----------------------------------------------------

    def remove_duplicates(self, entities):

        unique = {}

        for entity in entities:

            key = (
                entity.start,
                entity.end,
                entity.entity_type,
            )

            if key not in unique:
                unique[key] = entity

        return list(unique.values())

    # ----------------------------------------------------
    # Detect Everything
    # ----------------------------------------------------

    def detect(self, text):

        regex_entities = self.regex_detect(text)

        person_entities = self.person_detect(text)

        entities = regex_entities + person_entities

        entities = self.remove_duplicates(entities)

        entities.sort(key=lambda x: x.start)

        return entities