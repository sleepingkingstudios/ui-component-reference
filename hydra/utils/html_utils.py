from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag

from hydra.utils.string_utils import kebab_case


_HEADING_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']


def _get_parent_children(headings: list, heading_level: int) -> list:
    children = headings

    for _ in range(1, heading_level):
        if len(children) == 0:
            return children

        children = children[-1]['children']

    return children


def _is_heading_tag(element: PageElement) -> bool:
    if not isinstance(element, Tag):
        return False

    if element.name == 'h1':
        return False

    return element.name in _HEADING_TAGS


def add_header_ids(fragment: BeautifulSoup) -> BeautifulSoup:
    """
    Adds auto-generated id attributes to header tags.

    Arguments:
        fragment (BeautifulSoup): The HTML to process.

    Returns:
        BeautifulSoup: The processed HTML.
    """
    for heading_tag in _HEADING_TAGS:
        for tag in fragment.find_all(heading_tag):
            tag.attrs['id'] = kebab_case(tag.text)

    return fragment


def parse_headings(fragment: BeautifulSoup) -> list:
    headings = []

    for element in fragment.children:
        if not _is_heading_tag(element):
            continue

        # Only generate headings for h2-h6 tags.
        heading_level = _HEADING_TAGS.index(element.name)
        heading = {
            'label': element.text,
            'url': f"#{element.attrs['id']}",
            'children': []
        }
        children = _get_parent_children(headings, heading_level)
        children.append(heading)

    return headings
