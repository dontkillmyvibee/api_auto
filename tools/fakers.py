from faker import Faker


class Fake:
    """Обёртка над Faker с доменными генераторами тестовых данных.

    Единая точка генерации: схемы и тесты обращаются к методам Fake, а не к
    Faker напрямую.
    """

    def __init__(self, faker: Faker):
        self.faker = faker

    def uuid4(self) -> str:
        return self.faker.uuid4()

    def email(self, domain: str | None = None) -> str:
        return self.faker.email(domain=domain)

    def first_name(self) -> str:
        return self.faker.first_name()

    def last_name(self) -> str:
        return self.faker.last_name()

    def middle_name(self) -> str:
        return self.faker.first_name()

    def phone_number(self) -> str:
        return self.faker.phone_number()

    def text(self) -> str:
        return self.faker.text()

    def sentence(self) -> str:
        return self.faker.sentence()

    def category(self) -> str:
        return self.faker.word()

    def integer(self, start: int = 1, end: int = 100) -> int:
        return self.faker.random_int(start, end)

    def amount(self, start: float = 1.0, end: float = 1000.0) -> float:
        return round(self.faker.pyfloat(min_value=start, max_value=end, right_digits=2), 2)


fake = Fake(faker=Faker())
