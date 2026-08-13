from faker import Faker
import random

fake = Faker("en_IN")


class FakeDataReplacer:

    def __init__(self):

        self.name_map = {}
        self.email_map = {}
        self.phone_map = {}
        self.company_map = {}
        self.address_map = {}
        self.ip_map = {}
        self.ssn_map = {}
        self.card_map = {}
        self.dob_map = {}

    # ---------------------------
    # PERSON
    # ---------------------------

    def fake_name(self, original):

        if original not in self.name_map:
            self.name_map[original] = fake.name()

        return self.name_map[original]

    # ---------------------------
    # EMAIL
    # ---------------------------

    def fake_email(self, original):

        if original not in self.email_map:
            self.email_map[original] = fake.email()

        return self.email_map[original]

    # ---------------------------
    # PHONE
    # ---------------------------

    def fake_phone(self, original):

        if original not in self.phone_map:
            self.phone_map[original] = "+91 " + str(
                random.randint(6000000000, 9999999999)
            )

        return self.phone_map[original]

    # ---------------------------
    # COMPANY
    # ---------------------------

    def fake_company(self, original):

        if original not in self.company_map:
            self.company_map[original] = fake.company()

        return self.company_map[original]

    # ---------------------------
    # ADDRESS
    # ---------------------------

    def fake_address(self, original):

        if original not in self.address_map:
            self.address_map[original] = (
                fake.address().replace("\n", ", ")
            )

        return self.address_map[original]

    # ---------------------------
    # IP
    # ---------------------------

    def fake_ip(self, original):

        if original not in self.ip_map:

            self.ip_map[original] = ".".join(
                str(random.randint(1, 254))
                for _ in range(4)
            )

        return self.ip_map[original]

    # ---------------------------
    # SSN
    # ---------------------------

    def fake_ssn(self, original):

        if original not in self.ssn_map:

            self.ssn_map[original] = (
                f"{random.randint(100,999)}-"
                f"{random.randint(10,99)}-"
                f"{random.randint(1000,9999)}"
            )

        return self.ssn_map[original]

    # ---------------------------
    # CREDIT CARD
    # ---------------------------

    def fake_card(self, original):

        if original not in self.card_map:
            self.card_map[original] = fake.credit_card_number()

        return self.card_map[original]

    # ---------------------------
    # DOB
    # ---------------------------

    def fake_dob(self, original):

        if original not in self.dob_map:

            self.dob_map[original] = fake.date_of_birth(
                minimum_age=18,
                maximum_age=80,
            ).strftime("%d/%m/%Y")

        return self.dob_map[original]

    # ---------------------------
    # Replace
    # ---------------------------

    def replace(self, text, entities):

        entities = sorted(
            entities,
            key=lambda x: x.start,
            reverse=True,
        )

        for entity in entities:

            value = entity.value

            if entity.entity_type == "PERSON":
                replacement = self.fake_name(value)

            elif entity.entity_type == "EMAIL":
                replacement = self.fake_email(value)

            elif entity.entity_type == "PHONE":
                replacement = self.fake_phone(value)

            elif entity.entity_type == "ORGANIZATION":
                replacement = self.fake_company(value)

            elif entity.entity_type == "ADDRESS":
                replacement = self.fake_address(value)

            elif entity.entity_type == "IP_ADDRESS":
                replacement = self.fake_ip(value)

            elif entity.entity_type == "SSN":
                replacement = self.fake_ssn(value)

            elif entity.entity_type == "CREDIT_CARD":
                replacement = self.fake_card(value)

            elif entity.entity_type == "DATE_TIME":
                replacement = self.fake_dob(value)

            else:
                replacement = "[REDACTED]"

            text = (
                text[:entity.start]
                + replacement
                + text[entity.end:]
            )

        return text