import pytest
from inspect import cleandoc
from typing import Any
from unittest.mock import patch
from bs4 import BeautifulSoup
from flask import render_template
from jinja2 import Environment, TemplateNotFound
from markupsafe import Markup

from hydra import create_app
from hydra.utils.render_utils import (
    parse_markdown,
    render_markdown,
    render_page,
)


def _mock_render_navigation(**context) -> str:
    environment = Environment()
    template = environment.from_string(
        cleandoc(
            """
            <ul class="navigation">
            {% for item in navigation %}
              <li>
                {{ item.label }}
                {% if item.children %}
                <ul>
                {% for child in item.children %}
                  <li>{{ child.label }}</li>
                {% endfor %}
                </ul>
                {% endif %}
              </li>
            {% endfor %}
            </ul>
            """
        )
    )

    return template.render(**context)


def _mock_render_page(**context: Any) -> str:
    environment = Environment()
    template = environment.from_string(
        cleandoc(
            """
            {{ navigation }}

            <article>
            {{ content }}
            </article>
            """
        )
    )

    return template.render(**context)


def _mock_render_template(template_name: str, **context: Any) -> str:
    if template_name == 'page/navigation.html':
        return _mock_render_navigation(navigation=context['navigation'])

    if template_name == 'page.html':
        return _mock_render_page(**context)

    return render_template(template_name, **context)


@pytest.fixture
def with_app_context():
    with create_app().app_context():
        yield


@pytest.fixture
def with_mocked_rendering():
    with patch('flask.render_template', side_effect=_mock_render_template):
        yield


class TestParseMarkdown:
    def test_invalid_template(self, with_app_context):
        with pytest.raises(TemplateNotFound):
            parse_markdown('invalid_template.md')

    def test_empty_template(self, with_app_context):
        fragment = parse_markdown('mocks/empty_template.md')

        assert type(fragment) is BeautifulSoup
        assert str(fragment) == ''

    def test_markdown_template(self, with_app_context):
        fragment = parse_markdown(
            'mocks/markdown_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <p>You have been recruited by the Star League to defend the
            frontier against Xur and the Ko-Dan Armada.</p>
            <h2 id="characters">Characters</h2>
            <h3 id="the-partner">The Partner</h3>
            <p>Grig</p>
            <h3 id="the-recruiter">The Recruiter</h3>
            <p>Centauri</p>
            """
        )

        assert type(fragment) is BeautifulSoup
        assert str(fragment) == expected

    def test_code_block_template(self, with_app_context):
        fragment = parse_markdown(
            'mocks/code_block_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <pre><code>recruiter = 'Star League'
            defend = 'the frontier'
            enemies = 'Xur and the Ko-Dan Armada'</code></pre>
            """
        )

        assert type(fragment) is BeautifulSoup
        assert str(fragment) == expected

    def test_highlighted_code_block_template(self, with_app_context):
        fragment = parse_markdown(
            'mocks/highlighted_code_block_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <div class="highlight"><pre><span></span><span class="n">recruiter</span> <span class="o">=</span> <span class="s1">'Star League'</span>
            <span class="n">defend</span> <span class="o">=</span> <span class="s1">'the frontier'</span>
            <span class="n">enemies</span> <span class="o">=</span> <span class="s1">'Xur and the Ko-Dan Armada'</span>
            </pre></div>
            """
        )

        assert type(fragment) is BeautifulSoup
        assert str(fragment) == expected


class TestRenderMarkdown:
    def test_invalid_template(self, with_app_context):
        with pytest.raises(TemplateNotFound):
            render_markdown('invalid_template.md')

    def test_empty_template(self, with_app_context):
        rendered = render_markdown('mocks/empty_template.md')

        assert type(rendered) is Markup
        assert rendered == ''

    def test_markdown_template(self, with_app_context):
        rendered = render_markdown(
            'mocks/markdown_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <p>You have been recruited by the Star League to defend the
            frontier against Xur and the Ko-Dan Armada.</p>
            <h2 id="characters">Characters</h2>
            <h3 id="the-partner">The Partner</h3>
            <p>Grig</p>
            <h3 id="the-recruiter">The Recruiter</h3>
            <p>Centauri</p>
            """
        )

        assert type(rendered) is Markup
        assert rendered == expected

    def test_code_block_template(self, with_app_context):
        rendered = render_markdown(
            'mocks/code_block_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <pre><code>recruiter = 'Star League'
            defend = 'the frontier'
            enemies = 'Xur and the Ko-Dan Armada'</code></pre>
            """
        )

        assert type(rendered) is Markup
        assert rendered == expected

    def test_highlighted_code_block_template(self, with_app_context):
        rendered = render_markdown(
            'mocks/highlighted_code_block_template.md',
            name='Starfighter'
        )
        expected = cleandoc(
            """
            <h1 id="greetings-starfighter">Greetings, Starfighter!</h1>
            <div class="highlight"><pre><span></span><span class="n">recruiter</span> <span class="o">=</span> <span class="s1">'Star League'</span>
            <span class="n">defend</span> <span class="o">=</span> <span class="s1">'the frontier'</span>
            <span class="n">enemies</span> <span class="o">=</span> <span class="s1">'Xur and the Ko-Dan Armada'</span>
            </pre></div>
            """
        )

        assert type(rendered) is Markup
        assert rendered == expected


class TestRenderPage:
    def test_invalid_template(self, with_app_context):
        with pytest.raises(TemplateNotFound):
            render_page('invalid_template.md')

    def test_empty_content(self, with_app_context, with_mocked_rendering):
        expected = cleandoc(
            """
            <ul class="navigation">

            </ul>

            <article>

            </article>
            """
        )
        rendered = render_page('mocks/empty_template.md')

        assert rendered == expected

    def test_markdown_template(self, with_app_context, with_mocked_rendering):
        expected = cleandoc(
            """
            <ul class="navigation">
             <li>
              Characters
              <ul>
               <li>
                The Partner
               </li>
               <li>
                The Recruiter
               </li>
              </ul>
             </li>
            </ul>
            <article>
             <h1 id="greetings-starfighter">
              Greetings, Starfighter!
             </h1>
             <p>
              You have been recruited by the Star League to defend the
            frontier against Xur and the Ko-Dan Armada.
             </p>
             <h2 id="characters">
              Characters
             </h2>
             <h3 id="the-partner">
              The Partner
             </h3>
             <p>
              Grig
             </p>
             <h3 id="the-recruiter">
              The Recruiter
             </h3>
             <p>
              Centauri
             </p>
            </article>
            """
        ) + '\n'
        rendered = render_page(
            'mocks/markdown_template.md',
            name='Starfighter'
        )
        pretty = BeautifulSoup(rendered, features="html.parser").prettify()

        assert pretty == expected
