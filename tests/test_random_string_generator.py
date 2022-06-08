import pytest

from url_shortener_app.random_string_generator import RandomStringGenerator


@pytest.mark.parametrize("length,count", ((2, 3), (3, 2)))
def test_get_random_strings_returns_set_of_strings(length, count):
    random_strings = RandomStringGenerator.get_random_strings(
        length=length, count=count
    )

    assert type(random_strings) is set
    assert len(random_strings) == count
    assert all(type(random_string) is str for random_string in random_strings)
    assert all(len(random_string) == length for random_string in random_strings)
