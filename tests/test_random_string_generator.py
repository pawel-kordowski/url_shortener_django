import pytest

from url_shortener_app.random_string_generator import RandomStringGenerator


@pytest.mark.parametrize("length", (2, 3))
def test_get_random_string_returns_string_of_a_given_length(length):
    random_string = RandomStringGenerator.get_random_string(length=length)

    assert type(random_string) is str
    assert len(random_string) == length


def test_get_random_string_returns_different_values():
    assert RandomStringGenerator.get_random_string(
        length=10
    ) != RandomStringGenerator.get_random_string(length=10)
