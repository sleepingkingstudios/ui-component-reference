import pytest  # noqa: F401
from inspect import cleandoc

from hydra.utils.markdown_utils import process_fenced_code_blocks


class TestProcessFencedCodeBlocks:
    def test_empty_document(self):
        document = ''

        assert process_fenced_code_blocks(document) == document

    def test_markdown_document(self):
        document = cleandoc(
            """
            # Greetings, Starfighter!

            You have been recruited by the Star League to defend the
            frontier against Xur and the Ko-Dan Armada!
            """
        )

        assert process_fenced_code_blocks(document) == document

    def test_code_block(self):
        document = cleandoc(
            """
            # Greetings, Starfighter!

            ```
            recruiter = 'Star League'
            defend = 'the frontier'
            enemies = 'Xur and the Ko-Dan Armada'
            ```
            """
        )
        expected = cleandoc(
            """
            # Greetings, Starfighter!

            <pre><code>recruiter = 'Star League'
            defend = 'the frontier'
            enemies = 'Xur and the Ko-Dan Armada'</code></pre>
            """
        )

        assert process_fenced_code_blocks(document) == expected

    def test_single_line_code_block(self):
        document = cleandoc(
            """
            # Greetings, Starfighter!

            ```
            recruiter = 'Star League'
            ```
            """
        )
        expected = cleandoc(
            """
            # Greetings, Starfighter!

            <pre><code>recruiter = 'Star League'</code></pre>
            """
        )

        assert process_fenced_code_blocks(document) == expected

    def test_highlighted_block(self):
        document = cleandoc(
            """
            # Greetings, Starfighter!

            ```python
            recruiter = 'Star League'
            defend = 'the frontier'
            enemies = 'Xur and the Ko-Dan Armada'
            ```
            """
        )
        expected = cleandoc(
            """
            # Greetings, Starfighter!

            <div class="highlight"><pre><span></span><span class="n">recruiter</span> <span class="o">=</span> <span class="s1">&#39;Star League&#39;</span>
            <span class="n">defend</span> <span class="o">=</span> <span class="s1">&#39;the frontier&#39;</span>
            <span class="n">enemies</span> <span class="o">=</span> <span class="s1">&#39;Xur and the Ko-Dan Armada&#39;</span>
            </pre></div>
            """
        ) + '\n'

        assert process_fenced_code_blocks(document) == expected
