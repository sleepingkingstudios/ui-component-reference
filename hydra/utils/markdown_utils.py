from re import compile, search

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexer import Lexer
from pygments.lexers import get_lexer_by_name


_fence_pattern = compile(r'```')


def _get_lexer_for(language: str) -> Lexer | None:
    if language == '' or language == 'none':
        return None

    return get_lexer_by_name(language, stripall=True)


def _generate_code_block(lines: list[str], language: str) -> str:
    lexer = _get_lexer_for(language)

    if lexer:
        code = '\n'.join(lines)
        formatter = HtmlFormatter(linenos=False, style='native')

        return highlight(code, lexer, formatter)
    else:
        return _generate_unhighlighted_block(lines)


def _generate_unhighlighted_block(lines: list[str]) -> str:
    buffer = []

    buffer.append(f"<pre><code>{lines[0]}")

    if len(lines) == 1:
        return f"{buffer[0]}</code></pre>"

    for line in lines[1:-1]:
        buffer.append(f"{line}")

    buffer.append(f"{lines[-1]}</code></pre>")

    return '\n'.join(buffer)


def process_fenced_code_blocks(raw_markdown: str) -> str:
    """
    Naïvely processes a Markdown document to apply fenced code blocks.

    Fenced code blocks are wrapped by three backticks and may have an
    optional language identifier:

    ```python
    def example_function():
        pass
    ```

    If the code block has a language identifier, the wrapped code will
    be processed using Pygments.

    Arguments:
        raw_markdown (str): The raw markdown file to process.

    Returns:
        str: The processed markdown.
    """
    output = []
    buffer = []
    indent = 0
    language = ''
    in_fence = False

    for line in str.splitlines(raw_markdown):
        if '```' not in line:
            if not in_fence:
                output.append(line)
            else:
                buffer.append(line[indent:])

            continue

        if in_fence:
            print('Ending code block...')

            output.append(_generate_code_block(buffer, language=language))
            buffer = []
            in_fence = False
        else:
            in_fence = True
            match = search(_fence_pattern, line)
            indent = match.start()
            language = line[match.end():]

            print(f'Starting code block (language={language})...')

    return '\n'.join(output)
