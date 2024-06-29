from typing import Any
from bs4 import BeautifulSoup
import flask
from markdown import markdown
from markupsafe import Markup

from hydra.utils.html_utils import add_header_ids, parse_headings
from hydra.utils.markdown_utils import process_fenced_code_blocks


def _pre_process_markdown(document: str) -> str:
    document = process_fenced_code_blocks(document)

    return document


def _post_process_markdown(fragment: BeautifulSoup) -> BeautifulSoup:
    fragment = add_header_ids(fragment)

    return fragment


def parse_markdown(template_name: str, **context: Any) -> BeautifulSoup:
    """
    Renders a Markdown file to intermediate HTML.

    Arguments:
        template_name (str): The name of the template to render.
        context: The variables to make available in the template.

    Returns:
        BeautifulSoup: The intermediate HTML representation.
    """
    raw_text = flask.render_template(template_name, **context)
    processed = _pre_process_markdown(raw_text)
    rendered = markdown(processed)
    fragment = BeautifulSoup(rendered, features="html.parser")
    fragment = _post_process_markdown(fragment)

    return fragment


def render_markdown(template_name: str, **context: Any) -> Markup:
    """
    Renders a Markdown file to HTML with Jinja2 template support.

    Arguments:
        template_name (str): The name of the template to render.
        context: The variables to make available in the template.

    Returns:
        Markup: The generated HTML.
    """
    return Markup(parse_markdown(template_name, **context))


def render_page(template_name: str, **context: Any) -> str:
    """
    Renders a template to a page with content and navigation.

    Arguments:
        template_name (str): The name of the template to render.
        context: The variables to make available in the template.

    Returns:
        str: The rendered page.
    """
    fragment = parse_markdown(template_name, **context)
    navigation = flask.render_template(
        'page/navigation.html',
        navigation=parse_headings(fragment)
    )

    return flask.render_template(
        'page.html',
        content=Markup(fragment),
        navigation=Markup(navigation)
    )
