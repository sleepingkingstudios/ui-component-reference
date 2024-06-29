import pytest  # noqa: F401

from hydra.utils.string_utils import kebab_case


class TestKebabCase:
    def test_empty_string(self):
        assert kebab_case('') == ''

    def test_lowercase_string(self):
        assert kebab_case('lowercase') == 'lowercase'

    def test_capitalized_string(self):
        assert kebab_case('Capitalized') == 'capitalized'

    def test_camel_case_string(self):
        assert kebab_case('CamelCase') == 'camel-case'

    def test_kebab_case_string(self):
        assert kebab_case('kebab-case') == 'kebab-case'

    def test_snake_case_string(self):
        assert kebab_case('snake_case') == 'snake-case'

    def test_string_with_punctuation(self):
        assert kebab_case('Greetings, Programs!') == 'greetings-programs'
