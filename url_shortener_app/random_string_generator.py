import random
import string


class RandomStringGenerator:
    chars = string.ascii_letters + string.digits

    @classmethod
    def get_random_string(cls, length: int) -> str:
        return "".join(random.choices(cls.chars, k=length))
