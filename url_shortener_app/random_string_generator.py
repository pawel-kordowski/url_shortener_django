from django.utils.crypto import get_random_string


class RandomStringGenerator:
    @classmethod
    def get_random_strings(cls, length: int, count: int) -> set[str]:
        return {get_random_string(length=length) for _ in range(count)}
