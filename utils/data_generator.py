from faker import Faker

fake = Faker()


class DataGenerator:
    @staticmethod
    def generate_user():
        password = "Test@" + fake.numerify("####")
        return {
            "name": fake.name(),
            "email": fake.unique.email(),
            "password": password,
            "phone": fake.numerify("01#########"),
        }

    @staticmethod
    def generate_invalid_email():
        return fake.word() + "@"

    @staticmethod
    def generate_short_password():
        return fake.password(length=4)
