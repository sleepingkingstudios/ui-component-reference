import pytest  # noqa: F401
from inspect import cleandoc
from bs4 import BeautifulSoup

from hydra.utils.html_utils import (
    add_header_ids,
    parse_headings,
)


class TestAddHeaderIds:
    def test_empty_fragment(self):
        fragment = BeautifulSoup('')
        processed = add_header_ids(fragment)

        assert str(processed) == ''

    def test_html_with_flat_headings(self):
        raw_html = cleandoc(
            """
            <h1>Top Heading</h1>

            <p>Introductory paragraph.</p>

            <h2>Middle Heading</h2>

            <p>Middle paragraph.</p>

            <h2>Final Heading</h2>

            <p>Final paragraph.</p>
            """
        )
        fragment = BeautifulSoup(raw_html, features="html.parser")
        processed = add_header_ids(fragment)
        expected = cleandoc(
            """
            <h1 id="top-heading">Top Heading</h1>
            <p>Introductory paragraph.</p>
            <h2 id="middle-heading">Middle Heading</h2>
            <p>Middle paragraph.</p>
            <h2 id="final-heading">Final Heading</h2>
            <p>Final paragraph.</p>
            """
        )

        assert str(processed) == expected

    def test_html_with_nested_headings(self):
        raw_html = cleandoc(
            """
            <h1>Top Heading</h1>

            <p>Introductory paragraph.</p>

            <h2>Middle Heading</h2>

            <p>Middle paragraph.</p>

            <h3>Inner Heading</h3>

            <p>Inner paragraph.</p>

            <h3>Another Inner Heading</h3>

            <p>Another inner paragraph.</p>

            <h4>Nested Heading</h4>

            <p>Nested paragraph.</p>

            <h2>Final Heading</h2>

            <p>Final paragraph.</p>
            """
        )
        fragment = BeautifulSoup(raw_html, features="html.parser")
        processed = add_header_ids(fragment)
        expected = cleandoc(
            """
            <h1 id="top-heading">Top Heading</h1>
            <p>Introductory paragraph.</p>
            <h2 id="middle-heading">Middle Heading</h2>
            <p>Middle paragraph.</p>
            <h3 id="inner-heading">Inner Heading</h3>
            <p>Inner paragraph.</p>
            <h3 id="another-inner-heading">Another Inner Heading</h3>
            <p>Another inner paragraph.</p>
            <h4 id="nested-heading">Nested Heading</h4>
            <p>Nested paragraph.</p>
            <h2 id="final-heading">Final Heading</h2>
            <p>Final paragraph.</p>
            """
        )

        assert str(processed) == expected


class TestParseHeadings:
    def test_empty_string(self):
        raw_html = ''
        fragment = BeautifulSoup(raw_html)

        assert parse_headings(fragment) == []

    def test_html_without_headings(self):
        raw_html = cleandoc(
            """
            <p><strong>Fake Heading</strong></p>

            <p>Real paragraph.</p>
            """
        )
        fragment = BeautifulSoup(raw_html, features="html.parser")

        assert parse_headings(fragment) == []

    def test_html_with_flat_headings(self):
        raw_html = cleandoc(
            """
            <h1 id="top-heading">Top Heading</h1>

            <p>Introductory paragraph.</p>

            <h2 id="middle-heading">Middle Heading</h2>

            <p>Middle paragraph.</p>

            <h2 id="final-heading">Final Heading</h2>

            <p>Final paragraph.</p>
            """
        )
        fragment = BeautifulSoup(raw_html, features="html.parser")
        expected = [
            {
                'label': 'Middle Heading',
                'url': '#middle-heading',
                'children': [],
            },
            {
                'label': 'Final Heading',
                'url': '#final-heading',
                'children': [],
            },
        ]

        assert parse_headings(fragment) == expected

    def test_html_with_nested_headings(self):
        raw_html = cleandoc(
            """
            <h1 id="top-heading">Top Heading</h1>

            <p>Introductory paragraph.</p>

            <h2 id="middle-heading">Middle Heading</h2>

            <p>Middle paragraph.</p>

            <h3 id="inner-heading">Inner Heading</h3>

            <p>Inner paragraph.</p>

            <h3 id="another-inner-heading">Another Inner Heading</h3>

            <p>Another inner paragraph.</p>

            <h4 id="nested-heading">Nested Heading</h4>

            <p>Nested paragraph.</p>

            <h2 id="final-heading">Final Heading</h2>

            <p>Final paragraph.</p>
            """
        )
        fragment = BeautifulSoup(raw_html, features="html.parser")
        expected = [
            {
                'label': 'Middle Heading',
                'url': '#middle-heading',
                'children': [
                    {
                        'label': 'Inner Heading',
                        'url': '#inner-heading',
                        'children': [],
                    },
                    {
                        'label': 'Another Inner Heading',
                        'url': '#another-inner-heading',
                        'children': [
                            {
                                'label': 'Nested Heading',
                                'url': '#nested-heading',
                                'children': [],
                            },
                        ],
                    },
                ],
            },
            {
                'label': 'Final Heading',
                'url': '#final-heading',
                'children': [],
            },
        ]

        assert parse_headings(fragment) == expected
