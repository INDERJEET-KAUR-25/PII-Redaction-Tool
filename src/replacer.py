from anonymizer import FakeDataGenerator


class PIIReplacer:

    def __init__(self):
        self.fake_generator = FakeDataGenerator()

    def replace(self, text, entities):
        """
        Replace detected PII entities with fake values.
        """

        # Sort from end to beginning to avoid changing indices
        entities = sorted(entities, key=lambda x: x.start, reverse=True)

        for entity in entities:

            replacement = self.get_replacement(entity)

            text = (
                text[:entity.start]
                + replacement
                + text[entity.end:]
            )

        return text

    def get_replacement(self, entity):

        entity_type = entity.entity_type

        if entity_type in ["PERSON"]:
            return self.fake_generator.fake_name(entity.value)

        elif entity_type in ["EMAIL", "EMAIL_ADDRESS"]:
            return self.fake_generator.fake_email(entity.value)

        elif entity_type in ["PHONE", "PHONE_NUMBER"]:
            return self.fake_generator.fake_phone(entity.value)

        elif entity_type in ["ORGANIZATION"]:
            return self.fake_generator.fake_company(entity.value)

        elif entity_type in ["LOCATION", "ADDRESS"]:
            return self.fake_generator.fake_address(entity.value)

        elif entity_type == "IP_ADDRESS":
            return "192.168.100.100"

        elif entity_type == "SSN":
            return "123-45-6789"

        elif entity_type == "CREDIT_CARD":
            return "4111 1111 1111 1111"

        elif entity_type in ["DATE", "DATE_TIME"]:
            return "01/01/2000"

        return entity.value